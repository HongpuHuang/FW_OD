# 读取所需模块
from .read import read_notoll
from .graph import Network
from copy import deepcopy  #已有的函数
import numpy as np
from .FW import calc_RG
import matplotlib.pyplot as plt
seed = 0 #因在这个代码里，路段流量观测值是我在全有全无分配基础上加了随机项生成的，为了保证能重复结果，需要指定随机种子    ？不懂
np.random.seed(seed)


BETA = {(1, 2):1, (2, 4):2, (2, 3):1,(1, 3):1,(4, 3):0}
def bineray_linesearch(net, y_flow, flow, fftime, capacity, k1=100, eps1=0.001, eps2=0.01):
    b_iter = 0
    low = 0 #a
    up = 1 #b
    alpha = 0.5*(low + up)
    sigma_alpha = 0
    for l in net.Link:
        d = y_flow[l] - flow[l]
        x_alpha = flow[l] + alpha * d

        t_alpha = BPR(net, fftime[l], capacity[l], x_alpha, 0.15,4)

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

            t_alpha = BPR(net, fftime[l], capacity[l], x_alpha, 0.15,4)

            sigma_alpha += t_alpha * d
        b_iter+=1
    return alpha

def BPR(net, fftime, capacity, flow, alpha, beta):
    if net.name != "T1":
        return (fftime*(1 + alpha * pow((flow/capacity),beta)))
    else:
        return (fftime + alpha*flow)

def all_or_nothing(net, o, predecessor, demand, flow1, OD_a, aux):
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
            flow1[now_link] += assign_x
            if aux == 1:
                OD_a[(o, d)][now_link]['X'] += assign_x
            else:
                OD_a[(o, d)][now_link]['f'] += assign_x
            h_n = t_n
            if h_n == o:
                break
    return (flow1, OD_a)




def FW_markOD(net, time, fftime, capacity, demand1, OD_a, k0, eps):
     #initialize
    #Flowall = {}
    #Descent = {}
    fw_iter = 0
    flow1 = {}
    y_flow = {}
    #buchang = []
    for link in net.Link:
        time[link] = fftime[link]
        flow1[link] = 0
        y_flow[link] = 0
        for od in OD_a.keys():
            OD_a[od][link]['f'] = 0
            OD_a[od][link]['X'] = 0

    relative_gap = float('inf')
    #RG_list = []
    #perform all or nothing
    for o in net.Odtree.keys():
        impedance, predecessor = net.LC(o, time, net.Outnode, net.Link)
        flow1, OD_a = all_or_nothing(net, o, predecessor, demand1, flow1, OD_a, aux=0)
    # Flowall[fw_iter] = deepcopy(flow)
    #main loop
    while (fw_iter < k0) and (relative_gap > eps):
        for ll in net.Link:

            time[ll] = BPR(net, fftime[ll], capacity[ll], flow1[ll], 0.15,4)

            for od in OD_a.keys():
                OD_a[od][ll]['X'] = 0
            y_flow[ll] = 0
        relative_gap = calc_RG(net, time,flow1, demand1)
        for o in net.Odtree.keys():
            impedance, predecessor = net.LC(o, time, net.Outnode, net.Link)
            y_flow, OD_a = all_or_nothing(net, o, predecessor, demand1, y_flow, OD_a, aux=1)
        alpha = bineray_linesearch(net, y_flow, flow1, fftime, capacity, k1=100, eps1=0.001, eps2=0.01)
        #buchang.append(alpha)
        for ll in net.Link:
            flow1[ll] = flow1[ll] + alpha * (y_flow[ll] - flow1[ll])
            for od in OD_a.keys():
                OD_a[od][ll]['f'] = OD_a[od][ll]['f'] + alpha * (OD_a[od][ll]['X'] - OD_a[od][ll]['f'])
                OD_a[od][ll]['P'] = OD_a[od][ll]['f']/demand1[od]
        fw_iter += 1
        #Flowall[fw_iter] = deepcopy(flow)
        #Descent[fw_iter] = deepcopy(y_flow)
    # print("fw_iter", fw_iter, "relative_gap", relative_gap)
    return (flow1, OD_a)



def relative_error_calc(demand_est, old_demand_est):   #用相对误差公式计算误差
    ###########################################################################
    # This function is used to run step 6
    # flow: (type:dict) flow[link] = value
    ###########################################################################
    # gap = \frac{\sqrt{\sum_{a}(V_a^n-\hat{V_a})^2}}{\sqrt{\sum_{a}\hat{V_a}^2}}
    relative_error = 0
    for od in demand_est.keys():
        if old_demand_est[od] != 0:
            oderror = abs(demand_est[od]-old_demand_est[od])/old_demand_est[od]
        else:
            oderror = 0
        if oderror > relative_error:
            relative_error = oderror
    return relative_error

def relative_error_calc2(flow, flow_observe):
    sum_diff = 0
    for ll in flow_observe.keys():
        sum_diff += pow(flow[ll] - flow_observe[ll], 2)
    relative_error = np.sqrt(sum_diff)/(np.sqrt(sum(pow(flow_observe[l], 2) for l in flow_observe.keys())))
    return relative_error



