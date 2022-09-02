## pytest-django
`pytest`를 기반을 한 Django 테스트를 위한 오픈 소스

## Pros and Cons
### Pros
* fixture를 통한 단위 테스트 관리
* Test 실행시마다 Database DDL이 실행 될 필요가 없음
* Multi-process Test 가능(pytest-xdist)
* 프로파일링 (pytest-benchmark)  
* pytest 기반의 수많은 오픈 소스 

### Cons
* Django TestCase, APITestCase에 비해 사용을 위한 학습 필요
* 많은 관련 오픈 소스로 적절한 오픈 소스를 선택하기 위한 시간 소모 
* 

## Install
```python
pip install pytest pytest-django
```

## Run Pytest Command 
* `pytest .`, `pytest`: 현재 폴더 이하 테스트
* `pytest app/authentication` `pytest app/authentication/tests/test_users.py` : 특정 폴더, 특정 파일 테스트   
* `pytest --fixtures` : 적용된 fixture list print
* `pytest -s` : print all

### Pytest Decorators
* `scope` 설정 : fixture가 실행되는 범위에 대해 정의합니다.  
  설정한 scope 단위로 fixture는 한 번만 생성되고 계속 재사용됩니다.
* 총 5개의 scope이 있으며, 범위의 크기는 아래와 같습니다.   
  function(default) < class < module < package < session

```python
@pytest.fixture(scope="function") : fixture가 함수 단위로 1회 생성됨(디폴트 설정으로, @pytest.fixture 와 같습니다.)
@pytest.fixture(scope="class") : fixture가 클래스 단위로 1회 생성됨
@pytest.fixture(scope="module") : fixture가 파일 단위로 1회 생성됨
@pytest.fixture(scope="package") : fixture가 패키지 단위로 1회 생성됨
@pytest.fixture(scope="session") : fixture가 test session동안 1회 생성됨
```


* `skip` : Skip 기능 
```python
@pytest.mark.skip(reason="Only local test")

@pytest.mark.skipif(
    os.environ.get("SKIP") != "1", 
    reason="It only works if SKIP is set to '1'"
)
```

* `xfail` : 


### `pytest.ini` options
```shell
; true, keep
django_debug_mode = true

; --reuse-db : 재사용 --create-db : 생성
addopts = --reuse-db 
```



### Ref
* pytest
  * 
* pytest-django
  * https://pytest-django.readthedocs.io/en/latest/index.html
  * https://github.com/pytest-dev/pytest-django
* 관련 
  * https://velog.io/@sangyeon217/pytest-fixture
  * https://towardsdatascience.com/make-your-python-tests-efficient-with-pytest-fixtures-3d7a1892265f