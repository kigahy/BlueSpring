import requests
import json
import time
from datetime import datetime


# 날짜 변환 함수
def convert_to_date(date_str, date_format, output_format="%Y-%m-%d"):
    try:
        date_obj = datetime.strptime(date_str, date_format)
        return date_obj.strftime(output_format)
    except ValueError:
        return None


# URL 요청 함수
def fetch_url_with_retries(url, retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise


# 안전한 JSON 로드 함수
def load_json_safe(filepath, default=None):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default if default is not None else []


# JSON 데이터를 가져와 JSON 파일로 저장하는 함수
def fetch_and_convert_to_json(topFinGrpNo, pageNo, products_json_filename, options_json_filename):
    api_key = 'adacd855f3d03e39ba22a2a45a5f8158'

    # 기존 데이터 로드
    existing_products = load_json_safe(products_json_filename, [])
    existing_options = load_json_safe(options_json_filename, [])

    is_continue = True
    while is_continue:
        url = f"http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo={topFinGrpNo}&pageNo={pageNo}"
        response = fetch_url_with_retries(url)
        data = response.json()
        result = data.get('result', None)

        if result is None:
            print(f"Invalid response: {data}")
            break

        is_continue = bool(result.get('max_page_no', {}) != result.get('now_page_no', {}))

        # 상품 데이터 처리
        products = result.get('baseList', [])
        for product in products:
            product_records = {
                'model': 'fin_products.depositproduct',
                'pk': product.get('fin_prdt_cd', None),  # fin_prdt_cd를 pk로 사용
                'fields': {
                    'dcls_month': convert_to_date(product.get('dcls_month', None), "%Y%m", "%Y-%m-01") if product.get('dcls_month', None) else None,
                    'fin_co_no': product.get('fin_co_no', None),
                    'kor_co_nm': product.get('kor_co_nm', None),
                    'fin_prdt_nm': product.get('fin_prdt_nm', None),
                    'join_way': product.get('join_way', None),
                    'mtrt_int': product.get('mtrt_int', None),
                    'spcl_cnd': product.get('spcl_cnd', None),
                    'join_deny': product.get('join_deny', None),
                    'join_member': product.get('join_member', None),
                    'etc_note': product.get('etc_note', None),
                    'max_limit': product.get('max_limit', None),
                    'dcls_strt_day': convert_to_date(product.get('dcls_strt_day', None), "%Y%m%d", "%Y-%m-%d") if product.get('dcls_strt_day', None) else None,
                    'dcls_end_day': convert_to_date(product.get('dcls_end_day', None), "%Y%m%d", "%Y-%m-%d") if product.get('dcls_end_day', None) else None,
                }
            }
            existing_products.append(product_records)

        # 옵션 데이터 처리
        options = result.get('optionList', [])
        for option in options:
            option_records = {
                'model': 'fin_products.depositoption',
                'pk': option.get('option_id', None),  # option_id를 pk로 사용
                'fields': {
                    'dcls_month': convert_to_date(option.get('dcls_month', None), "%Y%m", "%Y-%m-01") if option.get('dcls_month', None) else None,
                    'fin_co_no': option.get('fin_co_no', None),
                    'fin_prdt_cd': option.get('fin_prdt_cd', None),  # 외래 키로 DepositProduct의 fin_prdt_cd 사용
                    'intr_rate_type': option.get('intr_rate_type', None),
                    'intr_rate_type_nm': option.get('intr_rate_type_nm', None),
                    'save_trm': option.get('save_trm', None),
                    'intr_rate': option.get('intr_rate', None),
                    'intr_rate2': option.get('intr_rate2', None)
                }
            }
            existing_options.append(option_records)

        print(f"topFinGrpNo={topFinGrpNo}, pageNo={pageNo}: 데이터 처리 완료.")
        pageNo += 1
        time.sleep(2)

    # DepositProduct JSON 파일로 저장
    with open(products_json_filename, 'w', encoding='utf-8') as file:
        json.dump(existing_products, file, ensure_ascii=False, indent=4)
    print(f"{products_json_filename} 저장 완료.")

    # DepositOption JSON 파일로 저장
    with open(options_json_filename, 'w', encoding='utf-8') as file:
        json.dump(existing_options, file, ensure_ascii=False, indent=4)
    print(f"{options_json_filename} 저장 완료.")


if __name__ == "__main__":
    # JSON 변환 실행
    topFinGrpNo_list = ["020000", "030200", "030300", "050000", "060000"]
    for topFinGrpNo in topFinGrpNo_list:
        fetch_and_convert_to_json(topFinGrpNo, 1, "deposit_products.json", "deposit_options.json")
