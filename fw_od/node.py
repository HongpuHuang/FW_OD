class Node:
    def __init__(self, node_id, l_in_empty, l_out_empty, X, Y):
        self.node_id = node_id
        self.l_in = l_in_empty
        self.l_out = l_out_empty
        self.X = X
        self.Y = Y
    def set_l_in(self, l_in):
        self.l_in.append(l_in)
    def set_l_out(self, l_out ):
        self.l_out.append(l_out)
    def set_SPP_u(self, u):
        self.u = u
    def set_SPP_p(self,p):
        self.p = p
    def set_X(self, X):
        self.X = X
    def set_Y(self, Y):
        self.Y = Y
    def set_Astar_g(self, g):
        self.g = g
    def set_Astar_h(self, h):
        self.h = h
    def set_Astar_f(self, f):
        self.f = f

class LINK:
    def __init__(self,  tail_node, head_node):

        self.tail_node = tail_node
        self.head_node = head_node

