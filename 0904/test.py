# age = 36
# txt = f"안녕하세요 저는 백효영인데요! 저의 나이는 {age * 2}입니다."
# txt2 = f"안녕하세요 저는 백효영인데요! 저의 나이는 {(age / 5):.2f}입니다."
# print(txt)
# print(txt2)


# txt = "banana"
# x = txt.center(20, "0")
# print(x)

# # 해당 요소 인덱스 반환 = indexof()
# txt2 = "안녕하세요 원이입니다 잘 부탁드립니다"
# y = txt2.find("원이")
# print(y)


# txt = "THIS IS PYTHOn"
# z = txt.isupper()
# print(z)


# txt = "Hello Sam!"
# mytable = str.maketrans("S", "P")
# print(txt.translate(mytable))


# import numpy as np

# arr = np.array([1, 2, 3])
# print(type(arr))

# arr0 = np.array(100)
# arr1 = np.array([1, 2, 3])
# arr2 = np.array([[1, 2, 3], [4, 5, 6]])
# print(arr0, arr1[1], arr2[1][1])

import numpy as np

arr = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
print("last element from 2nd dim: ", arr[1, -1])

arr1 = np.array([1, 2, 3, 4, 5, 6, 7])
print(arr1[1:5])

arr2 = np.array([1, 2, 3, 4, 5, 6, 7])
print(arr2[4:])

arr3 = np.array([1, 2, 3, 4, 5, 6, 7])
print(arr3[-3:-1])

arr4 = np.array([1, 2, 3, 4, 5, 6, 7])
print(arr4[::2])

arr6 = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
print(arr6[0:2, 2])
