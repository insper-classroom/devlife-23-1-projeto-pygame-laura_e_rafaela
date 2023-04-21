import pygame 
import random

class Player(pygame.sprite.Sprite):

    def __init__(self,window):
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
        self.rect.y=540


    def update(self,all_biscoitos):
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                return -1 
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_d] or tecla[pygame.K_RIGHT]:
            self.indice_img=(self.indice_img+1)%len(self.images_animation)
            image=pygame.image.load(self.images_animation[self.indice_img])
            self.image=pygame.transform.scale(image, (60,60))
            self.pegou_biscoito(all_biscoitos)
            all_biscoitos.update(True)
            return True 
        all_biscoitos.update(False)
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

    def __init__(self, window,y):
        pygame.sprite.Sprite.__init__(self)
        self.window=window
        image=pygame.image.load('jogo/Assets_jogo/biscoitos/biscoito_redondo.png')
        self.image=pygame.transform.scale(image, (30,30))
        self.h=self.image.get_height()
        self.radius=(self.h)/2
        self.last_updated=0
        self.rect=self.image.get_rect()
        self.rect.x=1300
        self.rect.y=y
        self.last_updated=0
        self.vel=-100

    def update(self,mexendo,):
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
