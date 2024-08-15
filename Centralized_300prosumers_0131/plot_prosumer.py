import numpy as np
# import cvxpy as cvx
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # 从结果文件中读取数据
    prosumer_save = np.load('result/prosumer_result.npy', allow_pickle=True).item()
    X_value = np.load('result/VPP_aggregator_output.npy')
    solution = np.load('result/OPT_value.npy')
    print('OPT_value', solution)
    # print(prosumer_save)
    # 这里决定了绘图的prosumer索引
    prosumer_index = 2

    PV_output = prosumer_save[prosumer_index][0]
    BESS_output = prosumer_save[prosumer_index][1]
    HVAC_output = prosumer_save[prosumer_index][2]
    load = prosumer_save[prosumer_index][3]
    net_output = prosumer_save[prosumer_index][4]

    # 创建图表
    plt.figure(figsize=(8, 5))

    # 颜色列表，每个折线对应一个颜色
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    labels = ['PV', 'ESS', 'HVAC', 'Load', 'Net power']
    # markers = ['o', 's', 'D', '^', 'v']  # 不同的标记样式
    markers = ['o', 's']

    # 循环绘制折线图
    for i, array in enumerate([PV_output, BESS_output, HVAC_output, load]):
        plt.plot(array, label=labels[i], color=colors[i], marker=markers[0], markersize=2.5, linewidth=2)

    plt.plot(net_output, label=labels[4], color=colors[4], marker=markers[1], markersize=4, linewidth=3)
    # 添加图例、标签等
    plt.legend(fontsize=12)
    plt.xlabel('Time (hour)', fontsize=14)
    plt.ylabel('Power output (kW)', fontsize=14)
    # plt.title('Prosumer Power Output and Load Profile')
    plt.grid(True, linestyle='--', alpha=0.7)

    # 设置横坐标刻度和标签
    plt.xticks(np.arange(0, 24, 6), labels=[i for i in range(0, 24, 6)])
    plt.xlim(0, 23)  # 限定 x 轴范围在 0 到 23

    # 显示图表
    plt.tight_layout()
    plt.show()
    # plt.savefig('prosumer_output.pdf', format='pdf')
    # # print('PV_output:', PV_output)
    # # print('BESS_output:', BESS_output)
    # # print('HVAC_output:', HVAC_output)
    # # print('load:', load)
    # # print('net_output:', net_output)

    # # 创建图形对象
    # fig, ax = plt.subplots(figsize=(10, 6))  # 宽度为10英寸，高度为6英寸

    # # 创建柱状图
    # ax.bar(bar_positions1, PV_output, width=bar_width, label='PV_output')
    # ax.bar(bar_positions2, BESS_output, width=bar_width, label='BESS_output')
    # ax.bar(bar_positions3, -HVAC_output, width=bar_width, label='HVAC_output')
    # ax.bar(bar_positions4, -load, width=bar_width, label='load')

    # # 调整折线图的x坐标
    # line_positions = bar_positions1 + 3*bar_width / 2

    # # 创建折线图
    # ax.plot(line_positions, net_output, color='c', linestyle='dotted', marker='o', markersize=3, label='net_output')

    # # 设置坐标轴标签
    # ax.set_xticks(line_positions)
    # ax.set_xticklabels(x_data)
    # ax.set_xlabel('Time (hour)', fontsize=12)
    # ax.set_ylabel('Power Output (kW)', fontsize=12)

    # # 设置刻度标签字体大小
    # ax.tick_params(axis='both', which='major', labelsize=10)

    # # 设置图例字体大小
    # ax.legend(fontsize=10)

    # # 显示图形
    # # plt.show()
    # plt.savefig('result/prosumer10.jpg', dpi=300)
    
    # # # 需要画SOC的图
    # # 设置画布大小
    # fig, ax = plt.subplots(figsize=(8, 6))

    # # 绘制折线图
    # plt.plot(x_data, BESS_SOC, color='blue', linestyle='-', marker='o', markersize=5, label='BESS_SOC')

    # # 设置x轴和y轴标签
    # plt.xlabel('Time (hour)')
    # plt.ylabel('BESS SOC (kWh)')

    # # 设置x轴和y轴刻度范围
    # plt.xlim(1, 24)
    # plt.savefig('result/prosumer10_BESS_SOC.jpg', dpi=300)


    # # 设置图例
    # plt.legend()

    # # # 显示图形
    # # plt.show()

    # # 需要画的第三个图是VPP作为一个整体与市场的交互变量
    # # 设置画布大小
    # fig, ax = plt.subplots(figsize=(8, 6))

    # # 绘制折线图
    # plt.plot(x_data, X_value, color='blue', linestyle='-', marker='o', markersize=5)

    # # 设置x轴和y轴标签
    # plt.xlabel('Time (hour)')
    # plt.ylabel('VPP aggregated power (kWh)')

    # # 设置x轴和y轴刻度范围
    # plt.xlim(1, 24)
    # # 保存到结果中
    # plt.savefig('result/VPP_output.jpg', dpi=300)
