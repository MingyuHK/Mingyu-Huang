import numpy as np
import cvxpy as cvx
import pandas as pd
import matplotlib.pyplot as plt
import time
# 从写的类中导入需要的东西

from prosumer_data import prosumer_data
from VPP_aggregator import VPP_aggregator


if __name__ == "__main__":
    start_time = time.time()
    prosumer_data_file = "data/prosumers50.xlsx"
    VPP_data_file = "data/VPP_data.xlsx"
    prosumers = prosumer_data(prosumer_data_file)
    prosumers.read_prosumer_data()
    # 初始化lambda
    lambda_para = np.zeros(24)
    mu_para = np.zeros(24)
    # 需要对solution进行初始化
    prosumers_pre_solution = 1.015*np.load('data/prosumers_net_output.npy')
    VPP_pre_solution = np.sum(prosumers_pre_solution, axis=0)
    OPT_value = np.load('data/OPT_value.npy')
    # prosumer_pre_solution = np.zeros(24)
    # VPP_pre_solution = np.zeros(24)
    # 在每个prosumer的角度求解主问题
    # 一共需要经历若干次迭代,给出迭代次数
    # 先完成第0步迭代，后面再循环，0步迭代的初始值，再去保存其他变量
    # 这里需要对保存的变量进行配置，用于后续的结果展示，在不同的差分隐私水平下，包括每个个体变量的最优解以及整体的最优解
    ite_num = 120
    # 迭代次数的索引
    k = 0
    # 变量保存，初始化为空
    prosumer_PV_save = {}
    prosumer_HVAC_save = {}
    prosumer_BESS_save = {}
    prosumer_BESS_SOC_save = {}
    prosumer_load_save = {}
    prosumer_net_power_save = {}
    VPP_aggregator_output_save = {}
    net_power_save = {}
    solution_save = {}
    while k < ite_num:
        k = k+1
        print('iteration_num:', k)
        # 保存primal问题解的变量
        all_net_power = []
        obj_solution = 0
        prosumer_num = len(prosumers.all_prosumer_para)
        print('lambda_para', lambda_para)
        print('mu_para', mu_para)
        # 迭代过程每一步的变量保存，初始化为空
        k_prosumer_PV_save = []
        k_prosumer_HVAC_save = []
        k_prosumer_BESS_save = []
        k_prosumer_BESS_SOC_save = []
        k_prosumer_load_save = []
        k_prosumer_net_power_save = []
        for prosumer_index in range(prosumer_num):
            prosumer_para = prosumers.all_prosumer_para[prosumer_index]
            prosumer_net_power, solution = prosumers.prosumer_primal_prob(prosumer_para, lambda_para, prosumers_pre_solution[prosumer_index])
            # prosumers_pre_solution_next.append(prosumer_net_power)
            obj_solution = obj_solution + solution
            # print('prosumer_solution:', prosumer_net_power)
            all_net_power.append(prosumer_net_power)
            k_prosumer_PV_save.append(prosumers.prosumer_PV_output.value)
            k_prosumer_HVAC_save.append(prosumers.prosumer_HVAC_output.value)
            k_prosumer_BESS_save.append(prosumers.prosumer_BESS_output.value)
            k_prosumer_BESS_SOC_save.append(prosumers.prosumer_BESS_SOC.value)
            k_prosumer_load_save.append(prosumers.prosumer_load)
            k_prosumer_net_power_save.append(prosumers.prosumer_net_output.value)
        # 整合所有primal问题的解
        all_net_power = np.array(all_net_power)
        prosumer_pre_solution = all_net_power
        all_net_power_sum = np.sum(all_net_power, axis=0)
        net_power_save[k] = all_net_power_sum
        print('all_net_power_sum', all_net_power_sum)
        # print('all_net_power:', all_net_power)
        # 将每一次迭代的结果加入字典变量
        prosumer_PV_save[k] = k_prosumer_PV_save
        prosumer_HVAC_save[k]  = k_prosumer_HVAC_save
        prosumer_BESS_save[k]  = k_prosumer_BESS_save
        prosumer_BESS_SOC_save[k]  = k_prosumer_BESS_SOC_save
        prosumer_load_save[k]  = k_prosumer_load_save
        prosumer_net_power_save[k]  = k_prosumer_net_power_save
        # VPP对对偶变量进行迭代
        # 先定义VPP这个类
        VPP_test = VPP_aggregator(VPP_data_file)
        # 读取数据
        VPP_test.read_VPP_data()
        # 对偶迭代获取下一步的lambda的值
        VPP_solution, solution = VPP_test.aggregator_update(lambda_para, VPP_pre_solution)
        print('VPP_solution:', VPP_solution)
        VPP_pre_solution = VPP_solution
        print('obj_solution:', obj_solution+solution)
        VPP_aggregator_output_save[k] = VPP_solution
        solution_save[k] = obj_solution+solution
        lambda_para_next_k = VPP_test.VPP_dual_prob(all_net_power, VPP_solution, lambda_para)
        lambda_para = lambda_para_next_k
    # 绘制迭代过程，在这个过程中调试参数获取不错的迭代结果
    values = list(solution_save.values())
    values = np.array(values)
    # 保存结果到result，后续画图及结果分析中使用
    np.save('result/solution_iteration.npy', values)
    # 指定保存文件的路径和文件名
    np.save('result/prosumer_PV_save.npy', prosumer_PV_save)
    np.save('result/prosumer_HVAC_save.npy', prosumer_HVAC_save)
    np.save('result/prosumer_BESS_save.npy', prosumer_BESS_save)
    np.save('result/prosumer_BESS_SOC_save.npy', prosumer_BESS_SOC_save)
    np.save('result/prosumer_load_save.npy', prosumer_load_save)
    np.save('result/prosumer_net_power_save.npy', prosumer_net_power_save)
    np.save('result/VPP_aggregator_output_save.npy', VPP_aggregator_output_save)
    # 绘图并显示
    end_time = time.time()
    print("Program run time: ", end_time - start_time)
    # plt.plot(values/OPT_value)
    # plt.show()

