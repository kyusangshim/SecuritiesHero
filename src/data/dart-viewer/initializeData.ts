const section1 = 
`<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>증권신고서</title>
    <style>
        body {
            font-family: 'Malgun Gothic', sans-serif;
            line-height: 1.6;
            margin: 20px;
            color: #333;
            background: white;
        }
        .document-content {
            max-width: 800px;
            margin: 0 auto;
        }
        .part {
            max-width: 800px;
            margin: 0 auto;
        }
        h1, h2, h3, h4, h5 {
            color: #2c3e50;
            margin-top: 30px;
            margin-bottom: 15px;
        }
        h1 { font-size: 28px; }
        h2 { font-size: 24px; }
        h3 { font-size: 20px; }
        h4 { font-size: 18px; }
        h5 { font-size: 16px; }
        p {
            margin-bottom: 15px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            border: 1px solid #ddd;
            text-align: left;
        }
        th {
            background-color: #f8f9fa;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="part">
        <h1 style="text-align: center; font-size: 24px; margin: 40px 0;">증권신고서</h1>
        <h2 style="text-align: center; font-size: 18px; margin: 20px 0;">(지분증권)</h2>
        
        <div style="margin: 40px 0;">
            <table style="width: 100%; border-collapse: collapse;">
                <tbody><tr>
                    <td style="padding: 10px; border: 1px solid #ddd; background: #f5f5f5; width: 150px;"><strong>금융위원회 귀중</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">2022년 08월 16일</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd; background: #f5f5f5;"><strong>회사명</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">오픈엣지테크놀로지 주식회사</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd; background: #f5f5f5;"><strong>대표이사</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">이성현</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd; background: #f5f5f5;"><strong>본점소재지</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">서울특별시 강남구 역삼로 114 한독빌딩 13층</td>
                </tr>
            </tbody></table>
        </div>
    </div>


</body>
</html>`

const section2 = 
`<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>대표이사 등의 확인</title>
    <style>
        body {
            font-family: 'Malgun Gothic', sans-serif;
            line-height: 1.6;
            margin: 20px;
            color: #333;
            background: white;
        }
        .document-content {
            max-width: 800px;
            margin: 0 auto;
        }
        .part {
            max-width: 800px;
            margin: 0 auto;
        }
        h1, h2, h3, h4, h5 {
            color: #2c3e50;
            margin-top: 30px;
            margin-bottom: 15px;
        }
        h2 { font-size: 24px; }
        p {
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="part">
        <h2>【 대표이사 등의 확인 】</h2>
        <p>본 회사는 이 증권신고서의 기재내용이 거짓이나 빠뜨린 것이 없으며, 기재된 내용이 모두 사실과 일치한다는 것을 확인합니다.</p>
        <div style="margin: 40px 0; text-align: right;">
            <p>2022년 08월 16일</p>
            <p><strong>오픈엣지테크놀로지 주식회사</strong></p>
            <p>대표이사 이성현 (인)</p>
        </div>
    </div>
</body>
</html>`

