# To avoid problems with {files}.png, you must run the program from the same directory as main.py

import pygame as pg
import random as rnd
import math

class Entity:
    def __init__(self, x, y, filename=None):
        self.x = x
        self.y = y
        self.img = pg.image.load(filename).convert_alpha() if not (filename is None) else pg.Surface((5,5))
        self.rect = self.img.get_rect(center = (x, y))
        self.flipped = False
        self.speed = 2
        
    def drawing(self, screen):
        screen.blit(self.img, self.rect)
    
    def movement(self, s_x=0, s_y=0):
        temp_x = self.rect.x
        self.rect.move_ip(s_x, s_y)
        if s_x < 0 and self.flipped:
            self.img = pg.transform.flip(self.img, True, False)
            self.flipped = False
        elif s_x > 0 and not self.flipped:
            self.img = pg.transform.flip(self.img, True, False)
            self.flipped = True

    def collide(self, other) -> bool:
        return self.rect.colliderect(other.rect)

class Player(Entity):
    def __init__(self, x=100, y=100):
        super().__init__(filename=r'.\monster.png', x=x,y=y)
        self.speed = 5
    
    def movement(self, s_x=0, s_y=0):
        super().movement(s_x=s_x, s_y=s_y)
        self.rect.x = min(max(0, self.rect.x), WIDTH - self.rect.width)
        self.rect.y = min(max(0, self.rect.y), HEIGHT - self.rect.height)  

class Enemy(Entity):
    def __init__(self, x=0, y=0):
        super().__init__(filename=r'./robot.png', x=x,y=y) # ,
        R = math.sqrt((HEIGHT/2)**2 + (WIDTH/2)**2) + math.sqrt(2)*self.rect.width
        angle = rnd.random()*2*math.pi
        self.rect.x = WIDTH/2 + math.cos(angle)*R
        self.rect.y = HEIGHT/2 + math.sin(angle)*R
        self.speed = 0.1

    def movement(self, player):
        x, y = self.rect.center[0] - player.rect.center[0], self.rect.center[1] - player.rect.center[1]
        cos_a = -x / math.sqrt(x**2 + y**2)
        sin_a = -y / math.sqrt(x**2 + y**2)
        super().movement((self.speed+5*(1000/(1000 + abs(x))))*cos_a, (self.speed+5*(1000/(1000 + abs(y))))*sin_a)   
    
class Bullet(Entity):
    def __init__(self, player, mouse_pos):  
        self.start_x, self.start_y = player.rect.center
        super().__init__(self.start_x, self.start_y)
        self.img.fill((255,255,0))
        x, y = self.start_x - mouse_pos[0], self.start_y - mouse_pos[1]

        temp_x = x*rnd.uniform(0.9, 1.1) if x != 0 else rnd.random()
        temp_y = y*rnd.uniform(0.9, 1.1) if y != 0 else rnd.random()
        cos_a = (temp_x)/max((math.sqrt(x**2 + y**2)), 1)
        sin_a = (temp_y)/max((math.sqrt(x**2 + y**2)), 1)


        self.s_x = 10 * -cos_a 
        self.s_y = 10 * -sin_a 
    
    def movement(self):
        super().movement(self.s_x, self.s_y)
        if not (0 < self.rect.x < WIDTH) or not(0 < self.rect.y < HEIGHT):
            return False
        return True

class Coin(Entity):
    def __init__(self, x, y, clock):
        super().__init__(filename=r"coin.png", x=x, y=y)
        self.timer = 0

    def lifespan(self) -> bool:
        self.timer += 1
        if self.timer > 50:
            return True

class Num_of_points():
    def __init__(self, num=0):
        self.num_of_points = num

    def __iadd__(self, num):
        return Num_of_points(self.num_of_points + num)

    def __lt__(self, other):
        return self.num_of_points < other
    
    def __str__(self):
        return f"{self.num_of_points}"

