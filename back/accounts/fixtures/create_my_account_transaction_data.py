from faker import Faker
import random
import json
from datetime import datetime, timedelta

# Faker 객체 초기화
fake = Faker()

# 거래 내역을 담을 리스트
transactions = []

# 시작 날짜를 2024년 10월 1일로 설정
start_date = datetime(2024, 10, 1)
pk = int(input('start pk: ').strip())
user_id = int(input('user pk: ').strip())
account_id = int(input('account pk: ').strip())  # 'account'로 변경

# 시작 balance는 1,000,000원
balance = int(input('start balance: ').strip())

# 10월 1일부터 10월 31일까지 각 날짜에 대해 거래 생성
for day in range(31):  # 31일 동안 반복 (10월 1일부터 31일까지)
    current_date = start_date + timedelta(days=day)

    # 시간 변수 초기화 (기준 시간이 될 현재 시간)
    current_time = datetime.combine(current_date, datetime.min.time())
    total_seconds = 0  # 총 누적 초를 초기화

    # 하루에 랜덤 수(20~100) 개의 거래를 생성
    while total_seconds < 86400:  # 86400초 (24시간) 이내로 거래를 생성
        # 거래 시간이 오름차순으로 증가하도록 설정
        random_seconds = random.randint(3600, 12000)  # 1초에서 1시간(3600초) 사이의 랜덤 초를 추가
        total_seconds += random_seconds  # 총 누적 초에 더함

        # 만약 하루를 넘어가는 경우, 생성 중지
        if total_seconds >= 86400:
            break

        # 새로운 거래 시간
        transaction_time = current_time + timedelta(seconds=total_seconds)

        # 일반 거래 (출금)
        transaction_amount = round(random.uniform(5000.00, 100000.00), 2)
        total_amount = transaction_amount  # 출금은 양수로 처리

        if balance - total_amount < 0:  # 잔액이 부족하면 입금 처리
            # 입금액 생성 (100,000원에서 3,000,000원 사이)
            deposit_amount = round(random.uniform(int(input('입금 최소액: ').strip()), int(input('입금 최대액: ').strip())), 2)
            balance += deposit_amount  # 입금 후 balance 갱신
            transaction = {
                "model": "accounts.myaccounttransaction",  # 'mycardtransaction'에서 'myaccounttransaction'으로 변경
                "pk": pk,  # 각 거래의 pk는 고유하도록 설정
                "fields": {
                    "user": user_id,  # 유저 ID
                    "account": account_id,  # 계좌 ID
                    "transaction_date": current_date.date().isoformat(),  # 날짜
                    "transaction_time": transaction_time.time().isoformat(),  # 시간
                    "money_amount": -deposit_amount,  # 입금 금액 (음수로 기록)
                    "content": "Deposit due to insufficient balance",  # 입금 내용
                    "balance": balance  # 현재 balance
                }
            }
            transactions.append(transaction)
            pk += 1  # pk 증가

        # 출금 거래
        balance -= total_amount  # balance 갱신
        transaction = {
            "model": "accounts.myaccounttransaction",  # 'mycardtransaction'에서 'myaccounttransaction'으로 변경
            "pk": pk,  # 각 거래의 pk는 고유하도록 설정
            "fields": {
                "user": user_id,  # 유저 ID
                "account": account_id,  # 계좌 ID
                "transaction_date": current_date.date().isoformat(),  # 날짜
                "transaction_time": transaction_time.time().isoformat(),  # 시간
                "money_amount": total_amount,  # 출금 금액
                "content": fake.sentence(),  # 랜덤 거래 내용
                "balance": balance  # 현재 balance
            }
        }
        transactions.append(transaction)
        pk += 1  # pk 증가

# 생성된 데이터를 JSON 형식으로 저장
with open('account_transaction_data.json', 'w') as f:
    json.dump(transactions, f, indent=2)

print(f"Created account transaction data")
