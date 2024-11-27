from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .models import User, MoneyGoal, JobGoal, MyCard, MyAccount, MyCardTransaction, MyAccountTransaction
import requests

# User 리스트 뷰
@api_view(['GET'])
def accounts_list(request):
    try:
        users = User.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 50
        result_page = paginator.paginate_queryset(users, request)
        data = [
            {
                'user_id': user.id,
                'user_name': user.username,
                'name': user.name,
                'nick_name': user.nick_name,
                'age': user.age,
                'gender': user.gender,
                'phone_number': user.phone_number,
                'email': user.email,
                'job': user.job,
                'interest': user.interest,
                'assets_amount': user.assets_amount,
                'salary' : user.salary,
                'education' : user.education,
                'region' : user.region,
            }
            for user in result_page
        ]
        return paginator.get_paginated_response(data)
    except Exception as e:
        return Response({"error": "An error occurred.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 사용자 이름으로 정보 조회하는 뷰
@api_view(['GET'])
def user_info(request, user_id):
    try:
        # 사용자 이름에 해당하는 User 객체를 조회
        user = User.objects.get(id=user_id)

        # 사용자 정보를 딕셔너리 형태로 반환
        data = {
            'user_id': user.id,
            'user_name': user.username,
            'name': user.name,
            'nick_name': user.nick_name,
            'age': user.age,
            'gender': user.gender,
            'phone_number': user.phone_number,
            'email': user.email,
            'job': user.job,
            'interest': user.interest,
            'assets_amount': user.assets_amount,
        }

        return Response(data)

    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": "An error occurred.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# MoneyGoal 리스트 뷰
@api_view(['GET'])
def money_goals_list(request):
    try:
        money_goals = MoneyGoal.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 50
        result_page = paginator.paginate_queryset(money_goals, request)
        data = [
            {
                'money_goal_id': goal.money_goal_id,
                'user_id': goal.user.id,
                'target_amount': goal.target_amount,
                'start_date': goal.start_date,
                'end_date': goal.end_date,
                'current_progress': goal.current_progress,
                'priority': goal.priority,
            }
            for goal in result_page
        ]
        return paginator.get_paginated_response(data)
    except Exception as e:
        return Response({"error": "An error occurred.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# JobGoal 리스트 뷰
@api_view(['GET'])
def job_goals_list(request):
    try:
        job_goals = JobGoal.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 50
        result_page = paginator.paginate_queryset(job_goals, request)
        data = [
            {
                'job_goal_id': goal.job_goal_id,
                'user_id': goal.user.id,
                'target_job': goal.target_job,
                'target_job_memo': goal.target_job_memo,
                'start_date': goal.start_date,
                'end_date': goal.end_date,
                'current_progress': goal.current_progress,
                'priority': goal.priority,
            }
            for goal in result_page
        ]
        return paginator.get_paginated_response(data)
    except Exception as e:
        return Response({"error": "An error occurred.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# MyCard 리스트 뷰
@api_view(['GET'])
def mycards_list(request):
    try:
        mycards = MyCard.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 50
        result_page = paginator.paginate_queryset(mycards, request)
        data = [
            {
                'card_id': card.card_id,
                'user_id': card.user.id,
                'card_name': card.card_name,
                'card_type': card.card_type,
                'company': card.company,
                'benefit': card.benefit,
                'anual_fee': card.anual_fee,
            }
            for card in result_page
        ]
        return paginator.get_paginated_response(data)
    except Exception as e:
        return Response({"error": "An error occurred.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# MyAccount 리스트 뷰
@api_view(['GET'])
def myaccounts_list(request):
    try:
        myaccounts = MyAccount.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 50
        result_page = paginator.paginate_queryset(myaccounts, request)
        data = [
            {
                'account_id': account.account_id,
                'user_id': account.user.id,
                'account_name': account.account_name,
                'company': account.company,
                'account_type': account.account_type,
            }
            for account in result_page
        ]
        return paginator.get_paginated_response(data)
    except Exception as e:
        return Response({"error": "An error occurred.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# MyCardTransaction 리스트 뷰
@api_view(['GET'])
def mycardtransactions_list(request):
    try:
        mycardtransactions = MyCardTransaction.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 50
        result_page = paginator.paginate_queryset(mycardtransactions, request)
        data = [
            {
                'transaction_id': transaction.transaction_id,
                'card_id': transaction.card.card_id,
                'transaction_date': transaction.transaction_date,
                'transaction_time': transaction.transaction_time,
                'money_amount': transaction.money_amount,
                'content': transaction.content,
                'balance': transaction.balance,
            }
            for transaction in result_page
        ]
        return paginator.get_paginated_response(data)
    except Exception as e:
        return Response({"error": "An error occurred.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# MyAccountTransaction 리스트 뷰
@api_view(['GET'])
def myaccounttransactions_list(request):
    try:
        # 모든 MyAccountTransaction 데이터를 가져옴
        transactions = MyAccountTransaction.objects.all()

        # 페이지네이션 설정
        paginator = PageNumberPagination()
        paginator.page_size = 10  # 한 페이지에 표시할 데이터 개수

        # 페이지네이션 적용
        result_page = paginator.paginate_queryset(transactions, request)

        # 데이터 변환 (직렬화 없이 Python 딕셔너리로 처리)
        data = [
            {
                'transaction_id': transaction.transaction_id,
                'account_id': transaction.account.account_id,
                'transaction_date': transaction.transaction_date,
                'transaction_time': transaction.transaction_time,
                'money_amount': transaction.money_amount,
                'content': transaction.content,
                'balance': transaction.balance,
            }
            for transaction in result_page
        ]

        # 페이지네이션된 응답 반환
        return paginator.get_paginated_response(data)

    except Exception as e:
        # 예외 처리: 오류 발생 시 에러 메시지 반환
        return Response(
            {"error": "An error occurred while processing the request.", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
# 유저 프로필 제공, 수정
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserProfileSerializer
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user  # 현재 로그인된 유저

    if request.method == 'GET':
        # GET 요청: 프로필 정보 가져오기
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)  # 직렬화된 프로필 반환

    elif request.method == 'PUT':
        # PUT 요청: 프로필 정보 수정
        data = request.data
        print(data)
        # 가능한 필드만 업데이트 (전체 필드 처리)
        valid_fields = ['nick_name', 'name', 'age', 'gender', 'phone_number', 'email', 'job', 'interest', 'assets_amount', 'salary', 'education', 'region']
        for field in valid_fields:
            if field in data:
                if field == 'age' and not data['age']: 
                    data['age'] = None
                setattr(user, field, data[field])

        # 프로필 정보 업데이트 후 저장
        try:
            user.save()
            # 수정된 프로필 데이터 반환
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

# Flask의 메일 전송 API URL
FLASK_EMAIL_API_URL = 'http://127.0.0.1:5001/send_email'
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_email(request):
    # 인증된 사용자만 접근
    user = request.user
    # 이메일 내용 받아오기
    content = request.data.get('content')    
    recipient = user.email
    # 메일 내용이나 이메일이 없다면
    if not content: return Response({"error": "Missing content for email."}, status=400)    
    try:
        response = requests.post( FLASK_EMAIL_API_URL, json={'content': content, 'recipient': recipient,})
        if response.status_code == 200: return Response({"message": "Email sent successfully!"})
        else: return Response({"error": "Failed to send email from Flask."}, status=response.status_code)    
    except requests.exceptions.RequestException as e: return Response({"error": str(e)}, status=500)    