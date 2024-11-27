# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Recruit
from fuzzywuzzy import fuzz
from rest_framework.permissions import IsAuthenticated
from .models import UserEvent, Support
from .serializers import UserEventSerializer, SupportSerializer
from rest_framework import status  # status 모듈 가져오기

User = get_user_model()

# 지원정보 알고리즘
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def supports_list(request):
    # 나이와 지역을 바탕으로 추천
    user = request.user
    user_age = user.age
    user_region = user.region
    user_interest = user.interest

    # 유사 문자열 비교 함수
    def is_similar(str1, str2):
        if not str1 or not str2:  # None 또는 빈 문자열 체크
            return 0
        return fuzz.partial_ratio(str1, str2)
    
    supports = Support.objects.all()
    refined_supports = []

    for support in supports:
        # 관심 정보 점수
        # 관심사가 없으면 점수 0으로 처리
        if not support.description:
            description_score = 0
        else:
            job_interests = [description.strip() for description in support.description.split(',')]

            description_score = max(is_similar(user_interest, job_interest) for job_interest in job_interests)

        # 지역 조건 점수 (여러 지역 중 최대 유사도)
        if support.region == "홈페이지 참조 바랍니다.":
            region_score = 100
        else:
            support_regions = [region.strip() for region in support.region.split(',')]
            region_score = max(is_similar(user_region, support_region) for support_region in support_regions)
        
        # 나이 조건 점수
        if (
            (support.start_age == 0 and support.end_age == 0) or  # 나이 무관
            (support.start_age > 0 and support.end_age == 0 and support.start_age <= user_age) or  # 최소 나이만 있는 경우
            (support.start_age <= user_age <= support.end_age if support.end_age > 0 else True)  # 일반적인 범위
        ):
            age_score = 100
        else:
            age_score = 0
        
        # 총 점수 계산
        total_score = region_score * 0.4 + age_score * 0.4 + description_score * 0.2

        if total_score > 0:
            refined_supports.append({
                "support_id": support.support_id,
                "title": support.title,
                "description":support.description,
                "content": support.contact,
                "scale": support.scale,
                "start_date": support.start_date,
                "end_date": support.end_date,
                "start_age": support.start_age,
                "end_age": support.end_age,
                "department": support.department,
                "contact": support.contact,
                "region": support.region,
                "url": support.url,
                "score": total_score,
            })

    refined_supports = sorted(refined_supports, key=lambda x: x["score"], reverse=True)[:12]   
    print(refined_supports)
    return Response({"recommended_supports": refined_supports})

# 채용공고 알고리즘
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recruits_list(request):
    user = request.user
    user_interest = user.interest
    user_age = user.age
    user_education = user.education
    user_region = user.region

    # 유사 문자열 비교 함수
    def is_similar(str1, str2):
        if not str1 or not str2:  # None 또는 빈 문자열 체크
            return 0
        return fuzz.partial_ratio(str1, str2)

    jobs = Recruit.objects.all()
    refined_jobs = []

    for job in jobs:
        # 관심사가 없으면 점수 0으로 처리
        if not job.interest:
            interest_score = 0
        else:
            job_interests = [interest.strip() for interest in job.interest.split(',')]
            interest_score = max(is_similar(user_interest, job_interest) for job_interest in job_interests)

        # 학력 조건 점수
        education_score = is_similar(user_education, job.required_education) if job.required_education != "학력무관" else 100

        # 지역 조건 점수 (여러 지역 중 최대 유사도)
        job_regions = [region.strip() for region in job.location.split(',')]
        region_score = max(is_similar(user_region, job_region) for job_region in job_regions)

        # 경력 조건 점수 (단순히 조건을 만족하면 100, 아니면 0)
        if (
            (job.min_experience == 0 and job.max_experience == 0) or  # 경력 무관
            (job.min_experience > 0 and job.max_experience == 0 and job.min_experience <= user_age) or  # 최소 경력만 있는 경우
            (job.min_experience <= user_age <= job.max_experience if job.max_experience > 0 else True)  # 일반적인 범위
        ):
            experience_score = 100
        else:
            experience_score = 0

        # 총 점수 계산
        total_score = interest_score * 0.4 + region_score * 0.3 + education_score * 0.2 + experience_score * 0.1

        # 조건을 만족하는 경우에만 추가
        if total_score > 0:
            refined_jobs.append({
                "company_name": job.company_name,
                "job_title": job.job_title,
                "location": job.location,
                "salary": job.salary if job.salary else "정보 없음",
                "job_url": job.job_url,
                "company_url": job.company_url,
                "start_date": job.posting_date if job.posting_date else "정보 없음",
                "end_date": job.expiration_date if job.expiration_date else "정보 없음",
                "job_type": job.job_type,
                "score": total_score  # 점수를 결과에 포함
            })

    # 점수로 정렬 (내림차순) 및 최대 5개로 제한
    refined_jobs = sorted(refined_jobs, key=lambda x: x["score"], reverse=True)[:15]
    return Response({"recommended_jobs": refined_jobs})

# 유저 일정 목록 조회 (GET) 및 새로운 일정 생성 (POST)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_event_list(request):
    # GET: 유저 일정 목록 조회
    if request.method == 'GET':
        user_events = UserEvent.objects.filter(user=request.user)
        serializer = UserEventSerializer(user_events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST: 새 일정 생성
    elif request.method == 'POST':
        data = request.data.copy()
        data['user'] = request.user.id  # 유저 ID 강제 지정
        serializer = UserEventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def user_event_detail(request):
    event_title = request.data.get('eventTitle')
    event_content = request.data.get('eventContent')
    start_date = request.data.get('startDate')
    end_date = request.data.get('endDate')

    if request.method == 'GET':
        try:
            user_event = UserEvent.objects.get(
                user=request.user,
                title=event_title,
                start_date=start_date,
                end_date=end_date
            )
        except UserEvent.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserEventSerializer(user_event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        try:
            user_event = UserEvent.objects.get(id = request.data.get('eventId'))
            user_event.delete()
            return Response({"message": "Event deleted successfully"}, status=status.HTTP_200_OK)
        except UserEvent.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'PUT':
        user_event = UserEvent.objects.get(id = request.data.get('eventId'))
        if user_event:
            user_event.title=event_title
            user_event.content=event_content
            user_event.start_date=start_date
            user_event.end_date=end_date
            user_event.save()
            return Response(UserEventSerializer(user_event).data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)


