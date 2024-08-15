import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
# 从写的类中导入需要的东西

from prosumer_data import prosumer_data
from VPP_aggregator import VPP_aggregator


if __name__ == "__main__":
    iteration_values = np.load('result/solution_iteration2.npy')
    iteration_values = iteration_values
    # 求取一个均值，作为结果的对比算例
    # average_value = iteration_values[45:88]
    # average_value = np.sum(average_value)/len(average_value)
    OPT_value = np.load('data/OPT_value.npy')
    OPT_value = OPT_value*np.ones(len(iteration_values))
    # average_value = average_value**np.ones(len(iteration_values))
    # print('iteration_values:', iteration_values)
    values = np.array(iteration_values/OPT_value)
    # 绘图并显示
    # 设置画布大小
    plt.figure(figsize=(8, 5))  # 宽度为8英寸，高度为6英寸
    plt.plot(iteration_values, color='blue', linestyle='-', linewidth=2.5, marker='o', markersize=3.5, label='Distributed solver')
    plt.plot(OPT_value, color='red', linestyle='--', label='Optimal solution')
    # # plt.plot(average_value, color='green', linestyle='--', label='Average value')
    # # 设置坐标轴标签
    plt.xlabel('Iteration number', fontsize=14)
    plt.ylabel('VPP profit ($)', fontsize=14)
    # # 添加网格线
    # plt.grid(True, linestyle='--', alpha=0.7)
    # # 设置横纵坐标范围为1-100
    # plt.xlim(0, 100)  # 限制 x 轴范围为1-5
    plt.ylim(0, 120)  # 限制 y 轴范围为10-30
    # plt.legend(fontsize=12)

    # # 设置横纵坐标刻度
    # x_ticks = range(0, 101, 10)
    # x_tick_labels = [str(i) for i in x_ticks]  # 将刻度转换为字符串
    # plt.xticks(x_ticks, labels=x_tick_labels, fontsize=12)  # 设置 x 轴刻度为1-5

    # plt.savefig('result/Obj_iteration_200.pdf', format='pdf')  # 指定dpi为300，可调整清晰度

    # 显示图形
    plt.show()
    # 其他的绘图处理
    # 某个prosumerd的net_power,直接叠加是否可行？
    prosumer_net_power_save = np.load('result/prosumer_net_power_save.npy', allow_pickle=True).item()
    # prosumer_net_power_value = prosumer_net_power_save[1][0]
    # VPP aggregator output
    VPP_aggregator_output_save = np.load('result/VPP_aggregator_output_save.npy', allow_pickle=True).item()
    # VPP_aggregator_output_save = np.array(VPP_aggregator_output_save)
    # print('VPP_aggregator_output_save_shape:', VPP_aggregator_output_save[1])
    # 创建一个新的绘图窗口
    # plt.figure(figsize=(10, 6))

    # # 绘图并显示
    # 这个是柱状堆叠图，效果不是很好，面积怎么样？
    # plt.plot(prosumer_net_power_value, color='blue', linestyle='-', marker='o', markersize=2)
    # plt.plot(average_value, color='green', linestyle='--', label='Average value')
    # fig, ax = plt.subplots(figsize=(10, 6))  # 宽度为10英寸，高度为6英寸
    # x_data = np.arange(1, 25)
    # 显示某个迭代轮次的堆叠柱状图结果
    iteration_num = 180
    prosumer_net_power_value = prosumer_net_power_save[iteration_num]
    prosumer_net_power_value = np.array(prosumer_net_power_value)
    prosumer_num = len(prosumer_net_power_value)
    hour_num = len(prosumer_net_power_value.T)
    # 创建画布
    # 创建画布和两个子图
    # fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 8))
    # 创建画布和两个子图
    # 创建画布和网格布局
    plt.figure(figsize=(10, 8))
    gs = GridSpec(2, 1, height_ratios=[1.5, 1])  # 上下两个子图，高度比例为2:1
    # 绘制热力图在第一个子图
    ax1 = plt.subplot(gs[0])
    # 绘制热力图
    heatmap = ax1.imshow(prosumer_net_power_value, cmap='viridis', aspect='auto')  # 使用 viridis 颜色映射

    # 添加颜色条
    colorbar = plt.colorbar(heatmap, ax=ax1)

    # 设置横坐标刻度和标签
    x_ticks = [0, 6, 12, 18]
    x_tick_labels = [str(i) for i in x_ticks]
    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(x_tick_labels)

    # 设置纵坐标刻度和标签
    y_ticks = [0, 9, 19, 29, 39, 49]
    y_tick_labels = [str(i+1) for (i) in y_ticks]
    ax1.set_yticks(y_ticks)
    ax1.set_yticklabels(y_tick_labels)
    # 设置坐标轴标签
    ax1.set_xlabel('Time (hour)', fontsize=12)
    ax1.set_ylabel('Prosumer index', fontsize=12)
    # 添加图例
    # plt.legend(['Prosumer net power'], loc='upper right')
    # 设置标题
    ax1.set_title('Prosumer net power output (kW)', fontsize=14)
    # plt.title('Prosumer net power output (kW)', fontsize=14)
    x_values = np.arange(24)  # 横坐标从1到24
    # 绘制线图在第二个子图
    # 绘制线图在第二个子图
    gs2 = gs[1].subgridspec(1, 2, width_ratios=[1, 0.14])  # 创建一个子网格，宽度比例设置为0.8
    ax2 = plt.subplot(gs2[0])
    # ax2 = plt.subplot(gs[1])
    # ax.plot(np.arange(1, hour_num+1), VPP_aggregator_output_save[iteration_num], color='blue', linestyle='-', marker='o', markersize=2)
    ax2.plot(x_values, VPP_aggregator_output_save[iteration_num], color='blue', linestyle='-', linewidth=2, marker='o', markersize=2)
    ax2.set_xlabel('Time (hour)', fontsize=12)
    # 设置横坐标刻度和标签，与热力图相同
    ax2.set_xlim(0, 23)
    x_ticks = [0, 6, 12, 18]
    x_tick_labels = [str(i) for i in x_ticks]
    ax2.set_xticks(x_ticks)
    ax2.set_xticklabels(x_tick_labels)
    ax2.set_ylabel('VPP aggregator power output (kW)', fontsize=12)
    # 在 ax2 子图上添加网格线
    ax2.grid(True, linestyle='--', alpha=0.7)
    # ax2.set_title('Line Chart')
    # plt.subplots_adjust(left=0.1, right=0.6, bottom=0.05, top=0.95, hspace=0.2)
    ax1.annotate('(a)', xy=(0.5, -0.2), xycoords='axes fraction', fontsize=14)
    ax2.annotate('(b)', xy=(0.5, -0.3), xycoords='axes fraction', fontsize=14)

    plt.tight_layout()

    # 显示图表
    plt.show()

    # plt.savefig('result/aggregator_result.pdf', format='pdf')  # 指定dpi为300，可调整清晰度


    # print('prosumer_net_power_value_shape:', np.array(prosumer_net_power_value).shape)
    # 计算每个类别的累积值
    # bottom = np.zeros(hour_num)
    # bar_width = 0.5
    # # 绘制柱状堆叠图
    # for i in range(prosumer_num):
    #     ax.bar(np.arange(1, hour_num+1), prosumer_net_power_value[i], width=bar_width, bottom=bottom)
    #     bottom += prosumer_net_power_value[i]
    # ax.plot(np.arange(1, hour_num+1), VPP_aggregator_output_save[iteration_num], color='blue', linestyle='-', marker='o', markersize=2)
    # # 设置坐标轴标签
    # ax.set_xticks(x_data)
    # ax.set_xticklabels(x_data)
    # ax.set_xlabel('Time (hour)', fontsize=12)
    # ax.set_ylabel('Power Output (kW)', fontsize=12)
    # # 保存图像为JPG格式
    # # fig.savefig('result/Output.jpg', dpi=300)  # 指定dpi为300，可调整清晰度
    # # 显示图形
    # plt.show()


