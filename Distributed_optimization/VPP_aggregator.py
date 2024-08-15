import numpy as np
import cvxpy as cvx
import pandas as pd

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
        
    def VPP_dual_prob(self, primal_solution, VPP_solution, lambda_para):
        rho_para = 0.1
        lambda_para_next_k = lambda_para - rho_para*(np.sum(primal_solution, axis=0) - VPP_solution)
        
        return lambda_para_next_k