from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # 유저 목록
    path('users/', views.accounts_list, name='accounts_list'),
    # 특정 유저 정보
    path('users/<int:user_id>/', views.user_info, name='user_info'),
    # 금융 목표 목록
    path('money_goals/', views.money_goals_list, name='money_goals_list'),
    # 직업 목표 목록
    path('job_goals/', views.job_goals_list, name='job_goals_list'),
    # 보유 카드 현황
    path('mycards/', views.mycards_list, name='mycards_list'),
    # 보유 통장 현황
    path('myaccounts/', views.myaccounts_list, name='myaccounts_list'),
    # 카드 거래내역
    path('mycardtransactions/', views.mycardtransactions_list, name='mycardtransactions_list'),
    # 통장 거래내역
    path('myaccounttransactions/', views.myaccounttransactions_list, name='myaccounttransactions_list'),
    # 프로필 정보
    path('profile/', views.profile, name='profile'),
    # 메일전송
    path('send_email/', views.send_email, name='send_email'),

]
