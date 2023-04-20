import pygame 

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
        self.clock=pygame.time.Clock()
        self.FPS=10

    def update(self):
        self.clock.tick(self.FPS)
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                return -1 
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_d] or tecla[pygame.K_RIGHT]:
            self.indice_img=(self.indice_img+1)%len(self.images_animation)
            image=pygame.image.load(self.images_animation[self.indice_img])
            self.image=pygame.transform.scale(image, (60,60))
            return True 
        return False
            
    def desenha(self):
        self.window.blit(self.image,self.rect)
        pygame.display.update()

class Biscoitos(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pass

class Nuvem(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


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
