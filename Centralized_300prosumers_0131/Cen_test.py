import numpy as np
import cvxpy as cvx
import pandas as pd
import matplotlib.pyplot as plt
# 从写的类中导入需要的东西

from prosumer_data import prosumer_data
from VPP_aggregator import VPP_aggregator


if __name__ == "__main__":
    fop = 0
    cons = []
    # 读取每个prosumer的参数
    prosumer_data_file = "data/prosumers50.xlsx"
    prosumers = prosumer_data(prosumer_data_file)
    prosumers.read_prosumer_data()
    prosumers.prosumer_variables()
    # 获取prosumer的运行约束
    prosumers_cons = prosumers.get_prosumer_cons()
    cons += prosumers_cons
    # 读取VPP价格信息及耦合约束
    VPP_data_file = "data/VPP_data.xlsx"
    # prosumer与VPP交互变量
    prosumer_net_power = prosumers.prosumer_net_output
    VPP_test = VPP_aggregator(VPP_data_file, prosumer_net_power)
    VPP_test.read_VPP_data()
    # 目标函数
    fop = fop + VPP_test.VPP_obj()
    # 耦合约束
    cons += VPP_test.VPP_cons()
    # 优化问题求解
    obj = cvx.Maximize(fop)
    prob = cvx.Problem(obj, cons)
    prob.solve(solver=cvx.GUROBI, reoptimize=True)
    status = prob.status
    solution = obj.value
    print(status, solution)

    # 结果保存
    # 保存交互变量，作为分布式优化算法生成的边界
    prosumers_net_output = prosumers.prosumer_net_output.value
    np.save('result/prosumers_net_output.npy', prosumers_net_output)

    # 对结果变量进行保存，供绘图使用
    # VPP的变量
    X_value = np.sum(prosumers.prosumer_net_output.value, axis=0)
    np.save('result/VPP_aggregator_output.npy', X_value)
    # 将每个prosumer的结果保存在字典向量中
    prosumer_save = {}
    for prosumer_index in range(prosumers.prosumer_num):
        prosumer_result = []
        prosumer_result.append(prosumers.prosumer_PV_output.value[prosumer_index])
        prosumer_result.append(prosumers.prosumer_BESS_output.value[prosumer_index])
        prosumer_result.append(prosumers.prosumer_HVAC_output.value[prosumer_index])
        prosumer_result.append(prosumers.prosumer_load[prosumer_index])
        prosumer_result.append(prosumers.prosumer_net_output[prosumer_index].value)
        prosumer_result.append(prosumers.prosumer_BESS_SOC.value[prosumer_index])
        prosumer_save[prosumer_index] = prosumer_result
    # 保存字典变量 
    # 指定保存文件的路径和文件名
    np.save('result/prosumer_result.npy', prosumer_save)
    # 对最优解的值进行保存
    OPT_value = solution
    np.save('result/OPT_value.npy', OPT_value)


