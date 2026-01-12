import requests as rq
from app.constants.financials.financials_mappings import keep_cols, ACCOUNT_MAP, STATEMENT_MAP
import re

# 환경 변수 가져오기
DART_API_KEY = '4643bd437d383b208294914ce72d693589458062'
url = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json"


def get_final_list(corp_code):
    fin_list = get_financial_data(corp_code)
    processed_list = process_list(fin_list, corp_code)
    final_list = deduplicate_financials(processed_list)
    return final_list




def get_financial_data(corp_code):
    params = {
        "crtfc_key": DART_API_KEY,
        "corp_code": corp_code,
        "bsns_year": 2024,
        "reprt_code": "11011",
        "fs_div": "CFS",
    }

    try:
        response = rq.get(url, params=params, timeout=10)
        result = response.json()

        if result.get("status") != "000":
            params["fs_div"] = "OFS"
            response = rq.get(url, params=params, timeout=10)
            result = response.json()

        data_list = result.get("list", [])

        fin_list = [
            {col: item[col] for col in keep_cols if col in item}
            for item in data_list
        ]

    except Exception as e:
        print(f"Exception fetching data for {corp_code}: {e}")
        return []

    return fin_list


def to_float(value):
    try:
        return float(value.replace(",", "")) if value not in (None, "", "-") else 0
    except:
        return 0

# 1. 매핑된 표준 계정명을 찾아주는 함수
def map_account_name(name: str, account_map: dict) -> str:
    for std_name, variants in account_map.items():
        if name in variants:  # variants 리스트 안에 있으면 표준명 반환
            return std_name
    return name  # 없으면 원래 이름 그대로


def clean_account_name(account_name: str) -> str:
    text = re.sub(
        r"^([ⅰ-ⅹⅠ-ⅩⅪⅫ]+|[IVXLCDM]+|\d+)\.\s*",
        "",
        account_name,
        flags=re.IGNORECASE,
    )
    return text.replace(" ", "").strip()



def process_list(fin_list, corp_code):
    process_list = []
    for item in fin_list:  # 아까 만든 전처리된 리스트
        account_nm = clean_account_name(item['account_nm'])
        mapped_name = map_account_name(account_nm, ACCOUNT_MAP)

        doc = {
            "corp_code": corp_code,
            "account_nm": mapped_name,  # 매핑된 표준 계정명
            "thstrm_amount": to_float(item["thstrm_amount"]),
            "frmtrm_amount": to_float(item["frmtrm_amount"]),
            "bfefrmtrm_amount": to_float(item["bfefrmtrm_amount"]),
            "sj_div": item["sj_div"]
        }
        process_list.append(doc)
    
    return process_list



def deduplicate_financials(docs):
    result, seen = [], {}

    for doc in docs:
        acc, sj_div = doc["account_nm"], doc["sj_div"]

        if acc in STATEMENT_MAP:
            preferred = STATEMENT_MAP[acc]
            if acc not in seen or (
                sj_div in preferred
                and preferred.index(sj_div) < preferred.index(seen[acc]["sj_div"])
            ):
                seen[acc] = doc
        else:
            result.append(doc)

    return result + list(seen.values())
