import pygame 

class Player(pygame.sprite.Sprite):
    def __init__(self,window):
        pygame.sprite.Sprite.__init__(self)
        self.window=window
        self.indice_img=3
        self.image=pygame.image.load(f'jogo/Assets_jogo/snow_monster/snow_monster_{self.indice_img}_direita.png')
        self.vidas=2
        self.h=self.image.get_height()
        self.radius=(self.h)/2
        self.last_updated=0
        self.rect=self.image.get_rect()
        self.rect.x=0
        self.rect.y=self.window.get_height()

    def update(self):
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                return -1 
            elif evento.type==pygame.KEYDOWN:
                if evento.key==pygame.K_RIGHT:
                    
    def desenha(self):
        

class Biscoitos(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Nuvem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Monstro(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    

class Tela_Jogo():
    def __init__(self,window):
        self.window=window
        self.


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
