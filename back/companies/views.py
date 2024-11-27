import csv
import os
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

@api_view(['GET'])
def companies_list(request):
    # CSV 파일 경로 설정
    csv_file_path = os.path.join(os.path.dirname(__file__), 'corporate_info.csv')
    
    # 페이지 네이션 설정
    paginator = PageNumberPagination()
    paginator.page_size = 50  # 한 페이지에 반환할 항목 수
    
    # 파일이 존재하는지 확인
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            # CSV 파일 읽기
            csv_reader = csv.DictReader(file)  # 헤더를 기준으로 딕셔너리 형태로 읽음
            data = [row for row in csv_reader]  # 모든 행을 리스트로 저장
            
            # 페이지 네이션 적용
            result_page = paginator.paginate_queryset(data, request)
            
            # JSON 응답 반환
            return paginator.get_paginated_response(result_page)
            
    except FileNotFoundError:
        return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
