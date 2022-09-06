from rest_framework import status

from app.articles.utils import request_naver


def health_check_naver() -> bool:
    response = request_naver()
    return True \
        if response.get('status_code') == status.HTTP_200_OK \
        else False
