import numpy as np
import cvxpy as cvx
import pandas as pd
import matplotlib.pyplot as plt

# 读取prosumer数据并写入字典，为后续约束条件建立使用
class prosumer_data:
    def __init__(self, prosumer_data_file):
        self.prosumer_data_file = prosumer_data_file
        
    def read_prosumer_data(self):
        # # DG参数，这里把DG删去了
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
        
    def prosumer_variables(self):
        # 变量定义
        # # DG输出
        # self.prosumer_DG_output = cvx.Variable((self.prosumer_num, self.hour_num))
        # PV输出
        self.prosumer_PV_output = cvx.Variable((self.prosumer_num, self.hour_num))
        # BESS输出
        self.prosumer_BESS_output = cvx.Variable((self.prosumer_num, self.hour_num))
        # BESS荷电状态
        self.prosumer_BESS_SOC = cvx.Variable((self.prosumer_num, self.hour_num))
        # HVAC输出
        self.prosumer_HVAC_output = cvx.Variable((self.prosumer_num, self.hour_num))
        # 室内温度
        self.prosumer_T_in = cvx.Variable((self.prosumer_num, self.hour_num))
        # 整体对外输出
        self.prosumer_net_output = cvx.Variable((self.prosumer_num, self.hour_num))
        
    def get_prosumer_cons(self):
        # 约束条件初始化
        cons = []
        # 对于每个prosumer，每天24小时的运行约束
        for prosumer_index in range(self.prosumer_num):
            for hour_index in range(self.hour_num):
                # # DG运行约束
                # cons += [self.prosumer_DG_output[prosumer_index][hour_index] <= 0]
                # # cons += [self.prosumer_DG_output[prosumer_index][hour_index] <= self.prosumer_DG_max[prosumer_index]]
                # cons += [self.prosumer_DG_output[prosumer_index][hour_index] >= 0]
                # # cons += [self.prosumer_DG_output[prosumer_index][hour_index] >= self.prosumer_DG_min[prosumer_index]]
                # PV出力约束
                cons += [self.prosumer_PV_output[prosumer_index][hour_index] <= self.prosumer_PV_max[prosumer_index][hour_index]]
                cons += [self.prosumer_PV_output[prosumer_index][hour_index] >= 0]
                # BESS输出约束
                cons += [self.prosumer_BESS_output[prosumer_index][hour_index] <= self.prosumer_BESS_max[prosumer_index]]
                cons += [self.prosumer_BESS_output[prosumer_index][hour_index] >= -self.prosumer_BESS_max[prosumer_index]]
                # BESS SOC上下界
                cons += [self.prosumer_BESS_SOC[prosumer_index][hour_index] <= self.prosumer_BESS_SOC_max[prosumer_index]]
                cons += [self.prosumer_BESS_SOC[prosumer_index][hour_index] >= 0]
                # cons += [self.prosumer_BESS_SOC[prosumer_index][hour_index] >= self.prosumer_BESS_SOC_min[prosumer_index]]
                # HVAC出力约束
                cons += [self.prosumer_HVAC_output[prosumer_index][hour_index] <= self.prosumer_HVAC_max[prosumer_index]]
                cons += [self.prosumer_HVAC_output[prosumer_index][hour_index] >= 0]
                # cons += [self.prosumer_HVAC_output[prosumer_index][hour_index] >= self.prosumer_HVAC_min[prosumer_index]]
                # 室内温度约束
                cons += [self.prosumer_T_in[prosumer_index][hour_index] <= self.prosumer_HVAC_F_max[prosumer_index]]
                cons += [self.prosumer_T_in[prosumer_index][hour_index] >= self.prosumer_HVAC_F_min[prosumer_index]]
                # 负荷平衡约束
                cons += [self.prosumer_net_output[prosumer_index][hour_index] ==  \
                         self.prosumer_PV_output[prosumer_index][hour_index] + self.prosumer_BESS_output[prosumer_index][hour_index] - \
                         (self.prosumer_HVAC_output[prosumer_index][hour_index] + self.prosumer_load[prosumer_index][hour_index])]
        # prosumer的时间耦合约束
        for prosumer_index in range(self.prosumer_num):
            # 初始化状态
            cons += [self.prosumer_BESS_SOC[prosumer_index][0] == 0.2*self.prosumer_BESS_SOC_max[prosumer_index]]
            cons += [self.prosumer_BESS_SOC[prosumer_index][self.hour_num-1] == 0.2*self.prosumer_BESS_SOC_max[prosumer_index]]
            cons += [self.prosumer_T_in[prosumer_index][0] == 25.0]
            cons += [self.prosumer_HVAC_output[prosumer_index][0] == 0]
            cons += [self.prosumer_BESS_output[prosumer_index][0] == 0]
            for hour_index in range(1, self.hour_num):
                # # DG爬坡约束
                # cons += [self.prosumer_DG_output[prosumer_index][hour_index] - self.prosumer_DG_output[prosumer_index][hour_index-1] <= self.prosumer_DG_ramp[prosumer_index]]
                # cons += [self.prosumer_DG_output[prosumer_index][hour_index] - self.prosumer_DG_output[prosumer_index][hour_index-1] >= -self.prosumer_DG_ramp[prosumer_index]]
                # 储能日平衡约束
                cons += [self.prosumer_BESS_SOC[prosumer_index][hour_index] == self.prosumer_BESS_SOC[prosumer_index][hour_index-1] - \
                         self.prosumer_BESS_output[prosumer_index][hour_index]]
                # HVAC室内温度动态约束
                cons += [self.prosumer_T_in[prosumer_index][hour_index] == self.prosumer_T_in[prosumer_index][hour_index-1] + \
                         self.prosumer_HVAC_alpha[prosumer_index]*(self.prosumer_T_out[prosumer_index][hour_index] - self.prosumer_T_in[prosumer_index][hour_index-1]) + \
                         self.prosumer_HVAC_beta[prosumer_index]*self.prosumer_HVAC_output[prosumer_index][hour_index]]
        
        return cons