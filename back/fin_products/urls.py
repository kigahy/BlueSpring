from django.urls import path
from . import views

app_name = 'fin_products'

urlpatterns = [
    # 예금 조회
    path('deposit_products/', views.deposit_products_list),
    # 예금 옵션 조회
    path('deposit_options/', views.deposit_options_list),
    # 적금 조회
    path('saving_products/', views.saving_products_list),
    # 적금 옵션 조회
    path('saving_options/', views.saving_options_list),
    # 특정 예금상품 기준, 관련 옵션 조회
    path('deposit_products/<str:fin_prdt_cd>/options/', views.deposit_product_options_list, name='deposit_product_options'),
    # 특정 적금상품 기준, 관련 옵션 조회
    path('saving_products/<str:fin_prdt_cd>/options/', views.saving_product_options_list, name='saving_product_options'),

    # 메인페이지, 최근 금융상품
    path('recent_prdt_main/', views.get_recent_prdt_main, name='get_recent_prdt_main'),
    # 조건별 상품검색
    path('search_by_condition/', views.search_by_condition, name='search_by_condition'),
    # 맞춤형 예적금추천
    path('rec_fin_prdts/', views.rec_fin_prdts, name='rec_fin_prdts'),
    # 메인페이지 최신 금융상품
    path('main/', views.main),
    path('main/dollar/', views.main_dollar),
]
