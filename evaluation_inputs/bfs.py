def bfs(node,goal,size,grid):
    queue = deque()
    queue.append(node)
    explored.append(node.point)
    while queue: