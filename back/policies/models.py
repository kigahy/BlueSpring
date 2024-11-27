from django.db import models

# Create your models here.
class YouthPolicy(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.TextField()  # 정책 데이터(XML 문자열 저장)
    created_at = models.DateTimeField(auto_now_add=True)  # 데이터 저장 시간

class PolicyUpdateLog(models.Model):
    key = models.CharField(max_length=50, unique=True)  # 고유 키 (예: "youth_policy_update")
    value = models.DateField()  # 업데이트 날짜