const section3 = 
`<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>요약정보</title>
    <style>
        body {
            font-family: 'Malgun Gothic', sans-serif;
            line-height: 1.6;
            margin: 20px;
            color: #333;
            background: white;
        }
        .document-content {
            max-width: 800px;
            margin: 0 auto;
        }
        .part {
            max-width: 800px;
            margin: 0 auto;
        }
        .part-title {
            color: #2c3e50;
            font-size: 28px;
            margin: 40px 0 30px 0;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
        }
        .section-2 {
            margin: 30px 0;
            padding: 20px 0;
            border-bottom: 1px solid #ecf0f1;
        }
        .section-2:last-child {
            border-bottom: none;
        }
        .section-2-title {
            color: #2c3e50;
            font-size: 20px;
            margin: 0 0 15px 0;
        }
        .warning-box {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .warning-title {
            color: #856404;
            font-size: 18px;
            margin-bottom: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            border: 1px solid #ddd;
            text-align: left;
        }
        th {
            background-color: #f8f9fa;
            font-weight: bold;
        }
        ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        li {
            margin-bottom: 8px;
        }
        p {
            margin-bottom: 15px;
        }
        h3 {
            color: #2c3e50;
            font-size: 18px;
            margin: 20px 0 10px 0;
        }
    </style>
</head>
<body>
    <div class="part">
        <h1 class="part-title">요약정보</h1>
        
        <div class="section-2" data-section="핵심투자위험">
            <h2 class="section-2-title">1. 핵심투자위험</h2>
            <div class="warning-box">
                <h4 class="warning-title">⚠️ 투자위험 경고</h4>
                <ul>
                    <li>이 증권의 투자에는 다음과 같은 위험이 있으므로 투자 전에 신중히 검토하시기 바랍니다.</li>
                    <li>증권의 가치는 시장상황에 따라 변동될 수 있으며, 투자원금의 손실이 발생할 수 있습니다.</li>
                    <li>회사의 영업실적 악화, 재무상태 변화 등으로 인해 투자손실이 발생할 수 있습니다.</li>
                    <li>시장 유동성 부족으로 인해 원하는 시점에 매도가 어려울 수 있습니다.</li>
                    <li>금리 변동, 환율 변동 등 거시경제적 요인에 의한 위험이 존재합니다.</li>
                    <li>코스닥 시장의 높은 변동성으로 인한 주가 급등락 위험이 있습니다.</li>
                </ul>
            </div>
            
            <h3>주요 투자위험 요소</h3>
            <p>투자자는 다음과 같은 주요 위험요소를 반드시 고려해야 합니다:</p>
            <ul>
                <li><strong>기술위험:</strong> 급속한 기술 변화로 인한 제품 경쟁력 저하 위험</li>
                <li><strong>시장위험:</strong> 경기 변동 및 산업 환경 변화에 따른 위험</li>
                <li><strong>경영위험:</strong> 핵심 인력 이탈 및 경영진 변화에 따른 위험</li>
                <li><strong>재무위험:</strong> 자금조달 및 유동성 확보의 어려움</li>
            </ul>
        </div>
        
        <div class="section-2" data-section="모집 또는 매출에 관한 일반사항">
            <h2 class="section-2-title">2. 모집 또는 매출에 관한 일반사항</h2>
            
            <h3>모집 개요</h3>
            <table>
                <tr style="background: #f8f9fa;">
                    <th>구분</th>
                    <th>내용</th>
                </tr>
                <tr>
                    <td>모집주식수</td>
                    <td>3,636,641주</td>
                </tr>
                <tr>
                    <td>모집 또는 매출예정금액</td>
                    <td>54,549,615,000원</td>
                </tr>
                <tr>
                    <td>발행가액</td>
                    <td>15,000원</td>
                </tr>
                <tr>
                    <td>액면가액</td>
                    <td>500원</td>
                </tr>
                <tr>
                    <td>발행가액의 액면가액에 대한 비율</td>
                    <td>3,000%</td>
                </tr>
                <tr>
                    <td>모집방법</td>
                    <td>일반공모</td>
                </tr>
            </table>
            
            <h3>공모 일정</h3>
            <table>
                <tr style="background: #f8f9fa;">
                    <th>구분</th>
                    <th>일정</th>
                </tr>
                <tr>
                    <td>수요예측</td>
                    <td>2022.08.22 ~ 2022.08.23</td>
                </tr>
                <tr>
                    <td>공모가격 결정</td>
                    <td>2022.08.24</td>
                </tr>
                <tr>
                    <td>일반투자자 청약</td>
                    <td>2022.08.25 ~ 2022.08.26</td>
                </tr>
                <tr>
                    <td>배정 및 환불</td>
                    <td>2022.08.30</td>
                </tr>
                <tr>
                    <td>납입일</td>
                    <td>2022.09.01</td>
                </tr>
                <tr>
                    <td>상장예정일</td>
                    <td>2022.09.07</td>
                </tr>
            </table>
            
            <h3>자금 사용 계획</h3>
            <p>이번 공모를 통해 조달된 자금은 다음과 같이 사용될 예정입니다:</p>
            <ul>
                <li><strong>연구개발비 (55%):</strong> 300억원 - 차세대 엣지 컴퓨팅 기술 개발</li>
                <li><strong>시설투자비 (27%):</strong> 150억원 - 생산설비 확충 및 사무공간 확장</li>
                <li><strong>운영자금 (18%):</strong> 100억원 - 마케팅 및 인력 충원</li>
            </ul>
            
            <h3>주관회사</h3>
            <p>본 공모의 주관회사는 다음과 같습니다:</p>
            <ul>
                <li><strong>대표주관회사:</strong> 미래에셋증권</li>
                <li><strong>공동주관회사:</strong> 삼성증권, 키움증권</li>
            </ul>
        </div>
    </div>
</body>
</html>`

