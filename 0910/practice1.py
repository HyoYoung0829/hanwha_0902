# async await
# js async await과 같음.


@app.get("/")
async def read_results():
    # await의 결과가 바로 오지 않는다면, 다른 작업을 수행할 수 있음
    # 결과가 도착하면 그때 나머지 작업 이어서 수행
    # 사용하는 라이브러리가 await을 요구하면 아래와 같이 작성하면 됨.
    results = await some_library()
    return results


# 만약 라이브러리가 async를 지원하지 않는다면, 그냥 def를 사용하면 됨.


# async가 무조건 항상 빠른건 아님.
# async를 지원하지 않는 라이브러리를 아래와 같이 사용하면
async def api():
    result = blocking_db_query()


# 오히려 해당 라이브러리가 실행되는동안 이벤트 루프가 막힐 수 있음.
# 따라서 확실하지 않으면 def 사용을 권장함.
# 보통 I/O에 효과가 좋음.

# ai agent에서의 활용.
# ai agent는 기다리는 작업이 많음. (I/O가 많음)
# 따라서 잘 활용하는게 중요함.

# 웹개발은 "동시성"의 이점을 크게 받고
# 머신러닝처럼 CPU/GPU 계산량이 많은 작업은 "병렬성"의 이점을 크게 받는다.
