####################################################################################
#先将社交网络和用户倾向的两个数据文件读取进来，G为社交网络，有30354个节点和3425670条边
#data为原始数据，是一个字典，包含1043436用户倾向和度的数据
####################################################################################
import networkx as nx
import pickle
import json
import math

# 用pickle加载gpickle文件
file_path = 'NHB_3w_new.gpickle'
with open(file_path, 'rb') as file:
    G = pickle.load(file)

# 打开 JSON 文件
with open('Xi_undirect.json', 'r') as file:
    # 使用 json.load() 读取 JSON 数据
    data = json.load(file)

####################################################################################
# 因为G是裁剪后的数据，
# 第一步，先把网络还原出来————在data数据中找到G网络中节点对应的用户倾向xi
####################################################################################

#把字典data中的数据分离成两个列表，以方便后续运算
degree = data['degree']             #degree是二维列表
xi = data['xi']                     #xi是一维列表

# #把原始数据中节点的编号放在一个列表中，方便与G网络节点的序号比对
# column = [row[0] for row in degree] #提取degree中每一行的第一个元素作为新的列表，原始数据节点的编号
# a = list(G.nodes)                   #G网络节点的编号

# #如果G网络节点与原始数据节点的编号一致，则对b的对应编号置一
# b = [0] * len(column)
# j = 0
# for i in range(len(column)):
#     if j < len(a) and column[i] == a[j]:
#         b[i] = 1
#         j = j + 1

# #求出G网络对应的用户倾向
# G_xi = []
# for i in range(len(b)):
#     if b[i] == 1:
#         G_xi.append(xi[i])
G_xi = []
for node in G.nodes():
    G_xi.append(xi[node])

####################################################################################
# 求G网络中每个节点对应的所有邻居的平均用户倾向
# 第一步，求出每个节点对应的邻居是哪些
# 第二步，对每一个节点的邻居的用户倾向求平均
####################################################################################

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

####################################################################################
# 画热力图
# 第一步，建立坐标系，横坐标是用户倾向（-1，1），纵坐标是用户邻居的平均倾向（-1，1）
# 第二步，将坐标系平均分成很多个小格子，统计落在小格子上的点的个数，再根据落在小格子上的点数的二维数据画出热力图
####################################################################################

# 将热力图分成1000*1000的小格子，计算落在小格子上的点
changdu = 50
headmap = [[0 for _ in range(changdu)] for _ in range(changdu)]

for i in range(len(G_xi)):
    y = math.trunc(G_xi[i]*changdu*0.5+0.5*changdu)
    x = math.trunc(-G_nbrxi[i]*changdu*0.5+0.5*changdu)
    headmap[x][y] = headmap[x][y] + 1

import numpy as np
import matplotlib.pyplot as plt

# 创建热力图
plt.figure(figsize=(10, 8))
heatmap = plt.imshow(headmap, cmap='inferno',interpolation='bicubic',extent=[-1, 1, -1, 1])

# 添加颜色条
# plt.colorbar(heatmap)

# 添加标题和标签
plt.title('')
plt.xlabel('Individual Leaning')
plt.ylabel('Neighborhood Leaning')

# # 隐藏横纵坐标刻度
# plt.xticks([])
# plt.yticks([])

# 显示图形
plt.show()