const section4 = 
`<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>제1부 모집 또는 매출에 관한 사항</title>
    <style>
      body {
        font-family: "Malgun Gothic", sans-serif;
        line-height: 1.6;
        margin: 20px;
        color: #333;
        background: white;
      }
      .document-content {
        max-width: 800px;
        margin: 0 auto;
      }
      .part {
        max-width: 800px;
        margin: 0 auto;
      }
      .part-title {
        color: #2c3e50;
        font-size: 28px;
        margin: 40px 0 30px 0;
        text-align: center;
        border-bottom: 3px solid #3498db;
        padding-bottom: 15px;
      }
      .section-1 {
        margin: 30px 0;
        padding: 20px 0;
        border-bottom: 2px solid #ecf0f1;
      }
      .section-1:last-child {
        border-bottom: none;
      }
      .section-1-title {
        color: #2c3e50;
        font-size: 24px;
        margin: 0 0 20px 0;
        border-left: 5px solid #3498db;
        padding-left: 15px;
      }
      .section-2 {
        margin: 20px 0;
        padding: 15px 0;
        border-bottom: 1px solid #f0f0f0;
      }
      .section-2:last-child {
        border-bottom: none;
      }
      .section-2-title {
        color: #2c3e50;
        font-size: 18px;
        margin: 0 0 10px 0;
      }
      p {
        margin-bottom: 15px;
      }
      ul {
        margin: 10px 0;
        padding-left: 20px;
      }
      li {
        margin-bottom: 8px;
      }
      h3 {
        color: #2c3e50;
        font-size: 16px;
        margin: 15px 0 8px 0;
      }
    </style>
  </head>
  <body>
    <div class="part">
      <h1 class="part-title">제1부 모집 또는 매출에 관한 사항</h1>

      <div class="section-1" data-section="모집 또는 매출에 관한 일반사항">
        <h2 class="section-1-title">I. 모집 또는 매출에 관한 일반사항</h2>

        <div class="section-2" data-section="공모개요">
          <h3 class="section-2-title">1. 공모개요</h3>
          <p>
            본 공모는 오픈엣지테크놀로지 주식회사의 코스닥시장 상장을 위한
            일반공모입니다.
          </p>
          <p>
            회사는 클라우드 기반 엣지 컴퓨팅 솔루션을 제공하는 기술기업으로,
            이번 상장을 통해 연구개발 투자 확대 및 글로벌 시장 진출을 계획하고
            있습니다.
          </p>
        </div>

        <div class="section-2" data-section="공모방법">
          <h3 class="section-2-title">2. 공모방법</h3>
          <p>
            본 공모는 「자본시장과 금융투자업에 관한 법률」에 따른 일반공모
            방식으로 진행됩니다.
          </p>
          <ul>
            <li>기관투자자 대상 수요예측: 70%</li>
            <li>일반투자자 대상 청약: 30%</li>
          </ul>
        </div>

        <div class="section-2" data-section="공모가격 결정방법">
          <h3 class="section-2-title">3. 공모가격 결정방법</h3>
          <p>공모가격은 수요예측을 통해 결정됩니다.</p>
          <p>
            수요예측 결과와 시장 상황을 종합적으로 고려하여 최종 공모가격을
            확정할 예정입니다.
          </p>
        </div>

        <div class="section-2" data-section="모집 또는 매출절차 등에 관한 사항">
          <h3 class="section-2-title">4. 모집 또는 매출절차 등에 관한 사항</h3>
          <p>모집절차는 다음과 같은 단계로 진행됩니다:</p>
          <ul>
            <li>수요예측 (기관투자자 대상)</li>
            <li>공모가격 결정</li>
            <li>일반투자자 청약</li>
            <li>배정 및 납입</li>
            <li>상장</li>
          </ul>
        </div>

        <div class="section-2" data-section="인수 등에 관한 사항">
          <h3 class="section-2-title">5. 인수 등에 관한 사항</h3>
          <p>본 공모의 주관회사는 다음과 같습니다:</p>
          <ul>
            <li>대표주관회사: 미래에셋증권</li>
            <li>공동주관회사: 삼성증권, 키움증권</li>
          </ul>
        </div>
      </div>

      <div class="section-1" data-section="증권의 주요 권리내용">
        <h2 class="section-1-title">II. 증권의 주요 권리내용</h2>
        <p>발행되는 주식의 주요 권리내용은 다음과 같습니다:</p>
        <ul>
          <li>의결권: 1주당 1개의 의결권</li>
          <li>배당권: 이익배당 및 잉여재산분배 참여권</li>
          <li>신주인수권: 신주 발행 시 우선 인수권</li>
        </ul>
      </div>

      <div class="section-1" data-section="투자위험요소">
        <h2 class="section-1-title">III. 투자위험요소</h2>

        <div class="section-2" data-section="사업위험">
          <h3 class="section-2-title">1. 사업위험</h3>
          <p>회사의 사업과 관련된 주요 위험요소는 다음과 같습니다:</p>
          <ul>
            <li>기술 변화에 따른 위험</li>
            <li>경쟁 심화에 따른 위험</li>
            <li>주요 고객사 의존도 위험</li>
          </ul>
        </div>

        <div class="section-2" data-section="회사위험">
          <h3 class="section-2-title">2. 회사위험</h3>
          <p>회사 고유의 위험요소:</p>
          <ul>
            <li>핵심 인력 이탈 위험</li>
            <li>지적재산권 관련 위험</li>
            <li>자금조달 위험</li>
          </ul>
        </div>

        <div class="section-2" data-section="기타위험">
          <h3 class="section-2-title">3. 기타위험</h3>
          <p>기타 투자 시 고려해야 할 위험요소:</p>
          <ul>
            <li>시장 변동성 위험</li>
            <li>유동성 위험</li>
            <li>규제 변화 위험</li>
          </ul>
        </div>
      </div>
      <div class="section-1" data-section="인수인의 의견(분석기관의 평가의견)">
        <h2 class="section-1-title">IV. 인수인의 의견(분석기관의 평가의견)</h2>
        <p>발행되는 주식의 주요 권리내용은 다음과 같습니다:</p>
        <ul>
          <li>의결권: 1주당 1개의 의결권</li>
          <li>배당권: 이익배당 및 잉여재산분배 참여권</li>
          <li>신주인수권: 신주 발행 시 우선 인수권</li>
        </ul>
      </div>
      <div class="section-1" data-section="자금의 사용목적">
        <h2 class="section-1-title">V. 자금의 사용목적</h2>
        <p>발행되는 주식의 주요 권리내용은 다음과 같습니다:</p>
        <ul>
          <li>의결권: 1주당 1개의 의결권</li>
          <li>배당권: 이익배당 및 잉여재산분배 참여권</li>
          <li>신주인수권: 신주 발행 시 우선 인수권</li>
        </ul>
      </div>
      <div
        class="section-1"
        data-section="그 밖에 투자자보호를 위해 필요한 사항"
      >
        <h2 class="section-1-title">
          VI. 그 밖에 투자자보호를 위해 필요한 사항
        </h2>
        <p>발행되는 주식의 주요 권리내용은 다음과 같습니다:</p>
        <ul>
          <li>의결권: 1주당 1개의 의결권</li>
          <li>배당권: 이익배당 및 잉여재산분배 참여권</li>
          <li>신주인수권: 신주 발행 시 우선 인수권</li>
        </ul>
      </div>
    </div>
  </body>
</html>`

