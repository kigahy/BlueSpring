from django.db import models
from django.conf import settings

# 사람인 API 채용공고
class Recruit(models.Model):
    recruit_id = models.AutoField(primary_key=True)  # 구분을 위한 pk
    job_url = models.URLField(max_length=500, default="회사 홈페이지에 방문하거나 E-mail로 지원 바랍니다.", null=True, blank=True)  # 채용 정보 URL
    company_url = models.CharField(max_length=500, default="회사 홈페이지에 방문하거나 E-mail로 지원 바랍니다.", null=True, blank=True)  # 회사 정보 URL
    company_name = models.CharField(max_length=255, null=True, blank=True)  # 회사명
    job_title = models.CharField(max_length=255, null=True, blank=True)  # 모집 분야
    job_code = models.CharField(max_length=100, default="0", null=True, blank=True)  # 직무 코드
    location = models.CharField(max_length=255, null=True, blank=True)  # 지역
    required_education = models.CharField(max_length=255, null=True, blank=True)  # 학력 조건
    experience_type = models.CharField(max_length=50, null=True, blank=True)  # 경력직 여부
    min_experience = models.IntegerField(null=True, blank=True)  # 최소 경력 (nullable)
    max_experience = models.IntegerField(null=True, blank=True)  # 최대 경력 (nullable)
    job_type = models.CharField(max_length=50, null=True, blank=True)
    salary = models.CharField(max_length=100, null=True, blank=True)  # 급여
    interest = models.CharField(max_length=255, null=True, blank=True)  # 관심 분야
    posting_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.position_title} at {self.company_name}"
    
# 온통청년 API 지원정보
class Support(models.Model):
    support_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500, default="홈페이지에 방문하거나 연락처로 컨택 바랍니다.", null=True, blank=True)
    description = models.CharField(max_length=500, default="상세정보는 홈페이지 참고 및 연락 바랍니다.", null=True, blank=True)
    content = models.CharField(max_length=500, default=True, null=True)
    scale = models.CharField(max_length=500, default="상세인원은 홈페이지 참고 및 연락 바랍니다.", null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    start_age = models.IntegerField(null=True, blank=True)
    end_age = models.IntegerField(null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(max_length=50, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(max_length=500, default="회사 홈페이지에 방문하거나 E-mail로 지원 바랍니다.")
    
    def __str__(self):
        # 제목과 부서를 조합해 객체를 읽기 쉽게 표시
        return f"{self.title} ({self.department})"

    
# 유저가 추가하는 일정 모델
class UserEvent(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 커스텀 유저 모델과 연결
        on_delete=models.CASCADE,
        related_name="user_events"
    )
    title = models.CharField(max_length=255)  # 일정 제목
    content = models.TextField(blank=True, null=True)  # 일정 내용
    start_date = models.DateField()  # 시작 날짜
    end_date = models.DateField()  # 종료 날짜

    def __str__(self):
        return self.title
    
# 중개 테이블
class UserRecruitInterest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 커스텀 유저 모델과 연결
        on_delete=models.CASCADE,
        related_name="user_recruit_interests"
        )
    recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE, related_name="interested_users")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.recruit.job_title}"

# # Create your models here.
# class Recruit(models.Model):
#     recruit_id = models.AutoField(primary_key = True)           # 구분 위한 pk
#     osition_title = models.CharField(max_length=255)            # 모집명
#     company_name = models.CharField(max_length=255)             # 회사명
#     position_title = models.CharField(max_length=255)           # 모집 분야
#     location = models.CharField(max_length=255)                 # 지역
#     education_require = models.CharField(max_length=255)        # 학력 조건
#     job_description = models.TextField()                        # 하는 일
#     experience_type = models.CharField(max_length=50)           # 경력직 여부
#     min_experience = models.IntegerField(null=True, blank=True) # 최소 경력 (nullable)
#     opening_date = models.DateField()                           # 채용 시작일
#     expiration_date = models.DateField()                        # 채용 마감일