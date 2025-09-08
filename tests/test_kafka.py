#C:\Users\user\Documents\FAST_API_LLM\Utility\test_kafka.py
"""
Kafka 통신 테스트 스크립트
Java 백엔드 없이 FastAPI의 Kafka 처리를 테스트
"""

import asyncio
import json
import logging
from datetime import datetime
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KafkaTester:
    """Kafka 테스트 클래스"""
    
    def __init__(self):
        self.bootstrap_servers = "localhost:9092"
        self.request_topic = "fastapi-equity-request"
        self.response_topic = "fastapi-equity-response"
        
    async def send_test_request(self):
        """테스트 주식 공모 주석 요청 전송"""
        producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda x: json.dumps(x, ensure_ascii=False).encode('utf-8')
        )
        
        try:
            await producer.start()
            
            # Java FastApiRequestDto와 동일한 구조의 테스트 데이터
            test_request = {
                "request_id": f"test_request_{int(datetime.now().timestamp())}",
                "request_type": "EQUITY_ANNOTATION",
                "company_name": "테스트주식회사",
                "ceo_name": "김대표",
                "address": "서울시 강남구",
                "establishment_date": "2020-01-01",
                "company_phone": "02-1234-5678",
                "company_website": "https://test.com",
                
                # S4_11A 필드들
                "S4_11A_1": "보통주",
                "S4_11A_2": "1000000",
                "S4_11A_3": "500",
                "S4_11A_4": "10000-12000",
                "S4_11A_5": "12000000000",
                "S4_11A_6": "일반공모",
                
                # S4_11B 필드들
                "S4_11B_1": "총액인수",
                "S4_11B_2": "테스트증권",
                "S4_11B_3": "보통주",
                "S4_11B_4": "1000000",
                "S4_11B_5": "12000000000",
                "S4_11B_6": "12000",
                "S4_11B_7": "공개모집",
                
                # S4_11C 필드들
                "S4_11C_1": "자본시장법",
                "S4_11C_2": "2024-03-20",
                "S4_11C_3": "2024-03-18~2024-03-19",
                "S4_11C_4": "2024-03-21",
                "S4_11C_5": "2024-03-25",
                
                "timestamp": datetime.now().isoformat()
            }
            
            # 요청 전송
            await producer.send(
                self.request_topic,
                key=test_request["request_id"].encode('utf-8'),
                value=test_request
            )
            
            logger.info(f"테스트 요청 전송 완료: {test_request['request_id']}")
            logger.info(f"회사명: {test_request['company_name']}")
            
            return test_request["request_id"]
            
        finally:
            await producer.stop()
    
    async def listen_responses(self, timeout_seconds=60):
        """응답 메시지 리스닝"""
        consumer = AIOKafkaConsumer(
            self.response_topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id="kafka-tester-group",
            auto_offset_reset='latest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')) if x else None
        )
        
        try:
            await consumer.start()
            logger.info("응답 리스닝 시작...")
            
            start_time = asyncio.get_event_loop().time()
            
            async for message in consumer:
                try:
                    response = message.value
                    request_id = response.get("request_id", "")
                    status = response.get("status", "")
                    company_name = response.get("company_name", "")
                    
                    logger.info(f"응답 수신: requestId={request_id}, status={status}, company={company_name}")
                    
                    # 주석 내용 출력
                    for i in range(1, 6):
                        note_key = f"S4_NOTE1_{i}"
                        if note_key in response:
                            logger.info(f"{note_key}: {response[note_key][:100]}...")
                    
                    if response.get("error_message"):
                        logger.error(f"에러 메시지: {response['error_message']}")
                    
                    break  # 첫 번째 응답만 처리
                    
                except Exception as e:
                    logger.error(f"응답 처리 오류: {str(e)}")
                
                # 타임아웃 체크
                if asyncio.get_event_loop().time() - start_time > timeout_seconds:
                    logger.warning("응답 대기 시간 초과")
                    break
                    
        finally:
            await consumer.stop()
    
    async def run_full_test(self):
        """전체 테스트 실행"""
        logger.info("=== Kafka 통신 테스트 시작 ===")
        
        try:
            # 1. 응답 리스너 시작 (백그라운드)
            response_task = asyncio.create_task(self.listen_responses())
            
            # 2. 요청 전송
            await asyncio.sleep(1)  # 리스너가 준비될 때까지 대기
            request_id = await self.send_test_request()
            
            # 3. 응답 대기
            await response_task
            
            logger.info("=== 테스트 완료 ===")
            
        except Exception as e:
            logger.error(f"테스트 실행 중 오류: {str(e)}")

async def main():
    """메인 함수"""
    tester = KafkaTester()
    await tester.run_full_test()

if __name__ == "__main__":
    asyncio.run(main())