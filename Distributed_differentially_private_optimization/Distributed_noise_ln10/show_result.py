import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
# 从写的类中导入需要的东西

from prosumer_data import prosumer_data
from VPP_aggregator import VPP_aggregator


if __name__ == "__main__":
    iteration_values = np.load('result/solution_iteration.npy')
    iteration_values = iteration_values[2:103]
    OPT_value = np.load('data/OPT_value.npy')
    OPT_value = OPT_value*np.ones(len(iteration_values))
    # *********************************
    # 设置画布大小
    plt.figure(figsize=(8, 5))  # 宽度为8英寸，高度为6英寸
    plt.plot(iteration_values, color='blue', linestyle='-', linewidth=2.5, marker='o', markersize=3.5, label='Distributed solver')
    plt.plot(OPT_value, color='red', linestyle='--', label='Optimal solution')
    # plt.plot(average_value, color='green', linestyle='--', label='Average value')
    # 设置坐标轴标签
    plt.xlabel('Iteration number', fontsize=14)
    plt.ylabel('VPP profit ($)', fontsize=14)
    # 添加网格线
    plt.grid(True, linestyle='--', alpha=0.7)
    # 设置横纵坐标范围为1-100
    plt.xlim(0, 100)  # 限制 x 轴范围为1-5
    # plt.ylim(10, 30)  # 限制 y 轴范围为10-30
    plt.legend(fontsize=12)
    # plt.show()

    plt.figure(figsize=(10, 8))
    gs = GridSpec(2, 1, height_ratios=[1.2, 1])  # 上下两个子图，高度比例为2:1
    # 绘制热力图在第一个子图
    ax1 = plt.subplot(gs[0])
    # 绘制热力图
    ax1.plot(iteration_values, color='blue', linestyle='-', linewidth=2.5, marker='o', markersize=3.5, label='Distributed solver with DP')
    ax1.plot(OPT_value, color='red', linestyle='--', label='Optimal solution')
    # 设置坐标轴标签
    ax1.set_xlabel('Iteration number', fontsize=12)
    ax1.set_ylabel('VPP profit ($)', fontsize=12)
    # 添加网格线
    ax1.grid(True, linestyle='--', alpha=0.7)
    # 设置横纵坐标范围为1-100
    ax1.set_xlim(0, 100)  # 限制 x 轴范围为1-5
    # plt.ylim(10, 30)  # 限制 y 轴范围为10-30
    ax1.legend(fontsize=12)

    # 设置横坐标刻度和标签
    x_ticks = range(0, 101, 10)
    x_tick_labels = [str(i) for i in x_ticks]
    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(x_tick_labels)

    x_values = np.arange(24)  # 横坐标从1到24
    # 绘制线图在第二个子图
    # 绘制线图在第二个子图
    prosumer_net_power_save = np.load('result/prosumer_net_power_save.npy', allow_pickle=True).item()
    VPP_aggregator_output_save = np.load('result/VPP_aggregator_output_save.npy', allow_pickle=True).item()
    # 显示某个迭代轮次的堆叠柱状图结果
    iteration_num = 100
    prosumer_net_power_value = prosumer_net_power_save[iteration_num]
    prosumer_net_power_value = np.array(prosumer_net_power_value)
    prosumer_num = len(prosumer_net_power_value)
    hour_num = len(prosumer_net_power_value.T)
    ax2 = plt.subplot(gs[1])
    # ax.plot(np.arange(1, hour_num+1), VPP_aggregator_output_save[iteration_num], color='blue', linestyle='-', marker='o', markersize=2)
    ax2.bar(np.arange(24), np.sum(prosumer_net_power_value, axis=0)-VPP_aggregator_output_save[iteration_num], color='green', alpha=0.7, label='Bar Chart')
    # # 设置坐标轴标签
    # ax2.set_xticks(x_data)
    # ax2.set_xticklabels(x_data)
    # ax2.set_xlabel('Time (hour)', fontsize=12)
    # ax2.set_ylabel('Power Output (kW)', fontsize=12)
    # # 保存图像为JPG格式
    # # 显示图形
    # plt.show()
    
    ax2.set_xlabel('Time (hour)', fontsize=12)
    # 设置横坐标刻度和标签，与热力图相同
    ax2.set_xlim(0, 23)
    x_ticks = [0, 6, 12, 18]
    x_tick_labels = [str(i) for i in x_ticks]
    ax2.set_xticks(x_ticks)
    ax2.set_xticklabels(x_tick_labels)
    ax2.set_ylabel('Constraint violation (kW)', fontsize=12)
    # 在 ax2 子图上添加网格线
    ax2.grid(True, linestyle='--', alpha=0.7)
    # ax2.set_title('Line Chart')
    # plt.subplots_adjust(left=0.1, right=0.6, bottom=0.05, top=0.95, hspace=0.2)
    # 调整子图布局
    # 使用 ax.annotate 在每个子图下方居中添加标签
    ax1.annotate('(a)', xy=(0.5, -0.18), xycoords='axes fraction', fontsize=12, ha='center')
    ax2.annotate('(b)', xy=(0.5, -0.22), xycoords='axes fraction', fontsize=12, ha='center')
    plt.tight_layout()
    # plt.show()
    plt.savefig('result/DP_result1.pdf', format='pdf')  # 指定dpi为300，可调整清晰度

    
    # 显示图形
    plt.show()