def recursion_link(linka, OD_a, demand, flow_obser, gamma):
    #步骤1 V_a = \sum_{od} {demand[od] * P_{od}^a}
    v_a = 0
    for od in OD_a.keys():
        v_a += OD_a[od][linka]['P']*demand[od] #计算出V_a
    ##########################################################################
    #步骤2 Y_a=\hat{V_a}/V_a
    if v_a != 0:
        yp = flow_obser[linka]/v_a
    else:
        #print('v_a equals 0! linka=', linka)
        yp = 1   #随便设的，不影响结果
    ##########################################################################
    #步骤3 demand[od] = Y_a^{P_{od}^a}*demand[od]
    for od in demand.keys():
        demand[od] = pow(yp, OD_a[od][linka]['P'])*demand[od]
    ##########################################################################
    return (v_a, yp, OD_a, demand)


def equili_esti(net, time, fftime, capacity, demand,  K0, e0,gamma_input, mode):   #K0是收敛次数，e0是收敛的精度
    ###########################################################################
    # mode: 1:谢老师说的方法：假定一个已知的OD矩阵demand_True，分配得到flow_observe作输入，再逐步迭代demand，最终结果趋近于demand_True
    #       2:直接随机生成flow_observe，这时由于flow_observe的输入不一定科学，所以RG不一定收敛但RG2一般条件下会收敛
    #       3：以T1网络为例，直接写好flow_observe
    # 建议T1采用mode 1,3进行测试，sf采用mode 1进行测试，Hearn也采用mode 1测试
    ###########################################################################
    # initialization
    RGlist = []   #收敛精度的列表
    RG2list = []
    flow = {}   #每个link上的flow是多少，将其存储为一个字典
    OD_a = {}   #类似于pija、Xija的字典，其第一层的key是od，也就是ij，第二层的key是link，也就是a
    yp_list = []
    k = 0   #循环从0开始
    lambda_list = {}
    for l in net.Link:
        flow[l] = 0   #把所有的flow都赋值为0
        lambda_list[l] = 0
    RG = float('inf')   #把收敛值设置为无穷大
    gamma = gamma_input #实际上没有使用，感觉没什么必要
    ###########################################################################
    # Initialize container
    for o in net.Odtree.keys():
        for d in net.Odtree[o]:
            OD_a[(o, d)] = {}   #对于每一个OD_a再初始化一个字典
            for l in net.Link:
                OD_a[(o, d)][l] = {}
                OD_a[(o, d)][l]['f'] = 0   #代表fija
                OD_a[(o, d)][l]['P'] = 0   #代表pija
                OD_a[(o, d)][l]['X'] = 0   #代表Xija
    ##########    FW     #####################
    FWflow, OD_a = FW_markOD(net, time, fftime, capacity, demand, OD_a, k0=400, eps=pow(10, -4))
    #print(OD_a)
    ###########################################################################
    # Randomly generate a flow observation matrix
    if (mode==3):
        flow_observe = {(1, 2):10, (2, 4):25 ,(2, 3):90, (1, 3):90 ,(4, 3):25}
    ###########################################
    elif (mode==2):
        flow_observe = deepcopy(flow)
        for l in flow_observe.keys():
            flow_observe[l] = 0.5*flow_observe[l]+np.random.rand()*1000   #得到后面待验证的矩阵
            if net.name == "T1":
                flow_observe[(4, 3)] = flow_observe[(2, 4)]
    ###############self-proof###################
    elif (mode==1):
        demand_true = deepcopy(demand)
        for od in demand.keys():
            if net.name == "T1":
                demand_true[od] = 0.5*demand[od]+np.random.rand()*100
            else:
                demand_true[od] = 0.5*demand[od]+np.random.rand()*1000
        flow_observe, _= FW_markOD(net, time, fftime, capacity, demand_true, OD_a, k0=400, eps=pow(10, -4))
    # print("demand_est:", demand)
    else:
        print("mode input is wrong")
    ###########################################################################
    # mainloop主循环
    while ((k<K0) and (RG>e0)):   #k<K0就是循环多少步，RG是收敛还没有达到精度
        yp_list.append([])
        k += 1   #把循环步数+1
        old_demand_est = deepcopy(demand)
        for l in flow_observe.keys():   # We need to do the recursion link by link!对每一个link进行迭代
            flow[l], new_yp, OD_a, demand = recursion_link(l, OD_a, demand, flow_observe, gamma)   #进行Step4
            yp_list[k-1].append(new_yp)
        ##########    FW     #####################
        FWflow, OD_a = FW_markOD(net, time, fftime, capacity, demand, OD_a, k0=400, eps=pow(10, -4))
#        print(OD_a)
        RG = relative_error_calc2(flow, flow_observe) # Flow similarity
        RG2 = relative_error_calc(demand, old_demand_est)   #OD similarity
        print("Step %s:"%k, "Flow similarity RG=%.8f"%RG, "OD RG2=%.8f"%RG2)   #打印相对误差
        # print("demand_est:", demand)
        RGlist.append(RG)   #把相对误差存起来
        RG2list.append(RG2)
    if (mode==1):
        print("demand_True", demand_true)
    return (RGlist, RG2list, demand)
