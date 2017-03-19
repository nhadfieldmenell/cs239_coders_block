def bfs(node,goal,size,grid):
    # breadth first search implementation
    queue = deque()
    queue.append(node)
    explored.append(node.point)