const section5 = 
`<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>제2부 발행인에 관한 사항</title>
  <style>
    body {
      font-family: 'Malgun Gothic', sans-serif;
      line-height: 1.6;
      margin: 20px;
      color: #333;
      background: white;
    }
    .document-content {
      max-width: 800px;
      margin: 0 auto;
    }
    .part {
      max-width: 800px;
      margin: 0 auto;
    }
    .part-title {
      color: #2c3e50;
      font-size: 28px;
      margin: 40px 0 30px 0;
      text-align: center;
      border-bottom: 3px solid #3498db;
      padding-bottom: 15px;
    }
    .section-1 {
      margin: 30px 0;
      padding: 20px 0;
      border-bottom: 2px solid #ecf0f1;
    }
    .section-1-title {
      color: #2c3e50;
      font-size: 24px;
      margin: 0 0 20px 0;
      border-left: 5px solid #3498db;
      padding-left: 15px;
    }
    .section-2 {
      margin: 20px 0;
      padding: 15px 0;
      border-bottom: 1px solid #f0f0f0;
    }
    .section-2-title {
      color: #2c3e50;
      font-size: 18px;
      margin: 0 0 10px 0;
    }
    p {
      margin-bottom: 15px;
    }
    ul {
      margin: 10px 0;
      padding-left: 20px;
    }
    li {
      margin-bottom: 8px;
    }
  </style>
</head>
<body>
    <div class="part">
      <h1 class="part-title">제2부 발행인에 관한 사항</h1>

      <div class="section-1" data-section="회사의 개요">
        <h2 class="section-1-title">I. 회사의 개요</h2>
        <div class="section-2" data-section="회사의 개요">
          <h3 class="section-2-title">1. 회사의 개요</h3>
          <p>회사의 설립 목적, 주요 사업 내용 및 조직 구조를 포함합니다.</p>
        </div>
        <div class="section-2" data-section="회사의 연혁">
          <h3 class="section-2-title">2. 회사의 연혁</h3>
          <p>회사의 설립부터 현재까지 주요 연혁 및 변동 사항을 기술합니다.</p>
        </div>
        <div class="section-2" data-section="자본금 변동사항">
          <h3 class="section-2-title">3. 자본금 변동사항</h3>
          <p>자본금의 증감 내역과 주요 변동 사유를 포함합니다.</p>
        </div>
        <div class="section-2" data-section="주식의 총수 등">
          <h3 class="section-2-title">4. 주식의 총수 등</h3>
          <p>발행 주식의 총수, 종류 및 주식 분포 현황을 포함합니다.</p>
        </div>
        <div class="section-2" data-section="정관에 관한 사항">
          <h3 class="section-2-title">5. 정관에 관한 사항</h3>
          <p>회사의 정관 주요 내용 및 개정 내역을 기술합니다.</p>
        </div>
      </div>

      <div class="section-1" data-section="사업의 내용">
        <h2 class="section-1-title">II. 사업의 내용</h2>
        <div class="section-2" data-section="사업의 개요">
          <h3 class="section-2-title">1. 사업의 개요</h3>
          <p>회사가 영위하는 주요 사업 분야와 시장 환경을 포함합니다.</p>
        </div>
        <div class="section-2" data-section="주요 제품 및 서비스">
          <h3 class="section-2-title">2. 주요 제품 및 서비스</h3>
          <p>회사의 주요 제품 및 서비스의 특징과 경쟁력을 기술합니다.</p>
        </div>
        <div class="section-2" data-section="원재료 및 생산설비">
          <h3 class="section-2-title">3. 원재료 및 생산설비</h3>
          <p>주요 원재료 공급 현황과 생산설비의 운영 상태를 포함합니다.</p>
        </div>
        <div class="section-2" data-section="매출 및 수주상황">
          <h3 class="section-2-title">4. 매출 및 수주상황</h3>
          <p>최근 매출 실적과 수주 현황 및 전망을 기술합니다.</p>
        </div>
        <div class="section-2" data-section="위험관리 및 파생거래">
          <h3 class="section-2-title">5. 위험관리 및 파생거래</h3>
          <p>사업 운영과 관련된 주요 리스크와 파생상품 거래 내역을 포함합니다.</p>
        </div>
        <div class="section-2" data-section="주요계약 및 연구개발활동">
          <h3 class="section-2-title">6. 주요계약 및 연구개발활동</h3>
          <p>주요 사업 계약과 연구개발 활동의 진행 상황을 기술합니다.</p>
        </div>
        <div class="section-2" data-section="기타 참고사항">
          <h3 class="section-2-title">7. 기타 참고사항</h3>
          <p>사업과 관련된 기타 중요한 정보를 포함합니다.</p>
        </div>
      </div>

      <div class="section-1" data-section="재무에 관한 사항">
        <h2 class="section-1-title">III. 재무에 관한 사항</h2>
        <div class="section-2" data-section="요약재무정보">
          <h3 class="section-2-title">1. 요약재무정보</h3>
          <p>최근 3개년 요약재무정보를 표 형태로 제공합니다.</p>
        </div>
        <div class="section-2" data-section="연결재무제표">
          <h3 class="section-2-title">2. 연결재무제표</h3>
          <p>연결 기준 재무상태표, 손익계산서, 현금흐름표를 포함합니다.</p>
        </div>
        <div class="section-2" data-section="연결재무제표 주석">
          <h3 class="section-2-title">3. 연결재무제표 주석</h3>
          <p>주요 회계처리기준 및 상세 항목별 설명을 포함합니다.</p>
        </div>
        <div class="section-2" data-section="재무제표">
          <h3 class="section-2-title">4. 재무제표</h3>
          <p>개별 기준 재무제표를 제공합니다.</p>
        </div>
        <div class="section-2" data-section="재무제표 주석">
          <h3 class="section-2-title">5. 재무제표 주석</h3>
          <p>재무제표 항목에 대한 상세 설명이 포함됩니다.</p>
        </div>
        <div class="section-2" data-section="배당에 관한 사항">
          <h3 class="section-2-title">6. 배당에 관한 사항</h3>
          <p>최근 3년간 배당 내역 및 배당 정책이 기술됩니다.</p>
        </div>
        <div class="section-2" data-section="증권의 발행을 통한 자금조달에 관한 사항">
          <h3 class="section-2-title">7. 증권의 발행을 통한 자금조달에 관한 사항</h3>
          <p>자금조달 내역과 사용계획이 포함됩니다.</p>
        </div>
        <div class="section-2" data-section="기타 재무에 관한 사항">
          <h3 class="section-2-title">8. 기타 재무에 관한 사항</h3>
          <p>기타 참고 가능한 재무 관련 정보가 포함됩니다.</p>
        </div>
      </div>

      <div class="section-1" data-section="회계감사인의 감사의견 등">
        <h2 class="section-1-title">IV. 회계감사인의 감사의견 등</h2>
        <div class="section-2" data-section="외부감사에 관한 사항">
          <h3 class="section-2-title">1. 외부감사에 관한 사항</h3>
          <p>외부 감사인의 감사 범위와 의견 요약을 포함합니다.</p>
        </div>
        <div class="section-2" data-section="내부통제에 관한 사항">
          <h3 class="section-2-title">2. 내부통제에 관한 사항</h3>
          <p>내부회계관리제도에 대한 감사의견과 평가 내용이 포함됩니다.</p>
        </div>
      </div>

      <div class="section-1" data-section="이사회 등 회사의 기관에 관한 사항">
        <h2 class="section-1-title">V. 이사회 등 회사의 기관에 관한 사항</h2>
        <div class="section-2" data-section="이사회에 관한 사항">
          <h3 class="section-2-title">1. 이사회에 관한 사항</h3>
          <p>이사회의 구성, 운영방식 및 주요 의사결정 내용이 포함됩니다.</p>
        </div>
        <div class="section-2" data-section="감사제도에 관한 사항">
          <h3 class="section-2-title">2. 감사제도에 관한 사항</h3>
          <p>감사위원회 또는 감사의 구성과 역할이 포함됩니다.</p>
        </div>
        <div class="section-2" data-section="주주총회 등에 관한 사항">
          <h3 class="section-2-title">3. 주주총회 등에 관한 사항</h3>
          <p>정기 및 임시주주총회의 절차 및 의결 내용이 포함됩니다.</p>
        </div>
      </div>

      <div class="section-1" data-section="주주에 관한 사항">
        <h2 class="section-1-title">VI. 주주에 관한 사항</h2>
        <div class="section-2" data-section="주주 구성 및 지분 현황">
          <h3 class="section-2-title">1. 주주 구성 및 지분 현황</h3>
          <p>주요 주주 목록, 지분율 및 주주 변동 사항을 포함합니다.</p>
        </div>
      </div>

      <div class="section-1" data-section="임원 및 직원 등에 관한 사항">
        <h2 class="section-1-title">VII. 임원 및 직원 등에 관한 사항</h2>
        <div class="section-2" data-section="임원 및 직원 등의 현황">
          <h3 class="section-2-title">1. 임원 및 직원 등의 현황</h3>
          <p>임직원의 직급별, 부서별 인원 현황 및 평균 근속연수 등을 포함합니다.</p>
        </div>
        <div class="section-2" data-section="임원의 보수 등">
          <h3 class="section-2-title">2. 임원의 보수 등</h3>
          <p>임원의 보수, 성과급 및 스톡옵션 부여 내역 등을 포함합니다.</p>
        </div>
      </div>

      <div class="section-1" data-section="계열회사 등에 관한 사항">
        <h2 class="section-1-title">VIII. 계열회사 등에 관한 사항</h2>
        <div class="section-2" data-section="계열회사 현황">
          <h3 class="section-2-title">1. 계열회사 현황</h3>
          <p>계열회사의 목록, 지분 관계 및 주요 거래 내역을 포함합니다.</p>
        </div>
      </div>

      <div class="section-1" data-section="대주주 등과의 거래내용">
        <h2 class="section-1-title">IX. 대주주 등과의 거래내용</h2>
        <div class="section-2" data-section="대주주와의 거래 내역">
          <h3 class="section-2-title">1. 대주주와의 거래 내역</h3>
          <p>대주주 및 특수관계인과의 주요 거래 내용과 조건을 포함합니다.</p>
        </div>
      </div>

      <div class="section-1" data-section="그 밖에 투자자 보호를 위하여 필요한 사항">
        <h2 class="section-1-title">X. 그 밖에 투자자 보호를 위하여 필요한 사항</h2>
        <div class="section-2" data-section="공시내용 진행 및 변경사항">
          <h3 class="section-2-title">1. 공시내용 진행 및 변경사항</h3>
          <p>공시 내용의 진행 상황 및 변경 내역을 포함합니다.</p>
        </div>
        <div class="section-2" data-section="우발부채 등에 관한 사항">
          <h3 class="section-2-title">2. 우발부채 등에 관한 사항</h3>
          <p>우발부채 및 잠재적 부채와 관련된 사항을 기술합니다.</p>
        </div>
        <div class="section-2" data-section="제재 등과 관련된 사항">
          <h3 class="section-2-title">3. 제재 등과 관련된 사항</h3>
          <p>법적 제재, 소송 및 규제 관련 사항을 포함합니다.</p>
        </div>
        <div class="section-2" data-section="작성기준일 이후 발생한 주요사항 등 기타사항">
          <h3 class="section-2-title">4. 작성기준일 이후 발생한 주요사항 등 기타사항</h3>
          <p>작성 기준일 이후 발생한 주요 이벤트 및 기타 참고사항을 포함합니다.</p>
        </div>
      </div>

      <div class="section-1" data-section="상세표">
        <h2 class="section-1-title">XI. 상세표</h2>
        <div class="section-2" data-section="상세 재무 및 운영 데이터">
          <h3 class="section-2-title">1. 상세 재무 및 운영 데이터</h3>
          <p>재무 및 운영과 관련된 상세한 표와 데이터를 포함합니다.</p>
        </div>
      </div>

    </div>
</body>
</html>`

