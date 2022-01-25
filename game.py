import pygame , sys , random
screen_width = 600
screen_height = 600
pygame.init()

gridsize = 20
grid_width = screen_width / gridsize
grid_height = screen_height / gridsize

light_green =(0,170,140) #  255, 255, 128 #light_yellow
dark_green =(0,140,120) # 209, 209, 0 #dark_green
#snack colors
orange_red ,black ,corn_flower_blue,deep_pink = (255,69,0) , (34,34,34), (100,149,237) , (255,20,147)

food_color = (250,200,0)
snake_color = (34,34,34)

up = (0,-1) # (x,y)
down = (0,1)
right = (1,0)
left = (-1,0)


class SNAKE:
    frame_velocity = 5
    def __init__(self):
        self.positions = [ ((screen_width/2 ) ,(screen_height/2)) ]
        self.lenght = 1
        self.direction = random.choice([up,down,right,left])
        self.color = snake_color
        self.score = 0
        self.level = 1
    def get_color(self):
        return self.color
    def draw(self,surface):
        for p in self.positions:
            rect = pygame.Rect((p[0],p[1]) , (gridsize , gridsize))
            pygame.draw.rect(surface, self.color, rect)
    def move(self):
        current = self.positions[0]
        x , y = self.direction
        new = ((current[0] + x * gridsize ),(current[1] + y * gridsize))
        
        if new[0] in range(0,screen_width) and new[1] in range(0,screen_height) and not new in self.positions[2 :]:
            self.positions.insert(0,new)
            if len(self.positions) > self.lenght:
                self.positions.pop()
        else : 
            self.reset()
    def reset(self):
        self.lenght = 1 
        self.positions = [ ((screen_width/2 ) ,(screen_height/2)) ]
        self.direction = random.choice([up,down,right,left])
        self.score = 0
        self.level = 1
        SNAKE.frame_velocity = 5
    def get_level(self):
        return self.level
    def level_increase(self,x):
        self.level += x
    def snake_color_changer(self,new_color) :
        self.color = new_color
    def handle_keys(self):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:# x e basarsam programı kapat
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN : #bir tuşa basarsam
                if event.key == pygame.K_UP: #yukarı tuşuna basarsam
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                    
    def turn(self,direction) :
        if (direction[0] * -1 ,direction[1] * -1) == self.direction: #eğer yılan ilerlediği yönün tersine gitmeye çalışıyorsa yaani kendi üzerinde gitmeye çalışıyorsa
            return
        else:
            self.direction = direction 
        
class FOOD :
    
    def __init__(self):
        self.position = (0,0)
        self.color = food_color
        self.random_position()
    def set_food_color(self,color):
        self.color = color
    def get_color(self):
        return self.color
    def random_position(self):
        self.position = (random.randint(0,grid_width - 1) * gridsize , random.randint(0,grid_height - 1) * gridsize)

    def draw(self,surface):
        rect = pygame.Rect((self.position[0],self.position[1]),(gridsize,gridsize))
        pygame.draw.rect(surface, self.color,rect)
    
        
def drawGrid(surface):
    for y in range(0,int(grid_height)):
        for x in range(0,int(grid_width)):
            if (x + y ) % 2 == 0:
                light = pygame.Rect((x * gridsize , y * gridsize),(gridsize,gridsize))
                pygame.draw.rect(surface , light_green ,light )     #çizim yapacağımız katman , renk , objemiz
            else:
                dark = pygame.Rect((x * gridsize , y * gridsize),(gridsize,gridsize))
                pygame.draw.rect(surface , dark_green ,dark )     #çizim yapacağımız katman , renk , objemiz
 

def main():
    red , orange ,aqua, yellow , fuchsia , blue = (255,0,0) , (255,165,0) ,(0,255,255),(255,255,0) , (255,0,255) , 	(0,0,255)
    screen = pygame.display.set_mode((screen_width,screen_height)) 
    clock =pygame.time.Clock()
    
    font = pygame.font.SysFont("arial",20) #font ailesi , punto
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    
    snake = SNAKE()
    food = FOOD()
    #Aşağıdaki while true dan sonraki 4 satırı handle keys fonksiyonunda kullandık onun için burda tekrar yazmaya gerek kalmadı o fonksiyonu yazmadan önce programdan çıkabilmeniz için kullanmanız gerekiyor.
    while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
        
        clock.tick(SNAKE.frame_velocity)#değeri büyüdükçe oyun hızlanacaktır
        snake.handle_keys()
        snake.move()
        
        drawGrid(surface)
        if snake.positions[0] == food.position :
            snake.lenght += 1
            snake.score += 1
            if snake.score > 0 and snake.score % 5 == 0:
                snake.level_increase(1)
                old_snake_color = snake.get_color()
                new_snake_color = snake.get_color()
                while old_snake_color == new_snake_color:
                    snake.snake_color_changer(random.choice([orange_red ,black ,corn_flower_blue,deep_pink]) )
                    new_snake_color = snake.get_color()
            food.random_position()
            SNAKE.frame_velocity += 1
            old_food_color , new_food_color = food.get_color(), food.get_color()
            while old_food_color == new_food_color:
                food.set_food_color( random.choice([red  ,aqua , fuchsia , blue]) )
                new_food_color = food.get_color()
        score_text = font.render("Score: {0}".format(snake.score ), True, (0,0,0))
        level_text = font.render("Level: {0}".format(snake.get_level()) , True ,(0,0,0) )
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface,(0,0))
        screen.blit(score_text,(10,5))
        screen.blit(level_text,(10,40))
        # screen.fill((255,0,0))    
        # rect = pygame.Rect(100,100,200,200)   # (x,y,w,h)
        # pygame.draw.rect(screen,(255,255,255),rect)  #düzlem , renk,obje
        # score_text = font.render("Score: 0", True,(0,0,0)) #metni ,yuvarlak mı değil mi , renk
        # screen.blit(score_text,(10,10))

        pygame.display.update()
main()
