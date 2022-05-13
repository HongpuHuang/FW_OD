import matplotlib.pyplot as plt
def plot_obj(objlist, algorithmname, netname):
    font1 = {'family' : 'Times New Roman','weight' : 'heavy','size' : 18}
    plt.figure(figsize=[12,6])
    if algorithmname == 'greedy':
        plt.plot(objlist, color = 'g', linewidth = 2, linestyle = '--',label=algorithmname)
    elif algorithmname == 'finT2':
        plt.plot(objlist, color = 'b', linewidth = 2, linestyle = '-.',label=algorithmname)
    elif algorithmname == 'GP':
        plt.plot(objlist, color = 'k', linewidth = 2, linestyle = ':',label=algorithmname)
    else:
        plt.plot(objlist, color = 'orange', linewidth = 2, linestyle = '-',label=algorithmname)
    plt.ylabel('Obj', fontdict=font1)
    plt.xlabel('Iteration', fontdict=font1)
    plt.legend()
    plt.show()
# =============================================================================
# 更美丽、直观地绘制Relative Gap图像——针对MulticlassMulticriteria的绘图
# 横轴：Iteration
# 纵轴：Relative Gap(log type)
# =============================================================================
def plot_RG(RGlist, algorithmname, netname):
    font1 = {'family' : 'Times New Roman','weight' : 'heavy','size' : 18}
    plt.figure(figsize=[12,6])
    if algorithmname == 'greedy':
        plt.plot(RGlist, color = 'g', linewidth = 2, linestyle = '--',label=algorithmname)
    elif algorithmname == 'finT2':
        plt.plot(RGlist, color = 'b', linewidth = 2, linestyle = '-.',label=algorithmname)
    elif algorithmname == 'GP':
        plt.plot(RGlist, color = 'k', linewidth = 2, linestyle = ':',label=algorithmname)
    else:
        plt.plot(RGlist, color = 'orange', linewidth = 2, linestyle = '-',label=algorithmname)
    plt.ylabel('Relative Gap', fontdict=font1)
    plt.xlabel('Iteration', fontdict=font1)
    plt.yscale('log')
    plt.legend()
    plt.savefig('./figures/MM/%s_%s.jpg'%(algorithmname, netname), dpi=300, bbox_inches='tight')
    plt.show()
# =============================================================================
# 更美丽、直观地绘制Relative Gap图像——针对标准交通分配问题的绘图
# 横轴：Iteration
# 纵轴：Relative Gap(log type)
# =============================================================================
def plot_RG_sd(RGlist, algorithmname, netname):
    font1 = {'family' : 'Times New Roman','weight' : 'heavy','size' : 18}
    plt.figure(figsize=[12,6])
    if algorithmname == 'greedy':
        plt.plot(RGlist, color = 'g', linewidth = 2, linestyle = '-',label=algorithmname)
    elif algorithmname == 'GP':
        plt.plot(RGlist, color = 'k', linewidth = 2, linestyle = '-',label=algorithmname)
    elif algorithmname == 'FW':
        plt.plot(RGlist, color = 'r', linewidth = 2, linestyle = '-',label=algorithmname)
    else:
        plt.plot(RGlist, color = 'b', linewidth = 2, linestyle = '-',label=algorithmname)
    plt.ylabel('Relative Gap', fontdict=font1)
    plt.xlabel('Iteration', fontdict=font1)
    plt.yscale('log')
    plt.legend()
    plt.savefig('./figures/standard/%s_%s.jpg'%(algorithmname, netname), dpi=300, bbox_inches='tight')
    plt.show()
# =============================================================================
# 网络可视化，将Link上的数值更直观地显示在网络上
# =============================================================================
import math
import numpy as np
from matplotlib.collections import LineCollection
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import colors

