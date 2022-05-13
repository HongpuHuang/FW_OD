class Network():
    def __init__(self,name, Innode, Outnode, Link, Odtree):
        self.name = name
        self.Innode = Innode
        self.Outnode = Outnode
        self.Link = Link
        self.Odtree = Odtree
    def LC(self, o, weight, Outnode, Link):
        impedance = {}
        predecessor = {}
        for i in Outnode.keys():
            if i != o:
                impedance[i] = float('inf')
            else:
                impedance[i] = 0
            predecessor[i] = -1
        Q = [o]
        while len(Q) != 0:
            i = Q[0]
            del Q[0]
            for j in Outnode[i]:
                l = (i,j)
                if impedance[j] > impedance[i] + weight[l]:
                    impedance[j] = impedance[i] + weight[l]
                    predecessor[j] = i
                    if j not in Q:
                        Q.append(j)
        return (impedance, predecessor)
    def LS(self, o, d, weight, Outnode, Link):
        impedance = {}
        predecessor = {}
        for ii in Outnode.keys():
            if ii != o:
                impedance[ii] = float('inf')
            else:
                impedance[ii] = 0
            predecessor[ii] = -1
        Q = [o]
        i = float('inf')
        while i != d:
            minw = Q[0]
            minim = impedance[minw]
            minindex = 0
            for index,w in enumerate(Q):
                if impedance[w] < minim:
                    minindex = index
                    minw = w
                    minim = impedance[w]
            i = minw
            del Q[minindex]
            for j in Outnode[i]:
                l = (i,j)
                if impedance[j] > impedance[i] + weight[l]:
                    impedance[j] = impedance[i] + weight[l]
                    predecessor[j] = i
                    if j not in Q:
                        Q.append(j)
        return (impedance, predecessor)

    def LC_2factors(self, o, weight1, weight2, a, Outnode):
        impedance1 = {}
        impedance2 = {}
        predecessor = {}
        for i in Outnode.keys():
            if i != o:
                impedance1[i] = 1000000000
                impedance2[i] = 1000000000
            else:
                impedance1[i] = 0
                impedance2[i] = 0
            predecessor[i] = -1
        Q = [o]
        while len(Q) != 0:
            i = Q[0]
            del Q[0]
            for j in Outnode[i]:
                l = (i,j)
                i_impedance = impedance1[i] + a * impedance2[i]
                j_impedance = impedance1[j] + a * impedance2[j]
                l_impedance = weight1[l] + a * weight2[l]
                if j_impedance  > (i_impedance + l_impedance):
                    impedance1[j] = impedance1[i] + weight1[l]
                    impedance2[j] = impedance2[i] + weight2[l]
                    predecessor[j] = i
                    if j not in Q:
                        Q.append(j)
        return (impedance1, impedance2, predecessor)

    def LS_2factors(self, o, d,  weight1, weight2, a, Outnode):
        impedance1 = {}
        impedance2 = {}
        predecessor = {}
        for ii in Outnode.keys():
            if ii != o:
                impedance1[ii] = 1000000000#注意0*float('nan')的问题
                impedance2[ii] = 1000000000
            else:
                impedance1[ii] = 0
                impedance2[ii] = 0
            predecessor[ii] = -1
        Q = [o]
        i = float('inf')
        while i != d:
            minw = Q[0]
            minim1 = impedance1[minw]
            minim2 = impedance2[minw]
            minindex = 0
            for index,w in enumerate(Q):
                if (impedance1[w] + a * impedance2[w]) < (minim1 + a * minim2):
                    minindex = index
                    minw = w
                    minim1 = impedance1[w]
                    minim2 = impedance2[w]
            i = minw
            del Q[minindex]
            for j in Outnode[i]:
                l = (i,j)
                i_impedance = impedance1[i] + a * impedance2[i]
                j_impedance = impedance1[j] + a * impedance2[j]
                l_impedance = weight1[l] + a * weight2[l]
                if j_impedance  > (i_impedance + l_impedance):
                    impedance1[j] = impedance1[i] + weight1[l]
                    impedance2[j] = impedance2[i] + weight2[l]
                    predecessor[j] = i
                    if j not in Q:
                        Q.append(j)
        return (impedance1, impedance2, predecessor)
