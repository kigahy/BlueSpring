from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .models import DepositProduct, DepositOption, SavingProduct, SavingOption
from .serializers import DepositProductSerializer, DepositOptionSerializer, SavingProductSerializer, SavingOptionSerializer
from django.db.models import Max
# DepositProduct 리스트 반환 API
@api_view(['GET'])
def deposit_products_list(request):
    # 페이지 네이션 설정
    paginator = PageNumberPagination()
    paginator.page_size = 50  # 한 페이지에 반환할 항목 수
    # 데이터베이스에서 DepositProduct 모델 데이터를 가져옵니다.
    products = DepositProduct.objects.all()
    # 페이지 네이션 적용
    result_page = paginator.paginate_queryset(products, request)
    # 직렬화
    serializer = DepositProductSerializer(result_page, many=True)    
    # JSON 응답 반환
    return paginator.get_paginated_response(serializer.data)


# DepositOption 리스트 반환 API
@api_view(['GET'])
def deposit_options_list(request):
    # 페이지 네이션 설정
    paginator = PageNumberPagination()
    paginator.page_size = 50  # 한 페이지에 반환할 항목 수
    # 데이터베이스에서 DepositOption 모델 데이터를 가져옵니다.
    options = DepositOption.objects.all()
    # 페이지 네이션 적용
    result_page = paginator.paginate_queryset(options, request)
    # 직렬화
    serializer = DepositOptionSerializer(result_page, many=True)
    # JSON 응답 반환
    return paginator.get_paginated_response(serializer.data)


# SavingProduct 리스트 반환 API
@api_view(['GET'])
def saving_products_list(request):
    # 페이지 네이션 설정
    paginator = PageNumberPagination()
    paginator.page_size = 50  # 한 페이지에 반환할 항목 수
    # 데이터베이스에서 SavingProduct 모델 데이터를 가져옵니다.
    products = SavingProduct.objects.all()
    # 페이지 네이션 적용
    result_page = paginator.paginate_queryset(products, request)
    # 직렬화
    serializer = SavingProductSerializer(result_page, many=True)
    # JSON 응답 반환
    return paginator.get_paginated_response(serializer.data)


# SavingOption 리스트 반환 API
@api_view(['GET'])
def saving_options_list(request):
    # 페이지 네이션 설정
    paginator = PageNumberPagination()
    paginator.page_size = 50  # 한 페이지에 반환할 항목 수
    # 데이터베이스에서 SavingOption 모델 데이터를 가져옵니다.
    options = SavingOption.objects.all()
    # 페이지 네이션 적용
    result_page = paginator.paginate_queryset(options, request)
    # 직렬화
    serializer = SavingOptionSerializer(result_page, many=True)
    # JSON 응답 반환
    return paginator.get_paginated_response(serializer.data)


