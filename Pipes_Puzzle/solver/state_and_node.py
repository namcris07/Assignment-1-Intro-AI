import copy

HEADING = [0, 90, 180, 270]

class State: 
    def __init__(self, matrix: list) -> None:
        self.head = copy.deepcopy(matrix)
        self.setBump()
        self.bumpWater()
        self.countBump = self.countBumpWater()

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, State):
            for i in range(5):
                for j in range(5):
                    if self.head[i][j]["heading"] != __o.head[i][j]["heading"] or \
                       self.head[i][j]["bump"] != __o.head[i][j]["bump"]:
                        return False
            return True
        return False

    def __hash__(self):
        state_tuple = tuple(
            tuple((self.head[i][j]["heading"], self.head[i][j]["bump"]) for j in range(5))
            for i in range(5)
        )
        return hash(state_tuple)

    def getNoWaterInPipe(self)->list:
        ans = []
        for i in range(5):
            for j in range(5):
                if self.head[i][j]["bump"] == False:
                    ans.append([i,j])
        return ans

    def triggledAt(self, list1: list):
        if self.checkConnectToCenter(list1[0], list1[1]) == True:
            self.head[list1[0]][list1[1]]["bump"] = True
        else:
            self.head[list1[0]][list1[1]]["bump"] = False
        self.stopWaterInValve(list1[0], list1[1])
        self.bumpWater(list1[0], list1[1])
        self.countBump = self.countBumpWater()

    def printState(self):
        i = 4
        j = 0
        while i >= 0:
            while j <=4:
                if self.head[i][j]["bump"] == True:
                    print("[{:^ 3d}] " .format(self.head[i][j]["heading"]), end = '' )
                else:
                    print(" {:^ 3d}  " .format(self.head[i][j]["heading"]), end = '')
                j += 1
            print("")
            i -= 1
            j = 0

    def setBump(self) -> None:
        for i in range(5):
            for j in range(5):
                self.head[i][j]["bump"] = False
        self.head[2][2]["bump"] = True

    def getAngle(self, pipe1)->list: 
        if pipe1["type"] == 1: 
            list1 = [pipe1["heading"]]
        elif pipe1["type"] == 2:
            list1 = [pipe1["heading"], pipe1["heading"] + 180]
        elif pipe1["type"] == 3: 
            list1 = [pipe1["heading"], pipe1["heading"] + 90]
        else:
            list1 = [pipe1["heading"] -90, pipe1["heading"], pipe1["heading"] + 90]
        for i in range(len(list1)):
            if list1[i] > 270:
                list1[i] -= 360
            elif list1[i] < 0:
                list1[i] += 360
        list1.sort()
        return list1       

    def getPosiblePosition(self, oy, ox)->list:
        ans = []
        if oy < 4:
            ans.append([oy + 1, ox])
        if oy > 0:
            ans.append([oy - 1, ox])
        if ox < 4:
            ans.append([oy, ox + 1])
        if ox > 0:
            ans.append([oy, ox -1])
        return ans

    def checkConnect(self, pipe1, pipe2, location) -> bool:
        list1 = self.getAngle(pipe1)
        list2 = self.getAngle(pipe2)

        if location == "right":
            if (0 in list1) and (180 in list2): return True
        elif location == "left":
            if (180 in list1) and (0 in list2): return True
        elif location == "down":
            if (90 in list1) and (270 in list2): return True
        elif location == "up":
            if (270 in list1) and (90 in list2): return True
        return False

    def bumpWater(self, oy = 2,ox = 2):
        if self.head[oy][ox]["bump"] == False:
            return
        queue = [[oy,ox]]
        while len(queue)!= 0:
            nodeO = queue.pop(0)
            i = nodeO[0]
            j = nodeO[1]
            if j  < 4:
                if self.checkConnect(self.head[i][j], self.head[i][j+1], "right") == 1 and self.head[i][j+1]["bump"] == False:
                    self.head[i][j+1]["bump"] = True
                    queue.append([i,j + 1])
            if j > 0:
                if self.checkConnect(self.head[i][j],self.head[i][j-1], "left") == 1 and self.head[i][j-1]["bump"] == False:
                    self.head[i][j-1]["bump"] = True
                    queue.append([i, j - 1])
            if i  < 4:
                if self.checkConnect(self.head[i][j],self.head[i+1][j], "up") == 1 and self.head[i+1][j]["bump"] == False:
                    self.head[i+1][j]["bump"] = True   
                    queue.append([i+1, j])    
            if i > 0:        
                if self.checkConnect(self.head[i][j],self.head[i-1][j], "down") == 1 and self.head[i-1][j]["bump"] == False:
                    self.head[i-1][j]["bump"] = True
                    queue.append([i-1, j])   

    def checkConnectToCenter(self,  oy,ox):
        queue = [[oy,ox]]
        visited = []
        while len(queue) != 0:
            if [2,2] in queue:
                return True
            i = queue[0][0]
            j = queue[0][1]
            visited.append(queue.pop(0))
            if j < 4: 
                if self.checkConnect(self.head[i][j], self.head[i][j + 1], "right") == True:
                    if [i,j + 1] not in visited and [i, j + 1] not in queue:
                        queue.append([i, j + 1])
            if j > 0:
                if self.checkConnect(self.head[i][j], self.head[i][j - 1], "left") == True:
                    if [i, j - 1] not in visited and [i, j - 1] not in queue:
                        queue.append([i, j - 1])
            if i < 4:
                if self.checkConnect(self.head[i][j], self.head[i+1][j], "up") == True:
                    if [i+1,j] not in visited and [i + 1, j] not in queue:
                        queue.append([i + 1, j])
            if i > 0:
                if self.checkConnect(self.head[i][j], self.head[i - 1][j], "down") == True:
                    if [i - 1, j] not in visited and [i - 1, j] not in queue:
                        queue.append([i - 1, j])
        return False

    def checkRecursionBump(self, oy, ox)->bool:
        if ox < 4:
            if self.checkConnect(self.head[oy][ox], self.head[oy][ox + 1], "right"):
                list1 = [  [[oy, ox + 1],[oy, ox]]      ]
                visited = []
                while len(list1) != 0:
                    current_node = list1.pop(0)
                    visited.append(current_node[1])
                    list2 = self.expand(current_node[0], current_node[1])
                    for item in list2:
                        if item in visited: return True
                        list1.append([item, current_node[0]])

        if ox > 0:
            if self.checkConnect(self.head[oy][ox], self.head[oy][ox - 1], "left"):
                list1 = [  [[oy, ox - 1],[oy, ox]]      ]
                visited = []
                while len(list1) != 0:
                    current_node = list1.pop(0)
                    visited.append(current_node[1])
                    list2 = self.expand(current_node[0], current_node[1])
                    for item in list2:
                        if item in visited: return True
                        list1.append([item, current_node[0]])      

        if oy < 4:
            if self.checkConnect(self.head[oy][ox], self.head[oy + 1][ox], "up"):
                list1 = [  [[oy + 1, ox],[oy, ox]]      ]
                visited = []
                while len(list1) != 0:
                    current_node = list1.pop(0)
                    visited.append(current_node[1])
                    list2 = self.expand(current_node[0], current_node[1])
                    for item in list2:
                        if item in visited: return True
                        list1.append([item, current_node[0]]) 
        if oy > 0:
            if self.checkConnect(self.head[oy][ox], self.head[oy - 1][ox], "down"):
                list1 = [  [[oy - 1, ox],[oy, ox]]      ]
                visited = []
                while len(list1) != 0:
                    current_node = list1.pop(0)
                    visited.append(current_node[1])
                    list2 = self.expand(current_node[0], current_node[1])
                    for item in list2:
                        if item in visited: return True
                        list1.append([item, current_node[0]]) 
        return False

    def expand(self, current: list, parrent: list):
        list1 = self.getPosiblePosition(current[0], current[1])
        list1.remove(parrent)
        ans = []
        for item in list1:
            if item[1] > current[1]:
                if self.checkConnect(self.head[current[0]][current[1]], self.head[item[0]][item[1]], "right") == True:
                    ans.append(item)
            elif item[1] < current[1]:
                if self.checkConnect(self.head[current[0]][current[1]], self.head[item[0]][item[1]], "left") == True:
                    ans.append(item)
            elif item[0] > current[0]:
                if self.checkConnect(self.head[current[0]][current[1]], self.head[item[0]][item[1]], "up") == True:
                    ans.append(item)               
            elif item[0] < current[0]:
                if self.checkConnect(self.head[current[0]][current[1]], self.head[item[0]][item[1]], "down") == True:
                    ans.append(item)
        return ans

    def stopWaterInValve(self, oy, ox):
        if (oy > 4 or oy < 0) or (ox > 4 or ox < 0): return 
        queue = self.getPosiblePosition(oy,ox)        
        visited = []
        while len(queue) != 0:
            i = queue[0][0]
            j = queue[0][1]
            queue.pop(0)
            visited.append([i,j])
            if self.head[i][j]["bump"] == True and self.checkConnectToCenter(i,j) == False:
                self.head[i][j]["bump"] = False
                queue1 = self.getPosiblePosition(i,j)
                for temp in queue1:
                    if self.head[temp[0]][temp[1]]["bump"] == True:
                        if temp not in visited and temp not in queue:
                            queue.append(temp)

    def countBumpWater(self):
        return len(self.getBumpPipe())

    def getBumpPipe(self)-> list:
        queueList1 =[[2,2]]
        visited = []
        while len(queueList1) != 0:
            lt = self.getPosiblePosition(queueList1[0][0],queueList1[0][1])
            visited.append(queueList1.pop(0))
            for item in lt:
                if self.head[item[0]][item[1]]["bump"] == True:
                    if item not in visited and item not in queueList1:
                        queueList1.append(item)   
        return visited

class Node:
    def __init__(self,matrix: list, rotate: list, previous) -> None:
        self.state = State(matrix)
        self.rotate = rotate
        if previous == None:
            self.previous = None
            self.step = 0
        else:
            self.previous = previous
            self.step = previous.step + 1

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Node):
            return self.state == __o.state
        return False
    
    def __lt__(self, other):
        return self.state.countBump > other.state.countBump

    def __bool__(self):
        if len(self.state.head) == 0: return False
        return True
        
    def getPipe(self, temp: list):
        return self.state.head[temp[0]][temp[1]]

def generate_successors(current: Node) -> list:
    ans = []    
    for i in range(5):
        for j in range(5):             
            for k in HEADING:                   
                if current.state.head[i][j]["heading"] == k:
                    continue   
                
                if current.state.head[i][j]["type"] == 2 and k in [180, 270]:
                    continue

                new_matrix = copy.deepcopy(current.state.head)
                new_matrix[i][j]["heading"] = k
                
                newNode = Node(new_matrix, [i,j], current)
                ans.append(newNode)
    return ans