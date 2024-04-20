#  File: ImageFill.py
#  Student Name: Vihaan Mehta
#  Student UT EID: vjm655


import os
import sys

# -----------------------PRINTING LOGIC, DON'T CHANGE ----------------------------

# this enables printing colors on Windows somehow
os.system("")

# code to reset the terminal color
RESET_CHAR = "\u001b[0m"
# color codes for the terminal
COLOR_DICT = {
    "black": "\u001b[30m",
    "red": "\u001b[31m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33m",
    "blue": "\u001b[34m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m"
}
# character code for a block
BLOCK_CHAR = "\u2588"

# Input: text is some string we want to write in a specific color
#   color is the name of a color that is looked up in COLOR_DICT
# Output: returns the string wrapped with the color code


def colored(text, color):
    color = color.strip().lower()
    if not color in COLOR_DICT:
        raise Exception(color + " is not a valid color!")
    return COLOR_DICT[color] + text

# Input: color is the name of a color that is looked up in COLOR_DICT
# prints a block (two characters) in the specified color


def print_block(color):
    print(colored(BLOCK_CHAR, color)*2, end='')

# -----------------------PRINTING LOGIC END ---------------------------


# Stack class; you can use this for your search algorithms
# Do not change.
class Stack(object):
    def __init__(self):
        self.stack = []

    # add an item to the top of the stack
    def push(self, item):
        self.stack.append(item)

    # remove an item from the top of the stack
    def pop(self):
        return self.stack.pop()

    # check the item on the top of the stack
    def peek(self):
        return self.stack[-1]

    # check if the stack if empty
    def is_empty(self):
        return len(self.stack) == 0

    # return the number of elements in the stack
    def size(self):
        return len(self.stack)


# Queue class; you can use this for your search algorithms
# Do not change.
class Queue(object):
    def __init__(self):
        self.queue = []

    # add an item to the end of the queue
    def enqueue(self, item):
        self.queue.append(item)

    # remove an item from the beginning of the queue
    def dequeue(self):
        return self.queue.pop(0)

    # checks the item at the top of the Queue
    def peek(self):
        return self.queue[0]

    # check if the queue is empty
    def is_empty(self):
        return len(self.queue) == 0

    # return the size of the queue
    def size(self):
        return len(self.queue)


# class for a graph node; contains x and y coordinates, a color, a list of edges and
# a flag signaling if the node has been visited (useful for serach algorithms)
# it also contains a "previous color" attribute. This might be useful for your
# flood fill implementation.
# Do not change.
class ColorNode:
    # Input: x, y are the location of this pixel in the image
    #   color is the name of a color
    def __init__(self, index, x, y, color):
        self.index = index
        self.color = color
        self.prev_color = color
        self.x = x
        self.y = y
        self.edges = []
        self.visited = False

    # Input: node_index is the index of the node we want to create an edge to in the node list
    # adds an edge and sorts the list of edges
    def add_edge(self, node_index):
        self.edges.append(node_index)

    # Input: color is the name of the color the node should be colored in;
    # the function also saves the previous color (might be useful for your
    # flood fill implementation)
    def visit_and_set_color(self, color):
        self.visited = True
        self.prev_color = self.color
        self.color = color

        print("Visited node " + str(self.index))


