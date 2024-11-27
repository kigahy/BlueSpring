from django.contrib.auth.models import AbstractUser
from django.db import models

# 사용자 정보
class User(AbstractUser):
    name = models.CharField(max_length=10)          # 이름
    nick_name = models.CharField(max_length=10)     # 닉네임
    age = models.IntegerField(null=True, blank=True)  # 나이
    gender = models.CharField(max_length=10, null=True, blank=True)  # 성별
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # 전화번호
    email = models.CharField(max_length=30, null=True, blank=True)
    job = models.CharField(max_length=100, null=True, blank=True)          # 직업
    interest = models.TextField(null=True, blank=True)                      # 관심사
    assets_amount = models.IntegerField(null=True, blank=True)              # 자산
    salary = models.PositiveIntegerField(null=True, blank=True)             # 연봉
    education = models.CharField(max_length=20, null=True, blank=True)      # 학력
    region = models.CharField(max_length=20, null=True, blank=True)         # 지역

    def __str__(self):
        return self.username


# 사용자 금융 관련 목표
class MoneyGoal(models.Model):
    money_goal_id = models.AutoField(primary_key=True)  # Auto increment PK
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="money_goals") # 외래키 FK 설정
    target_amount = models.DecimalField(max_digits=15, decimal_places=2)  # 목표 금액
    start_date = models.DateField()  # 시작 날짜
    end_date = models.DateField()  # 종료 날짜
    current_progress = models.IntegerField()  # 현재 진행 상태
    priority = models.IntegerField()  # 우선 순위
    

# 사용자 Job 관련 목표
class JobGoal(models.Model):
    job_goal_id = models.AutoField(primary_key=True)  # Auto increment PK
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_goals")  # 외래키 FK 설정
    target_job = models.CharField(max_length=255)  # 목표 직업
    target_job_memo = models.TextField(null=True, blank=True)  # 목표 직업 메모
    start_date = models.DateField()  # 시작 날짜
    end_date = models.DateField()  # 종료 날짜
    current_progress = models.BooleanField()  # 목표 직업 달성 여부 (True or False)
    priority = models.IntegerField()  # 우선 순위


# 사용자 보유 카드
class MyCard(models.Model):
    card_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='cards', on_delete=models.CASCADE)
    card_name = models.CharField(max_length=255)
    card_type = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    benefit = models.TextField(null=True, blank=True)
    anual_fee = models.DecimalField(max_digits=10, decimal_places=2)


# 사용자 보유 통장
class MyAccount(models.Model):
    account_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='accounts', on_delete=models.CASCADE)
    account_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    account_type = models.CharField(max_length=255)


# 사용자 카드 거래내역
class MyCardTransaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='card_transactions', on_delete=models.CASCADE)
    card = models.ForeignKey(MyCard, related_name='transactions', on_delete=models.CASCADE)
    transaction_date = models.DateField()
    transaction_time = models.TimeField()
    money_amount = models.DecimalField(max_digits=10, decimal_places=2)
    content = models.TextField(null=True, blank=True)


# 사용자 통장 거래내역
class MyAccountTransaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    account = models.ForeignKey(MyAccount, related_name='transactions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='account_transactions', on_delete=models.CASCADE)  # 사용자와 연결
    transaction_date = models.DateField()
    transaction_time = models.TimeField()
    money_amount = models.DecimalField(max_digits=10, decimal_places=2)
    content = models.TextField(null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

