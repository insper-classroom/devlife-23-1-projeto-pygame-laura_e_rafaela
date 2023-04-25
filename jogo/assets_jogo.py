import pygame 

class Player(pygame.sprite.Sprite):

    def __init__(self,window, tela_jogo):
        pygame.sprite.Sprite.__init__(self)
        self.window=window
        self.indice_img=0
        self.images_animation=['jogo/Assets_jogo/Gingerman/gingerman_1.png','jogo/Assets_jogo/Gingerman/gingerman_2.png','jogo/Assets_jogo/Gingerman/gingerman_3.png','jogo/Assets_jogo/Gingerman/gingerman_4.png']
        image=pygame.image.load(self.images_animation[self.indice_img])
        self.image=pygame.transform.scale(image, (60,60))
        self.vidas=2
        self.h=self.image.get_height()
        self.radius=(self.h)/5
        self.last_updated=0
        self.rect=self.image.get_rect()
        self.rect.x=50
        self.rect.y=420
        self.pulo = False
        self.vel_y = 0
        self.ace = 500
        self.tela_jogo = tela_jogo
        self.t0 = 0
        self.chao=420
        self.fonte=pygame.font.Font('jogo/Assets_jogo/fontes/OnlineWebFonts_COM_2486b26012f1198dc8c84cbf5c960f98/font_jogo/PressStart2P.ttf')
        cookie=pygame.image.load('jogo/Assets_jogo/biscoitos/biscoito_redondo.png')
        self.cookie=pygame.transform.scale(cookie,(20,20))
        self.cookies_coletados=0

    def update(self,all_biscoitos,all_plataformas):
        tempo_frame = pygame.time.get_ticks()
        dt = (tempo_frame - self.t0)/1000
        self.t0 = tempo_frame
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                return -1 
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and not self.pulo:
                    self.pulo = True
                    self.vel_y=-450
                    image=pygame.image.load(self.images_animation[2])
                    self.image=pygame.transform.scale(image, (60,60))
                if evento.key == pygame.K_DOWN and self.pulo and self.vel_y<0:
                    self.vel_y*=-1

        #verifica se ele está na plataforma
        plataforma = self.esta_na_plataforma(all_plataformas)
        if plataforma and self.vel_y>0:
                self.chao=248
        else:
            self.chao=420 
        self.vel_y += self.ace * dt
        self.rect.y += self.vel_y * dt

        #barreira pro boneco não atravessar o chão
        if self.rect.y >= self.chao:
            self.rect.y=self.chao
            self.pulo=False
            self.vel=0
        self.pegou_biscoito(all_biscoitos,self)

        if not(self.pulo):
            self.indice_img=(self.indice_img+1)%2
            image=pygame.image.load(self.images_animation[self.indice_img])
            self.image=pygame.transform.scale(image, (60,60))
        
        elif self.vel_y<0:
            image=pygame.image.load(self.images_animation[2])
            self.image=pygame.transform.scale(image, (60,60))

        elif self.vel_y>0:
            image=pygame.image.load(self.images_animation[3])
            self.image=pygame.transform.scale(image, (60,60))
        all_biscoitos.update(True)
        all_plataformas.update(True)
        return True
            
    def desenha(self):
        self.window.blit(self.image,self.rect)
        desenho_coracoes=self.fonte.render(chr(9829)*self.vidas,True,(255,0,0))
        self.window.blit(desenho_coracoes,(0,0))
        desenho_cookies=self.fonte.render(f' x {self.cookies_coletados}',True,(0,0,0))
        self.window.blit(desenho_cookies,(1202,5))
        self.window.blit(self.cookie,(1195,1))
        pygame.display.update()

    def pegou_biscoito(self,biscoitos,player):
        if pygame.sprite.spritecollideany(self,biscoitos)==None:
                return False
        else:
            player.cookies_coletados+=1
            pygame.sprite.spritecollideany(self,biscoitos).kill()
            return True
    
    def esta_na_plataforma(self,all_plataformas):
        return pygame.sprite.spritecollideany(self,all_plataformas)

class Biscoito(pygame.sprite.Sprite):

    def __init__(self, window,y, x):
        pygame.sprite.Sprite.__init__(self)
        self.window=window
        image=pygame.image.load('jogo/Assets_jogo/biscoitos/biscoito_redondo.png')
        self.image=pygame.transform.scale(image, (30,30))
        self.h=self.image.get_height()
        self.radius=(self.h)/2
        self.last_updated=0
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.last_updated=0
        self.vel=-120

    def update(self,mexendo):
        v1=pygame.time.get_ticks()
        if mexendo:
            delta_t=(v1-self.last_updated)/1000
            self.last_updated=v1 
            self.rect.x=self.rect.x+(self.vel*delta_t)
        self.last_updated=v1
        
    def draw(self):
        self.window.blit(self.image,self.rect)


class Monstro(pygame.sprite.Sprite):

    def __init__(self,window):
        pygame.sprite.Sprite.__init__(self)
        self.window=window
        self.indice_img=0
        self.images_animation=[]
        image=pygame.image.load(self.images_animation[self.indice_img])
        self.image=pygame.transform.scale(image, (80,80))
        self.vidas=1
        self.h=self.image.get_height()
        self.radius=(self.h)/2
        self.last_updated=0
        self.rect=self.image.get_rect()
        self.rect.x=500
        self.rect.y=520

    def update(self):
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                return -1 
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_d] or tecla[pygame.K_RIGHT]:
            self.indice_img=(self.indice_img+1)%len(self.images_animation)
            image=pygame.image.load(self.images_animation[self.indice_img])
            self.image=pygame.transform.scale(image, (80,80))
        
        
    def desenha(self):
        self.window.blit(self.image,self.rect)

class Plataforma (pygame.sprite.Sprite):
    def __init__(self, x, width,window):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("jogo/Assets_jogo/snow_ground.png")
        self.image = pygame.transform.scale(image, (80,60))
        self.h=20
        self.x=x
        self.y=300
        self.width = width
        self.rect =pygame.Rect(self.x+15,self.y,self.width+40,self.h)
        self.window=window
        self.last_updated=0
        self.vel=-120
        self.radius=self.h/2

    def draw(self):
        self.window.blit(self.image, self.rect.y)

    def update(self,mexendo):
        v1=pygame.time.get_ticks()
        if mexendo:
            delta_t=(v1-self.last_updated)/1000
            self.last_updated=v1 
            self.rect.x=self.rect.x+(self.vel*delta_t)
        self.last_updated=v1
