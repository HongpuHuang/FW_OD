# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:33:21 2019

@author: lenovo
"""
# =============================================================================
# 本算法使用Frank Wolfe算法解决标准交通分配问题
# =============================================================================
from .read import read_notoll
from .graph import Network
from copy import deepcopy
#from time import clock


def BPR(fftime, capacity, flow, alpha, beta):

    return (fftime + alpha*flow)

def bineray_linesearch(net, y_flow, flow, fftime, capacity, k1=100, eps1=0.001, eps2=0.01):
    b_iter = 0
    low = 0 #a
    up = 1 #b
    alpha = 0.5*(low + up)
    sigma_alpha = 0
    for l in net.Link:
        d = y_flow[l] - flow[l]
        x_alpha = flow[l] + alpha * d

        t_alpha = BPR(fftime[l], capacity[l], x_alpha, 0.15,4)

        sigma_alpha += t_alpha*d
    while ((b_iter < k1) and ((abs(sigma_alpha) > eps1) or (up - low > eps2))) or (sigma_alpha > 0):#让其在梯度为负得到那边停下
        #print(abs(sigma_alpha), up - low)
        if sigma_alpha <0:
            low = alpha
        else:
            up = alpha
        alpha = 0.5*(low + up)
        sigma_alpha = 0
        for l in net.Link:
            d = y_flow[l] - flow[l]
            x_alpha = flow[l] + alpha*d

            t_alpha = BPR(fftime[l], capacity[l], x_alpha, 0.15,4)

            sigma_alpha += t_alpha * d
        b_iter+=1
    return alpha

def all_or_nothing(net, o, predecessor, demand, flow):
    for d in net.Odtree[o]:
        if d == o:
            continue
        if demand[(o,d)] == 0:
            continue
        assign_x = demand[(o,d)]
        h_n = d
        while True:
            t_n = predecessor[h_n]
            #print(t_n, h_n)
            now_link = (t_n, h_n)
            #print(assign_x)
            flow[now_link] += assign_x
            h_n = t_n
            if h_n == o:
                break
    return (flow)
#def modified_all_or_nothing(net, o, predecessor, demand, flow, time, fftime,capacity):
#    for d in net.Odtree[o]:
#        if demand[(o,d)] == 0:
#            continue
#        assign_x = demand[(o,d)]
#        h_n = d
#        while True:
#            t_n = predecessor[h_n]
#            now_link = (t_n, h_n)
#            flow[now_link] += assign_x
#            time[now_link] = BPR(fftime[now_link], capacity[now_link],flow[now_link],0.15,4)
#            h_n = t_n
#            if h_n == o:
#                break
#    return (flow, time)
#def modified_all_or_nothing_y_flow(net, o, predecessor, demand, y_flow, time, fftime,capacity):
#    copy_time = deepcopy(time)
#    for d in net.Odtree[o]:
#        if demand[(o,d)] == 0:
#            continue
#        assign_x = demand[(o,d)]
#        h_n = d
#        while True:
#            t_n = predecessor[h_n]
#            now_link = (t_n, h_n)
#            y_flow[now_link] += assign_x
#            copy_time[now_link] = BPR(fftime[now_link], capacity[now_link],y_flow[now_link],0.15,4)
#            h_n = t_n
#            if h_n == o:
#                break
#    return (y_flow, copy_time)
#reletive gap
def calc_RG(net, time, flow, demand):
    fenzi = 0
    for o in net.Odtree.keys():
        impedance, predecessor = net.LC(o, time, net.Outnode, net.Link)
        for i,j in zip(impedance.keys(),impedance.values()):
            try:
                fenzi += demand[(o,i)]*j
            except:
                pass
    fenmu = 0
    for ll in net.Link:


        fenmu += time[ll] * flow[ll]
    #print('分母total time', fenmu)
    relative_gap = (1-fenzi/fenmu)
    return relative_gap

def FW(net, time, fftime, capacity, demand, k0, eps):
    #initialize
    Flowall = {}
    Descent = {}
    fw_iter = 0
    flow = {}
    y_flow = {}
    buchang = []
    for link in net.Link:
        flow[link] = 0
        y_flow[link] = 0
    relative_gap = float('inf')
    RG_list = []
    #perform all or nothing
    for o in net.Odtree.keys():
        impedance, predecessor = net.LC(o, time, net.Outnode, net.Link)
        flow = all_or_nothing(net, o, predecessor, demand, flow)
#    for l in net.Link:
#        print(l,flow[l])
    #print('第一次all or nothing 结束了')
    Flowall[fw_iter] = deepcopy(flow)
    #main loop
    while (fw_iter < k0) and (relative_gap > eps):
        #print('当前是第:%s步'%fw_iter)
        #step1
        for ll in net.Link:
            time[ll] = BPR(fftime[ll], capacity[ll], flow[ll], 0.15,4)

        #step2
        for link in net.Link:#每次循环前清空y_flow
            y_flow[link] = 0
#        sumtime1 = 0
#        sumtime2 = 0
        for o in net.Odtree.keys():
#            start = clock()
            #find shorest path of the whole newtork
            impedance, predecessor = net.LC(o, time, net.Outnode, net.Link)
#            end1 = clock()
            #all or nothing assignment
            y_flow = all_or_nothing(net, o, predecessor, demand, y_flow)
#            end2 = clock()
#            time1 = end1-start
#            time2 =  end2-end1
#            sumtime1 += time1
#            sumtime2 += time2
        #print('第%s步：'%fw_iter, sumtime1, sumtime2)
        #计算 relative gap
        relative_gap = calc_RG(net, time,flow, demand)
        print('第%s步：RG = '%fw_iter, relative_gap)
        RG_list.append(relative_gap)
        #line search 并移动
        alpha = bineray_linesearch(net, y_flow, flow, fftime, capacity, k1=100, eps1=0.001, eps2=0.01)
        buchang.append(alpha)
        for ll in net.Link:
            flow[ll] = flow[ll] + alpha * (y_flow[ll] - flow[ll])
        #迭代循环
        fw_iter += 1
        Flowall[fw_iter] = deepcopy(flow)
        Descent[fw_iter] = deepcopy(y_flow)
    return (time, flow, RG_list, Flowall, Descent, buchang)

#from GP import calc_BPR_tadao

#    Margin = {}
#    for l in Link:
#        Margin[l] = Flow[l]*calc_BPR_tadao(Flow[l], Capacity[l], Fftime[l])

#import matplotlib.pyplot as plt
#plt.plot(buchanglist)



#import pandas as pd
#DescentD = pd.DataFrame(Descent)
#DescentD.to_csv('Descent.csv')



#def modified_FW(net, time, fftime, capacity, demand, k0, eps):
#    #initialize
#    fw_iter = 0
#    flow = {}
#    y_flow = {}
#    for link in net.Link:
#        flow[link] = 0
#        y_flow[link] = 0
#    relative_gap = float('inf')
#    RG_list = []
#    #perform all or nothing
#    for o in net.Odtree.keys():
#        impedance, predecessor = net.LC(o, time, net.Outnode, net.Link)
#        flow, time = modified_all_or_nothing(net, o, predecessor, demand, flow, time, fftime, capacity)
#    copy_time = deepcopy(time)##
#    #main loop
#    while (fw_iter < k0) and (relative_gap > eps):
#        print('当前是第:%s步'%fw_iter)
#        #step1
#        for ll in net.Link:
#            time[ll] = BPR(fftime[ll], capacity[ll], flow[ll], 0.15,4)
#        #step2
#        for link in net.Link:#每次循环前清空y_flow
#            y_flow[link] = 0
#        for o in net.Odtree.keys():
#            #find shorest path of the whole newtork
#            impedance, predecessor = net.LC(o, time, net.Outnode, net.Link)
#            #impedance, predecessor = net.LC(o, copy_time, net.Outnode, net.Link)
#            #all or nothing assignment
#            y_flow = all_or_nothing(net, o, predecessor, demand, y_flow)
#            #y_flow, copy_time =  modified_all_or_nothing_y_flow(net, o, predecessor, demand, y_flow, copy_time, fftime,capacity)
#        #计算 relative gap
#        relative_gap = calc_RG(time,flow, demand)
#        print('relative gap = ', relative_gap)
#        RG_list.append(relative_gap)
#        #line search 并移动
#        alpha = bineray_linesearch(net, y_flow, flow, fftime, capacity, k1=100, eps1=0.001, eps2=0.01)
#        for ll in net.Link:
#            flow[ll] = flow[ll] + alpha * (y_flow[ll] - flow[ll])
#        #迭代循环
#        fw_iter += 1
#    return (time, flow, RG_list)
#Time, Flow, RG_list = modified_FW(net, Time, Fftime, Capacity, Demand, k0=2000, eps=pow(10,-4))
