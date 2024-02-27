import networkx as nx
import pickle
import json
import math
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# 用pickle加载gpickle文件
file_path = 'NHB_3w_new.gpickle'
with open(file_path, 'rb') as file:
    G = pickle.load(file)

# 打开 JSON 文件
with open('Xi_undirect.json', 'r') as file:
    # 使用 json.load() 读取 JSON 数据
    data = json.load(file)

degree = data['degree']             #degree是二维列表
xi = data['xi']                     #xi是一维列表

G_xi = []
for node in G.nodes():
    G_xi.append(xi[node])

G_nbr = []      #二维列表，存储G网络的所有节点的邻居
for node in G.nodes():
    nbr = list(G.neighbors(node))
    G_nbr.append(nbr)

G_nbrxi = []    #G网络所有节点邻居的平均倾向
for i in range(len(G_nbr)):
    totalxi = 0
    for j in range(len(G_nbr[i])):
        totalxi = totalxi + xi[G_nbr[i][j]]
    G_nbrxi.append(totalxi/len(G_nbr[i]))

# # 画G_xi的分布直方图
# sns.histplot(G_xi, bins=30, kde=True, color='blue')

# # 添加标签和标题
# plt.xlabel('leaning')
# plt.ylabel('number')
# plt.title('individual')

# # 显示图形
# plt.show()

# # 画G_nbrxi的分布直方图
# sns.histplot(G_nbrxi, bins=30, kde=True, color='blue')

# # 添加标签和标题
# plt.xlabel('leaning')
# plt.ylabel('number')
# plt.title('neighbor')

# # 显示图形
# plt.show()

# 画热力图
changdu = 50        # 定义热力图的像素点的个数
xiangsu = [[0 for _ in range(changdu)] for _ in range(changdu)]     # 生成一个50*50的列表

# 这一个像素点的排列需要尤其注意x和y的位置，以及为什么x的计算公式中要加一个负号
for i in range(len(G_xi)):
    y = math.trunc(G_xi[i]*changdu*0.5+0.5*changdu)
    x = math.trunc(-G_nbrxi[i]*changdu*0.5+0.5*changdu)
    xiangsu[x][y] = xiangsu[x][y] + 1

# 创建热力图
plt.figure(figsize=(10, 10))
heatmap = plt.imshow(xiangsu, cmap='inferno',interpolation='bicubic',extent=[-1, 1, -1, 1])

# 添加标题和标签
plt.title('')
plt.xlabel('Individual Leaning')
plt.ylabel('Neighborhood Leaning')

# 显示图形
plt.show()