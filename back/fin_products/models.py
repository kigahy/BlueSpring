from django.db import models


# Deposit Product 모델
class DepositProduct(models.Model):
    fin_prdt_cd = models.CharField(primary_key=True, max_length=10)
    dcls_month = models.DateField(null=True, blank=True)  # YYYY-MM-01 형식
    fin_co_no = models.CharField(max_length=10, null=True, blank=True)
    kor_co_nm = models.CharField(max_length=255, null=True, blank=True)
    fin_prdt_nm = models.CharField(max_length=255, null=True, blank=True)
    join_way = models.CharField(max_length=255, null=True, blank=True)
    mtrt_int = models.CharField(max_length=255, null=True, blank=True)
    spcl_cnd = models.CharField(max_length=255, null=True, blank=True)
    join_deny = models.CharField(max_length=255, null=True, blank=True)
    join_member = models.CharField(max_length=255, null=True, blank=True)
    etc_note = models.TextField(null=True, blank=True)
    max_limit = models.CharField(max_length=255, null=True, blank=True)
    dcls_strt_day = models.DateField(null=True, blank=True)  # YYYY-MM-DD 형식
    dcls_end_day = models.DateField(null=True, blank=True)  # YYYY-MM-DD 형식

    def __str__(self):
        return f'{self.fin_prdt_nm} ({self.kor_co_nm})'


# Deposit Option 모델
class DepositOption(models.Model):
    # option_id를 기본 키로 설정
    option_id = models.AutoField(primary_key=True)  # option_id가 기본 키로 설정
    # DepositOption이 DepositProduct에 외래 키로 연결됨
    fin_prdt_cd = models.ForeignKey(DepositProduct, related_name="options", on_delete=models.CASCADE)  # ForeignKey 설정

    # DepositOption 모델의 기본 키는 자동 생성되는 option_id
    dcls_month = models.DateField(null=True, blank=True)  # YYYY-MM-01 형식
    fin_co_no = models.CharField(max_length=10, null=True, blank=True)
    intr_rate_type = models.CharField(max_length=255, null=True, blank=True)
    intr_rate_type_nm = models.CharField(max_length=255, null=True, blank=True)
    save_trm = models.IntegerField()
    intr_rate = models.CharField(max_length=255, null=True, blank=True)
    intr_rate2 = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'Option for {self.deposit_product.fin_prdt_nm} ({self.fin_co_no})'


# Deposit Product 모델
class SavingProduct(models.Model):
    fin_prdt_cd = models.CharField(primary_key=True, max_length=10)
    dcls_month = models.DateField(null=True, blank=True)  # YYYY-MM-01 형식
    fin_co_no = models.CharField(max_length=10, null=True, blank=True)
    kor_co_nm = models.CharField(max_length=255, null=True, blank=True)
    fin_prdt_nm = models.CharField(max_length=255, null=True, blank=True)
    join_way = models.CharField(max_length=255, null=True, blank=True)
    mtrt_int = models.CharField(max_length=255, null=True, blank=True)
    spcl_cnd = models.CharField(max_length=255, null=True, blank=True)
    join_deny = models.CharField(max_length=255, null=True, blank=True)
    join_member = models.CharField(max_length=255, null=True, blank=True)
    etc_note = models.TextField(null=True, blank=True)
    max_limit = models.CharField(max_length=255, null=True, blank=True)
    dcls_strt_day = models.DateField(null=True, blank=True)  # YYYY-MM-DD 형식
    dcls_end_day = models.DateField(null=True, blank=True)  # YYYY-MM-DD 형식

    def __str__(self):
        return f'{self.fin_prdt_nm} ({self.kor_co_nm})'


# Deposit Option 모델
class SavingOption(models.Model):
    # 기본 키를 option_id로 설정
    option_id = models.AutoField(primary_key=True)  # option_id가 기본 키로 설정
    # DepositOption이 DepositProduct에 외래 키로 연결됨
    fin_prdt_cd = models.ForeignKey(SavingProduct, related_name="options", on_delete=models.CASCADE)  # ForeignKey 설정
    # DepositOption 모델의 기본 키는 자동 생성되는 option_id
    dcls_month = models.DateField(null=True, blank=True)  # YYYY-MM-01 형식
    fin_co_no = models.CharField(max_length=10, null=True, blank=True)
    intr_rate_type = models.CharField(max_length=255, null=True, blank=True)
    intr_rate_type_nm = models.CharField(max_length=255, null=True, blank=True)
    rsrv_type = models.CharField(max_length=255, null=True, blank=True)
    rsrv_type_nm = models.CharField(max_length=255, null=True, blank=True)
    save_trm = models.IntegerField()    
    # save_trm = models.CharField(max_length=255, null=True, blank=True)
    intr_rate = models.CharField(max_length=255, null=True, blank=True)
    intr_rate2 = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'Option for {self.deposit_product.fin_prdt_nm} ({self.fin_co_no})'