def network_v(nodeloc, net, weight, weightname, drawnode, drawtext, addcontent):#drawnode, drawtext=0或1
    # choose parameters
        #Networkname
    if net.name == 'sf':
        networkname = 'The Sioux Falls Network'
    elif net.name == 'cs':
        networkname = 'The Chicago Sketch Network'
    elif net.name == 'cs':
        networkname = 'The Anaheim Network'
    elif net.name == 'toy':
        networkname = 'The 9-nodes Toy Network'
    elif net.name == 'bmc':
        networkname = 'The Berlin-Mitte-Center Network'
    else:
        networkname = 'Unknown Network'
    # pre-calculate
    nodeloc = np.array(list(nodeloc.values()))
    networkScale = math.sqrt(len(nodeloc))
    linkSize = 18/networkScale
    nodeSize = 100/networkScale
    laneSpacing = (max(nodeloc[:,0]) - min(nodeloc[:,0]))/networkScale*0.05
    linknodeloc = np.zeros((len(net.Link), 4)) #Tail X, Tail Y, Head X, Head Y
    for i in range(len(net.Link)):
        tail = net.Link[i][0] - 1
        head = net.Link[i][1] - 1
        linknodeloc[i, 0], linknodeloc[i, 1] = nodeloc[tail, 0], nodeloc[tail, 1]
        linknodeloc[i, 2], linknodeloc[i, 3] = nodeloc[head, 0], nodeloc[head, 1]
    phi = np.arctan2(linknodeloc[:, 3] - linknodeloc[:, 1], linknodeloc[:, 2] - linknodeloc[:, 0])
    dx = np.sin(phi) * laneSpacing
    dy = (-1)*np.cos(phi) * laneSpacing
    linknodeloc[:, 0] = linknodeloc[:, 0] + dx
    linknodeloc[:, 1] = linknodeloc[:, 1] + dy
    linknodeloc[:, 2] = linknodeloc[:, 2] + dx
    linknodeloc[:, 3] = linknodeloc[:, 3] + dy
    # plot link
#    segments=np.empty(shape=[0,2,2])
#    for i in range(len(net.Link)):
#        segment = np.array([[linknodeloc[i,0], linknodeloc[i,1]], [linknodeloc[i,2], linknodeloc[i,3]]]).reshape(-1,2,2)
#        segments = np.vstack((segments,segment))
    segments = linknodeloc.reshape(-1,2,2)
    weight = np.array(list(weight.values()))
    fig = plt.figure(figsize=[13,15])
    ax = plt.axes()
    font1 = {'family':'Times New Roman', 'weight':'heavy', 'size':18}
    font2 = {'family':'Times New Roman', 'weight':'black', 'size':20}
    lc = LineCollection(segments, cmap='coolwarm')
    lc.set_array(weight)
    lc.set_linewidth(linkSize)
    line = ax.add_collection(lc)
    # figure elements
    ax.set_aspect(1)#横纵比例一致
    ax.set_xlim(min(nodeloc[:,0])-5,max(nodeloc[:,0])+5)
    ax.set_ylim(min(nodeloc[:,1])-5,max(nodeloc[:,1])+5)
    ax.set_ylabel('Coordinate Y', fontdict=font1)
    ax.set_xlabel('Coordinate X', fontdict=font1)
    ax.set_title(label=networkname, fontdict=font2)
    # figure colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right',size=0.3,pad=0.3) #size调整宽度，pad调整间距
    #是否强制范围
#    bounds=np.arange(4000, 25000, 2000)
#    norm = colors.BoundaryNorm(bounds ,20)
#    cbar =fig.colorbar(line, ax=ax, cax=cax, norm=norm, boundaries=bounds)

    cbar =fig.colorbar(line, ax=ax, cax=cax)
    cbar.set_label(label=weightname, fontdict=font1)
    # plot node
    if drawnode == 1:
        ax.plot(nodeloc[:, 0], nodeloc[:, 1], 'o', markersize=nodeSize,color='silver',alpha=0.9)
    # plot node text
    if drawtext == 1:
        for i in range(nodeloc.shape[0]):
            ax.text(nodeloc[i, 0]-laneSpacing*1.4/2, nodeloc[i, 1]-laneSpacing*1.4/2, str(i+1), fontsize = 50/networkScale)
    plt.savefig('./figures/%s.jpg'%(addcontent),dpi=300)
    plt.show()


