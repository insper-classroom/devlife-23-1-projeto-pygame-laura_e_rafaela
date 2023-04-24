import pygame 

class Player(pygame.sprite.Sprite):

    def __init__(self,window, tela_jogo):
        pygame.sprite.Sprite.__init__(self)
        self.window=window
        self.indice_img=0
        self.images_animation=['jogo/Assets_jogo/Gingerman/gingerman_1.png','jogo/Assets_jogo/Gingerman/gingerman_2.png']
        image=pygame.image.load(self.images_animation[self.indice_img])
        self.image=pygame.transform.scale(image, (60,60))
        self.vidas=2
        self.h=self.image.get_height()
        self.radius=(self.h)/2
        self.last_updated=0
        self.rect=self.image.get_rect()
        self.rect.x=50
        self.rect.y=420
        self.pulo = False
        self.vel_y = 0
        self.ace = 1
        self.tela_jogo = tela_jogo
        self.t0 = 0

    def update(self,all_biscoitos,all_plataformas):
        tempo_frame = pygame.time.get_ticks()
        dt = (tempo_frame - self.t0)/1000
        self.t0 = tempo_frame
        self.vel_y += self.ace * dt
        self.rect.y += self.vel_y * dt
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                return -1 
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                self.pulo = True
        if self.rect.y >=420:
            self.rect.y=420
        if self.rect.y >= 420 and self.pulo:
            self.vel_y=-400
            self.pulo = False
        if self.rect.y <= 250:
            self.vel_y = 400
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_d] or tecla[pygame.K_RIGHT]: 
            self.indice_img=(self.indice_img+1)%2
            image=pygame.image.load(self.images_animation[self.indice_img])
            self.image=pygame.transform.scale(image, (60,60))
            self.pegou_biscoito(all_biscoitos)
            all_biscoitos.update(True)
            all_plataformas.update(True)
            return True 
        all_biscoitos.update(False)
        all_plataformas.update(False)
        return False
            
    def desenha(self):
        self.window.blit(self.image,self.rect)
        pygame.display.update()

    def pegou_biscoito(self,biscoitos):
        for biscoito in biscoitos:
            pegou=pygame.sprite.collide_circle(self,biscoito)
            if pegou:
                biscoito.kill()
                return True 
        return False

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
        self.rect =self.image.get_rect()
        self.rect.x=x
        self.rect.y=300
        self.width = width
        self.window=window
        self.last_updated=0
        self.vel=-120

    def draw(self):
        self.window.blit(self.image, self.rect.y)

    def update(self,mexendo):
        v1=pygame.time.get_ticks()
        if mexendo:
            delta_t=(v1-self.last_updated)/1000
            self.last_updated=v1 
            self.rect.x=self.rect.x+(self.vel*delta_t)
        self.last_updated=v1
