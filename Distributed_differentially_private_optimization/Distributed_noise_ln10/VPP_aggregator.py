import numpy as np
import cvxpy as cvx
import pandas as pd
import sympy as sp

class VPP_aggregator:
    def __init__(self, VPP_data_file):
        self.VPP_data_file = VPP_data_file
        # self.prosumer_net_power = prosumer_net_power
        # self.prosumer_num = prosumer_net_power.shape[0]
        # aggregator需要承担两项职责，1. aggregator变量的迭代；2. 对偶变量的梯度下降更新

    def read_VPP_data(self):
        self.VPP_data = pd.read_excel(self.VPP_data_file, header=0, index_col=0)
        # 市场交易价格
        self.market_buy_price = self.VPP_data.loc['Market_buy ($/Mwh)', '1':'24'].values/250
        self.market_sell_price = self.VPP_data.loc['Market_sell ($/Mwh)', '1':'24'].values/250
        self.hour_num = len(self.market_buy_price)
        # prosumer time of use价格
        # self.prosumer_tou_price = self.VPP_data.loc['TOU ($/kwh)', '1':'24'].values
        # # prosumer 卖电价格
        # self.prosumer_fit_price = self.VPP_data.loc['FIT ($/kwh)', '1':'24'].values
        # 聚合最大最小电力
        self.power_min = self.VPP_data.loc['min', '1':'24'].values
        self.power_max = self.VPP_data.loc['max', '1':'24'].values
        
    def aggregator_update(self, lambda_para, VPP_pre_solution):
        # 定义变量
        self.VPP_output = cvx.Variable(self.hour_num)
        # aggregator角度的目标函数，只与市场交易价格相关
        VPP_fop = 0
        for hour_index in range(self.hour_num):
            VPP_buy = self.market_buy_price[hour_index]*self.VPP_output[hour_index]
            VPP_sell = self.market_sell_price[hour_index]*self.VPP_output[hour_index]
            # 这里是通过取最小值的方式得到分段凹函数，这里需要考虑等式约束的嵌入原则，以及如何同于迭代
            VPP_fop = VPP_fop + cvx.minimum(VPP_buy, VPP_sell) - lambda_para[hour_index]*self.VPP_output[hour_index]
        # VPP_fop = VPP_fop + 1/2*cvx.sum_squares(self.VPP_output - VPP_pre_solution)                     
        # 只考虑最大最小值约束
        cons = []
        for hour_index in range(self.hour_num):
            cons += [self.VPP_output <= 200]
            cons += [self.VPP_output >= -200]
        
        obj = cvx.Maximize(VPP_fop - 1/(2*0.1)* cvx.sum_squares(self.VPP_output - VPP_pre_solution))
        prob = cvx.Problem(obj, cons)
        prob.solve(solver=cvx.GUROBI, reoptimize=True)
        # 获取本地最优解并返回
        VPP_solution = self.VPP_output.value
        # solution = obj.value
        solution = VPP_fop.value
            
        return VPP_solution, solution
            
#     def VPP_virtual_dual_prob(self, mu_para, primal_solution, VPP_solution):
#         rho_para = 0.02
#         lambda_para = mu_para + rho_para*(np.sum(primal_solution, axis=0) - VPP_solution)
        
#         return lambda_para
    
    def VPP_noise_gen(self, y_value):
        # 创建符号变量
        x, u, y = sp.symbols('x u y')

        # 定义要积分的函数
        exp_u = sp.exp(-u**2/2)  # 正态分布的概率密度函数
        inte_u = sp.integrate(exp_u, (u, x, sp.oo))
        original_function = (1/sp.sqrt(2*sp.pi)) * inte_u

        # 求解反函数
        inverse_function = sp.solve(original_function - y, x)

        # 代入数值计算反函数的值
        # y_value = 0.1  # 替换为你想要计算的 y 值
        result = inverse_function[0].subs(y, y_value).evalf()
        return result

    def VPP_dual_prob(self, primal_solution, VPP_solution, lambda_para):
        # 在梯度上加噪声，噪声信号的设计与灵敏度相关
        # 这里的差分隐私需求给的很小，测算原始数据分别给的多少
        # 差分隐私预算，两个参数
        epsilon = np.log(10)
        delta = 1e-3
        # 计算24维的L2灵敏度
        hour_num = len(primal_solution.T)
        gradient_L2 = np.zeros(hour_num)
        # 寻找L2灵敏度
        max_vector = 0
        for i in range(len(primal_solution)):
            for j in range(len(primal_solution)):
                if i != j:
                    norm = np.abs(primal_solution[i] - primal_solution[j])
                    max_vector = np.maximum(max_vector, norm)
        gradient_L2 = 0.1*max_vector
        # 初始化高斯噪声的参数
        means = np.zeros(hour_num)  # 均值为0, 24维的高斯噪声，均值都为0
        # 初始化标准差为0
        std_devs = np.zeros(hour_num) 
        # 根据L2灵敏度计算需要加的高斯噪声的标准差
        for hour_index in range(hour_num):
            std_devs[hour_index] = gradient_L2[hour_index] * (1.65 + np.sqrt(1.65**2+2*epsilon)) / (2*epsilon)
        # # 生成维度为24的高斯噪声向量
        print('std_devs:', std_devs)
        gaussian_noise = np.random.normal(means, std_devs, size=hour_num)
        rho_para = 0.1
        # 在对偶变量迭代的时候，在对偶变量的值上加上高斯噪声，看结果会有什么变化
        lambda_para_next_k = lambda_para - rho_para*(np.sum(primal_solution, axis=0) - VPP_solution) + gaussian_noise
        
        return lambda_para_next_k