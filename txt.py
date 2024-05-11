import numpy as np

# 定义两个矩阵
matrix1 = np.array([[1, 2],
                    [3, 4]])
matrix2 = np.array([[5, 6],
                    [7, 8]])

# 执行矩阵乘法
result = np.dot(matrix1, matrix2)

# 输出结果
print("矩阵乘法结果：")
print(result)