import search
import random
import math

class SokobanProblem(search.Problem):
    """This class implements a sokoban problem"""
    def __init__(self, initial):
        """Don't forget to implement the goal test
        You should change the initial to your own representation"""
        self.platform=[]
        i=0
        for row in initial:
            self.platform.append([])
            for cell in row:
                self.platform[i].append(cell)
            i+=1
        self.location_player=-1
        self.count_targets=0
        self.location_box=[]
        self.location_target=[]
        self.count_box_on_target=0
        self.rows=len(self.platform)
        self.cols=len(self.platform[0])
        for row in range(0,len(self.platform)):
            for cell in range(0,len(self.platform[row])):
                if self.platform[row][cell]==17 or self.platform[row][cell]==37  or self.platform[row][cell]==27:
                    self.location_player=(row,cell)
                    if self.platform[row][cell] == 27:
                        self.location_target.append((row, cell))
                        self.count_targets += 1
                elif self.platform[row][cell]==15 or self.platform[row][cell]==35 or self.platform[row][cell]==25:
                    if self.platform[row][cell]==25:
                        self.count_box_on_target += 1
                        self.location_target.append((row, cell))
                        self.count_targets += 1
                    self.location_box.append((row, cell))
                elif self.platform[row][cell]==20:
                    self.location_target.append((row, cell))
                    self.count_targets+=1
                elif self.platform[row][cell]==25:
                    self.count_box_on_target+=1

        #print (initial)

        self.deadlocks_cells=self.deadlocks(self.platform,self.location_box,self.location_target)
        initial=(self.rows,self.cols,(self.location_player),tuple(self.location_box),tuple(self.location_target),self.count_targets,self.count_box_on_target,
                 initial,tuple(self.deadlocks_cells))

        search.Problem.__init__(self, initial)
        
    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a tuple, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        act=[]
        location_player = state[2]
        if location_player[0]!=0:
            if state[7][location_player[0]-1][location_player[1]]!=99:
                act.append("U")
        if location_player[0] != state[0]-1:
            if state[7][location_player[0] + 1][location_player[1]] != 99:
                act.append("D")
        if location_player[1] != 0:
            if state[7][location_player[0]][location_player[1]-1] != 99:
                act.append("L")
        if location_player[1] != state[1]-1:
            if state[7][location_player[0]][location_player[1]+1] != 99:
                act.append("R")
        return tuple(act)

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        i = 0
        new_platform=[]
        for row in state[7]:
            new_platform.append([])
            for cell in row:
                new_platform[i].append(cell)
            i += 1

        #box_in_place=state[6]
        #location_player=state[2]
        location_player=state[2]
        count_box_on_target=state[6]
        if action=="U":
            if state[2][0]==0: #player at top row
                return state
            elif state[7][state[2][0]-1][state[2][1]]==99: # player against wall
                return state
            elif state[2][0]==1:
                res= self.move_player(state[7],new_platform,action,"one",location_player,count_box_on_target )
                if res==0:
                    return state
                location_player = res[1]
                count_box_on_target = res[2]
            elif state[2][0]>1:
                if state[7][state[2][0]-1][state[2][1]]==15:
                    res=self.move_player(state[7],new_platform,action,"two",location_player,count_box_on_target )
                    if res == 0:
                        return state
                    location_player = res[1]
                    count_box_on_target = res[2]
                     
                elif  state[7][state[2][0]-1][state[2][1]]==25: #remove box from target
                    res =self.move_player( state[7], new_platform, action, "target",location_player,count_box_on_target )
                    if res == 0:
                        return state
                    location_player = res[1]
                    count_box_on_target = res[2]
                     
                elif state[7][state[2][0]-1][state[2][1]]==10 or state[7][state[2][0]-1][state[2][1]]==20:
                    res =self.move_player(state[7],new_platform,action,"empty_spot",location_player,count_box_on_target )
                    location_player = res[1]
                    count_box_on_target = res[2]
                     
                elif state[7][state[2][0]-1][state[2][1]]==99:
                    return state
                elif state[7][state[2][0] - 1][state[2][1]]==30: #need correction for ice
                    #new_platform[state[2][0] - 1][state[2][1]] += 7
                    #new_platform[state[2][0]][state[2][1]] -= 7
                    #location_player = (state[2][0] - 1, state[2][1])
                    res = self.move_player(state[7], new_platform, action, "ice_player", location_player, count_box_on_target )
                    location_player = res[0]
                    count_box_on_target = res[1]

                elif state[7][state[2][0] - 1][state[2][1]]==35: #need correction for ice
                    if state[7][state[2][0]-2][state[2][1]]==99 or state[7][state[2][0]-2][state[2][1]]==15 or state[7][state[2][0]-2][state[2][1]]==25  or state[7][state[2][0]-2][state[2][1]]==35: #player against two boxes or box that cant move
                        return state
                    if state[7][state[2][0] - 2][state[2][1]] == 20:  # put box at target
                        new_platform[state[2][0] - 2][state[2][1]] = 25  # the box
                        new_platform[state[2][0] - 1][state[2][1]] += 2  # the player
                        count_box_on_target += 1
                        new_platform[state[2][0]][state[2][1]] -= 7
                        location_player = (state[2][0] - 1, state[2][1])
                         
                    elif state[7][state[2][0] - 2][state[2][1]] == 10:  # put box at empty spot
                        new_platform[state[2][0] - 2][state[2][1]] = 15
                        new_platform[state[2][0] - 1][state[2][1]] += 2
                        new_platform[state[2][0]][state[2][1]] -= 7
                        location_player = (state[2][0] - 1, state[2][1])
                         
                    elif state[7][state[2][0] - 2][state[2][1]] == 30:  # put box at empty ice
                        res = self.move_player(state[7], new_platform, action, "ice_box", location_player, count_box_on_target )
                        location_player = res[0]
                        count_box_on_target = res[1]
                         
                        #new_platform[state[2][0] - 2][state[2][1]] = 35
                        #new_platform[state[2][0] - 1][state[2][1]] += 2
                    # delete last place player


        if action=="D":
            if state[2][0]==state[0]-1: #player at bottom row
                return state
            elif state[7][state[2][0]+1][state[2][1]]==99: # player against wall
                return state
            elif state[2][0]==state[0]-2: #player have one row more
                res = self.move_player(state[7], new_platform, action, "one",location_player,count_box_on_target )
                #location_player = self.location_player
                if res== 0:
                    return state
                location_player = res[1]
                count_box_on_target = res[2]
                 
            elif state[0]-1-state[2][0]>1:
                if state[7][state[2][0]+1][state[2][1]]==15:
                    res = self.move_player( state[7], new_platform, action, "two",location_player,count_box_on_target )
                    #location_player = self.location_player
                    if res == 0:
                        return state
                    location_player = res[1]
                    count_box_on_target = res[2]
                     
                elif state[7][state[2][0]+1][state[2][1]]==25: #remove box from target
                    res=self.move_player( state[7], new_platform, action, "target",location_player,count_box_on_target )
                    if res == 0:
                        return state
                    location_player = res[1]
                    count_box_on_target = res[2]
                     
                elif state[7][state[2][0]+1][state[2][1]]==10 or state[7][state[2][0]+1][state[2][1]]==20:
                    res=self.move_player( state[7], new_platform, action, "empty_spot",location_player,count_box_on_target )
                    location_player = res[1]
                    count_box_on_target = res[2]
                     
                elif state[7][state[2][0]+1][state[2][1]]==99:
                    return state
                elif state[7][state[2][0]+1][state[2][1]]==30: #need correction for ice
                    #new_platform[state[2][0] + 1][state[2][1]] += 7
                    #new_platform[state[2][0]][state[2][1]] -= 7
                    #location_player = (state[2][0] + 1, state[2][1])
                    res = self.move_player(state[7], new_platform, action, "ice_player", location_player, count_box_on_target )
                    location_player = res[0]
                    count_box_on_target = res[1]
                elif state[7][state[2][0]+1][state[2][1]]==35: #need correction for ice
                    if state[7][state[2][0]+2][state[2][1]]==99 or state[7][state[2][0]+2][state[2][1]]==15 or state[7][state[2][0] + 2][state[2][1]] == 25 or state[7][state[2][0] + 2][state[2][1]] == 35: #player against two boxes or box that cant move
                        return state
                    if state[7][state[2][0] + 2][state[2][1]] == 20:  # put box at target
                        new_platform[state[2][0] + 2][state[2][1]] = 25  # the box
                        new_platform[state[2][0] + 1][state[2][1]] += + 2  # the player
                        count_box_on_target += 1
                        new_platform[state[2][0]][state[2][1]] = new_platform[state[2][0]][state[2][1]] - 7
                        location_player = (state[2][0] + 1, state[2][1])
                         
                    elif state[7][state[2][0] + 2][state[2][1]] == 10:  # put box at empty spot
                        new_platform[state[2][0] + 2][state[2][1]] = 15
                        new_platform[state[2][0] + 1][state[2][1]] += 2
                        new_platform[state[2][0]][state[2][1]] = new_platform[state[2][0]][state[2][1]] - 7
                        location_player = (state[2][0] + 1, state[2][1])
                         
                    elif state[7][state[2][0] + 2][state[2][1]] == 30:  # put box at empty ice
                        res = self.move_player(state[7], new_platform, action, "ice_box", location_player, count_box_on_target )
                        location_player = res[0]
                        count_box_on_target = res[1]
                         
                        #new_platform[state[2][0] + 2][state[2][1]] = 35
                        #new_platform[state[2][0] + 1][state[2][1]] += 2
                    # delete last place player







        if action=="R":
            if state[2][1]==state[1]-1: #player at right column
                return state
            elif state[7][state[2][0]][state[2][1]+1]==99: # player against wall
                return state
            elif state[2][1]==state[1]-2: #player have one column more
                res = self.move_player( state[7], new_platform, action, "one",location_player,count_box_on_target )
                #location_player = self.location_player
                if res == 0:
                    return state
                location_player = res[1]
                count_box_on_target = res[2]
                 
            elif state[1]-1-state[2][1]>1:
                if state[7][state[2][0]][state[2][1] + 1]==15:
                    res = self.move_player(state[7], new_platform, action, "two",location_player,count_box_on_target )
                    if res == 0:
                        return state
                    location_player = res[1]
                    count_box_on_target = res[2]
                     
                elif state[7][state[2][0]][state[2][1]+1]==25: #remove box from target
                    res =self.move_player( state[7], new_platform,action, "target",location_player,count_box_on_target )
                    if res == 0:
                        return state
                    location_player = res[1]
                    count_box_on_target = res[2]
                     
                elif state[7][state[2][0]][state[2][1]+1]==10 or  state[7][state[2][0]][state[2][1]+1]==20:
                    res =self.move_player(state[7], new_platform, action, "empty_spot",location_player,count_box_on_target )
                    location_player = res[1]
                    count_box_on_target = res[2]
                     
                elif state[7][state[2][0]][state[2][1]+1]==99:
                    return state
                elif state[7][state[2][0]][state[2][1]+1]==30: #need correction for ice
                    #new_platform[state[2][0]][state[2][1]+1] += 7
                    #new_platform[state[2][0]][state[2][1]] -= 7
                    #location_player = (state[2][0], state[2][1]+1)
                    res = self.move_player(state[7], new_platform, action, "ice_player", location_player, count_box_on_target )
                    location_player = res[0]
                    count_box_on_target = res[1]
                elif state[7][state[2][0]][state[2][1] + 1] == 35:  # need correction for ice
                    if state[7][state[2][0]][state[2][1]+2]==99 or state[7][state[2][0]][state[2][1]+2]==15 or state[7][state[2][0]][state[2][1]+2]==25  or state[7][state[2][0]][state[2][1]+2]==35: #player against two boxes or box that cant move
                        return state
                    if state[7][state[2][0]][state[2][1] + 2] == 20:  # put box at target
                        new_platform[state[2][0]][state[2][1] + 2] = 25  # the box
                        new_platform[state[2][0]][state[2][1] + 1] += 2  # the player
                        count_box_on_target += 1
                        new_platform[state[2][0]][state[2][1]] -= 7
                        location_player = (state[2][0], state[2][1] + 1)
                         
                    elif state[7][state[2][0]][state[2][1] + 2] == 10:  # put box at empty spot
                        new_platform[state[2][0]][state[2][1] + 2] = 15
                        new_platform[state[2][0]][state[2][1] + 1] += 2
                        new_platform[state[2][0]][state[2][1]] -= 7
                        location_player = (state[2][0], state[2][1] + 1)
                         
                    elif state[7][state[2][0]][state[2][1] + 2] == 30:  # put box at empty ice
                        res = self.move_player(state[7], new_platform, action, "ice_box", location_player, count_box_on_target )
                        location_player = res[0]
                        count_box_on_target = res[1]
                         
                        #new_platform[state[2][0]][state[2][1] + 2] = 35
                        #new_platform[state[2][0]][state[2][1] + 1] += 2
                    # delete last place player


        if action=="L":
            if state[2][1]==0: #player at left column
                return state
            elif state[7][state[2][0]][state[2][1]-1]==99: # player against wall
                return state
            elif state[2][1]==1: #player have one column more
                res = self.move_player( state[7], new_platform, action, "one",location_player,count_box_on_target )
                #location_player = self.location_player
                if res == 0:
                    return state
                location_player = res[1]
                count_box_on_target = res[2]
                 
            elif state[2][1]>1:
                if state[7][state[2][0]][state[2][1] - 1]==15:
                    res = self.move_player( state[7], new_platform, action, "two",location_player,count_box_on_target )
                    #location_player = self.location_player
                    if res == 0:
                        return state
                    location_player = res[1]
                    count_box_on_target = res[2]
                     
                elif state[7][state[2][0]][state[2][1]-1]==25: #remove box from target
                    res =self.move_player( state[7], new_platform, action, "target",location_player,count_box_on_target )
                    if res == 0:
                        return state
                    location_player = res[1]
                    count_box_on_target = res[2]
                     
                elif state[7][state[2][0]][state[2][1]-1]==10 or state[7][state[2][0]][state[2][1]-1]==20:
                    res =self.move_player( state[7], new_platform, action, "empty_spot",location_player,count_box_on_target )
                    location_player = res[1]
                    count_box_on_target = res[2]
                     
                elif state[7][state[2][0]][state[2][1]-1]==99:
                    return state
                elif state[7][state[2][0]][state[2][1]-1]==30: #need correction for ice
                    #new_platform[state[2][0]][state[2][1]-1] += 7
                    #new_platform[state[2][0]][state[2][1]] -= 7
                    #location_player = (state[2][0], state[2][1]-1)
                    res = self.move_player(state[7], new_platform, action, "ice_player", location_player, count_box_on_target )
                    location_player = res[0]
                    count_box_on_target = res[1]
                elif state[7][state[2][0]][state[2][1]-1]==35: #need correction for ice
                    if state[7][state[2][0]][state[2][1]-2]==99 or state[7][state[2][0]][state[2][1]-2]==15  or state[7][state[2][0]][state[2][1]-2]==25 or state[7][state[2][0]][state[2][1]-2]==35: #player against two boxes or box that cant move
                        return state
                    if state[7][state[2][0]][state[2][1] - 2] == 20:  # put box at target
                        new_platform[state[2][0]][state[2][1] - 2] = 25  # the box
                        new_platform[state[2][0]][state[2][1] - 1] += 2  # the player
                        count_box_on_target += 1
                        new_platform[state[2][0]][state[2][1]] -= 7
                        location_player = (state[2][0], state[2][1] - 1)
                         
                    elif state[7][state[2][0]][state[2][1] - 2] == 10:  # put box at empty spot
                        new_platform[state[2][0]][state[2][1] - 2] = 15
                        new_platform[state[2][0]][state[2][1] - 1] += 2
                        new_platform[state[2][0]][state[2][1]] -= 7
                        location_player = (state[2][0], state[2][1] - 1)
                        
                    elif state[7][state[2][0]][state[2][1] - 2] == 30:  # put box at empty spot
                        res = self.move_player(state[7], new_platform, action, "ice_box", location_player, count_box_on_target )
                        location_player = res[0]
                        count_box_on_target = res[1]
                         
                        #new_platform[state[2][0]][state[2][1] - 2] = 35
                        #new_platform[state[2][0]][state[2][1] - 1] += 2
                    # delete last place player


        count_box_on_target=self.update_box_no_target(new_platform)
        location_box=tuple(self.update_box_loc(new_platform))
        return (state[0],state[1],location_player,location_box,state[4],state[5],
                count_box_on_target,tuple(tuple(x) for x in new_platform),state[8] )


    def goal_test(self, state):
        """ Given a state, checks if this is the goal state.
         Returns True if it is, False otherwise."""
        if state[5]==state[6]:
            #print("DONE!")
            return True
        return False

    def h(self, node):
        #print (node)
        """ This is the heuristic. It gets a node (not a state,
        state can be accessed via node.state)
        and returns a goal distance estimate"""

        #goal awareness
        if  node.state[5]== node.state[6]:
            return 0
        #distance=0
        #deadlocks
        for box in node.state[3]:
            if box in node.state[8]:
                return float('inf')

        temp=0
        target_deadlock=self.target_deadlock(node.state[7],node.state[4])
        if target_deadlock:
            temp=3
        elif target_deadlock==-1:
            return float('inf')

        if self.is_box_stuck(node.state[7],node.state[3],node.state[8]):
            return float('inf')

        box_targets={}
        boxes={}
        for box in node.state[3]:
            boxes[box]={}
            boxes[box]['used']=0
            boxes[box]['target'] = None

        for target in node.state[4]:
            box_targets[target]={}
            #box_targets[target]['isTarget'] = 0
            box_targets[target]['dist']=float('inf')
            box_targets[target]['box'] = None

        flag = False
        while flag is False:
            flag = True
            for box in boxes:
                if boxes[box]['used'] == 0:
                    flag = False
                    break
            if flag:
                break
            # if node.state[7][4][1] == 25 and node.state[7][6][2] == 15:
            #    print("b")

            for target in box_targets:
                min = box_targets[target]['dist']
                for box in boxes:
                    path = abs(box[1] - target[1]) + abs(box[0] - target[0])
                    if path < min:  # found better path
                        if boxes[box]['used'] == 1:
                            other_target = boxes[box]['target']
                            if box_targets[other_target]['dist'] > path:  # found better box for target
                                if box_targets[target]['box'] is not None:
                                    boxes[box_targets[target]['box']]['used'] = 0
                                    boxes[box_targets[target]['box']]['target'] = None
                                box_targets[other_target]['box'] = None
                                box_targets[other_target]['dist'] = float('inf')
                                box_targets[target]['box'] = box
                                box_targets[target]['dist'] = path
                                boxes[box]['target'] = target
                                min = path
                        else:
                            if box_targets[target]['box'] is not None:
                                boxes[box_targets[target]['box']]['used'] = 0
                                boxes[box_targets[target]['box']]['target'] = None
                            boxes[box]['used'] = 1
                            boxes[box]['target'] = target
                            box_targets[target]['box'] = box
                            box_targets[target]['dist'] = path
                            min = path

        #print("b")


            #targets[target]=1
                #elif box_targets[box]['isTarget'] == 1:
            #for target in targets:
            #    min_dist=float('inf')
            #    for box in box_targets:
            #        path = abs(box[1] - target[1]) + abs(box[0] - target[0])
            #        if min_dist>path:
            #            if box_targets[box]['target']!=target and targets[target]==1:
            #                for temp_box in box_targets:
            #                    if box_targets[temp_box]['target']==target and box_targets[temp_box]['dist']<path:
            #                        box_targets[temp_box]['dist'] = float('inf')
            #                        box_targets[temp_box]['target'] = None
            #                        if box_targets[box]['target'] != None:
            #                            targets[box_targets[box]['target']] = 0
            #                        box_targets[box]['target'] = target
            #                        box_targets[box]['dist'] = path
            #            elif targets[target]==0 and box_targets[box]['dist']>path:
            #                if box_targets[box]['target'] != None:
            #                    targets[box_targets[box]['target']] = 0
            #                box_targets[box]['target'] = target
            #                box_targets[box]['dist'] = path
            #                targets[target] = 1


            #if node.state[7][4][1]==25 and node.state[7][6][2]==15:
            #    print("b")



        #for box in box_targets:
        #    for other_box in box_targets:
        #        #if (box==(4,1) and other_box==(6,2)) or (other_box==(4,1) and box==(6,2)):
        #        #    print("b")
        #        path1=abs(box[1] - box_targets[other_box]['target'][1]) + abs(box[0] - box_targets[other_box]['target'][0])
        #        path2 = abs(other_box[1] - box_targets[box]['target'][1]) + abs(other_box[0] - box_targets[box]['target'][0])
        #        if path1<path2 and path2<=box_targets[other_box]['dist']:
        #            new_target=box_targets[box]['target']
        #            new_d=box_targets[box]['dist']
        #            box_targets[box]['target']=box_targets[other_box]['target']
        #            box_targets[box]['dist'] =path1
        #            box_targets[other_box]['target'] = new_target
        #            box_targets[other_box]['dist'] = path2











        sum=0
        for box in box_targets:
            sum+= box_targets[box]['dist']

        #min = float('inf')
        #for box in box_targets:
        #    try:
        #        if min>box_targets[box]['dist']:
        #            min=box_targets[box]['dist']
        #    except:
        #        print(box)
        #for box in box_targets:
        #    for other_box in box_targets:
        #        if box==other_box:
        #            continue
        #        if box_targets[box]['dist']>box_targets[other_box]['dist']:
        #            sum+=box_targets[box]['dist']-box_targets[other_box]['dist']



        nearest_box_dist=float('inf')
        nearest_box=None
        player=node.state[2]


        for box in node.state[3]:
            if node.state[7][box[0]][box[1]]!=25:
                box_tar = boxes[box]['target']
                min_dis = float('inf')
                col=0
                row=0
                if box_tar[0] < box[0]:
                    row=1
                elif box_tar[0] > box[0]:
                    row=-1
                else:
                   row=0
                if box_tar[1] < box[1]:
                    col=1
                elif box_tar[1] > box[1]:
                    col=-1
                else:
                    col=0
                if col==-1 and row==-1:
                    col=0
                path = abs(box[1]+col - player[1]) + abs(box[0]+row - player[0])
                if nearest_box_dist>path:
                    nearest_box_dist=path
                    nearest_box=box






        #print(nearest_box)
        #sec_nearest_box=None
        #sec_nearest_box_dist = float('inf')
        #for box in node.state[3]:
        #    if nearest_box!=box and node.state[7][box[0]][box[1]] != 25:
        #        path = abs(box[1] - nearest_box[1]) + abs(box[0] - nearest_box[0])
        #        if path>sec_nearest_box_dist:
        #            sec_nearest_box=box
        #            sec_nearest_box_dist=path





        return 0.4*sum+0.6*nearest_box_dist#+temp#node.state[6]#+sec_nearest_box_dist
    """Feel free to add your own functions"""

    def target_deadlock(self,platform,targets):
        for target in targets:
            if platform[target[0]][target[1]]==25:
                continue
            if target[0]==0:#target in first row
                if target[1]==0:#target left corner
                    if platform[target[0]][1]==15 or platform[target[0]][1]==25 or platform[target[0]][1]==35 or platform[target[0]][1]==99: #next col not free
                        if platform[target[0]+1][0]==15 or platform[target[0]+1][0]==25 or platform[target[0]+1][0]==35 or platform[target[0]+1][0]==99: #next row not free
                            return True
                elif target[1]==len(platform[0])-1:  #target right corner
                    if platform[target[0]][len(platform[0])-2]==15 or platform[target[0]][len(platform[0])-2]==25 or platform[target[0]][len(platform[0])-2]==35 or platform[target[0]][len(platform[0])-2]==99: #next col not free
                        if platform[target[0]+1][len(platform[0])-1]==15 or platform[target[0]+1][len(platform[0])-1]==25 or platform[target[0]+1][len(platform[0])-1]==35 or platform[target[0]+1][len(platform[0])-1]==99: #next row not free
                            return True
                else: #target not in corner
                    if  platform[target[0]+1][target[1]]==99:
                        if platform[target[0]][target[1]-1] == 25 and platform[target[0]][target[1]+1]==99:
                            if target[1]-1>0 and platform[target[0]][target[1]-2]== 25 or platform[target[0]][target[1]-2]== 15 or platform[target[0]][target[1]-2]== 35:
                                return -1
                            return True
                        elif platform[target[0]][target[1]-1]==99 and platform[target[0]][target[1]+1]==25:
                            return True
            if target[0]==len(platform)-1:#target in last row
                if target[1]==0:#target left corner
                    if platform[target[0]][1]==15 or platform[target[0]][1]==25 or platform[target[0]][1]==35 or platform[target[0]][1]==99: #next col not free
                        if platform[target[0]-1][0]==15 or platform[target[0]-1][0]==25 or platform[target[0]-1][0]==35 or platform[target[0]-1][0]==99: #prev row not free
                            if len(platform[0])>2 and platform[target[0]][2]==15 or platform[target[0]][2]==25 or platform[target[0]][2]==35 or platform[target[0]][2]==99:
                                return True
                elif target[1]==len(platform[0])-1:  #target right corner
                    if platform[target[0]][len(platform[0])-2]==15 or platform[target[0]][len(platform[0])-2]==25 or platform[target[0]][len(platform[0])-2]==35 or platform[target[0]][len(platform[0])-2]==99: #next col not free
                        if platform[target[0]-1][len(platform[0])-1]==15 or platform[target[0]-1][len(platform[0])-1]==25 or platform[target[0]-1][len(platform[0])-1]==35 or platform[target[0]-1][len(platform[0])-1]==99: #prev row not free
                            return True
                else: #target not in corner
                    if  platform[target[0]-1][target[1]]==99: #wall above target
                        if platform[target[0]][target[1]-1] == 25 and platform[target[0]][target[1]+1]==99:
                            if target[1]-1>0 and platform[target[0]][target[1]-2]== 25 or platform[target[0]][target[1]-2]== 15 or platform[target[0]][target[1]-2]== 35:
                                return -1
                            return True
                        elif platform[target[0]][target[1]-1]==99 and platform[target[0]][target[1]+1]==25:
                            return True




    def move_player(self,platform,new_platform,dircetion,scenario,location_player,count_box_on_target):
        parm_row=None
        parm_col=None
        if dircetion=="U":
            parm_col=0
            parm_row=-1
        elif dircetion=="D":
            parm_col=0
            parm_row=1
        elif dircetion == "R":
            parm_col = 1
            parm_row = 0
        elif dircetion == "L":
            parm_col = -1
            parm_row = 0
        if scenario=="one":
            return self.one_move_left(parm_row,parm_col,location_player,platform,new_platform,count_box_on_target)
        elif scenario=="two":
            return self.move_box(parm_row, parm_col,location_player,  platform, new_platform,count_box_on_target)
        elif scenario=="empty_spot":
            return self.move_empty_spot(parm_row, parm_col,location_player, platform, new_platform,count_box_on_target)
        elif scenario=="target":
            return self.move_from_target(parm_row, parm_col,location_player, platform, new_platform,count_box_on_target)
        elif scenario=="ice_player":
            return self.move_ice_only_player(parm_row, parm_col, location_player, platform, new_platform, count_box_on_target)
        elif scenario=="ice_box":
            if dircetion=="L" or dircetion=="R":
                return self.move_ice_col(parm_row, parm_col, location_player, platform, new_platform, count_box_on_target)
            else:
                return self.move_ice_row(parm_row, parm_col, location_player, platform, new_platform, count_box_on_target)


    def one_move_left(self,parm_row,parm_col,location_player,platform,new_platform,count_box_on_target ):
        player_row=location_player[0]
        player_col=location_player[1]
        if platform[player_row +parm_row][player_col + parm_col] == 15 or platform[player_row +parm_row][player_col+ parm_col] == 99 or platform[player_row +parm_row][player_col+ parm_col] == 25 or platform[player_row +parm_row][player_col + parm_col] == 35:  # player against wall or box that cant move
            return 0
        else:
            # move player
            if platform[player_row+ parm_row][player_col + parm_col] == 20:
                new_platform[player_row +parm_row][player_col + parm_col] = 27
            elif platform[player_row +parm_row][player_col + parm_col] == 30:
                new_platform[player_row +parm_row][player_col + parm_col] = 37
            elif platform[player_row +parm_row][player_col + parm_col] == 10:
                new_platform[player_row +parm_row][player_col + parm_col] = 17
            # delete last place player
            new_platform[player_row][player_col] -= 7
            location_player = (player_row + parm_row, player_col + parm_col)
             
            return 1, location_player, count_box_on_target


    def move_ice_only_player(self, parm_row, parm_col, location_player, platform, new_platform, count_box_on_target):
        player_row = location_player[0]
        player_col = location_player[1]
        if parm_row == 0:
            limit = len(new_platform[0])
        else:
            limit = len(new_platform)
        j = 1
        while j < limit and player_row + j * parm_row<limit and  player_col + j * parm_col<limit  and platform[player_row + j * parm_row][player_col + j * parm_col] == 30:
            new_platform[player_row + j * parm_row][player_col + j * parm_col] = 37
            # new_platform[player_row + j * parm_row - 1 * parm_row][player_col+j * parm_col - 1 * parm_col] += 2
            new_platform[location_player[0]][location_player[1]] -= 7
            location_player = (player_row + j * parm_row, player_col + j * parm_col)
            j += 1
        if j < limit and player_row + j * parm_row<limit and  player_col + j * parm_col<limit and (platform[player_row + j * parm_row][player_col + j * parm_col] == 10 or \
                          platform[player_row + j * parm_row][player_col + j * parm_col] == 20 or \
                          platform[player_row + j * parm_row][
                              player_col + j * parm_col] == 30):  # more room with empty spot or target
            new_platform[player_row + j * parm_row][player_col + j * parm_col] += 7
            if new_platform[player_row + j * parm_row][player_col + j * parm_col] == 25:
                count_box_on_target += 1
            new_platform[player_row + j * parm_row - 1 * parm_row][player_col + j * parm_col - 1 * parm_col] -= 7
            # new_platform[location_player[0]][location_player[1]] -= 7
            location_player = (player_row + j * parm_row, player_col + j * parm_col)

        return (location_player, count_box_on_target)

    def move_ice_row(self, parm_row, parm_col, location_player, platform, new_platform, count_box_on_target):
        player_row = location_player[0]
        player_col = location_player[1]
        num_rows = len(new_platform)
        # try:
        j = 2
        while j < num_rows and player_row + j * parm_row<num_rows and platform[player_row + j * parm_row][player_col] == 30:  # more ice
            new_platform[player_row + j * parm_row][player_col] += 5
            new_platform[player_row + j * parm_row - 1 * parm_row][player_col] -= 5
            # new_platform[location_player[0]][location_player[1]] -= 7
            # location_player = (player_row + j*parm_row - 1*parm_row, player_col)
            j += 1
        if j < num_rows and player_row + j * parm_row<num_rows and (
                platform[player_row + j * parm_row][player_col] == 10 or platform[player_row + j * parm_row][player_col] == 20 or
                platform[player_row + j * parm_row][player_col] == 30 or platform[player_row + j * parm_row][
                    player_col] == 35):  # more room with empty spot or target
            new_platform[player_row + j * parm_row][player_col] += 5
            if new_platform[player_row + j * parm_row][player_col] == 25:
                count_box_on_target += 1
            new_platform[player_row + j * parm_row - 1 * parm_row][player_col] -= 5
            # new_platform[location_player[0]][location_player[1]] -= 7
            # location_player = (player_row + j*parm_row - 1*parm_row, player_col)
        # except:
        #    new_platform[player_row + 2*parm_row][player_col] = 35
        #    new_platform[player_row + 1*parm_row][player_col] += 2
        #    location_player = (player_row + 1*parm_row, player_col)
        new_platform[location_player[0]][location_player[1]] -= 7
        new_platform[player_row + 1 * parm_row][player_col] += 7
        location_player = (player_row + 1 * parm_row, player_col)

        return location_player, count_box_on_target

    def move_ice_col(self, parm_row, parm_col, location_player, platform, new_platform, count_box_on_target):
        player_row = location_player[0]
        player_col = location_player[1]
        num_col = len(new_platform[0])
        # ry:
        j = 2
        while j < num_col and player_col + j * parm_col<num_col and platform[player_row][player_col + j * parm_col] == 30:  # more ice
            new_platform[player_row][player_col + j * parm_col] += 5
            new_platform[player_row][player_col - 1 * parm_col + j * parm_col] -= 5
            # new_platform[location_player[0]][location_player[1]] -= 7
            # location_player = (player_row , player_col-1*parm_col +j*parm_col)
            j += 1
        if j < num_col and player_col + j * parm_col<num_col and (platform[player_row][player_col + j * parm_col] == 10 or platform[player_row][
            player_col + j * parm_col] == 20 or
                            platform[player_row][player_col + j * parm_col] == 30 or platform[player_row][
                                player_col + j * parm_col] == 35):  # more room with empty spot or target
            new_platform[player_row][player_col + j * parm_col] += 5
            if new_platform[player_row][player_col + j * parm_col] == 25:
                count_box_on_target += 1
            new_platform[player_row][player_col - 1 * parm_col + j * parm_col] -= 5
            # new_platform[location_player[0]][location_player[1]] -= 7
            # location_player = (player_row , player_col-1*parm_col+j*parm_col)

        # except:
        #    new_platform[player_row ][player_col+2*parm_col] = 35
        #    new_platform[player_row ][player_col+1*parm_col] += 2
        #    location_player = (player_row, player_col+1*parm_col)
        new_platform[location_player[0]][location_player[1]] -= 7
        new_platform[player_row][player_col + 1 * parm_col] += 7
        location_player = (player_row, player_col + 1 * parm_col)

        return location_player, count_box_on_target

    def move_box(self,parm_row,parm_col,location_player,platform,new_platform,count_box_on_target ):
        player_row = location_player[0]
        player_col = location_player[1]
        if platform[player_row + 2*parm_row][player_col + 2* parm_col ] == 99 or platform[player_row + 2*parm_row][player_col + 2* parm_col ] == 15 or platform[player_row + 2 * parm_row][player_col + 2 * parm_col] == 25 or platform[player_row + 2*parm_row][player_col + 2* parm_col ] == 35:  # player against two boxes or box that cant move
            return 0
        else:
            if platform[player_row + 2*parm_row][player_col + 2* parm_col ] == 20:  # put box at target
                new_platform[player_row + 2*parm_row][player_col + 2* parm_col] = 25  # the box
                new_platform[player_row + 1*parm_row][player_col + 1* parm_col] += 2  # the player
                location_player = (player_row +parm_row, player_col + parm_col)
                count_box_on_target += 1
            elif platform[player_row + 2*parm_row][player_col + 2* parm_col] == 10:  # put box at empty spot
                new_platform[player_row + 2*parm_row][player_col + 2* parm_col] = 15
                new_platform[player_row + 1*parm_row][player_col + 1* parm_col] += 2
                location_player = (player_row + parm_row, player_col + parm_col)

            elif platform[player_row + 2*parm_row][player_col + 2* parm_col] == 30:  # put box at empty ice
                if parm_row == 0:
                    res = self.move_ice_col(parm_row,parm_col,location_player,platform,new_platform,count_box_on_target)
                elif parm_col == 0:
                    res = self.move_ice_row(parm_row, parm_col, location_player, platform, new_platform, count_box_on_target)
                location_player = res[0]
                count_box_on_target = res[1]
                 
                return 1, location_player, count_box_on_target
                #new_platform[player_row + 2 * parm_row][player_col + 2 * parm_col] = 35
                #new_platform[player_row + 1 * parm_row][player_col + 1 * parm_col] += + 2
                #location_player = (player_row + parm_row, player_col + parm_col)
                #########UPDATE ICE!!!!!!!!!

            # delete last place player
            new_platform[player_row][player_col] -= 7
             
            return 1,location_player,count_box_on_target

    def move_empty_spot(self,parm_row,parm_col,location_player,platform,new_platform,count_box_on_target):
        player_row = location_player[0]
        player_col = location_player[1]
        new_platform[player_row + 1 * parm_row][player_col + 1 * parm_col] += 7
        new_platform[player_row][player_col] -= 7
        location_player = (player_row + 1 * parm_row,player_col + 1 * parm_col)
        return (1,location_player,count_box_on_target)

    def move_from_target(self,parm_row,parm_col,location_player,platform,new_platform,count_box_on_target ):
        player_row = location_player[0]
        player_col = location_player[1]
        if platform[player_row + 2 * parm_row][player_col + 2 * parm_col] == 99 or platform[player_row + 2 * parm_row][player_col + 2 * parm_col] == 15 or platform[player_row + 2 * parm_row][player_col + 2 * parm_col] == 25 or platform[player_row + 2 * parm_row][player_col + 2 * parm_col] == 35:  # player against two boxes or box that cant move
            return 0
        new_platform[player_row + 2 * parm_row][player_col + 2 * parm_col] += 5
        if new_platform[player_row + 2 * parm_row][player_col + 2 * parm_col]!=25:
            count_box_on_target -= 1
        new_platform[player_row + 1 * parm_row][player_col + 1 * parm_col] += 2
        new_platform[player_row][player_col] -= 7
        location_player = (player_row + 1 * parm_row,player_col + 1 * parm_col)
         
        return 1,location_player,count_box_on_target

    def update_box_loc(self,platform):
        location_box=[]
        for row in range(0,len(platform)):
            for cell in range(0,len(platform[row])):
                if platform[row][cell]==15 or platform[row][cell]==25 or platform[row][cell]==35:
                    location_box.append((row, cell))
        return location_box

    def update_box_no_target(self,platform):
        count=0
        for row in range(0,len(platform)):
            for cell in range(0,len(platform[row])):
                if  platform[row][cell]==25 :
                    count+=1
        return count

    def deadlocks(self,platform,boxes,goals):
        deadlocks_cells=[]
        #place deadlocks in corners
        if platform[0][0] != 20 :
            if platform[0][0] != 99:
                deadlocks_cells.append((0, 0))
            # if platform[1][0]!=20 and platform[1][0]!=99:
            #    deadlocks_cells.append((1, 0))
        if platform[0][len(platform[0]) - 1] != 20:
            if platform[0][len(platform[0]) - 1] != 99:
                deadlocks_cells.append((0, len(platform[0]) - 1))
            # if  platform[1][len(platform[0]) - 1] != 20 and platform[1][len(platform[0]) - 1] != 99:
            #    deadlocks_cells.append((1, len(platform[0]) - 1))
        if platform[len(platform) - 1][0] != 20:
            if platform[len(platform) - 1][0] != 99:
                deadlocks_cells.append((len(platform) - 1, 0))
            # if platform[len(platform) - 1][1] != 20 and platform[len(platform) - 1][1] != 99:
            #    deadlocks_cells.append((len(platform) - 1, 1))
        if platform[len(platform) - 1][len(platform[0]) - 1] != 20:
            if platform[len(platform) - 1][len(platform[0]) - 1] != 99:
                deadlocks_cells.append((len(platform) - 1, len(platform[0]) - 1))
            # if platform[len(platform) - 1][len(platform[0]) - 2] != 20 and platform[len(platform) - 1][len(platform[0]) - 2] != 99:
            #    deadlocks_cells.append((len(platform) - 1, len(platform[0]) - 2))

        if 20 not in platform[0]:
            left=0
            right=len(platform[0])-1
            while left<right:
                if left+1!=right and (platform[0][left]==99 or (0,left) in deadlocks_cells) and (platform[0][right] == 99 or (0, right) in deadlocks_cells):
                    if platform[0][left+1]!=99:
                        deadlocks_cells.append((0,left+1))
                    left+=1
                elif platform[0][left]==99 or (0,left) in deadlocks_cells:
                    right-=1
                elif platform[0][right] == 99 or (0, right) in deadlocks_cells:
                    left+=1
                else:
                    left+=1
                    right-=1
        if 20 not in platform[len(platform)-1]:
            left=0
            right=len(platform[0])-1
            while left<right:
                if left+1!=right and (platform[len(platform)-1][left]==99 or (len(platform)-1,left) in deadlocks_cells) and\
                        (platform[len(platform)-1][right] == 99 or (len(platform)-1, right) in deadlocks_cells):
                    if platform[len(platform) - 1][left + 1] != 99:
                        deadlocks_cells.append((len(platform)-1,left+1))
                    left+=1
                elif platform[len(platform)-1][left]==99 or (len(platform)-1,left) in deadlocks_cells:
                    right-=1
                elif platform[len(platform)-1][right] == 99 or (len(platform)-1, right) in deadlocks_cells:
                    left+=1
                else:
                    left+=1
                    right-=1
        check=True
        for cell in range(0,len(platform)):
            if 20==platform[cell][0]:
                check=False
        if check==True:
            cell=0
            top=0
            bottom=len(platform)-1
            while top<bottom:
                if top+1!=bottom and (platform[top][cell]==99 or (top,cell) in deadlocks_cells) and\
                        (platform[bottom][cell] == 99 or (bottom, cell) in deadlocks_cells):
                    if platform[top+1][cell]!=99:
                        deadlocks_cells.append((top+1,cell))
                    top+=1
                elif (platform[top][cell]==99 or (top,cell) in deadlocks_cells):
                    bottom-=1
                elif (platform[bottom][cell] == 99 or (bottom, cell) in deadlocks_cells):
                    top+=1
                else:
                    top+=1
                    bottom-=1

        check = True
        for cell in range(0, len(platform)):
            if 20==platform[cell][len(platform[0])-1]:
                check = False

        if check==True:
            cell=len(platform[0])-1
            top=0
            bottom=len(platform)-1
            while top<bottom:
                if top+1!=bottom  and (platform[top][cell]==99 or (top,cell) in deadlocks_cells) and\
                        (platform[bottom][cell] == 99 or (bottom, cell) in deadlocks_cells):
                    if platform[top+1][cell]!=99:
                        deadlocks_cells.append((top+1,cell))
                    top+=1
                elif (platform[top][cell]==99 or (top,cell) in deadlocks_cells):
                    bottom-=1
                elif (platform[bottom][cell] == 99 or (bottom, cell) in deadlocks_cells):
                    top+=1
                else:
                    top+=1
                    bottom-=1
        #walls corners inside the platform
        for row in range(1,len(platform)-1):
            for cell in range(1,len(platform[0])-1):
                if platform[row][cell]==10 or platform[row][cell]==30:
                    if (platform[row][cell-1]==99 and platform[row-1][cell]==99) or (platform[row][cell-1]==99 and platform[row+1][cell]==99) \
                               or  (platform[row][cell + 1] == 99 and platform[row - 1][cell] == 99) or (platform[row][cell+1]==99 and platform[row+1][cell]==99):
                        deadlocks_cells.append((row, cell))

        #check walls
        cell_num=0
        for cell in platform[0]: #first row
            if cell==99 and cell_num==0:
                if platform[0][1]!=20:
                    deadlocks_cells.append((0, 1))
            elif cell==99 and cell_num==len(platform[0])-1:
                if platform[0][cell_num-1]!=20:
                    deadlocks_cells.append((0, cell_num-1))
            elif cell == 99:
                if platform[0][cell_num - 1] != 20:
                    deadlocks_cells.append((0, cell_num - 1))
                if platform[0][cell_num + 1] != 20:
                    deadlocks_cells.append((0, cell_num + 1))
            cell_num+=1
        cell_num = 0
        for cell in platform[len(platform)-1]:  # last row
            if cell == 99 and cell_num == 0:
                if platform[len(platform)-1][1] != 20:
                    deadlocks_cells.append((len(platform)-1, 1))
            elif cell == 99 and cell_num == len(platform[0]) - 1:
                if platform[len(platform)-1][cell_num - 1] != 20:
                    deadlocks_cells.append((len(platform)-1, cell_num - 1))
            elif cell == 99:
                if platform[len(platform)-1][cell_num - 1] != 20:
                    deadlocks_cells.append((len(platform)-1, cell_num - 1))
                if platform[len(platform)-1][cell_num + 1] != 20:
                    deadlocks_cells.append((len(platform)-1, cell_num + 1))
            cell_num+=1


        for row_num in range(0,len(platform)-1): #first col
            if  row_num==0 and platform[row_num][0]==99:
                if platform[row_num+1][0]!=20:
                    deadlocks_cells.append((1,0))
            if row_num==len(platform)-1 and platform[row_num][0] == 99:
                if platform[row_num - 1][0] != 20:
                    deadlocks_cells.append((row_num-1, 0))
            if  platform[row_num][0] == 99:
                if platform[row_num - 1][0] != 20:
                    deadlocks_cells.append((row_num-1, 0))
                if platform[row_num + 1][0] != 20:
                    deadlocks_cells.append((row_num+1, 0))

        for row_num in range(0, len(platform)-1):  # last col
            if row_num == 0 and platform[row_num][len(platform[0])-1] == 99:
                if platform[row_num + 1][len(platform[0])-1] != 20:
                    deadlocks_cells.append((1, len(platform[0])-1))
            if row_num == len(platform) - 1 and platform[row_num][len(platform[0])-1] == 99:
                if platform[row_num - 1][len(platform[0])-1] != 20:
                    deadlocks_cells.append((row_num, len(platform[0])-1))
            if platform[row_num][len(platform[0])-1] == 99:
                if platform[row_num - 1][len(platform[0])-1] != 20:
                    deadlocks_cells.append((row_num, len(platform[0])-1))
                if platform[row_num + 1][len(platform[0])-1] != 20:
                    deadlocks_cells.append((row_num, len(platform[0])-1))

        #deadlock between two deadlocks
        for row in range(1, len(platform) - 1):
            for cell in range(1, len(platform[0]) - 1):
                if (row,cell-1) in deadlocks_cells and (row,cell+1) in deadlocks_cells:
                    if platform[row-1][cell]==99 or platform[row+1][cell]==99:
                        deadlocks_cells.append((row,cell))




        return list(set(deadlocks_cells))


    def is_box_stuck(self,platform,boxes,deadlocks):
        for box in boxes:
            for box2 in boxes:
                if box==box2:
                    continue
                if box[0]==box2[0] and abs(box[1]-box2[1])==1:

                    if box[0]==0 and platform[1][box[1]]==99 and platform[1][box2[1]]==99:
                        return True
                    elif box[0]==len(platform)-1 and platform[box[0]-1][box[1]]==99 and platform[box[0]-1][box2[1]]==99:
                        return True
                    #elif (box[0]>0 and box[0]<(len(platform)-2)) and ((platform[box[0]-1][box[1]]==99 and platform[box[0]-1][box2[1]]==99) or\
                     #       (platform[box[0]+1][box2[1]]==99 and platform[box[0]+1][box2[1]]==99)):
                    #    return True

                elif box[1]==box2[1] and abs(box[0]-box2[0])==1:
                    if box[1] == 0 and platform[box[0]][box[1]] == 99 and platform[box2[0]][box2[1]] == 99:
                        return True
                    elif box[1] == len(platform[0]) - 1 and platform[box[0]][box[1]-1] == 99 and platform[box2[0]][box2[1]-1] == 99:
                        return True
                    #elif box[1]>0 and box[1]<len(platform[0]) - 2 and ((platform[box[0]][box[1]-1] == 99 and platform[box2[0]][box2[1]-1] == 99) or (
                    #        platform[box[0]][box[1]+1] == 99 and platform[box2[0]][box2[1]+1] == 99)):
                    #    return True












def create_sokoban_problem(game):
    return SokobanProblem(game)

