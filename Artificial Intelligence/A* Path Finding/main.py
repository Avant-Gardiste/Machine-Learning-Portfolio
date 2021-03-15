import pygame
import math, random, sys
from tkinter import messagebox, Tk

# Set up the display
width, height = 600, 600
size = (width, height) 
pygame.init()
win = pygame.display.set_mode(size)
pygame.display.set_caption('A* Path Finding')

clock = pygame.time.Clock()

cols, rows = 40, 40

grid = []
startSet, endSet = [], []
path = []

w = width//cols
h = height//rows

# Build visualizing tool
class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        
    def show(self, win, col):
        if self.wall == True:
            col = (0, 0, 0)
        pygame.draw.rect(win, col, (self.x*w, self.y*h, w-1, h-1))
    
    def add_neighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y+1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])
        #Add Diagonals
        if self.x < cols - 1 and self.y < rows - 1:
            self.neighbors.append(grid[self.x+1][self.y+1])
        if self.x < cols - 1 and self.y > 0:
            self.neighbors.append(grid[self.x+1][self.y-1])
        if self.x > 0 and self.y < rows - 1:
            self.neighbors.append(grid[self.x-1][self.y+1])
        if self.x > 0 and self.y > 0:
            self.neighbors.append(grid[self.x-1][self.y-1])

def Wall(pos, state):
    i = pos[0] // w
    j = pos[1] // h
    grid[i][j].wall = state
            
def heuristic(a, b):
    return math.sqrt((a.x - b.x)**2 + abs(a.y - b.y)**2)

for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Spot(i, j))
    grid.append(arr)

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)

start = grid[2][2]
end = grid[cols - cols//2][rows - cols//4]

startSet.append(start)

def main():
    flag = False
    noflag = True
    startflag = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    Wall(pygame.mouse.get_pos(), True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    startflag = True

        if startflag:
            if len(startSet) > 0:
                winner = 0
                for i in range(len(startSet)):
                    if startSet[i].f < startSet[winner].f:
                        winner = i

                current = startSet[winner]
                
                if current == end:
                    temp = current
                    while temp.prev:
                        path.append(temp.prev)
                        temp = temp.prev 
                    if not flag:
                        flag = True
                        Tk().wm_withdraw()
                        messagebox.showinfo("Final Solution", "Done !" )
                    elif flag:
                        continue

                if flag == False:
                    startSet.remove(current)
                    endSet.append(current)

                    for neighbor in current.neighbors:
                        if neighbor in endSet or neighbor.wall:
                            continue
                        tempG = current.g + 1

                        newPath = False
                        if neighbor in startSet:
                            if tempG < neighbor.g:
                                neighbor.g = tempG
                                newPath = True
                        else:
                            neighbor.g = tempG
                            newPath = True
                            startSet.append(neighbor)
                        
                        if newPath:
                            neighbor.h = heuristic(neighbor, end)
                            neighbor.f = neighbor.g + neighbor.h
                            neighbor.prev = current

            else:
                if noflag:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "Can't find path :(" )
                    noflag = False

        win.fill((0, 20, 20))
        for i in range(cols):
            for j in range(rows):
                spot = grid[j][i]
                spot.show(win, (255, 255, 255))
                if flag and spot in path:
                    spot.show(win, (25, 120, 250))
                elif spot in endSet:
                    spot.show(win, (255, 0, 0))
                elif spot in startSet:
                    spot.show(win, (39, 115, 33))
                try:
                    if spot == end:
                        spot.show(win, (25, 120, 250))
                except Exception:
                    pass
                
        pygame.display.flip()

if __name__ == '__main__':
	main()