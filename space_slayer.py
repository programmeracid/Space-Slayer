import pygame, sys, random, math

pygame.font.init()
pygame.init()



WIDTH, HEIGHT = 1280,720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
dif = 0
pygame.display.set_caption("Space Slayer")
playerimg = pygame.transform.scale(pygame.image.load('imgs\\player.png'), (100,100))
playbimg = pygame.image.load('imgs\\playbut.png')
optbimg = pygame.transform.scale(pygame.image.load('imgs\\how.png'),(268,61))
bgimg = pygame.image.load('imgs\\bg.jpg')
enemyimg =  pygame.transform.scale(pygame.image.load('imgs\\enemy.png'),(50,50))
playerbulletimg =  pygame.transform.scale(pygame.image.load('imgs\\bullet.png'),(10,10))
enemyrocketimg =  pygame.transform.scale(pygame.image.load('imgs\\erocket.png'),(20,20))
enemybulletimg =  pygame.transform.scale(pygame.image.load('imgs\\enemybullet.png'),(10,10))
healthimg = pygame.transform.scale(pygame.image.load('imgs\\health.png'), (40,40))
instimg = pygame.image.load('imgs\\inst.png')
backimg =  pygame.transform.scale(pygame.image.load('imgs\\back.png'),(64,48))
easyimg = pygame.image.load('imgs\\Easy.png')
normalimg = pygame.image.load('imgs\\Normal.png')
hardimg = pygame.image.load('imgs\\Hard.png')
crosshairimg = pygame.transform.scale(pygame.image.load('imgs\\crosshair.png'),(15,15))
chodifimg = pygame.transform.scale(pygame.image.load('imgs\\Choose Difficulty.png'),(368,61))
seleasyimg = pygame.transform.scale(pygame.image.load('imgs\\Seleasy.png'),(526,61))
selnormalimg = pygame.transform.scale(pygame.image.load('imgs\\Selnormal.png'),(589,61))
selhardimg = pygame.transform.scale(pygame.image.load('imgs\\Selhard.png'),(521,61))
objectimg =  pygame.transform.scale(pygame.image.load('imgs\\object.png'),(100,100))
objectimg =  pygame.transform.rotate(objectimg,180)
bsnd = pygame.mixer.Sound('Sounds\\button.mp3')
ebsnd = pygame.mixer.Sound('Sounds\\enemybullet.mp3')
ersnd = pygame.mixer.Sound('Sounds\\enemyrocket.mp3')
exsnd = pygame.mixer.Sound('Sounds\\explosion.mp3')
hlsnd = pygame.mixer.Sound('Sounds\\health.mp3')
colsnd = pygame.mixer.Sound('Sounds\\collision.mp3')
col1snd = pygame.mixer.Sound('Sounds\\collision1.mp3')
pygame.display.set_icon(playerimg)
pygame.mixer.set_num_channels(200)

class Button(pygame.sprite.Sprite):
                def __init__(self,x,y,image) :
                                super().__init__()
                                self.image = image
                                self.rect = self.image.get_rect(center = (x,y))
                                
                                self.clicked = False ; self.action = False
                def update(self) :
                                self.action = False
                                pos = pygame.mouse.get_pos()
                                if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == True  and self.clicked == False:
                                        self.clicked = True
                                        self.action = True
                                        
                                        
                                if pygame.mouse.get_pressed()[0] == False :
                                        self.clicked = False
                                WIN.blit(self.image,(self.rect.x, self.rect.y))

