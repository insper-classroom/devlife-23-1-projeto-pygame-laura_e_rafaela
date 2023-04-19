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
        self.rect.x=0
        self.rect.y=540

    def update(self):
        self.indice_img=(self.indice_img+1)%len(self.images_animation)

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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    

class Tela_Jogo():
    
    def __init__(self,window):
        self.window=window
        fundo=pygame.image.load('jogo/Assets_jogo/img_fundo.png')
        self.fundo=pygame.transform.scale(fundo, (800, 750))
        self.player=Player(self.window)

    def atualiza(self):
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                return -1 
            self.player.update()
        return self 
    
    def desenha(self):
        self.window.blit(self.fundo,(0,0))
        self.player.desenha()
        pygame.display.update()


class Jogo: 
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Cookie Rush')
        self.largura_tela=800
        self.altura_tela=750
        self.window=pygame.display.set_mode((self.largura_tela,self.altura_tela))
        self.tela_atual=Tela_Jogo(self.window)
    
    def game_loop(self):
        rodando=True 
        while rodando:
            self.tela_atual=self.tela_atual.atualiza()
            if self.tela_atual==-1:
                rodando=False
            else:self.tela_atual.desenha()



if __name__ == '__main__':
    Jogo().game_loop()   
