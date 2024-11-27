from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import MyCardTransaction, MyAccountTransaction

User = get_user_model()  # 커스텀 모델을 가져옴

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 프로필에 필요한 부분만 넣어도 될듯
        exclude = ['password']


class UserSerializerTest(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class MyCardTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCardTransaction
        fields = '__all__'


class MyAccountTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyAccountTransaction
        fields = '__all__'