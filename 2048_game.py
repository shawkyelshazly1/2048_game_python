'''
    2048 Game using PYQT5, by - Shaq
'''

#imports
import random
import pygame, sys

#direction constants
UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4
TILE_SIZE = [150,150]
BG = (187, 173, 160)


OFFSETS = {
    UP: (1,0),
    DOWN: (-1,0),
    RIGHT: (0,-1),
    LEFT: (0,1)
}

tile_colors = {
    0:(204, 192, 179),
    2:(238, 228, 218),
    4:(237, 224, 200),
    8:(242, 177, 121),
    16:(245, 149, 99),
    32:(246, 124, 95),
    64:(246, 94, 59),
    128:(237, 207, 114),
    256:(237, 204, 97),
    512:(237, 200, 80),
    1024:(237, 197, 63),
    2048:(237, 194, 46),
    4096:(62, 57, 51)
}

tile_font_color = {
    0:(200, 200, 200),
    2:(119, 110, 101),
    4:(119, 110, 101),
    8:(249, 246, 242),
    16:(249, 246, 242),
    32:(249, 246, 242),
    64:(249, 246, 242),
    128:(249, 246, 242),
    256:(249, 246, 242),
    512:(249, 246, 242),
    1024:(249, 246, 242),
    2048:(249, 246, 242),
    4096:(249, 246, 242)
}



#helper functions
def slide(line):
    '''
        return slided list of numbers to the left replacing empty spots with 0s
        line: given list of numbers
    '''
    temp_list = [0]*len(line)
    idx = 0
    for tile in line:
        if tile != 0:
            temp_list[idx] = tile
            idx += 1
    return temp_list

def slide_and_merge(line):
    '''
        return slided & merged list to the left having each position merged once only and empty spaces replaced with 0s
        line: given list of numbers
    '''
    mrged_line = slide(line)
    for idx in range(len(mrged_line)-1):
        if mrged_line[idx] == mrged_line[idx+1]:
            mrged_line[idx] += mrged_line[idx+1]
            mrged_line[idx+1] = 0
            mrged_line = slide(mrged_line)
    return mrged_line


