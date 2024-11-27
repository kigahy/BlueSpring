import requests
from rest_framework.decorators import api_view
from django.http import JsonResponse
import xmltodict
import environ

# 환경 변수 초기화
env = environ.Env()
environ.Env.read_env()  # .env 파일을 읽어서 환경 변수를 설정

# API 키를 환경 변수에서 가져오기
API_KEY_JOBYOUNG = env('API_KEY_JOBYOUNG', default=None)  # 키가 없으면 None 반환

# Mock 데이터
MOCK_DATA = {
    "response": {
        "items": [
            {"policy_id": "P001", "policy_name": "청년 주거 지원"},
            {"policy_id": "P002", "policy_name": "청년 창업 지원"},
            {"policy_id": "P003", "policy_name": "청년 구직 활동 지원"}
        ]
    }
}

# 정책 조회
@api_view(['GET'])
def get_youth_policies(request):    
    if not API_KEY_JOBYOUNG:
        # API 키가 없을 때는 Mock 데이터 반환
        return JsonResponse(MOCK_DATA, safe=False)
    
    url = f'https://www.youthcenter.go.kr/opi/youthPlcyList.do?openApiVlak={API_KEY_JOBYOUNG}&display=6'    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            xml_data = response.text
            data_dict = xmltodict.parse(xml_data)
            return JsonResponse(data_dict, safe=False)
        else:
            return JsonResponse({'error': 'API 요청 실패', 'status_code': response.status_code}, status=500)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

# 정책 조회 디테일
@api_view(['GET'])
def get_youth_policies_detail(request, policy_id):    
    if not API_KEY_JOBYOUNG:
        # API 키가 없을 때는 Mock 데이터 반환
        return JsonResponse({'error': 'API 키가 없습니다. 디테일 조회는 불가능합니다.'}, status=400)

    url = f'https://www.youthcenter.go.kr/opi/youthPlcyList.do?openApiVlak={API_KEY_JOBYOUNG}&display=1&srchPolicyId={policy_id}'    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            xml_data = response.text
            data_dict = xmltodict.parse(xml_data)
            return JsonResponse(data_dict, safe=False)
        else:
            return JsonResponse({'error': 'API 요청 실패', 'status_code': response.status_code}, status=500)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

from datetime import date
from .models import YouthPolicy, PolicyUpdateLog
# 메인페이지에서 보여줄 정책
@api_view(['GET'])
def get_youth_policies_main(request):
    today = date.today()
    # 1. 최신 업데이트 날짜 확인
    update_log, created = PolicyUpdateLog.objects.get_or_create(
        key="youth_policy_update", defaults={"value": today}
    )
    # 오늘 업데이트가 이미 되었다면 저장된 정보를 불러오자
    if update_log.value == today: 
        latest_policy = YouthPolicy.objects.last()
        # 만약 저장된 정보가 유효하다면(빈값이 아님) 바로 return 아닌경우는 아래에서 데이터 저장 후 return
        if latest_policy: return JsonResponse(xmltodict.parse(latest_policy.data), safe=False)

    # 최신 데이터가 없거나, 업데이트 날짜가 오늘이 아니면 Open API 호출
    url = f'https://www.youthcenter.go.kr/opi/youthPlcyList.do?openApiVlak={API_KEY_JOBYOUNG}&bizTycdSel=023020,023040&display=6&srchPolyBizSecd=003001&srchSortOrder=4'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            xml_data = response.text  # XML 데이터 저장
            data_dict = xmltodict.parse(xml_data)  # XML을 Python dict로 변환
            # 정책 데이터 저장
            YouthPolicy.objects.create(data=xml_data)
            # 업데이트 날짜 갱신
            update_log.value = today
            update_log.save()
            # 새 데이터를 반환
            return JsonResponse(data_dict, safe=False)
        else:
            return JsonResponse({'error': 'API 요청 실패', 'status_code': response.status_code}, status=500)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)


import xml.etree.ElementTree as ET
from rapidfuzz import fuzz
# XML 데이터 파싱 함수
def parse_xml_data(xml_data, similarity_threshold=0, compare_string=''):
    # XML 데이터 파싱
    root = ET.fromstring(xml_data)
    
    # 필요한 데이터 추출
    policies = []
    for policy in root.findall('.//youthPolicy'):
        biz_id = policy.find('bizId').text
        poly_biz_sjnm = policy.find('polyBizSjnm').text
        poly_itcn_cn = policy.find('polyItcnCn').text
        
        # 전체 XML 내용과 비교 문자열의 유사도 계산
        # 정책 내용과 비교할 기준 문자열을 전체 XML과 비교
        xml_string = ET.tostring(policy, encoding='unicode')
        similarity = fuzz.ratio(xml_string, compare_string)
        
        # 유사도가 설정한 임계값 이상일 경우 정책 추가
        if similarity >= similarity_threshold:
            policies.append({
                'biz_id': biz_id,
                'poly_biz_sjnm': poly_biz_sjnm,
                'poly_itcn_cn': poly_itcn_cn,
                'similarity': similarity
            })
    
    return policies

# 정책상품 추천 api
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import xml.etree.ElementTree as ET
# 요청 메서드 확인
@api_view(['GET'])
# 인증된 사용자만 접근 가능
@permission_classes([IsAuthenticated])
def rec_policies(request):
    # 현재 로그인된 사용자 정보 가져오기
    # user = request.user
    # region = user.region.strip().split()

    # city_codes = {
    #     '중앙부처': '003001',
    #     '서울': '003002001', '서울시': '003002001', '부산': '003002002', '부산시': '003002002',
    #     # 다른 지역 코드 생략...
    # }
    
    # city = region[0]
    # province = ''
    # if len(region) > 1: 
    #     province = region[1]

    # display = '100'
    # bizTycdSel = ''
    # srchPolyBizSecd = '003001,' + city_codes.get(city, '')
    # srchEdubg = '대졸'
    # srchWord = ''
    # url = f'https://www.youthcenter.go.kr/opi/youthPlcyList.do?openApiVlak={API_KEY_JOBYOUNG}&display={display}&bizTycdSel={bizTycdSel}&srchPolyBizSecd={srchPolyBizSecd}&srchWord={srchWord}'
    
    # response = requests.get(url)
    
    # if response.status_code != 200:
    #     return Response({'error': 'API 요청 실패'}, status=500)
    # # XML 데이터를 파싱하고, 유사도 기준으로 필터링
    # policies = parse_xml_data(response.text, similarity_threshold=0, compare_string=user.interest)
    
    # return Response({'policies': policies}, status=200)
    pass

def test():
    pass