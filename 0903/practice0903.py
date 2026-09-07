# x = 5
# y = "John"
# print(x)
# print(type(x))
# print(y)
# print(type(y))


# # 함수 정의만.
# def myFunc():
#     global x
#     x = "fantastic"


# # 함수 콜.
# myFunc()
# print("life is" + x)


# str = "Hello, World!"
# # 문자열 길이 반환 (정수)
# print(len(str))
# print()

# for x in str:
#     print(x)
#     print("------")


# # 해당 문자열이 원본 문자열에 존재하는지 반환하는 문법 => boolean
# txt = "The best things in life are free!"
# print("free" in txt)

# # 문자열의 인덱스를 바탕으로 특정 구간만 출력 할 수 있다.
# b = "Hello, World!"
# print(b[2:5])
# print(b[:5])
# print(b[2:])


# a = "  Hello, World!  "
# # 대문자 변환
# print(a.upper())
# # 소문자 변환
# print(a.lower())
# # 앞뒤 공백 제거 = trim()
# print(a.strip())


# a = "  Hello, Horld!  "
# # 특정 문자 대체
# print(a.replace("H", "J"))
# # 문자 쪼개기. (배열에 담아줌)
# print(a.split(","))


# 클래스 정의
class Person:
    # 클래스 초기화
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # 메서드
    def greet(self):
        print("Hello, my name is " + self.name)

    def display_info(self):
        print(f"이름: {self.name}, 나이: {self.age}")


# Obj 생성
p1 = Person("홍길동", 16)
p2 = Person("벤자민", 22)
p3 = Person("세종대왕", 30)

# 메서드 호출
print(p2.name, p2.age)
p2.greet()
p2.display_info()


# class Person:
#     pass

# # 이런식으로 빈 클래스를 바탕으로 Obj를 만들 수 도 있다.
# p1 = Person()
# p1.name = "홍길동"
# p1.age = 16
# p1.eye = 2.0

# print(p1.name, p1.age, p1.eye)
