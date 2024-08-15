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
    prosumer_index = 10

    PV_output = prosumer_save[prosumer_index][0]
    BESS_output = prosumer_save[prosumer_index][1]
    HVAC_output = prosumer_save[prosumer_index][2]
    load = prosumer_save[prosumer_index][3]
    net_output = prosumer_save[prosumer_index][4]

    # 创建图表
    plt.figure(figsize=(8, 5))

    # 颜色列表，每个折线对应一个颜色
    # colors = ['red', 'blue', 'green', 'orange', 'purple']
    # labels = ['PV', 'ESS', 'HVAC', 'Load', 'Net power']
    colors = ['red', 'blue', 'green', 'orange']
    labels = ['PV', 'ESS', 'HVAC', 'Load']
    # markers = ['o', 's', 'D', '^', 'v']  # 不同的标记样式
    markers = ['o', 's']
    print('size:', len(PV_output))
    # # 循环绘制折线图
    # for i, array in enumerate([PV_output, BESS_output, -HVAC_output, -load]):
    #     plt.plot(array, label=labels[i], color=colors[i], marker=markers[0], markersize=2.5, linewidth=2)
    # 绘制柱状堆叠图
    plt.bar(np.arange(24), PV_output, label=labels[0], alpha=0.7)
    plt.bar(np.arange(24), BESS_output, bottom=PV_output, label=labels[1], alpha=0.7)
    plt.bar(np.arange(24), -HVAC_output, bottom=PV_output+BESS_output, label=labels[2], alpha=0.7)
    plt.bar(np.arange(24), -load, bottom=PV_output+BESS_output-HVAC_output, label=labels[3], alpha=0.7)
    # 绘制面积堆叠图
    # plt.stackplot(np.arange(24), PV_output, BESS_output, -HVAC_output, -load,  labels=labels, colors=colors, alpha=0.7)
    plt.plot(net_output, label='Net power', color='purple', marker=markers[1], markersize=4, linewidth=3)
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
    plt.savefig('prosumer_output.pdf', format='pdf')
