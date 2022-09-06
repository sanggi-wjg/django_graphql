import requests
from requests import Response
from rest_framework import status


def request_naver() -> dict:
    print('======  이게 보이면 Mocking 되지 않은 것! =====')
    # return requests.get("https://www.naver.com")
    return {
        'status_code': status.HTTP_200_OK,
        'detail': "success",
    }