const section6 = 
`<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>【 전문가의 확인 】</title>
  <style>
    body {
      font-family: 'Malgun Gothic', sans-serif;
      line-height: 1.6;
      margin: 20px;
      color: #333;
      background: white;
    }
    .document-content {
      max-width: 800px;
      margin: 0 auto;
    }
    .part {
      max-width: 800px;
      margin: 0 auto;
    }
    .part-title {
      color: #2c3e50;
      font-size: 28px;
      margin: 40px 0 30px 0;
      text-align: center;
      border-bottom: 3px solid #3498db;
      padding-bottom: 15px;
    }
    .section-2 {
      margin: 20px 0;
      padding: 15px 0;
      border-bottom: 1px solid #f0f0f0;
    }
    .section-2-title {
      color: #2c3e50;
      font-size: 18px;
      margin: 0 0 10px 0;
    }
    p {
      margin-bottom: 15px;
    }
    ul {
      margin: 10px 0;
      padding-left: 20px;
    }
    li {
      margin-bottom: 8px;
    }
  </style>
</head>
<body>
    <div class="part">
      <h1 class="part-title">【 전문가의 확인 】</h1>
      <div class="section-2" data-section="전문가의 확인">
        <h3 class="section-2-title">1. 전문가의 확인</h3>
        <p>전문가의 검토 및 확인 절차와 그 결과에 대한 내용을 포함합니다.</p>
      </div>
      <div class="section-2" data-section="전문가와의 이해관계">
        <h3 class="section-2-title">2. 전문가와의 이해관계</h3>
        <p>전문가와 회사 간의 이해관계 및 잠재적 이해충돌 사항을 기술합니다.</p>
      </div>
    </div>
</body>
</html>`

export function initializeData() {
  const sectionsData = {
    section1: section1,
    section2: section2,
    section3: section3,
    section4: section4,
    section5: section5,
    section6: section6,
  };

  return sectionsData;
}