class Game():
    def __init__(self,grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.board = []
        self.reset()
        self.indicies = {}
        self.indicies[UP] = [[0,col] for col in range(self.grid_width)]
        self.indicies[DOWN] = [[self.grid_height-1,col] for col in range(self.grid_width)]
        self.indicies[RIGHT] = [[row,self.grid_width-1] for row in range(self.grid_height)]
        self.indicies[LEFT] = [[row,0] for row in range(self.grid_height)]
        self.moved_tile = False
        self.ranges = {}
        self.ranges[UP] = self.grid_height
        self.ranges[DOWN] = self.grid_height
        self.ranges[RIGHT] = self.grid_width
        self.ranges[LEFT] = self.grid_width
        self.game_ongoing = False
        self.game_end = False
        self.current_score = 0
        
    def reset(self):
        '''
            resetting board full of 0s
        '''
        self.board = [[0*0 for col in range(self.grid_width)] for row in range(self.grid_height)]
        self.new_tile()
    
    def __str__(self):
        '''
            printing the board string representitive
        '''
        board_str = ""
        board_str += "\n"
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                tile = self.get_tile(row,col)
                board_str += str(tile) + " "
            board_str += "\n"

        return board_str

    def get_tile(self,row,col):
        '''
            returning the tile value on the board
            args: col: column idx, row: row idx
        '''
        return self.board[row][col]

    def get_grid_width(self):
        '''
            returning grid width value
        '''
        return self.grid_width

    def get_grid_height(self):
        '''
            returning grid height value
        '''
        return self.grid_height
        
    def get_empty_positions(self):
        '''
            returning list of empty tiles that contains 0s [row,col]
        '''
        empty_slots = []
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                tile = self.get_tile(row,col)
                if tile == 0:
                    empty_slots.append([row,col])
        return empty_slots

    def set_current_score(self):
        '''
            returning list of empty tiles that contains 0s [row,col]
        '''
        score = 0
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                tile = self.get_tile(row,col)
                if score == 0:
                    score = tile
                elif tile > score:
                    score = tile
                

        self.current_score = score

    def set_tile(self,row,col,value):
        '''
            set tile value in board list
        '''
        self.board[row][col] = value

    def new_tile(self):
        '''
            adding new tile in random empty slot with value (2)- 90% of the time // (4)- 10% of the time
        '''
        empty_slots = self.get_empty_positions()

        if len(empty_slots) > 0:
            tile_pos = random.choice(empty_slots)
            confidence_level = random.randint(1,10)

            if confidence_level >= 9:
                self.set_tile(tile_pos[0],tile_pos[1],4)
            else:
                self.set_tile(tile_pos[0],tile_pos[1],2)

    def move(self, direction):
        '''
            move tiles based in given direction, if moved tiles spawn new tile at random position
        '''
        reached_End = False
        self.moved_tile = False
        list_of_tiles = []
        for indice in self.indicies[direction]:
            for step in range(self.ranges[direction]):
                row = indice[0] + step * OFFSETS[direction][0]
                col = indice[1] + step * OFFSETS[direction][1]
                tile = self.get_tile(row,col)
                list_of_tiles.append(tile)
            
            merged_tiles = slide_and_merge(list_of_tiles)

            if merged_tiles != list_of_tiles:
                for step in range(self.ranges[direction]):
                    row = indice[0] + step * OFFSETS[direction][0]
                    col = indice[1] + step * OFFSETS[direction][1]
                    self.set_tile(row,col,merged_tiles[step])
                    
                    if merged_tiles[step] == 2048:
                        reached_End = True
                self.moved_tile = True

            list_of_tiles = []
        if reached_End:
            self.game_ongoing = False
            self.set_current_score()


        if self.moved_tile:
            self.new_tile()
        elif len(self.get_empty_positions()) == 0:
            self.game_ongoing = False
            self.set_current_score()


class Game_GUI():
    def __init__(self,game):
        pygame.init()
        self._game = game
        self.font = pygame.font.Font(None,100)
        self.grid_width = game.get_grid_width()
        self.grid_height = game.get_grid_height()
        self.width = TILE_SIZE[0] * self.grid_width
        self.height = TILE_SIZE[1] * self.grid_height
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.current_score = self._game.current_score    
        self.highest_score = self.load_highest_score() 

    def play(self):
        '''
            main function to run the game frame & display
        '''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self._game.game_ongoing:
                        self._game.game_ongoing = False
                        if self.current_score > self.highest_score:
                            self.highest_score = self.current_score
                            self.save_highest_score()
                    else:
                        sys.exit()
                else:
                    if self._game.game_ongoing:
                        self.game_movement(event)
                    else:
                        if self.current_score >= self.highest_score:
                            self.highest_score = self.current_score
                            self.save_highest_score()
                        self.mouse_handler(event)
                        
            
            if self._game.game_ongoing:
                self.screen.fill(BG)
                self.draw_grid()
            else:
                self.screen.fill((0,0,0))
                self.draw_splash()
            pygame.display.update()

    def game_movement(self, event):
        '''
            function to get movment change based on event
        '''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self._game.move(UP)
            elif event.key == pygame.K_DOWN:
                self._game.move(DOWN)
            elif event.key == pygame.K_RIGHT:
                self._game.move(RIGHT)
            elif event.key == pygame.K_LEFT:
                self._game.move(LEFT)
        elif event.type == pygame.KEYUP:
            pass
        
    def draw_grid(self):
        '''
            drawing grid on screen frame using rects
        '''
        for y_pos in range(self.grid_height):
            for x_pos in range(self.grid_width):
                tile = self._game.get_tile(y_pos,x_pos)
                rect = pygame.Rect(x_pos*(TILE_SIZE[0]+1),y_pos*(TILE_SIZE[1]+1),TILE_SIZE[0],TILE_SIZE[1])
                pygame.draw.rect(self.screen,tile_colors[tile],rect)
                if tile != 0:
                    text_surf = self.font.render(str(tile),True,tile_font_color[tile])
                    text_rect = [text_surf.get_rect().width/2,text_surf.get_rect().height/2]
                    self.screen.blit(text_surf,(rect.centerx-text_rect[0],rect.centery-text_rect[1]))

    def draw_splash(self):
        '''
            drawing splash screen to start game and end game
        '''
        global new_game_button
        text_surf = self.font.render("2048 Game",True,(200,200,200))
        font2 = pygame.font.Font(None,75)
        text_surf2 = font2.render("Start Game",True,(249, 246, 242))
        text_rect = [text_surf.get_rect().width/2,text_surf.get_rect().height/2]
        text_rect2 = [text_surf2.get_rect().width/2,text_surf2.get_rect().height/2]
        self.screen.blit(text_surf,((self.width/2)-text_rect[0],(self.height/3)-text_rect[1]))
        new_game_button = pygame.Rect((self.width/2)-150,(self.height/1.7)-50,300,100)
        pygame.draw.rect(self.screen,(245, 149, 99),new_game_button)
        self.screen.blit(text_surf2,(new_game_button.centerx-text_rect2[0],new_game_button.centery-text_rect2[1]))

        font3 = pygame.font.Font(None,35)
        self.current_score = self._game.current_score
        text_surf3 = font3.render("Current Score: " + str(self.current_score),True,(200, 200, 200))
        text_rect3 = [text_surf3.get_rect().width/2,text_surf3.get_rect().height/2]
        self.screen.blit(text_surf3,((self.width/2)-text_rect3[0],(self.height-150)-text_rect3[1]))

        text_surf4 = font3.render("Highest Score: " + str(self.highest_score),True,(200, 200, 200))
        text_rect4 = [text_surf4.get_rect().width/2,text_surf4.get_rect().height/2]
        self.screen.blit(text_surf4,((self.width/2)-text_rect4[0],(self.height-100)-text_rect4[1]))

    def mouse_handler(self, event):
        '''
        handling mouse click to start game
        '''
        global new_game_button
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if new_game_button.collidepoint(event.pos):
                self._game.reset()
                self._game.game_ongoing = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass

    def load_highest_score(self):
        try:
            file = open("scores.txt", "r")
            if file.mode == 'r':
                content = file.readline()
                if content == '':
                    return 0
                else:
                    score = int(content)
                    return score
            file.close()
        except FileNotFoundError:
            return 0 

    def save_highest_score(self):
        try:
            file = open("scores.txt", "r+")
            file.seek(0)
            file.truncate()
            file.write(str(self.highest_score))
            file.close()
        except FileNotFoundError:
            file = open("scores.txt", "w+")
            file.write(str(self.highest_score))
            file.close()


#running game
run_game = Game_GUI(Game(4,4))

run_game.play()


