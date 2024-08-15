# 读取测试数据，计算均值及方差
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 从写的类中导入需要的东西

from prosumer_data import prosumer_data
from VPP_aggregator import VPP_aggregator
from distributed_solution import distributed_solution


if __name__ == "__main__":
    # 从result中读取结果
    # 迭代了3次，需要对三次求和
    OPT_result_save = np.load('outer_ite_result/OPT_result_save.npy', allow_pickle=True).item()
    OPT_result_list = list(OPT_result_save.values())
    OPT_result = np.array(OPT_result_list) 
    # print('type:', type(OPT_result_save))
    print('size:', len(OPT_result_save))
    print('OPT_result_save:', OPT_result)
    final_obj_save = np.load('outer_ite_result/final_obj_save.npy', allow_pickle=True).item()
    final_obj_list = list(final_obj_save.values())
    final_obj = np.array(final_obj_list)
    # print('type:', type(final_obj_save))
    # print('size:', final_obj_save.shape)
    print('final_obj_save:', final_obj)
    final_prosumer_output_save = np.load('outer_ite_result/final_prosumer_output_save.npy', allow_pickle=True).item()
    final_prosumer_output_list = list(final_prosumer_output_save.values())
    final_prosumer_output = np.array(final_prosumer_output_list)
    # print('type:', type(final_prosumer_output_save))
    # print('size:', final_prosumer_output_save.shape)
    print('final_prosumer_output_save:', final_prosumer_output)
    final_aggregator_output_save = np.load('outer_ite_result/final_aggregator_output_save.npy', allow_pickle=True).item()
    final_aggregator_output_list = list(final_aggregator_output_save.values())
    final_aggregator_output = np.array(final_aggregator_output_list)
    # print('type:', type(final_aggregator_output_save))
    # print('size:', final_aggregator_output_save.shape)
    print('final_aggregator_output_save:', final_aggregator_output)

    # np.save('outer_ite_result/final_obj_save.npy', final_obj_save)
    # np.save('outer_ite_result/final_prosumer_output_save.npy', final_prosumer_output_save)
    # np.save('outer_ite_result/final_aggregator_output_save.npy', final_aggregator_output_save)
    # 计算OPT gap
    diff_OPT = abs(final_obj - OPT_result)
    # diff_OPT作为一个随机变量的均值和方差
    # Calculate the mean of the array
    diff_OPT_mean_value = np.mean(diff_OPT)

    # Calculate the variance of the array
    diff_OPT_variance_value = np.std(diff_OPT)

    print("diff_OPT_Mean:", diff_OPT_mean_value)
    print("diff_OPT_Variance:", diff_OPT_variance_value)

    # 计算对约束的总体违背
    diff_cons = abs(final_prosumer_output - final_aggregator_output)
    diff_sum = np.sum(diff_cons, axis=1)
    # print("diff_sum:", diff_sum)
    # Calculate the mean of the array
    diff_cons_mean_value = np.mean(diff_sum)

    # Calculate the variance of the array
    diff_cons_variance_value = np.std(diff_sum)
    print("diff_cons_Cons_Mean:", diff_cons_mean_value)
    print("diff_cons_Cons_Variance:", diff_cons_variance_value)

    # 保存到工作区
    result_20 = np.array([diff_OPT_mean_value, diff_OPT_variance_value, diff_cons_mean_value, diff_cons_variance_value])
    # 指定保存的文件路径
    save_path = 'outer_ite_result/result_ln2.npy'

    # 使用numpy.save()函数保存数组到文件
    np.save(save_path, result_20)

    # 测试结果读取
    # 使用numpy.load()函数从文件夹中读取数组
    # loaded_values = np.load('outer_ite_result/result_28.npy')

    # print("Loaded array:", loaded_values)
    fig, ax = plt.subplots(figsize=(10, 6))  # 宽度为10英寸，高度为6英寸
    x_data = np.arange(1, 25)
    # 显示某个迭代轮次的堆叠柱状图结果
    iteration_num = 85
    # prosumer_net_power_value = prosumer_net_power_save[iteration_num]
    # prosumer_net_power_value = np.array(prosumer_net_power_value)
    # prosumer_num = len(prosumer_net_power_value)
    # hour_num = len(prosumer_net_power_value.T)
    # print('prosumer_net_power_value_shape:', np.array(prosumer_net_power_value).shape)
    # 计算每个类别的累积值
    # bottom = np.zeros(hour_num)
    ax.plot(np.arange(1, 25), final_prosumer_output[0], color='red', linestyle='-', marker='o', markersize=2)
    # bar_width = 0.8
    # # 绘制柱状堆叠图
    # for i in range(prosumer_num):
    #     ax.bar(np.arange(1, hour_num+1), prosumer_net_power_value[i], width=bar_width, bottom=bottom)
    #     bottom += prosumer_net_power_value[i]
    ax.plot(np.arange(1, 25), final_aggregator_output[0], color='blue', linestyle='-', marker='o', markersize=2)
    # 设置坐标轴标签
    ax.set_xticks(x_data)
    ax.set_xticklabels(x_data)
    ax.set_xlabel('Time (hour)', fontsize=12)
    ax.set_ylabel('Power Output (kW)', fontsize=12)
    # 保存图像为JPG格式
    fig.savefig('result/Output.jpg', dpi=300)  # 指定dpi为300，可调整清晰度
    # 显示图形
    plt.show()
    print('final_prosumer_output[0]', final_prosumer_output[0])
    print('final_aggregator_output[0]', final_aggregator_output[0])