def network_v_notcontinuous(nodeloc, capproblem,  net, weight, weightname, drawnode, drawtext, addcontent):  # drawnode, drawtext=0或1
    if capproblem != 0:
        weight1 = [(k, weight[k]) for k in sorted(weight.keys())]
        weight = {}
        for i in weight1:
            weight[i[0]] = i[1]
    # choose parameters
    # Networkname
    if net.name == 'sf':
        networkname = 'The Sioux Falls Network'
    elif net.name == 'cs':
        networkname = 'The Chicago Sketch Network'
    elif net.name == 'cs':
        networkname = 'The Anaheim Network'
    elif net.name == 'toy':
        networkname = 'The 9-nodes Toy Network'
    elif net.name == 'bmc':
        networkname = 'The Berlin-Mitte-Center Network'
    elif net.name == 'ft':
        networkname = 'Florian Test Network'
    else:
        networkname = 'Unknown Network'
    # pre-calculate
    #nodeloc = np.array(list(nodeloc.values()))
    xnodelist = []
    ynodelist = []
    for i in nodeloc.keys():
        xnodelist.append(nodeloc[i][0])
        ynodelist.append(nodeloc[i][1])
    networkScale = math.sqrt(len(nodeloc))
    linkSize = 18 / networkScale
    nodeSize = 100 / networkScale
    laneSpacing = (max(xnodelist) - min(xnodelist)) / networkScale * 0.05
    if capproblem == 0:
        linknodeloc = np.zeros((len(net.Link), 4))  # Tail X, Tail Y, Head X, Head Y
        for i in range(len(net.Link)):
            tail = net.Link[i][0]
            head = net.Link[i][1]
            linknodeloc[i, 0], linknodeloc[i, 1] = nodeloc[tail][0], nodeloc[tail][1]
            linknodeloc[i, 2], linknodeloc[i, 3] = nodeloc[head][0], nodeloc[head][1]
    else:
        linknodeloc = np.zeros((len(weight), 4))
        for i in range(len(weight)):
            linklist = list(weight.keys())
            tail = linklist[i][0]
            head = linklist[i][1]
            linknodeloc[i, 0], linknodeloc[i, 1] = nodeloc[tail][0], nodeloc[tail][1]
            linknodeloc[i, 2], linknodeloc[i, 3] = nodeloc[head][0], nodeloc[head][1]
    phi = np.arctan2(linknodeloc[:, 3] - linknodeloc[:, 1], linknodeloc[:, 2] - linknodeloc[:, 0])
    dx = np.sin(phi) * laneSpacing
    dy = (-1) * np.cos(phi) * laneSpacing
    linknodeloc[:, 0] = linknodeloc[:, 0] + dx
    linknodeloc[:, 1] = linknodeloc[:, 1] + dy
    linknodeloc[:, 2] = linknodeloc[:, 2] + dx
    linknodeloc[:, 3] = linknodeloc[:, 3] + dy
    # plot link
    #    segments=np.empty(shape=[0,2,2])
    #    for i in range(len(net.Link)):
    #        segment = np.array([[linknodeloc[i,0], linknodeloc[i,1]], [linknodeloc[i,2], linknodeloc[i,3]]]).reshape(-1,2,2)
    #        segments = np.vstack((segments,segment))
    segments = linknodeloc.reshape(-1, 2, 2)
    weight = np.array(list(weight.values()))
    fig = plt.figure(figsize=[13, 15])
    ax = plt.axes()
    font1 = {'family': 'Times New Roman', 'weight': 'heavy', 'size': 18}
    font2 = {'family': 'Times New Roman', 'weight': 'black', 'size': 20}
    lc = LineCollection(segments, cmap='coolwarm')
    lc.set_array(weight)
    lc.set_linewidth(linkSize)
    line = ax.add_collection(lc)
    # figure elements
    ax.set_aspect(1)  # 横纵比例一致
    ax.set_xlim(min(xnodelist) - 5, max(xnodelist) + 5)
    ax.set_ylim(min(ynodelist) - 5, max(ynodelist) + 5)
    ax.set_ylabel('Coordinate Y', fontdict=font1)
    ax.set_xlabel('Coordinate X', fontdict=font1)
    ax.set_title(label=networkname, fontdict=font2)
    # figure colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size=0.3, pad=0.3)  # size调整宽度，pad调整间距
    # 是否强制范围
    #    bounds=np.arange(4000, 25000, 2000)
    #    norm = colors.BoundaryNorm(bounds ,20)
    #    cbar =fig.colorbar(line, ax=ax, cax=cax, norm=norm, boundaries=bounds)

    cbar = fig.colorbar(line, ax=ax, cax=cax)
    cbar.set_label(label=weightname, fontdict=font1)
    # plot node
    # nodeloc = np.array(list(nodeloc.values()))
    if drawnode == 1:
        ax.plot(xnodelist, ynodelist, 'o', markersize=nodeSize, color='silver', alpha=0.9)
    # plot node text
    if drawtext == 1:
        for i in nodeloc.keys():
            ax.text(nodeloc[i][0] - laneSpacing * 1.4 / 2, nodeloc[i][1] - laneSpacing * 1.4 / 2, i,
                    fontsize=50 / networkScale)
    plt.savefig('./figures/%s.jpg' % (addcontent), dpi=300)
    plt.show()