def main():
        

        LEVEL = 1 + dif
        gameLEVEL = LEVEL - dif
        
        
        class Player(pygame.sprite.Sprite):
                vel = (HEIGHT/120)
                livesleft = 3
                hits = 0
                def __init__(self) :
                        super().__init__()
                        self.image = playerimg
                        self.rect = self.image.get_rect(center = (WIDTH/2, HEIGHT/2))
                        self.health = 200
                        self.flag = 1
                        self.respawntime = -FPS*2
                        self.invinc = False
                        self.color = (0,255,0)
                        
                        
                def update(self) :
                        
                        self.dy  = 0
                        self.dx = 0
                        ks = pygame.key.get_pressed()      #keystate
                        if ks[pygame.K_w] and self.rect.y - self.vel > 0:
                                self.dy = -self.vel
                        if ks[pygame.K_a] and self.rect.x - self.vel > 0 :
                                self.dx = -self.vel
                        if ks[pygame.K_s] and self.rect.y + self.rect.height + self.vel + 16 < HEIGHT:
                                self.dy = +self.vel
                        if ks[pygame.K_d] and self.rect.x + self.rect.width + self.vel < WIDTH :
                                self.dx = +self.vel
                        self.rect.x += self.dx
                        self.rect.y += self.dy
                        self.respawn_msg()
                        self.health_bar()
                        self.invincibility()
                                
                def respawn_msg(self) :
                        
                        if ticks < self.respawntime + FPS*2 and not lost :
                                respawn_label = dispmsg_font.render("Respawned", 1, (255,255,255))
                                WIN.blit(respawn_label,(WIDTH/2-20,HEIGHT - 50))
                        
                                    
                def create_bullet(self) :
                        pbsnd = pygame.mixer.Sound('Sounds\\playerbullet.mp3')
                        pbsnd.play()
                        return Bullet(self.rect.centerx,self.rect.centery)

                def givexy(self) :
                        
                        return self.rect.centerx, self.rect.centery
                
                def life(self,amount) :
                        
                        if self.invinc == False :
                                self.health += amount
                                
                                if self.health <= 0 :
                                        self.respawn()
                                        self.livesleft -= 1
                                        
                def health_bar(self) :
                        
                        self.bar = pygame.Surface((self.health*2,10))
                        if self.health> 100 : self.color = (0,255,0)
                        elif 50<self.health<100 : self.color = (255,255,0)
                        elif self.health<50 : self.color = (255,0,0)
                        self.bar.fill(self.color)
                        WIN.blit(self.bar,((WIDTH - self.health*2)/2,20))
                        
                def respawn(self) :
                        self.rect.centerx = WIDTH
                        self.rect.centery = HEIGHT/2
                        self.health = 200
                        self.respawntime = ticks
                        self.invinc = True
                def invincibility(self) :
                        
                        if self.respawntime + FPS * 3 < ticks :
                                self.invinc = False
                        if self.invinc == True :
                                invins_label = dispmsg_font.render("Invinicibility On for "+str(int((self.respawntime - ticks+ FPS*3)/FPS + 1)) + ' s', 1, (255,255,255))
                                WIN.blit(invins_label,(WIDTH/2-20,HEIGHT - 70))
                                
                        
                

        class Bullet(pygame.sprite.Sprite) :
               
                def __init__(self,px,py) :
                        
                        super().__init__()
                        self.bs = (HEIGHT/24) + LEVEL*5
                        mx,my = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
                        self.image = playerbulletimg
                        self.rect = self.image.get_rect(center = (px,py))
                        self.angle = math.atan2(my - py,mx-px)                   
                        self.dx = math.cos(self.angle)*self.bs
                        self.dy = math.sin(self.angle)*self.bs
                        

                        
                def update(self) :
                        
                        self.rect.x += self.dx
                        self.rect.y += self.dy
                        if self.rect.x >= WIDTH :
                                self.kill()
                        elif self.rect.y >= HEIGHT:
                                self.kill()


        class EnemyBullet(pygame.sprite.Sprite):
                
                
                def __init__(self,ex,ey,tx,ty) :
                        
                        super().__init__()
                        self.image = enemybulletimg
                        self.ebs  = HEIGHT/144 + LEVEL*0.5
                        self.rect = self.image.get_rect(center = (ex,ey))
                        self.angle = math.atan2(ty - ey,tx-ex)
                        self.dx = math.cos(self.angle)*self.ebs
                        self.dy = math.sin(self.angle)*self.ebs
                        
                def update(self) :
                        
                        self.rect.x += self.dx
                        self.rect.y += self.dy
                        if self.rect.x >= WIDTH:
                                self.kill() 
                        elif self.rect.y >= HEIGHT :
                                self.kill()
        class EnemyRocket(pygame.sprite.Sprite) :
                
                def __init__(self,ex,ey,tx,ty) :
                        super().__init__()
                        self.image = enemyrocketimg
                        self.ers  = HEIGHT/160 + LEVEL*0.5
                        self.rect = self.image.get_rect(center = (ex,ey))
                        self.angle = math.atan2(ty - ey,tx-ex)
                        self.dx = math.cos(self.angle)*self.ers
                        self.dy = math.sin(self.angle)*self.ers
                def update(self) :
                        
                        self.rect.x += self.dx
                        self.rect.y += self.dy
                        if self.rect.x >= WIDTH:
                                self.kill() 
                        elif self.rect.y >= HEIGHT :
                                self.kill()
                        
                        
        class Enemy(pygame.sprite.Sprite) :
                
                
                
                def __init__(self) :

                        super().__init__()
                        self.image = enemyimg
                        self.rect = self.image.get_rect(center = (random.randint(-WIDTH,0),random.randint(0,HEIGHT)))
                        self.health = LEVEL /2
                        self.target = 'not fixed'
                        self.dx = 0
                        self.dy = 0
                        self.d = 3 + LEVEL * 0.2
                        self.msgtime = ticks
                        self.ticks = 0
                        self.rticks = 0
                        self.invisflag = False
                        self.invistime = 0
                        
                        
                def update(self) :
                         
                        self.create_enemy_bullet()
                        self.create_enemy_rocket()
                        
                        if self.target != 'fixed' :
                                self.getxy(0,0,WIDTH,HEIGHT)        
                        elif self.target == 'fixed' :
                                self.angle = math.atan2(self.my - self.rect.centery,self.mx-self.rect.centerx)
                                self.dx = math.cos(self.angle)*self.d
                                self.dy = math.sin(self.angle)*self.d
                                self.rect.centerx += self.dx
                                self.rect.centery += self.dy
                                x,y = self.rect.centerx, self.rect.centery
                                if abs(self.mx - x) < 5 and abs(self.my - y) < 5 :
                                        self.target = 'not fixed'
                                if self.msgtime != 0 :
                                        self.display_msg()
                                if LEVEL > 6 :
                                        self.invisible()
                
                def getxy(self,startx ,starty , endx, endy) :
                        
                        if startx > endx :
                                startx,endx = endx, startx 
                        if starty > endy :
                                starty,endy = endy, starty 
                        
                        self.mx,self.my = random.randint(startx,endx),random.randint(starty,endy)
                        self.target = 'fixed'
                
                def collided(self) :
                        
                        if self.dx >= 0 :
                                self.xdir = 'right'
                                self.tolx = -3 
                        else :
                                self.xdir = 'left'
                                self.tolx = 3 
                        if self.dy >= 0 :
                                self.ydir = 'down'
                                self.toly = -3 
                        else :
                                self.ydir = 'up'
                                self.toly = 3  

                        if self.xdir == 'right' :
                                self.endx = 0
                        else :
                                self.endx = WIDTH
                        if self.ydir == 'down' :
                                self.endy = 0
                        else :
                                self.endy = HEIGHT
                        
                        
                        E.getxy(self.rect.centerx + self.tolx ,self.rect.centery + self.toly,self.endx,self.endy)
                        
                def life(self,hitter) :
                        if hitter == 'player' : exsnd.play()
                        self.health -= 1
                        if self.health <= 0 :
                                
                                self.kill()
                                enemy_group.add(Enemy())
                                if hitter == 'player' :
                                        nonlocal killcount
                                        killcount += 1
                                
                def create_enemy_bullet(self) :
                        
                        self.ticks += 1
                        if self.ticks % 10 == 0 and self.ticks >= 180 :
                                ebsnd.play()
                                Ebullet_group.add(EnemyBullet(self.rect.centerx, self.rect.centery,player.rect.centerx, player.rect.centery))
                        if self.ticks > 200 :
                                self.ticks = 0
                        
                        
                def create_enemy_rocket(self) :
                        
                        self.rticks += 1
                        if self.rticks == 300 :
                                self.rticks = 0
                                ersnd.play()
                                Erocket_group.add(EnemyRocket(self.rect.centerx, self.rect.centery,player.rect.centerx, player.rect.centery))
                                
                def display_msg(self) :
                        
                        if (self.msgtime + FPS*2) > ticks : 
                                label = dispmsg_font.render('Enemy Killed x'+str(killcount), 1, (255,255,255))
                                WIN.blit(label,(WIDTH/2-20,HEIGHT - 30))
                                
                def invisible(self) :
                        
                        if self.invisflag == False :
                                self.invistime = random.randint(ticks,ticks+FPS*20)
                                self.invisflag = True
                                
                        if self.invistime + FPS * 2> ticks :
                                if self.invistime < ticks :
                                        self.image = pygame.Surface((50,50))
                                        self.rect = self.image.get_rect(center = (self.rect.centerx,self.rect.centery))
                                        
                        else :
                                self.invisflag = False
                                self.image = enemyimg
                                self.rect = self.image.get_rect(center = (self.rect.centerx,self.rect.centery))
                                


        class Object(pygame.sprite.Sprite) :
                
                def __init__(self) :
                        
                        super().__init__()
                        self.image = objectimg
                        self.rect = self.image.get_rect(center = (random.randint(0,WIDTH),random.randint(HEIGHT,HEIGHT*2)))
                        
                def update(self) :
                        
                        self.rect.centery -= 2
                        if self.rect.centery < -100 :
                                self.kill()
                                object_group.add(Object())
                                
    

        class Health(pygame.sprite.Sprite) :
                
                def __init__(self) :
                        
                        super().__init__()
                        self.image = healthimg
                        self.rect = self.image.get_rect(center = (random.randint(0,WIDTH),random.randint(0,HEIGHT)))


        run = True

        FPS = 60
        ticks = 0
        gametime = 0
        main_font = pygame.font.SysFont("candara", 40)
        lost_font = pygame.font.SysFont("candara", 60)
        dispmsg_font = pygame.font.SysFont("comicsans", 15)

        lost = False
        lost_count = 0
        killcount = 0

        player = Player()
        backb = Button(WIDTH/2,HEIGHT-60,backimg)

        player_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        bullet_group = pygame.sprite.Group()
        object_group = pygame.sprite.Group()
        Ebullet_group = pygame.sprite.Group()
        Erocket_group = pygame.sprite.Group()
        health_group = pygame.sprite.Group()
        button_group = pygame.sprite.Group()
        player_group.add(player)
        health_group.add(Health())
        button_group.add(backb)

        for i in range(2):
                enemy_group.add(Enemy())
                object_group.add(Object())
        

        clock = pygame.time.Clock()
        HEALTH_FONT = pygame.font.SysFont('comicsans', 10)
        size = 70 ; add = 1


        def mouse() :
                
                pygame.mouse.set_visible(False)
                x,y = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
                WIN.blit(crosshairimg,(x,y))
                
        def over_text() :
                
                nonlocal size,add
                over_font = pygame.font.SysFont("candara", int(size))
                over_label = over_font.render('GAME OVER',1,(0,50,255))
                WIN.blit(over_label,(WIDTH/2 - over_label.get_width()/2,350))
                size += add
                if size >= 80 or size <= 60 : add*=-1

        def music() :
                pygame.mixer.music.load('Sounds\\easybg.mp3')
                pygame.mixer.music.play(-1)
            
                
                                    
        def redraw_window():
                
                nonlocal gametime, killcount
                WIN.blit(bgimg, (0,0))
                if not lost :
                        bullet_group.draw(WIN)
                        Ebullet_group.draw(WIN)
                        Erocket_group.draw(WIN)
                        health_group.draw(WIN)
                        enemy_group.draw(WIN)
                        player_group.draw(WIN)
                        object_group.draw(WIN)
                        

                        player_group.update()
                        Ebullet_group.update()
                        Erocket_group.update()
                        enemy_group.update()
                        bullet_group.update()
                        
                        
                        lives_label = main_font.render(f"Lives: {player.livesleft}", 1, (255,5,25))
                        level_label = main_font.render("Wave: "+str(gameLEVEL), 1, (20,10,255))
                        time_label = main_font.render('Time : '+str(gametime),1,(255,255,0))
                        kills_label = main_font.render(' Kills : '+str(killcount),1,(20,255,25))
                        player_health_label = HEALTH_FONT.render("Health: " + str(int(player.health)), 1, (255,255,255))

                        WIN.blit(lives_label, (40, 30))
                        WIN.blit(level_label, (WIDTH - 170, 80))
                        WIN.blit(time_label,(40 ,80))
                        WIN.blit(kills_label,(WIDTH - 170,30))
                        WIN.blit(player_health_label,(player.rect.x + 15,player.rect.y +85))
                        mouse()
                
                if lost:
                    
                    pygame.mouse.set_visible(True)
                    score = gametime*10 + killcount*40
                    button_group.update()
                    over_text()
                    time_label = lost_font.render("You survived for " + str(gametime) + ' seconds!', 1, (25,255,25))
                    score_label = lost_font.render("FINAL SCORE : "+str(score), 1, (255,255,0))
                    
                    WIN.blit(time_label, (WIDTH/2 - time_label.get_width()/2, 450))
                    WIN.blit(score_label, (WIDTH/2 - score_label.get_width()/2, 550))
                    button_group.draw(WIN)
                    if backb.action :
                            nonlocal run
                            run = False
                    
                    player.vel = 0
                    
                elif gametime != int(ticks/FPS) :
                        gametime += 1
                        
                
                pygame.display.flip()              
        music()
        
        #Game Loop
        
        while run :
                
                clock.tick(FPS)
                redraw_window()
                

                if player.livesleft <= 0:
                        lost = True
                        
                for event in pygame.event.get() :
                        if event.type == pygame.QUIT :
                                pygame.quit()
                                sys.exit()
                                
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                                bullet_group.add(player.create_bullet())
                
         
                #Collision detection for loops for sprites
                                
                if len(object_group) < 2 : object_group.add(Object())        
                for E in enemy_group :
                        sprite_hits = pygame.sprite.spritecollide(E,bullet_group,True)     #Enemy and Player Bullet
                        for hit in sprite_hits :
                                E.life('player')
                                player.hits += 1
                old_LEVEL = LEVEL                
                LEVEL = dif + player.hits//10 + 1
                gameLEVEL = LEVEL - dif 
                if old_LEVEL != LEVEL  and gameLEVEL % 5 == 0 : 
                   enemy_group.add(Enemy())
                   object_group.add(Object())
                
                sprite_hits = pygame.sprite.spritecollide(player,health_group,True)             #Health kit and Player
                if sprite_hits : player.life(random.randrange(20,50,5)) ; hlsnd.play()
                        
                for O in object_group :                                                                  
                        sprite_hits = pygame.sprite.spritecollide(O,bullet_group,True)            # object and  player bullet
                for O in object_group : 
                        sprite_hits = pygame.sprite.spritecollide(O,Ebullet_group,True)          # object and enemy bullet
                for E in enemy_group :
                        for O in object_group :
                                sprite_hits = pygame.sprite.collide_rect(E,O)                           #enemy and object
                                if sprite_hits :
                                        E.life('object')
                                        E.collided()      
                                else :  O.update()
                                
                sprite_hits = pygame.sprite.spritecollide(player,Ebullet_group,True)           #player and enemy bullet
                if sprite_hits :
                        player.life(-(LEVEL*2.5))                                                              ##Enemy bullet damage increases with level'''
                        col1snd.play()
                sprite_hits = pygame.sprite.spritecollide(player,Erocket_group,True)           #player and enemy rocket
                if sprite_hits :
                        player.life(-(LEVEL*5))
                        colsnd.play()
                for O in object_group :
                        sprite_hits = pygame.sprite.spritecollide(O,player_group,False)           #player and object
                        if sprite_hits :
                                player.life(-(LEVEL*10))
                                colsnd.play()
                                O.kill()
                ticks += 1
                if ticks % 1000 == 0 : health_group.add(Health())
        pygame.mixer.music.stop()           