# 예금 상품 옵션 조회
@api_view(['GET'])
def deposit_product_options_list(request, fin_prdt_cd):
    # 페이지 네이션 설정
    paginator = PageNumberPagination()
    paginator.page_size = 50  # 한 페이지에 반환할 항목 수
    
    try:
        # 해당 예금 상품을 찾음
        product = DepositProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
        # 해당 예금 상품에 연관된 옵션들을 가져옴
        options = DepositOption.objects.filter(fin_prdt_cd=product)
        
        # 최고 금리 계산 (intr_rate 값을 기준으로)
        max_intr_rate = options.aggregate(max_rate=Max('intr_rate2'))['max_rate']

        # 페이지 네이션 적용
        result_page = paginator.paginate_queryset(options, request)
        
        # 직렬화
        serializer = DepositOptionSerializer(result_page, many=True)

        # 응답 데이터에 최고 금리 추가
        response_data = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'max_intr_rate': max_intr_rate,  # 최고 금리 추가
            'results': serializer.data,
        }

        # JSON 응답 반환
        return Response(response_data)
    
    except DepositProduct.DoesNotExist:
        return Response({"error": "예금 상품을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)


# 적금 상품 옵션 조회
@api_view(['GET'])
def saving_product_options_list(request, fin_prdt_cd):
    
    # 페이지 네이션 설정
    paginator = PageNumberPagination()
    paginator.page_size = 50  # 한 페이지에 반환할 항목 수
    
    try:
        # 해당 적금 상품을 찾음
        product = SavingProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
        # 해당 적금 상품에 연관된 옵션들을 가져옴
        options = SavingOption.objects.filter(fin_prdt_cd=product)
        
        # 최고 금리 계산 (intr_rate 값을 기준으로)
        max_intr_rate = options.aggregate(max_rate=Max('intr_rate2'))['max_rate']

        # 페이지 네이션 적용
        result_page = paginator.paginate_queryset(options, request)
        
        # 직렬화
        serializer = SavingOptionSerializer(result_page, many=True)

        # 응답 데이터에 최고 금리 추가
        response_data = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'max_intr_rate': max_intr_rate,  # 최고 금리 추가
            'results': serializer.data,
        }

        # JSON 응답 반환
        return Response(response_data)
    
    except SavingProduct.DoesNotExist:
        return Response({"error": "적금 상품을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

from django.db.models import Q    
from .serializers import SavingOptionSelectSerializer, DepositOptionSelectSerializer
# 예, 적금 상세검색
@api_view(['GET'])
def search_by_condition(request):
    data = request.GET
    keyword = data.get('keyword')
    productType = data.get('productType')    
    # min_term = float(data.get('min_term', 0)) or -1
    min_term = float(data.get('min_term', 0) or -1 )
    max_term = float(data.get('max_term', 0) or 1000)
    intr_rate_type = data.get('intr_rate_type', '')
    rsrv_type = data.get('cum_type', '') 


    if productType == '예금':
        # 키워드가 포함된 상품만 가져옴
        products = DepositProduct.objects.filter(
            Q(kor_co_nm__icontains=keyword) |
            Q(fin_prdt_nm__icontains=keyword) |
            Q(spcl_cnd__icontains=keyword) |
            Q(etc_note__icontains=keyword) 
            )
        # products와 일치하는 options만 추출
        options = DepositOption.objects.filter(fin_prdt_cd__in=products)
        options = options.filter(save_trm__gte=min_term, save_trm__lte=max_term)  
        if intr_rate_type: options = options.filter(intr_rate_type=intr_rate_type)
        Optionserializer = DepositOptionSelectSerializer(options, many=True)

    elif productType == '적금':
        products = SavingProduct.objects.filter(
            Q(kor_co_nm__icontains=keyword) |
            Q(fin_prdt_nm__icontains=keyword) |
            Q(spcl_cnd__icontains=keyword) |
            Q(etc_note__icontains=keyword) 
            )
        # products와 일치하는 options만 추출
        options = SavingOption.objects.filter(fin_prdt_cd__in=products)
        options = options.filter(save_trm__gte=min_term, save_trm__lte=max_term)
        if intr_rate_type: options = options.filter(intr_rate_type=intr_rate_type)
        if rsrv_type: options = options.filter(rsrv_type=rsrv_type)
        Optionserializer = SavingOptionSelectSerializer(options, many=True)

    return Response(Optionserializer.data)


from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from accounts.models import MyAccountTransaction, MyCardTransaction
from django.db.models import Sum, DateTimeField, F, Value
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.font_manager as fm
# Agg 백엔드 사용
matplotlib.use('Agg')
# 폰트 경로 및 설정
font_path = 'C:/Windows/Fonts/malgun.ttf'  # 윈도우에서 한글 폰트 경로
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
# 음수 기호 처리
plt.rcParams['axes.unicode_minus'] = False
from io import BytesIO
import base64
from django.db.models.functions import TruncHour, Cast, Concat
from decimal import Decimal

# 요청 메서드 확인
@api_view(['GET'])
# 인증된 사용자만 접근 가능
@permission_classes([IsAuthenticated])
def rec_fin_prdts(request):
    # 현재 로그인된 사용자 정보 가져오기
    user = request.user  

    # 해당 유저의 통장 거래내역과 카드 거래내역을 가져옵니다.
    account_transactions = MyAccountTransaction.objects.filter(user=user)
    card_transactions = MyCardTransaction.objects.filter(user=user)

    # 통장 데이터 분석 (수입과 지출을 합산)
    monthly_income = account_transactions.filter(money_amount__lt=0).aggregate(Sum('money_amount'))['money_amount__sum'] or Decimal(0)
    monthly_expense = account_transactions.filter(money_amount__gt=0).aggregate(Sum('money_amount'))['money_amount__sum'] or Decimal(0)

    # 카드 사용 내역 분석
    monthly_card_spending = card_transactions.aggregate(Sum('money_amount'))['money_amount__sum'] or Decimal(0)

    # 그래프 생성 함수
    # 그래프 생성 함수
    def generate_3d_hourly_graph(data, title, xlabel='일자', ylabel='시간대', zlabel='금액', point_labels=None, interval=3):
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')

        # X, Y, Z 데이터 준비
        x_data = [i for i in range(0, len(data['dates']), interval)]  # 인덱스를 interval 간격으로 사용
        y_data = data['times'][::interval]  # 시간대 (00시, 01시, ..., 23시)에서 interval 간격으로 추출
        z_data = data['spendings'][::interval]  # 해당 시간대별 소비 금액에서 interval 간격으로 추출

        # 3D 점 그래프
        ax.scatter(x_data, y_data, z_data, c=z_data, cmap='viridis')

        # X축, Y축, Z축 레이블 설정
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_zlabel(zlabel, fontsize=12)

        # X축에 일자 표시
        ax.set_xticks(x_data)
        ax.set_xticklabels([data['dates'][i] for i in x_data], rotation=45, fontsize=10)

        # 그래프 제목 설정
        ax.set_title(title, fontsize=14)

        # Z축에 금액 표시
        if point_labels:
            for i, label in enumerate(point_labels[::interval]):  # point_labels도 interval 간격으로 표시
                ax.text(x_data[i], y_data[i], z_data[i], f"{label:,.0f}", fontsize=9)

        plt.tight_layout()  # 레이아웃 자동 조정
        
        # 그래프 이미지를 메모리에서 처리하여 base64로 인코딩하여 반환
        img_stream = BytesIO()
        fig.savefig(img_stream, format='png')
        img_stream.seek(0)
        img_base64 = base64.b64encode(img_stream.getvalue()).decode('utf-8')
        return img_base64

    # 카드 거래 내역을 1시간 단위로 묶어서 분석
    card_transactions_hourly = card_transactions.annotate(
        # transaction_date와 transaction_time을 결합하여 DateTime으로 변환
        transaction_datetime=Cast(
            Concat(
                F('transaction_date'), 
                Value(' '),  # 날짜와 시간 사이에 공백 추가
                F('transaction_time')
            ),
            DateTimeField()
        )
    ).annotate(
        hour=TruncHour('transaction_datetime')  # 결합된 DateTime에서 1시간 단위로 묶기
    ).values('hour').annotate(
        total_spending=Sum('money_amount')  # 1시간 단위로 소비 금액 합산
    ).order_by('hour')
    # 굿
    # 카드 시간대별 소비 분석 (X축은 일자, Y축은 시간대)
    card_hour_data = {
        'dates': [transaction['hour'].strftime("%Y-%m-%d %H:00") for transaction in card_transactions_hourly],  # 일자 + 시간 추출
        'times': [transaction['hour'].hour for transaction in card_transactions_hourly],  # 시간 추출 (00시, 01시, ..., 23시)
        'spendings': [float(transaction['total_spending']) for transaction in card_transactions_hourly],  # Decimal을 float으로 변환
    }

    card_point_labels = [transaction['total_spending'] for transaction in card_transactions_hourly]  # 해당 시간대별 합산 금액

    card_hour_graph = generate_3d_hourly_graph(card_hour_data, "시간대별 카드 소비 분석", xlabel="일자", ylabel="시간대", point_labels=card_point_labels)

    # 통장 시간대별 소비 분석 (X축은 일자, Y축은 시간대)
    account_transactions_hourly = account_transactions.annotate(
        # transaction_date와 transaction_time을 결합하여 DateTime으로 변환
        transaction_datetime=Cast(
            Concat(
                F('transaction_date'), 
                Value(' '),  # 날짜와 시간 사이에 공백 추가
                F('transaction_time')
            ),
            DateTimeField()
        )
    ).annotate(
        hour=TruncHour('transaction_datetime')  # 결합된 DateTime에서 1시간 단위로 묶기
    ).values('hour').annotate(
        total_spending=Sum('money_amount')  # 1시간 단위로 소비 금액 합산
    ).order_by('hour')

    # 통장 시간대별 소비 분석 (X축은 일자, Y축은 시간대)
    account_hour_data = {
        'dates': [transaction['hour'].strftime("%Y-%m-%d %H:00") for transaction in account_transactions_hourly],  # 일자 + 시간 추출
        'times': [transaction['hour'].hour for transaction in account_transactions_hourly],  # 시간 추출 (00시, 01시, ..., 23시)
        'spendings': [float(transaction['total_spending']) for transaction in account_transactions_hourly],  # Decimal을 float으로 변환
    }

    account_point_labels = [transaction['total_spending'] for transaction in account_transactions_hourly]  # 해당 시간대별 합산 금액

    account_hour_graph = generate_3d_hourly_graph(account_hour_data, "시간대별 통장 소비 분석", xlabel="일자", ylabel="시간대", point_labels=account_point_labels)

    # 소비 패턴을 바탕으로 한 리스크 상태 분석
    risks = []
    if monthly_expense > monthly_income:
        risks.append("지출이 수입보다 많습니다. 저축 가능 금액을 확인하세요.")
    if monthly_card_spending > (monthly_income * Decimal('0.8')):  # 카드 사용 비율이 수입 대비 80% 초과
        risks.append("카드 사용 비율이 수입 대비 80%를 초과했습니다. 과소비를 줄이세요.")

    # 예금 상품 추천 (12개월 이상의 예금을 고금리 순으로 3개 추천)
    deposit_options = DepositOption.objects.filter(save_trm__gte=12).order_by('-intr_rate')[:3]
    recommendations = []
    for option in deposit_options:
        recommendations.append({
            "type": "예금",
            "product_name": option.fin_prdt_cd.fin_prdt_nm,
            "company_name": option.fin_prdt_cd.kor_co_nm,
            "interest_rate": option.intr_rate,
            "save_term": option.save_trm,
        })

    # 최고 지출 시간대 1시간 단위로 분석 (Top 3 시간대)
    top3_hours_account = sorted(account_transactions_hourly, key=lambda x: x['total_spending'], reverse=True)[:3]
    top3_hours_card = sorted(card_transactions_hourly, key=lambda x: x['total_spending'], reverse=True)[:3]
    print(monthly_income, monthly_expense, 111111111111111)
    # 최종 응답 반환
    return Response({
        "account_hour_graph": account_hour_graph,  # 시간대별 통장 소비 그래프
        "card_hour_graph": card_hour_graph,  # 1시간 단위 카드 소비 그래프
        "hour_spending_account": list(account_transactions_hourly),  # 시간대별 통장 소비 데이터
        "hour_spending_card": list(card_transactions_hourly),  # 시간대별 카드 소비 데이터
        "monthly_account_income": monthly_income,  # 월 수입
        "monthly_account_expense": monthly_expense,  # 월 지출
        "monthly_card_spending": monthly_card_spending,  # 월 카드 지출
        "risks": risks,  # 위험 분석
        "recommendations": recommendations,  # 예금 상품 추천
        "top3_hours_account": top3_hours_account,  # 최고 지출 시간대 (통장)
        "top3_hours_card": top3_hours_card,  # 최고 지출 시간대 (카드)
    })


from .serializers import DepositProductWithOptionsSerializer, SavingProductWithOptionsSerializer
@api_view(['GET'])
def get_recent_prdt_main(request):
    deposits = DepositProduct.objects.all().order_by('-dcls_strt_day')[:3]
    # DepositProduct와 연결된 DepositOption을 직렬화
    deposits_serializer = DepositProductWithOptionsSerializer(deposits, many=True)

    savings = SavingProduct.objects.all().order_by('-dcls_strt_day')[:3]
    # SavingProduct와 연결된 SavingOption을 직렬화
    savings_serializer = SavingProductWithOptionsSerializer(savings, many=True)

    return Response({'deposits': deposits_serializer.data, 'savings': savings_serializer.data})


@api_view(['GET'])
def main(request):
    latest_deposits = DepositProduct.objects.order_by('-dcls_strt_day')[:3]
    latest_savings = SavingProduct.objects.order_by('-dcls_strt_day')[:3]

    deposits_serializer = DepositProductWithOptionsSerializer(latest_deposits, many=True)
    savings_serializer = SavingProductWithOptionsSerializer(latest_savings, many=True)

    return Response({'deposits': deposits_serializer.data, 'savings': savings_serializer.data})

import requests
from bs4 import BeautifulSoup
@api_view(['GET'])
def main_dollar(request):
    url = 'https://finance.naver.com/marketindex/exchangeDetail.naver?marketindexCd=FX_USDKRW'
    # requests로 페이지 다운로드
    response = requests.get(url)
    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    # 미국 달러 환율 추출
    usd_krw = soup.find('table', class_='tbl_calculator')
    # 환율 값 추출
    usd = usd_krw.find('td').text.strip()

    # 'today' 클래스를 가진 div 안에서 em 태그를 찾기
    today_div = soup.find('div', class_='today')
    em_tag = today_div.find('em')
    if em_tag.get('class')[0] == 'no_down': usd_fluc = 'blue'
    else: usd_fluc = 'red'
    # usd_fluc.split('_')
    # em 태그의 클래스 속성 추출
    # if 'down' in em_tag.get('class'): usd_fluc = 'blue'
    # else: usd_fluc = 'red'

    url = 'https://finance.naver.com/marketindex/exchangeDetail.naver?marketindexCd=FX_JPYKRW'
    # requests로 페이지 다운로드
    response = requests.get(url)
    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    # 환율 추출
    jpy_krw = soup.find('table', class_='tbl_calculator')
    # 환율 값 추출
    jpy = jpy_krw.find('td').text.strip()
    # 'today' 클래스를 가진 div 안에서 em 태그를 찾기
    today_div = soup.find('div', class_='today')
    em_tag = today_div.find('em')
    # # em 태그의 클래스 속성 추출
    if em_tag.get('class')[0] == 'no_down': jpy_fluc = 'blue'
    else: jpy_fluc = 'red'

    url = 'https://finance.naver.com/marketindex/exchangeDetail.naver?marketindexCd=FX_EURKRW'
    # requests로 페이지 다운로드
    response = requests.get(url)
    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    # 환율 추출
    eur_krw = soup.find('table', class_='tbl_calculator')
    # 환율 값 추출
    eur = eur_krw.find('td').text.strip()
    # 'today' 클래스를 가진 div 안에서 em 태그를 찾기
    today_div = soup.find('div', class_='today')
    em_tag = today_div.find('em')
    if em_tag.get('class')[0] == 'no_down': eur_fluc = 'blue'
    else: eur_fluc = 'red'

    url = 'https://finance.naver.com/marketindex/exchangeDetail.naver?marketindexCd=FX_CNYKRW'
    # requests로 페이지 다운로드
    response = requests.get(url)
    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    # 환율 추출
    cny_krw = soup.find('table', class_='tbl_calculator')
    # 환율 값 추출
    cny = cny_krw.find('td').text.strip()
    # 'today' 클래스를 가진 div 안에서 em 태그를 찾기
    today_div = soup.find('div', class_='today')
    em_tag = today_div.find('em')
    if em_tag.get('class')[0] == 'no_down': cny_fluc = 'blue'
    else: cny_fluc = 'red'

    return Response({'usd': usd, 'jpy': jpy, 'eur': eur, 'cny': cny, 
                     'usd_fluc': usd_fluc, 'jpy_fluc': jpy_fluc, 
                     'cny_fluc': cny_fluc, 'eur_fluc': eur_fluc})