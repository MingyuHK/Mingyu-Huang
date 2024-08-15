import sympy as sp
import numpy as np

# 创建符号变量
x, u, y = sp.symbols('x u y')

# 定义要积分的函数
exp_u = sp.exp(-u**2/2)  # 正态分布的概率密度函数
inte_u = sp.integrate(exp_u, (u, x, sp.oo))
original_function = (1/sp.sqrt(2*sp.pi)) * inte_u

# 求解反函数
inverse_function = sp.solve(original_function - y, x)

# 代入数值计算反函数的值
y_value = 0.05  # 替换为你想要计算的 y 值
result = inverse_function[0].subs(y, y_value).evalf()
# epsilon = np.log(1e3)

# t = (1.28 + np.sqrt(1.28**2+2*epsilon)) / epsilon

# 打印反函数的值
print(f"反函数在 y = {y_value} 处的值是:", result)