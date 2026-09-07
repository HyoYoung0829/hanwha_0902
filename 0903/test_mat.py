import matplotlib.pyplot as plt
import numpy as np

# 리스트를 NumPy 배열로 변환
ypoints = np.array([3, 8, 1, 10, 24, 3, 56, 35, 3, 4, 5, 24])

# ypoints의 값을 그래프로 그림
# "o:r"
# o : 각 데이터 위치를 원(circle)으로 표시
# : : 점선(dotted line)으로 연결
# r : 빨간색(red)으로 표시
plt.plot(ypoints, "o:r")

# 만든 그래프를 화면에 출력
plt.show()
