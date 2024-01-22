import pygame
import requests
a1=[[0,0,0,2,6,0,7,0,1],
    [6,8,0,0,7,0,0,9,0],
    [1,9,0,0,0,4,5,0,0],
    [8,2,0,1,0,0,0,4,0],
    [0,0,4,6,0,2,9,0,0],
    [0,5,0,0,0,3,0,2,8],
    [0,0,9,3,0,0,0,7,4],
    [0,4,0,0,5,0,0,3,6],
    [7,0,3,0,1,8,0,0,0]]

WIDTH = 550
background_color = (251,247,245)
original_grid_element_color = (52, 31, 151)

response = requests.get("https: //sugoku.herokuapp.com/board?difficulty=easy")
grid = response.json ()['board']
grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]

def main():
    pygame.init()
    win = pygame. display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Sudoku")
    win.fill (background_color)
    myfont = pygame.font.SysFont('Comic Sans MS', 35)

    for i in range(0,10):
        if i%3==0:
            pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i, 500), 4)
            pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 4)


        pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i, 500), 2)
        pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 2)
    pygame.display.update()

    for i in range(0,len(grid[0])):
        for j in range(0,len(grid[0])):
            if(0<grid[i],[j]<10):
                value = myfont.render(str(grid[i][j]), True, original_grid_element_color)
                win.blit(value, ((j+1)*50 + 15, (i+1)*50 + 15))

    while True:
        for event in pygame.event.get ():
            if event. type == pygame. QUIT:
                pygame.quit ()
                return
            
main() 