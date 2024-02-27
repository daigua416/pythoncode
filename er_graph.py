import networkx as nx
import matplotlib.pyplot as plt
import random

def initialize_sir(graph, initial_infected_fraction):
    # 设置每个节点的初始状态
    node_states = {'S': set(), 'I': set(), 'R': set()}
    
    # 随机选择一定比例的节点作为初始感染者
    num_infected = 1 # 初始感染者的个数
    infected_nodes = random.sample(sorted(graph.nodes()), num_infected)     # sorted() 该函数可以对可迭代对象进行排序
                                                                            # graph.nodes() 返回的是节点标识符的列表
                                                                            # random.sample()  函数用于从指定的序列中随机选择指定数量的唯一元素，返回一个列表
    
    for node in graph.nodes():
        if node in infected_nodes:
            node_states['I'].add(node)
        else:
            node_states['S'].add(node)
    
    return node_states

def sir_model(graph, initial_infected_fraction, beta, gamma, num_steps):
    states = initialize_sir(graph, initial_infected_fraction)
    susceptible_nodes = states['S']
    infected_nodes = states['I']
    recovered_nodes = states['R']
    
    history = {'S': [len(susceptible_nodes)], 'I': [len(infected_nodes)], 'R': [len(recovered_nodes)]}  
    
    for step in range(num_steps):
        new_infected_nodes = set()
        new_recovered_nodes = set()
        
        # 传播过程
        for infected_node in infected_nodes:
            neighbors = set(graph.neighbors(infected_node))
            susceptible_neighbors = neighbors.intersection(susceptible_nodes)
            
            for neighbor in susceptible_neighbors:
                if random.random() < beta:
                    new_infected_nodes.add(neighbor)
        
        # 恢复过程
        for node in infected_nodes:
            if random.random() < gamma:
                new_recovered_nodes.add(node)
        
        # 更新状态
        susceptible_nodes -= new_infected_nodes
        infected_nodes |= new_infected_nodes
        infected_nodes -= new_recovered_nodes
        recovered_nodes |= new_recovered_nodes
        
        # 记录每个步骤的状态
        history['S'].append(len(susceptible_nodes))
        history['I'].append(len(infected_nodes))
        history['R'].append(len(recovered_nodes))
    
    return history

# 生成ER网络
num_nodes = 1000
average_degree = 4
er_graph = nx.erdos_renyi_graph(num_nodes, p=average_degree/(num_nodes-1))

# 运行SIR模型
initial_infected_fraction = 0.01  # 初始感染者占总人口的比例
beta = 1  # 传播率
gamma = 1  # 恢复率
num_steps = 50  # 模拟的步数

result = sir_model(er_graph, initial_infected_fraction, beta, gamma, num_steps)

# 可视化结果
plt.plot(result['S'], label='Susceptible')
plt.plot(result['I'], label='Infected')
plt.plot(result['R'], label='Recovered')
plt.xlabel('Steps')
plt.ylabel('Number of Nodes')
plt.legend()
plt.show()

########################################################################################
# 先跑一个指定beta、gamma值的SIR模型
# 第一步，生成一个1000个节点且平均度为4的ER网络
# 第二步，初始化ER网络，定义三个变量存放S态、I态、R态节点的数量，并随机指定一个节点作为初始感染节点
# 第三步，模拟传染过程，结束该过程判断条件为I态节点数量为0，
########################################################################################

import networkx as nx
import matplotlib.pyplot as plt
import random

num_nodes = 1000
average_degree = 4
er_graph = nx.erdos_renyi_graph(num_nodes, p=average_degree/(num_nodes-1), seed = 10)   # 生成一个ER网络，p表示两节点之间连边的概率

node_states = {'S': set(), 'I': set(), 'R': set()}  # set()是一个用于创建集合（set）的构造函数