import numpy as np
import cvxpy as cvx
import pandas as pd

# 读取prosumer数据并写入字典，为后续约束条件建立使用
# 原始数据先读取，写入字典里，然后用循环的方式调用求解
# 采用对每个prosumer单独读取数据并建模的方式，需要引入for 循环
class prosumer_data:
    def __init__(self, prosumer_data_file):
        self.prosumer_data_file = prosumer_data_file
        
    def read_prosumer_data(self):
        # # DG参数，这里把DG的从设备中移除
        # self.prosumer_DG = pd.read_excel(self.prosumer_data_file, sheet_name="DG", header=0, index_col=0)
        # self.prosumer_DG_min = self.prosumer_DG.loc[:, 'min'].values
        # self.prosumer_DG_max = self.prosumer_DG.loc[:, 'max'].values
        # self.prosumer_DG_ramp = self.prosumer_DG.loc[:, 'ramp'].values
        # self.prosumer_num = len(self.prosumer_DG_min)
        # PV参数
        self.prosumer_PV = pd.read_excel(self.prosumer_data_file, sheet_name="PV", header=0, index_col=0)
        self.prosumer_PV_max = self.prosumer_PV.loc[:, '1':'24'].values
        self.hour_num = len(self.prosumer_PV_max.T)
        self.prosumer_num = len(self.prosumer_PV_max)
        # BESS参数
        self.prosumer_BESS = pd.read_excel(self.prosumer_data_file, sheet_name="BESS", header=0, index_col=0)
        self.prosumer_BESS_min = self.prosumer_BESS.loc[:, 'min'].values
        self.prosumer_BESS_max = self.prosumer_BESS.loc[:, 'max'].values
        self.prosumer_BESS_SOC_min = self.prosumer_BESS.loc[:, 'SOC_min'].values
        self.prosumer_BESS_SOC_max = self.prosumer_BESS.loc[:, 'SOC_max'].values
        # HVAC参数
        self.prosumer_HVAC = pd.read_excel(self.prosumer_data_file, sheet_name="HVAC", header=0, index_col=0)
        self.prosumer_HVAC_min = self.prosumer_HVAC.loc[:, 'min'].values
        self.prosumer_HVAC_max = self.prosumer_HVAC.loc[:, 'max'].values
        self.prosumer_HVAC_F_min = self.prosumer_HVAC.loc[:, 'F_min'].values
        self.prosumer_HVAC_F_max = self.prosumer_HVAC.loc[:, 'F_max'].values
        self.prosumer_HVAC_alpha = self.prosumer_HVAC.loc[:, 'alpha'].values
        self.prosumer_HVAC_beta = self.prosumer_HVAC.loc[:, 'beta'].values
        # 室外温度
        self.prosumer_T_out = pd.read_excel(self.prosumer_data_file, sheet_name="T_out", header=0, index_col=0)
        self.prosumer_T_out = self.prosumer_T_out.loc[:, '1':'24'].values
        # 负荷
        self.prosumer_load = pd.read_excel(self.prosumer_data_file, sheet_name="Load", header=0, index_col=0)
        self.prosumer_load = self.prosumer_load.loc[:, '1':'24'].values
        # 日前市场价格参数
        self.prosumer_price = pd.read_excel(self.prosumer_data_file, sheet_name="price", header=0, index_col=0)
        # prosumer time of use价格
        self.prosumer_tou_price = self.prosumer_price.loc['TOU ($/Mwh)', '1':'24'].values/250
        # prosumer 卖电价格
        self.prosumer_fit_price = self.prosumer_price.loc['FIT ($/Mwh)', '1':'24'].values/250
        # 市场电价Market ($/kwh)
        # self.prosumer_market_price = self.prosumer_price.loc['Market ($/kwh)', '1':'24'].values
        # 定义prosumers字典变量，保存每个prosumer的外部边界条件
        self.all_prosumer_para = {}
        for prosumer_index in range(self.prosumer_num):
            # 定义每个prosumer单独的字典变量，保存prosumer内部的数据
            prosumer_para = {}
            # prosumer_para['DG_min'] = self.prosumer_DG_min[prosumer_index]
            # prosumer_para['DG_max'] = self.prosumer_DG_max[prosumer_index]
            # prosumer_para['DG_ramp'] = self.prosumer_DG_ramp[prosumer_index]
            prosumer_para['PV_max'] = self.prosumer_PV_max[prosumer_index]
            prosumer_para['BESS_min'] = self.prosumer_BESS_min[prosumer_index]
            prosumer_para['BESS_max'] = self.prosumer_BESS_max[prosumer_index]
            prosumer_para['BESS_SOC_min'] = self.prosumer_BESS_SOC_min[prosumer_index]
            prosumer_para['BESS_SOC_max'] = self.prosumer_BESS_SOC_max[prosumer_index]
            prosumer_para['HVAC_min'] = self.prosumer_HVAC_min[prosumer_index]
            prosumer_para['HVAC_max'] = self.prosumer_HVAC_max[prosumer_index]
            prosumer_para['HVAC_F_min'] = self.prosumer_HVAC_F_min[prosumer_index]
            prosumer_para['HVAC_F_max'] = self.prosumer_HVAC_F_max[prosumer_index]
            prosumer_para['HVAC_alpha'] = self.prosumer_HVAC_alpha[prosumer_index]
            prosumer_para['HVAC_beta'] = self.prosumer_HVAC_beta[prosumer_index]
            prosumer_para['T_out'] = self.prosumer_T_out[prosumer_index]
            prosumer_para['load'] = self.prosumer_load[prosumer_index]
            prosumer_para['tou_price'] = self.prosumer_tou_price
            prosumer_para['fit_price'] = self.prosumer_fit_price
            # prosumer_para['market_price'] = self.prosumer_market_price
            # 把每个prosumer的参数保存在prosumers_para里面
            self.all_prosumer_para[prosumer_index] = prosumer_para 
        
    def prosumer_primal_prob(self, prosumer_para, lambda_para, prosumer_pre_solution):
        # 变量定义
        # # DG输出
        # prosumer_DG_output = cvx.Variable(self.hour_num)
        # PV输出
        self.prosumer_PV_output = cvx.Variable(self.hour_num)
        # BESS输出
        self.prosumer_BESS_output = cvx.Variable(self.hour_num)
        # BESS荷电状态
        self.prosumer_BESS_SOC = cvx.Variable(self.hour_num)
        # HVAC输出
        self.prosumer_HVAC_output = cvx.Variable(self.hour_num)
        # 室内温度
        self.prosumer_T_in = cvx.Variable(self.hour_num)
        # 整体对外输出
        self.prosumer_net_output = cvx.Variable(self.hour_num)
        # rho_para = 0.02
        # 目标函数：确保是凹函数
        prosumer_fop = 0
        for hour_index in range(self.hour_num):
            prosumer_tou = - prosumer_para['tou_price'][hour_index]*self.prosumer_net_output[hour_index]
            prosumer_fit = - prosumer_para['fit_price'][hour_index]*self.prosumer_net_output[hour_index]
            # 这里是通过取最小值的方式得到分段凹函数
            # 先采用最简单的方式，只给出一个上界耦合约束
            prosumer_fop = prosumer_fop + cvx.minimum(prosumer_tou, prosumer_fit) + lambda_para[hour_index]*self.prosumer_net_output[hour_index]
        
            # # 对市场电价带来的收益进行分解,变为每个prosumer自身的收益函数
            # prosumer_fop = prosumer_fop + prosumer_para['market_price'][hour_index]*prosumer_net_output[hour_index]
        # prosumer_fop = prosumer_fop + 1/2*cvx.sum_squares(prosumer_net_output - prosumer_pre_solution)   
        # prosumer本地约束
        cons = []
        for hour_index in range(self.hour_num):
            # # DG运行约束
            # cons += [prosumer_DG_output[hour_index] <= prosumer_para['DG_max']]
            # cons += [prosumer_DG_output[hour_index] >= 0]
            # PV出力约束
            cons += [self.prosumer_PV_output[hour_index] <= prosumer_para['PV_max'][hour_index]]
            cons += [self.prosumer_PV_output[hour_index] >= 0]
            # BESS输出约束
            cons += [self.prosumer_BESS_output[hour_index] <= prosumer_para['BESS_max']]
            cons += [self.prosumer_BESS_output[hour_index] >= -prosumer_para['BESS_max']]
            # BESS SOC上下界
            cons += [self.prosumer_BESS_SOC[hour_index] <= prosumer_para['BESS_SOC_max']]
            cons += [self.prosumer_BESS_SOC[hour_index] >= 0]
            # HVAC出力约束
            cons += [self.prosumer_HVAC_output[hour_index] <= prosumer_para['HVAC_max']]
            cons += [self.prosumer_HVAC_output[hour_index] >= 0]
            # 室内温度约束
            cons += [self.prosumer_T_in[hour_index] <= prosumer_para['HVAC_F_max']]
            cons += [self.prosumer_T_in[hour_index] >= prosumer_para['HVAC_F_min']]
            # 负荷平衡约束
            cons += [self.prosumer_net_output[hour_index] == \
                     self.prosumer_PV_output[hour_index] + self.prosumer_BESS_output[hour_index] - \
                     (self.prosumer_HVAC_output[hour_index] + prosumer_para['load'][hour_index])]
        # prosumer的时间耦合约束
        # 初始化状态
        cons += [self.prosumer_BESS_SOC[0] == 0.2*prosumer_para['BESS_SOC_max']]
        cons += [self.prosumer_BESS_SOC[self.hour_num-1] == 0.2*prosumer_para['BESS_SOC_max']]
        cons += [self.prosumer_T_in[0] == 25.0]
        cons += [self.prosumer_HVAC_output[0] == 0]
        cons += [self.prosumer_BESS_output[0] == 0]
        for hour_index in range(1, self.hour_num):
            # # DG爬坡约束
            # cons += [prosumer_DG_output[hour_index] - prosumer_DG_output[hour_index-1] <= prosumer_para['DG_ramp']]
            # cons += [prosumer_DG_output[hour_index] - prosumer_DG_output[hour_index-1] >= -prosumer_para['DG_ramp']]
            # 储能日平衡约束
            cons += [self.prosumer_BESS_SOC[hour_index] == self.prosumer_BESS_SOC[hour_index-1] - self.prosumer_BESS_output[hour_index]]
            # HVAC室内温度动态约束
            cons += [self.prosumer_T_in[hour_index] == self.prosumer_T_in[hour_index-1] + \
                     prosumer_para['HVAC_alpha']*(prosumer_para['T_out'][hour_index] - self.prosumer_T_in[hour_index-1]) + \
                     prosumer_para['HVAC_beta']*self.prosumer_HVAC_output[hour_index]]
        
        obj = cvx.Maximize(prosumer_fop - 1/(2*0.1)*cvx.sum_squares(self.prosumer_net_output - prosumer_pre_solution))
        prob = cvx.Problem(obj, cons)
        prob.solve(solver=cvx.GUROBI, reoptimize=True)
        # 获取本地最优解并返回
        prosumer_solution = self.prosumer_net_output.value
        # solution = obj.value
        solution = prosumer_fop.value
        
        return prosumer_solution, solution