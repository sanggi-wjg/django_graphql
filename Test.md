## Test

* https://velog.io/@sangyeon217/pytest-fixture
* https://towardsdatascience.com/make-your-python-tests-efficient-with-pytest-fixtures-3d7a1892265f

### Command 
* `pytest --fixtures` : 적용된 fixture list print  


### Run Test 
```
pytest .
pytest app/authentication
pytest -s
```

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


