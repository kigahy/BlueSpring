from django.urls import path
from . import views

app_name = 'policies'

urlpatterns = [
    # 정책 조회
    path('youth_policies/', views.get_youth_policies, name='get_youth_policies'),
    path('youth_policies/detail/<str:policy_id>/', views.get_youth_policies_detail, name='get_youth_policies_detail'),
    path('youth_policies_main/', views.get_youth_policies_main, name='get_youth_policies_main'),
    # 맞춤형 정책추천
    path('rec_policies/', views.rec_policies, name='rec_policies'),
]