class info_window():
    def __init__(self, left_side, right_side, screen, score):
        self.font = pg.font.SysFont("Times New Roman", 20)
        self.info_field = pg.Surface((right_side-left_side, screen.get_height()))  
        self.rect_info_field = self.info_field.get_rect(topleft=(left_side, 0))
        self.screen = screen
        self.rect_text = pg.Rect((self.rect_info_field.left + 10, 10), (self.rect_info_field.width - 20, self.rect_info_field.height/2))
        self.score = score

    def drawing(self):
        global score
        info = f"SCORE : {score}, Controll:, 1. W - top, 2. A - left, 3. D - right, 4. S - down, 5. Fire - LMB".split(',')
        info += ['', "ESC - exit, Space - pause", "Get 1000 points, good luck!"]
        info_text = [self.font.render(el, True, (255, 0, 0)) for el in info]
        
        self.screen.blit(self.info_field, self.rect_info_field)
        for i, el in enumerate(info_text):
            self.screen.blit(el, (self.rect_text.left, self.rect_text.top + i*20))
        
    def pause(self):
        text = self.font.render("PAUSE", True, (255, 0, 0), (0,0,0))
        screen.blit(text, (HEIGHT>>1, WIDTH>>1))
        pg.display.flip()

    def death(self):
        raw_text = ['This is the end of game!', 'Thnx for playing!', f"YOUR SCORE: {score}", "For RESTART press R"]
        font = pg.font.SysFont("Times New Roman", 30)
        for i in range(len(raw_text)):
            text = font.render(raw_text[i], True, (255, 0, 0), (0,0,0))
            screen.blit(text, ((HEIGHT>>1)-i*100, (WIDTH>>1) + i*30))
        pg.display.flip()
        pass

    def congrats(self):
        raw_text = ['This is the end of game!', 'Thnx for playing!', f"YЩГ'VE REACHED THE GOAL!!!", "GAME WILL END AUTOMATICALLY"]
        font = pg.font.SysFont("Times New Roman", 30)
        for i in range(len(raw_text)):
            text = font.render(raw_text[i], True, (255, 255, 0), (0,0,0))
            screen.blit(text, ((HEIGHT>>1)-i*100, (WIDTH>>1) + i*30))
        pg.display.flip()
        pg.time.wait(3000)
    
class game_handler():   
    def __init__(self):
        pg.init()
        self.ghost = Player(x=WIDTH/2, y=HEIGHT/2)
        self.clock = pg.time.Clock()
        self.info = info_window(WIDTH, WIDTH_2, screen, score)
        self.table_enemy = []
        self.table_bullet = []
        self.table_coins = []
        self.pause_flag = True
        self.death_flag = False
    
    def execute(self):
        global score
        while True and score < 1001:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYUP and event.key == pg.K_SPACE:
                    self.pause_flag = not self.pause_flag
                if event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                    exit()
                if event.type == pg.KEYUP and event.key == pg.K_r:
                    self.death_flag = False
                    return True
            
            self.clock.tick(60)
            if self.death_flag:
                self.info.death()
                continue

            if not self.pause_flag:
                self.info.pause()
                continue    
            prs_keys = pg.key.get_pressed()
            if prs_keys[pg.K_LEFT] or prs_keys[pg.K_a]:
                self.ghost.movement(s_x=-self.ghost.speed)
            if prs_keys[pg.K_RIGHT] or prs_keys[pg.K_d]:
                self.ghost.movement(s_x=self.ghost.speed)
            if prs_keys[pg.K_DOWN] or prs_keys[pg.K_s]:
                self.ghost.movement(s_y=self.ghost.speed)
            if prs_keys[pg.K_UP] or  prs_keys[pg.K_w]:
                self.ghost.movement(s_y=-self.ghost.speed)

            timer = pg.time.get_ticks()
            if rnd.random() > .95 / math.exp(timer*0.000005):
                self.table_enemy.append(Enemy())

            if pg.mouse.get_pressed()[0]:
                self.table_bullet.append(Bullet(self.ghost, pg.mouse.get_pos()))           
            
            for ind, enemy in enumerate(self.table_enemy):
                enemy.movement(self.ghost)
                if enemy.collide(self.ghost):
                    #self.info.death()
                    #self.death_flag = True
                    del self.table_enemy[ind]

            for i, bullet in enumerate(self.table_bullet):
                if bullet.movement():
                    for j, enemy in enumerate(self.table_enemy):
                        if bullet.collide(enemy):
                            self.table_coins.append(Coin(enemy.rect.x, enemy.rect.y, self.clock))
                            del self.table_enemy[j]
                            del self.table_bullet[i]
                            score += 1
                else:
                    del self.table_bullet[i]

            for i, coin in enumerate(self.table_coins):
                if coin.collide(self.ghost):
                    del self.table_coins[i]
                    score += 5
                elif coin.lifespan():
                    del self.table_coins[i]
            
            screen.fill((40, 40, 40))
            for el in self.table_coins:
                el.drawing(screen)
            for el in self.table_enemy:
                el.drawing(screen)
            for el in self.table_bullet:
                el.drawing(screen)
            self.ghost.drawing(screen)
            self.info.drawing()
            pg.display.flip()
        
        self.info.congrats()
        exit()
        

WIDTH, HEIGHT = 1000, 1000
WIDTH_2 = WIDTH + 400
score = Num_of_points()
screen = pg.display.set_mode((WIDTH_2, HEIGHT))  

game = game_handler()
while True:
    score = Num_of_points()
    game = game_handler()
    game.execute()
    continue