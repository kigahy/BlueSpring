from rest_framework import serializers
from .models import DepositProduct, DepositOption, SavingProduct, SavingOption

# Serializer 클래스 정의
class DepositProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = '__all__'  # 모든 필드를 직렬화


class DepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = '__all__'


class SavingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProduct
        fields = '__all__'


class SavingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = '__all__'


class DepositOptionSelectSerializer(serializers.ModelSerializer):
    # 외래 키를 통해 DepositProduct 모델의 필드를 추가
    kor_co_nm = serializers.CharField(source='fin_prdt_cd.kor_co_nm', read_only=True)
    fin_prdt_nm = serializers.CharField(source='fin_prdt_cd.fin_prdt_nm', read_only=True)
    etc_note = serializers.CharField(source='fin_prdt_cd.etc_note', read_only=True)
    class Meta:
        model = DepositOption
        exclude = ('option_id', 'intr_rate_type', 'fin_co_no')


class SavingOptionSelectSerializer(serializers.ModelSerializer):
    
    # 외래 키를 통해 DepositProduct 모델의 필드를 추가
    kor_co_nm = serializers.CharField(source='fin_prdt_cd.kor_co_nm', read_only=True)
    fin_prdt_nm = serializers.CharField(source='fin_prdt_cd.fin_prdt_nm', read_only=True)
    etc_note = serializers.CharField(source='fin_prdt_cd.etc_note', read_only=True)

    class Meta:
        model = SavingOption
        exclude = ('option_id', 'intr_rate_type', 'fin_co_no', "rsrv_type", )


class DepositProductWithOptionsSerializer(serializers.ModelSerializer):
    # DepositProduct의 모든 필드를 포함시킴
    class Meta:
        model = DepositProduct
        fields = '__all__'  # DepositProduct의 모든 필드를 포함
    # DepositOption을 중첩 직렬화
    options = DepositOptionSerializer(many=True, read_only=True)


class SavingProductWithOptionsSerializer(serializers.ModelSerializer):
    # DepositProduct의 모든 필드를 포함시킴
    class Meta:
        model = SavingProduct
        fields = '__all__'  # DepositProduct의 모든 필드를 포함
    # SavingOption을 중첩 직렬화
    options = SavingOptionSerializer(many=True, read_only=True)

class Test():
    pass