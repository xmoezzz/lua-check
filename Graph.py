from __future__ import print_function
from collections import defaultdict


#not safe for MT
class GraphStep:
    def __init__(self,vertices):
        self.V      = vertices
        self.graph  = defaultdict(list)
        self.result = []
        self.path   = []
        self.visited = None
        self.genfunc = None
        self.inited  = False
        self.s       = 0
        self.d       = 0
   
    def AddEdge(self,u,v):
        self.graph[u].append(v)
    
    def FindAllPathsUtil(self, u, d): 
        self.visited[u]= True
        self.path.append(u)
        if u == d:
            #self.result.append(self.path)
            yield self.path
        else:
            for i in self.graph[u]:
                if self.visited[i]==False: #try python3?
                    for result in self.FindAllPathsUtil(i, d):
                        yield result
        
        self.path.pop()
        self.visited[u]= False
   
    def FindAllPaths(self, s, d):
        self.ClearResult()
        self.visited =[False]*(self.V)
        self.inited  = True
        self.s       = s
        self.d       = d
        self.genfunc = self.FindAllPathsUtil(s, d)
        return self.genfunc
    
    def GetGenerator(self):
        if self.inited == False:
            raise RuntimeError('GraphStep : not initialized')
        return self.genfunc
    
    def Next(self):
        if self.inited == False:
            raise RuntimeError('GraphStep : not initialized')
        
        path = None
        try:
            path = self.genfunc.next()
        except StopIteration:
            path = None
        return path
    
    def __ReScheSchedule(self):
        self.ClearResult()
        self.visited =[False]*(self.V)
        self.inited  = True
        self.genfunc = self.FindAllPathsUtil(self.s, self.d)
        return self.genfunc
    
    def KillBranchNode(self, node):
        if self.inited == False:
            raise RuntimeError('GraphStep : not initialized')
        if node == 0 or node == len(self.graph) - 1:
            raise RuntimeError('GraphStep : cannot kill root node or terminal node')
        if node in self.graph:
            prev_branch_node = node - 1
            if len(self.graph[prev_branch_node]) >= 2:
                try:
                    self.graph[prev_branch_node].remove(node)
                    self.__ReScheSchedule()
                except:
                    pass
            else:
                raise RuntimeError('GraphStep : previous node != branch node')
        else:
            raise RuntimeError('GraphStep : unknown node')
                

    
    def GetResult(self):
        return self.result
    
    def ClearResult(self):
        self.result = []
        self.path   = []
        self.genfunc= None
        self.visited= None
        self.inited = False
