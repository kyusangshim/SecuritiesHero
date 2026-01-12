# app/kafka/kafka_service.py
import asyncio
import json
import logging
from typing import Dict, Any, Optional

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from app.config import settings
from app.AI.services.equity_annotation_service import EquityAnnotationService

logger = logging.getLogger(__name__)


class KafkaService:
    """Kafka 통신 서비스 - Java 백엔드와 FastAPI 간 메시지 브리지"""

    def __init__(self):
        self.bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS
        self.consumer_group = settings.KAFKA_CONSUMER_GROUP
        self.request_topic = settings.KAFKA_REQUEST_TOPIC or "fastapi-equity-request"
        self.response_topic = settings.KAFKA_RESPONSE_TOPIC or "fastapi-equity-response"

        self.consumer: Optional[AIOKafkaConsumer] = None
        self.producer: Optional[AIOKafkaProducer] = None
        self.equity_service = EquityAnnotationService()

        self.is_running = False

    async def start(self) -> None:
        """Kafka 서비스 시작"""
        try:
            self.consumer = AIOKafkaConsumer(
                self.request_topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.consumer_group,
                auto_offset_reset="latest",
                value_deserializer=lambda x: json.loads(x.decode("utf-8")) if x else None,
            )

            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda x: json.dumps(x, ensure_ascii=False).encode("utf-8"),
            )

            await self.consumer.start()
            await self.producer.start()
            self.is_running = True

            logger.info(f"Kafka 서비스 시작됨 ✅ [request={self.request_topic}, response={self.response_topic}]")
            asyncio.create_task(self._consume_messages())

        except Exception as e:
            logger.error(f"Kafka 서비스 시작 실패 ❌: {e}")
            await self.stop()
            raise

    async def stop(self) -> None:
        """Kafka 서비스 중지"""
        self.is_running = False

        try:
            if self.consumer:
                await self.consumer.stop()
                logger.info("Kafka Consumer 중지됨")
            if self.producer:
                await self.producer.stop()
                logger.info("Kafka Producer 중지됨")
        except Exception as e:
            logger.error(f"Kafka 서비스 중지 중 오류: {e}")

    async def _consume_messages(self) -> None:
        """Kafka 메시지 리스닝 & 처리"""
        logger.info("Kafka 메시지 리스닝 시작... 🎧")

        try:
            async for message in self.consumer:
                if not self.is_running:
                    break

                kafka_data = message.value
                logger.info(f"Kafka 메시지 수신: key={message.key}, partition={message.partition}")

                try:
                    response = await self._process_equity_request(kafka_data)
                    await self._send_kafka_message(response)
                except Exception as e:
                    logger.error(f"메시지 처리 중 오류: {e}")
                    await self._send_error_response(kafka_data, str(e))

        except Exception as e:
            logger.error(f"Kafka 메시지 소비 중 오류: {e}")
        finally:
            logger.info("Kafka 메시지 리스닝 종료")

    async def _process_equity_request(self, kafka_data: Dict[str, Any]) -> Dict[str, Any]:
        """주석 생성 요청 처리"""
        request_id = kafka_data.get("request_id", "")
        company_name = kafka_data.get("company_name", "")
        logger.info(f"주석 생성 처리 시작: requestId={request_id}, company={company_name}")

        request_data = self._convert_java_request(kafka_data)

        response = await self.equity_service.process_kafka_request({
            "requestId": request_id,
            "companyName": company_name,
            "requestData": request_data,
        })

        return {
            "request_id": response.requestId,
            "status": "SUCCESS" if response.status == "success" else "FAILED",
            "company_name": response.companyName,
            "S4_NOTE1_1": response.S4_NOTE1_1,
            "S4_NOTE1_2": response.S4_NOTE1_2,
            "S4_NOTE1_3": response.S4_NOTE1_3,
            "S4_NOTE1_4": response.S4_NOTE1_4,
            "S4_NOTE1_5": response.S4_NOTE1_5,
            "processing_time_ms": response.processingTimeMs,
            "timestamp": response.timestamp,
            "error_message": response.errorMessage,
        }

    def _convert_java_request(self, java_data: Dict[str, Any]) -> Dict[str, Any]:
        """Java → Python 요청 변환"""
        return {k: java_data.get(k) for k in [
            "company_name", "ceo_name", "address", "establishment_date", "company_phone", "company_website",
            "S4_11A_1", "S4_11A_2", "S4_11A_3", "S4_11A_4", "S4_11A_5", "S4_11A_6",
            "S4_11B_1", "S4_11B_2", "S4_11B_3", "S4_11B_4", "S4_11B_5", "S4_11B_6", "S4_11B_7",
            "S4_11C_1", "S4_11C_2", "S4_11C_3", "S4_11C_4", "S4_11C_5"
        ]}

    async def _send_kafka_message(self, payload: Dict[str, Any]) -> None:
        """Kafka 응답 전송"""
        try:
            request_id = payload.get("request_id", "unknown")
            await self.producer.send(
                self.response_topic,
                key=request_id.encode("utf-8"),
                value=payload,
            )
            await self.producer.flush()
            logger.info(f"Kafka 응답 전송 완료 ✅: requestId={request_id}, status={payload.get('status')}")
        except Exception as e:
            logger.error(f"Kafka 응답 전송 실패 ❌: {e}")

    async def _send_error_response(self, original_data: Dict[str, Any], error_message: str) -> None:
        """Kafka 에러 응답 전송"""
        request_id = original_data.get("request_id", "unknown")
        company_name = original_data.get("company_name", "")

        error_response = {
            "request_id": request_id,
            "status": "FAILED",
            "company_name": company_name,
            "S4_NOTE1_1": "기본 주석 1",
            "S4_NOTE1_2": "기본 주석 2",
            "S4_NOTE1_3": "기본 주석 3",
            "S4_NOTE1_4": "기본 주석 4",
            "S4_NOTE1_5": "기본 주석 5",
            "processing_time_ms": 0,
            "timestamp": "error",
            "error_message": error_message,
        }
        await self._send_kafka_message(error_response)

    async def health_check(self) -> Dict[str, Any]:
        """Kafka 서비스 상태"""
        return {
            "service": "KafkaService",
            "status": "healthy" if self.is_running and self.consumer and self.producer else "unhealthy",
            "is_running": self.is_running,
            "topics": {"request": self.request_topic, "response": self.response_topic},
            "bootstrap_servers": self.bootstrap_servers,
        }


# 전역 인스턴스
kafka_service = KafkaService()


async def get_kafka_service() -> KafkaService:
    return kafka_service
