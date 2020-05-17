# CS3243 Introduction to Artificial Intelligence
# Project 1: k-Puzzle

import os
import sys

# Running script on your own - given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

from collections import deque

class Node(object):
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        self.init_state = self.flatten(init_state)
        self.goal_state = self.flatten(goal_state)
        self.width = len(init_state)
        self.goal_node = None


    def solve(self):
        if self.isSolvable() == False:
            return ["UNSOVLABLE"]
        else:
            self.BFS()
            listOfMoves = self.backTrack()
            return listOfMoves

    def flatten(self, ls):
        return tuple([element for i in ls for element in i])

    #check inversions
    def isSolvable(self):
        state = self.init_state
        inversions = 0
        length = len(state)
        emptyCell = 0

        for i in range(length):
            if state[i] == 0:
                emptyCell = i
                continue
            for j in range(i + 1, length):
                if state[j] == 0:
                    continue
                else:
                    if state[i] > state[j]:
                        inversions += 1
        
        if self.width % 2 == 1:
            return inversions % 2 == 0
        else:
            rowFromBot = length - blank // length - 1
            return rowFromBot % 2 == inversions % 2

    #Breath-First Search
    def BFS(self):
        frontier = deque()
        visited = set()
        root = Node(self.init_state, None, None)
        frontier.append(root)
        visited.add(self.hashKey(root.state))

        if root.state == self.goal_state:
            self.goal_node = root
            return
        
        while frontier != set():
            node = frontier.popleft()
            ngbrs = self.explore(node)
            for v in ngbrs:
                hashState = self.hashKey(v.state)
                if hashState not in visited:
                    visited.add(hashState)
                    frontier.append(v)
                    if (v.state == self.goal_state):
                        self.goal_node = v
                        return

    #defining a hash for our visited state
    def hashKey(self, state):
        key = ""
        for i in state:
            key += str(i)
        return key

    #exploring adjacent nodes/ branching out
    def explore(self, node):
        left = Node(self.move(node.state, "LEFT"), node, "LEFT")
        right = Node(self.move(node.state, "RIGHT"), node, "RIGHT")
        top = Node(self.move(node.state, "UP"), node, "UP")
        bottom = Node(self.move(node.state, "DOWN"), node, "DOWN")
        nList = [left, right, top, bottom]
        newList = []
        for v in nList:
            if v.state == None:
                continue
            else:
                newList.append(v)
        

        return newList

    #Move empty cell up down left or right
    def move(self, state, action):
        tempState = list(state)
        grid = [[0 for x in range(self.width)] for y in range(self.width)]
        
        counter = 0
        emptyR = -1
        emptyC = -1


        for i in range(self.width):
            for j in range(self.width):
                if tempState[counter] == 0:
                    emptyR = i
                    emptyC = j
                
                grid[i][j] = tempState[counter]
                counter += 1
        if action == "LEFT":
            #swap empty cell with cell on the right
            try:
                temp = grid[emptyR][emptyC + 1]
                grid[emptyR][emptyC] = temp
                grid[emptyR][emptyC + 1] = 0
                return self.flatten(grid)
            except IndexError:
                return None
        
        if action == "RIGHT":
            #swap empty cell with cell on the left
            try:
                if (emptyC - 1) < 0:
                    return None 
                temp = grid[emptyR][emptyC - 1]
                grid[emptyR][emptyC] = temp
                grid[emptyR][emptyC - 1] = 0
                return self.flatten(grid)
            except IndexError:
                return None

        if action == "UP":
            #swap empty cell with cell below
            try:
                temp = grid[emptyR + 1][emptyC]
                grid[emptyR][emptyC] = temp
                grid[emptyR + 1][emptyC] = 0
                return self.flatten(grid)
            except IndexError:
                return None

        if action == "DOWN":
            #swap empty cell with cell above
            try:
                if emptyR - 1 < 0:
                    return None
                temp = grid[emptyR - 1][emptyC]
                grid[emptyR][emptyC] = temp
                grid[emptyR - 1][emptyC] = 0
                return self.flatten(grid)
            except IndexError:
                return None    

    def backTrack(self):
        moves = list()
        node = self.goal_node

        while node.parent != None:
            moves.append(node.action)
            print(node.action)
            node = node.parent
        moves.reverse()
        return moves

  

if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()
    
    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]
    

    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')