def main_menu():
        
        
        
        def title_text() :
                
                nonlocal size,add
                title_font = pygame.font.SysFont("candara", int(size))
                title_label = title_font.render('SPACE SLAYER',1,(0,255,255))
                WIN.blit(title_label,(WIDTH/2 - title_label.get_width()/2,200))
                size += add
                if size >= 80 or size <= 60 :
                        add*=-1



                
        playb = Button(WIDTH/2,HEIGHT/2,playbimg)
        optb = Button(WIDTH/2, HEIGHT/2 + 125, optbimg)
        difb = Button(WIDTH/2, HEIGHT/2 + 200, chodifimg)
        button_group = pygame.sprite.Group()
        button_group.add(playb)
        button_group.add(optb)
        button_group.add(difb)
        sub_font = pygame.font.SysFont('comicsans',20)
        dev_label = sub_font.render('Developed using Python',1,(255,255,255))
        game_label = sub_font.render('A Space Themed Shooter Game',1,(255,255,255))
        pygame.mixer.music.load('Sounds\\bgmusic.mp3')
        pygame.mixer.music.play(-1)
        
        size = 70;add = 0.2
        run = True
        while run:
                WIN.blit(bgimg, (0,0))
                WIN.blit(dev_label,(WIDTH - dev_label.get_width() - 10, HEIGHT - 50))
                WIN.blit(game_label,(10, HEIGHT - 50))
                
                if dif == 0 :
                        WIN.blit(seleasyimg,(int(WIDTH/2 - seleasyimg.get_width()/2), HEIGHT-100))
                if dif == 3 :
                        WIN.blit(selnormalimg,(int(WIDTH/2 - selnormalimg.get_width()/2), HEIGHT-100))
                if dif == 6 :
                        WIN.blit(selhardimg,(int(WIDTH/2 - selhardimg.get_width()/2), HEIGHT-100))
                        
                title_text()
                
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                button_group.update()
                button_group.draw(WIN)
                if playb.action :
                        bsnd.play()
                        pygame.mixer.music.unload()
                        main()
                        pygame.mixer.music.load('Sounds\\bgmusic.mp3')
                        pygame.mixer.music.play(-1)
                        bsnd.play()
                if optb.action :
                        bsnd.play()
                        instructions()
                        bsnd.play()
                if difb.action :
                        bsnd.play()
                        choose_difficulty()
                        bsnd.play()
                pygame.display.update()        
        pygame.quit()


