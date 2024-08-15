import numpy as np
import cvxpy as cvx
import pandas as pd
import matplotlib.pyplot as plt

class VPP_aggregator:
    def __init__(self, VPP_data_file, prosumer_net_power):
        self.VPP_data_file = VPP_data_file
        self.prosumer_net_power = prosumer_net_power
        self.prosumer_num = prosumer_net_power.shape[0]

    def read_VPP_data(self):
        self.VPP_data = pd.read_excel(self.VPP_data_file, header=0, index_col=0)
        # 市场交易价格，由于直接下载的交易电价是$/MWh，因此这里要先除以1000的倍比
        self.market_buy_price = self.VPP_data.loc['Market_buy ($/Mwh)', '1':'24'].values/250
        self.market_sell_price = self.VPP_data.loc['Market_sell ($/Mwh)', '1':'24'].values/250
        self.hour_num = len(self.market_buy_price)
        # prosumer time of use价格
        self.prosumer_tou_price = self.VPP_data.loc['TOU ($/Mwh)', '1':'24'].values/250
        # prosumer 卖电价格
        self.prosumer_fit_price = self.VPP_data.loc['FIT ($/Mwh)', '1':'24'].values/250
        # 聚合最大最小电力
        # self.power_min = self.VPP_data.loc['min', '1':'24'].values
        self.power_max = self.VPP_data.loc['max', '1':'24'].values
        
    def VPP_obj(self):
        # 总体收益变量定义
        fop = 0
        # 每个小时的情况
        # 需要转置，改行索引为小时，为了计算方便
        self.prosumer_power = cvx.transpose(self.prosumer_net_power)
        for hour_index in range(self.hour_num):
            # 与市场的交易情况
            # 在这种场景下，VPP与市场的交易价格被认为是定值
            fop = fop + cvx.minimum(self.market_buy_price[hour_index]*cvx.sum(self.prosumer_power[hour_index]), \
                                    self.market_sell_price[hour_index]*cvx.sum(self.prosumer_power[hour_index]))
            # 与prosumer的交易情况
            # 这里是分段线性函数，用max处理，具体参考http://cvxopt.org/userguide/modeling.html
            # 这里需要保证从每个prosumer获取的收益是凹函数，因为要最大化目标函数
            for prosumer_index in range(self.prosumer_num):
                prosumer_tou = - self.prosumer_tou_price[hour_index]*self.prosumer_power[hour_index][prosumer_index]
                prosumer_fit = - self.prosumer_fit_price[hour_index]*self.prosumer_power[hour_index][prosumer_index]
                # 这里是通过取最小值的方式得到分段凹函数
                fop = fop + cvx.minimum(prosumer_tou, prosumer_fit)

        return fop
    
    def VPP_cons(self):
        # 站在VPP角度的耦合约束
        cons = []
        self.prosumer_power = cvx.transpose(self.prosumer_net_power)
        for hour_index in range(self.hour_num):
            cons += [cvx.sum(self.prosumer_power[hour_index]) <= 200]
            cons += [cvx.sum(self.prosumer_power[hour_index]) >= -200]
            # cons += [cvx.sum(self.prosumer_power[hour_index]) <= self.power_max[hour_index]]
            # cons += [cvx.sum(self.prosumer_power[hour_index]) >= -self.power_max[hour_index]]
            
        return cons