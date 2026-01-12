<img width="1424" height="800" alt="image" src="https://github.com/user-attachments/assets/c67483b7-0a22-4e47-bef8-8078d2045518" />

<div align="center">

# 🦸‍♂️ Securities Hero (증권히어로)
### AI 기반 증권신고서 자동 생성 및 분석 자동화 플랫폼
  
**[ 🏆 더존 AX CAMP 1기 최종 프로젝트 '대상' 수상 ]** 

<br />

![Java](https://img.shields.io/badge/Java-17-007396?style=for-the-badge&logo=java&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.3.5-6DB33F?style=for-the-badge&logo=springboot&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Kafka](https://img.shields.io/badge/Apache%20Kafka-3.7.1-231F20?style=for-the-badge&logo=apachekafka&logoColor=white)

</div>

---

## 🌟 Introduction
**증권히어로**는 방대한 기업 공시 데이터를 수집·파싱하고, **LangGraph 기반의 멀티 에이전트 시스템**을 통해 전문적인 증권신고서 초안 작성 및 검증 과정을 혁신적으로 자동화하는 플랫폼입니다.

---

## 🏗️ System Architecture
프로젝트는 **이벤트 기반 마이크로서비스 아키텍처**를 지향하며, 각 모듈은 고유의 역할을 수행합니다.



1.  **Utility**: DART XML 데이터를 실시간 수집 및 파싱하여 OpenSearch에 색인합니다.
2.  **AI (LangGraph)**: 수집된 데이터를 바탕으로 멀티 에이전트가 리포트 생성 및 검증 절차를 수행합니다.
3.  **Backend**: 비즈니스 로직 처리, 사용자 관리 및 Kafka를 통한 모듈 간 상태 동기화를 담당합니다.
4.  **Frontend**: 사용자에게 완성된 리포트 뷰어와 편집 도구를 제공합니다.

---

## 📂 Repository Structure (Monorepo)

```text
SecuritiesHero/
├── AI/           # LangGraph 기반 AI 에이전트 및 리포트 생성 엔진 (Spring Boot)
├── Backend/      # API Gateway 및 메인 비즈니스 서버 (Spring Boot)
├── Frontend/     # React 기반 사용자 인터페이스 (TypeScript/Tailwind)
└── Utility/      # DART 데이터 파싱 및 OpenSearch 인계 엔진 (FastAPI)
```

---

## ✨ Key Features

### LangGraph 기반 멀티 에이전트 시스템
- 단순한 프롬프트 실행이 아닌, **Source Selection -> Draft Generation -> Cross Validation**으로 이어지는 순환형 워크플로우를 통해 리포트의 신뢰성을 극대화합니다.
- AI 에이전트가 생성된 초안을 자체 검증(Self-Correction)하여 법적·형식적 오류를 최소화합니다.

### 고성능 데이터 파이프라인 (RAG)
- **Utility** 모듈에서 DART의 복잡한 공시 XML 데이터를 구조화된 JSON으로 변환하여 **OpenSearch**에 실시간 색인합니다.
- AI 에이전트는 색인된 데이터를 바탕으로 근거 있는(Grounding) 답변을 생성하는 RAG(Retrieval-Augmented Generation) 시스템을 구현합니다.

### 이벤트 기반 비동기 처리
- 사용자의 리포트 생성 요청은 **Kafka**를 통해 비동기로 처리되며, 작업 완료 시 백엔드와 프론트엔드에 실시간으로 상태를 공유합니다.

### 리포트 에디터 및 버전 관리
- AI가 생성한 초안을 사용자가 직접 편집할 수 있으며, 수정 이력을 **버전별로 관리**하여 이전 상태로의 복구가 용이합니다.

---

## 🎥 시연 영상

[![Securities Hero Demo Video](https://img.youtube.com/vi/kbONGfd1nsM/0.jpg)](https://www.youtube.com/watch?v=kbONGfd1nsM)

*이미지를 클릭하면 시연 영상(YouTube)으로 이동합니다.*
