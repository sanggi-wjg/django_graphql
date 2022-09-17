import requests


def request_naver() -> dict:
    print('======  이게 보이면 Mocking 되지 않은 것! =====')
    response = requests.get("https://www.naver.com")
    return {
        'status_code': response.status_code,
        'headers': response.headers,
    }
