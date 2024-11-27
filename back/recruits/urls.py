from django.urls import path
from . import views

app_name = 'recruits'

urlpatterns = [
    # path('<int:user_id>/', views.recruits_list, name='recruits_list'), // pk가 아니라 token으로 받기 때문에 userid 필요없음
    path('', views.recruits_list, name='recruits_list'), # 채용공고 리스트로, 일단 미뤄둠

    path('user-events/', views.user_event_list, name='user-event-list'),  # 일정 목록 조회 및 생성
    path('user-events/detail/', views.user_event_detail, name='user-event-detail'),  # 일정 세부 조회, 수정, 삭제
    
    path('supports/', views.supports_list, name="supports_list"),
]
