# age = 36

# # f-string 안에서는 {} 안에 변수나 계산식을 바로 넣을 수 있음
# txt = f"안녕하세요 저는 백효영인데요! 저의 나이는 {age * 2}입니다."

# # :.2f = 소수점 둘째 자리까지 표시
# txt2 = f"안녕하세요 저는 백효영인데요! 저의 나이는 {(age / 5):.2f}입니다."

# print(txt)
# print(txt2)


# txt = "banana"

# # 문자열을 총 20칸 가운데 정렬
# # 빈 공간은 "0"으로 채움
# x = txt.center(20, "0")

# print(x)


# # find("문자열")
# # 찾은 문자열이 시작되는 인덱스를 반환
# # 못 찾으면 -1 반환
# # JavaScript의 indexOf()와 비슷함
# txt2 = "안녕하세요 원이입니다 잘 부탁드립니다"

# y = txt2.find("원이")

# print(y)


# txt = "THIS IS PYTHOn"

# # 문자열의 알파벳이 모두 대문자인지 확인
# # 하나라도 소문자가 있으면 False
# z = txt.isupper()

# print(z)


# txt = "Hello Sam!"

# # 문자열 치환 규칙 생성
# # "S"를 "P"로 바꾸는 변환표
# mytable = str.maketrans("S", "P")

# # 변환표를 문자열에 적용
# print(txt.translate(mytable))


# NumPy 라이브러리를 np라는 이름으로 사용
import numpy as np

# 2차원 NumPy 배열 생성
arr = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])

# arr[행, 열]
# 1번 행 = 두 번째 배열
# -1 = 마지막 요소
# 결과: 10
print("last element from 2nd dim: ", arr[1, -1])


arr1 = np.array([1, 2, 3, 4, 5, 6, 7])

# 슬라이싱 [start:end]
# start 인덱스는 포함, end 인덱스는 제외
# 인덱스 1 ~ 4
# 결과: [2 3 4 5]
print(arr1[1:5])


arr2 = np.array([1, 2, 3, 4, 5, 6, 7])

# [4:] = 인덱스 4부터 끝까지
# 결과: [5 6 7]
print(arr2[4:])


arr3 = np.array([1, 2, 3, 4, 5, 6, 7])

# 음수 인덱스는 뒤에서부터 셈
# -3 = 뒤에서 세 번째 → 5
# -1은 슬라이싱의 종료 지점이므로 포함되지 않음
# 결과: [5 6]
print(arr3[-3:-1])


arr4 = np.array([1, 2, 3, 4, 5, 6, 7])

# 슬라이싱 [start:end:step]
# ::2 = 처음부터 끝까지 2칸씩 이동
# 결과: [1 3 5 7]
print(arr4[::2])


arr6 = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])

# 2차원 배열 슬라이싱
# arr6[행 범위, 열]
#
# 0:2 = 0번 행부터 2번 행 직전까지 → 0, 1번 행
# 2 = 각 행의 2번 인덱스(세 번째 값)
#
# 첫 번째 행 → 3
# 두 번째 행 → 8
# 결과: [3 8]
print(arr6[0:2, 2])