# class that contains the graph
# You will add code to this class.
class ImageGraph:
    def __init__(self, image_size):
        self.nodes = []
        self.image_size = image_size

    # prints the image formed by the nodes on the command line
    def print_image(self):
        img = [["black" for i in range(self.image_size)] for j in range(self.image_size)]

        # fill img array
        for node in self.nodes:
            img[node.y][node.x] = node.color

        for line in img:
            for pixel in line:
                print_block(pixel)
            print()
        # print new line/reset color
        print(RESET_CHAR)

    # sets the visited flag to False for all nodes
    def reset_visited(self):
        for i in range(len(self.nodes)):
            self.nodes[i].visited = False

    # implement your adjacency matrix printing here.
    def print_adjacency_matrix(self):
        print("Adjacency matrix:")

        # Here, we do a double loop through the list of nodes, checking
        # if the adjacency matrix contains an edge for a certain node
        for x in range(len(self.nodes)):
            for y in range(len(self.nodes)):
                    # If there is more than 0 edges, we print a 1
                if self.nodes[x].edges.count(y) > 0:
                    print("1", end = "")
                else:
                    # Else, we print a 0
                    print("0", end = "")
            print()
        print()
                

    # implement your bfs algorithm here. Call print_image() after coloring a node
    # Input: graph is the graph containing the nodes
    #   start_index is the index of the currently visited node
    #   color is the color to fill the area containing the current node with
    def bfs(self, start_index, color):
        # reset visited status
        self.reset_visited()
        # print initial state
        print("Starting BFS; initial state:")
        self.print_image()
     
        # Our starting node is obtained from the start_index variable
        startNode = self.nodes[start_index]
        
        # We save the starting color into a variable, then visit and change the color of the starting node
        startingColor = startNode.color
        startNode.visit_and_set_color(color) 
        
        # Classic implementation of BFS with a set and queue
        discoveredSet = set()
        frontierQueue = Queue()
        visitedList = []

        # We enqueue the starting node and add it to the discovered set
        frontierQueue.enqueue(startNode)
        discoveredSet.add(startNode)
        
        # While the frontier queue is not empty, we pop a node from it and run the following algorithm:
        while frontierQueue.is_empty() == False:
            currentNode = frontierQueue.dequeue()
            # If the node being dequeued is the correct color and not in visitedList, we add it to visitedList
            if currentNode.color is startingColor and visitedList.__contains__(currentNode) == False:
                visitedList.append(currentNode)

            # For every vertex in the list of edges of the currentNode, we run a series of checks:
            for adjacentVertex in currentNode.edges:
                    # First, we see if the color of the current node is the same as the starting color, 
                    # and that the node is not already discovered
                if  self.nodes[adjacentVertex].color == startingColor and discoveredSet.__contains__(self.nodes[adjacentVertex]) == False:
                    
                    # If the node passes the checks, we visit it and set its color to the desired color
                    self.nodes[adjacentVertex].visit_and_set_color(color)
                    # The node is added to the frontierQueue and discoveredSet, and the image is printed
                    frontierQueue.enqueue(self.nodes[adjacentVertex])
                    discoveredSet.add(self.nodes[adjacentVertex])
                    self.print_image()
       
    # implement your dfs algorithm here. Call print_image() after coloring a node
    # Input: graph is the graph containing the nodes
    #   start_index is the index of the currently visited node
    #   color is the color to fill the area containing the current node with

    def dfs(self, start_index, color):
        # reset visited status
        self.reset_visited()
        # print initial state
        print("Starting DFS; initial state:")
        self.print_image()

        # We obtain the starting node from start_index and save its color
        startNode = self.nodes[start_index]
        startingColor = startNode.color
        # Next, we push the node to the stack and create our visitedSet
        vertexStack = Stack()
        vertexStack.push(startNode)                        
        visitedSet = set()
       
       # While the vertexStack is not empty, we run the following algorithm:
        while vertexStack.size() > 0:
            # First, we pop a vertex from the stack
            currentVertex = vertexStack.pop() 
            # We check if the vertex is not already visited and if it has the correct starting color
            if currentVertex not in visitedSet and currentVertex.color == startingColor:
                # If the vertex passes the checks, we visit it and set its color, adding it to the visitedSet
                currentVertex.visit_and_set_color(color)
                visitedSet.add(currentVertex)
                # Next, we check our current vertex's edges, representing DFS. Instead of tracing each path equally,
                # we try to go as far as possible on one path
                for adjacentVertex in currentVertex.edges:
                    # If the node is the correct color and has not been visited, we again push to vertexStack
                    if  self.nodes[adjacentVertex].color == startingColor and self.nodes[adjacentVertex] not in visitedSet:
                        vertexStack.push(self.nodes[adjacentVertex])
                # Finally, we print the image
                self.print_image()
                        
            


# Creates an Image Graph using input, the Color Node class and the ImageGraph class.
def create_graph(data):
    # creates graph from read in data
    data_list = data.split("\n")

    # get size of image, number of nodes
    image_size = int(data_list[0])
    node_count = int(data_list[1])

    graph = ImageGraph(image_size)

    index = 2

    # create nodes
    for i in range(node_count):
        # node info has the format "x,y,color"
        node_info = data_list[index].split(",")
        new_node = ColorNode(len(graph.nodes), int(node_info[0]), int(node_info[1]), node_info[2])
        graph.nodes.append(new_node)
        index += 1

    # read edge count
    edge_count = int(data_list[index])
    index += 1

    # create edges between nodes
    for i in range(edge_count):
        # edge info has the format "fromIndex,toIndex"
        edge_info = data_list[index].split(",")
        # connect node 1 to node 2 and the other way around
        graph.nodes[int(edge_info[0])].add_edge(int(edge_info[1]))
        graph.nodes[int(edge_info[1])].add_edge(int(edge_info[0]))
        index += 1

    # read search info
    search_info = data_list[index].split(",")
    search_start = int(search_info[0])
    search_color = search_info[1]

    return graph, search_start, search_color


''' ##### DRIVER CODE #####
    ##### Do not change, except for the debug flag '''


def main():

    # Debug flag - set to False before submitting
    debug = False
    if debug:
        in_data = open('small.in')
    else:
        in_data = sys.stdin

    # read input
    data = in_data.read()

    # create graph
    graph, search_start, search_color = create_graph(data)

    # print matrix
    graph.print_adjacency_matrix()

    # run bfs
    graph.bfs(search_start, search_color)

    # reset by creating graph again
    graph, search_start, search_color = create_graph(data)

    # run dfs
    graph.dfs(search_start, search_color)


if __name__ == "__main__":
    main()
