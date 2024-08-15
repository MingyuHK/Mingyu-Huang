# 这里计算加入差分隐私之后的OPT_gap
# 计算机制是：给定终止迭代次数，反复计算100次得均值与方差
# 首先把distributed 写成一个类，调用distributed这个类

import numpy as np
import cvxpy as cvx
import pandas as pd
import matplotlib.pyplot as plt
# 从写的类中导入需要的东西

from prosumer_data import prosumer_data
from VPP_aggregator import VPP_aggregator
from distributed_solution import distributed_solution

import concurrent.futures
import numpy as np

import concurrent.futures
import numpy as np

import concurrent.futures
import numpy as np

if __name__ == "__main__":
    prosumer_data_file = "data/prosumers50.xlsx"
    VPP_data_file = "data/VPP_data.xlsx"
    # 定义分布式求解的这个类，包括两个输入文件
    # 在这里定义外环迭代
    k = 0
    Dis_solve = distributed_solution(VPP_data_file, prosumer_data_file)
    # 开启迭代
    max_ite = 10
    # 把每一次迭代的结果保存在字典变量中
    # 先定义字典变量
    OPT_result_save = {}
    final_obj_save = {}
    final_prosumer_output_save = {}
    final_aggregator_output_save = {}
    result_save = {}
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = {executor.submit(Dis_solve.iteration_process): k for k in range(max_ite)}

    for future in concurrent.futures.as_completed(futures):
        k = futures[future]
        OPT_value, final_obj, final_prosumer_output, final_aggregator_output = future.result()
        OPT_result_save[k] = OPT_value
        # print('OPT_value', OPT_value)
        final_obj_save[k] = final_obj
        final_prosumer_output = np.array(final_prosumer_output)
        final_prosumer_output_save[k] = np.sum(final_prosumer_output, axis=0)
        # print('prosumer_output:', np.sum(final_prosumer_output, axis=0))
        final_aggregator_output = np.array(final_aggregator_output)
        final_aggregator_output_save[k] = final_aggregator_output
        # print('final_aggregator_output_shape:', final_aggregator_output)

    # while k < max_ite:
    #     k = k+1
    #     print('outer_ite:', k)
        # result_k = {}
    # for k in range(max_ite):
        # OPT_value, final_obj, final_prosumer_output, final_aggregator_output = Dis_solve.iteration_process()
        # OPT_result_save[k] = OPT_value
        # print('OPT_value', OPT_value)
        # final_obj_save[k] = final_obj
        # final_prosumer_output = np.array(final_prosumer_output)
        # final_prosumer_output_save[k] = np.sum(final_prosumer_output, axis=0)
        # print('prosumer_output:', np.sum(final_prosumer_output, axis=0))
        # final_aggregator_output = np.array(final_aggregator_output)
        # final_aggregator_output_save[k] = final_aggregator_output
        # print('final_aggregator_output_shape:', final_aggregator_output)
        # 通过print进行调试
        # print('result_k:', result_k)
        # 将每一个结果存入字典
        # result_save[k] = result_k

    np.save('outer_ite_result/OPT_result_save.npy', OPT_result_save)
    np.save('outer_ite_result/final_obj_save.npy', final_obj_save)
    np.save('outer_ite_result/final_prosumer_output_save.npy', final_prosumer_output_save)
    np.save('outer_ite_result/final_aggregator_output_save.npy', final_aggregator_output_save)