def instructions() :
        
        backb = Button(WIDTH/2,HEIGHT-50,backimg)
        button_group = pygame.sprite.Group()
        button_group.add(backb)
        run = True
        while run :
                
                WIN.blit(bgimg,(0,0))
                
                for event in pygame.event.get() :
                        if event.type == pygame.QUIT :
                                pygame.quit()
                                sys.exit()
                
                WIN.blit(bgimg,(0,0))
                WIN.blit(instimg,(WIDTH/2 - instimg.get_width()/2,HEIGHT/2 - instimg.get_height()/2))
                button_group.draw(WIN)
                button_group.update()
                

                pygame.display.update()
                if backb.action :
                        run = False
                

def choose_difficulty() :
        
        easyb = Button(WIDTH/2 + 300,HEIGHT/4,easyimg)
        normalb = Button(WIDTH/2 + 300,HEIGHT*2/4,normalimg)
        hardb = Button(WIDTH/2+ 300,HEIGHT*3/4,hardimg)
        button_group = pygame.sprite.Group()
        button_group.add(easyb)
        button_group.add(normalb)
        button_group.add(hardb)
        
        run = True
        global dif
        while run :
                
                for event in pygame.event.get() :
                        if event.type == pygame.QUIT :
                                pygame.quit()
                                sys.exit()
                                
                WIN.blit(bgimg,(0,0))
                WIN.blit(playerimg,(300,HEIGHT/2 - playerimg.get_height()/2))
                WIN.blit(enemyimg,(500,HEIGHT/2 - enemyimg.get_height()/2))
                WIN.blit(objectimg,(400,HEIGHT - 200))
                button_group.draw(WIN)
                button_group.update()
                if easyb.action :
                        dif = 0 ; run = False
                elif normalb.action :
                        dif = 3 ; run = False
                elif hardb.action :
                        dif = 6 ; run = False

                pygame.display.update()
                
        
main_menu()


