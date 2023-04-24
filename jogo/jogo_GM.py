import pygame 
from assets_jogo import * 
import math
import random

class Tela_Jogo():
    
    def __init__(self,window):
        self.window=window
        fundo=pygame.image.load('jogo/Assets_jogo/img_fundo.png'). convert()
        self.fundo=pygame.transform.scale(fundo, (800, 600))
        self.clock=pygame.time.Clock()
        self.FPS=15
        self.player=Player(self.window, self)
        self.tiles=math.ceil(self.window.get_width()/self.fundo.get_width())+1
        self.scroll=0
        self.andando=False
        self.biscoito_dx = 0
        self.plat_dx=0
        self.all_biscoitos=pygame.sprite.Group()
        self.all_plataformas = pygame.sprite.Group()
        self.sound=pygame.mixer.Sound('jogo/Assets_jogo/jingle-bells-rock-energetic-positive-upbeat-happy-christmas-party-125676.mp3')
        self.musica_tocando=False
        for i in range(10):
            y=random.randint(250,410)
            x = random.randint(self.biscoito_dx+500,1500 + self.biscoito_dx)
            self.all_biscoitos.add(Biscoito(self.window,y,x))
        for i in range(6):
            x = random.randint(100, 1000)
            width = random.randint(2, 6)
            self.all_plataformas.add(Plataforma(x,width,self.window))
        
    def atualiza(self):
        if not(self.musica_tocando):
            self.sound.play()
            self.musica_tocando=True
        self.clock.tick(self.FPS)
        self.biscoito_dx += 1500
        for i in range(10):
            y=random.randint(250,410)
            x = random.randint(self.biscoito_dx+500,1500 + self.biscoito_dx)
            self.all_biscoitos.add(Biscoito(self.window,y,x))
        self.plat_dx+=1000
        for i in range(10):
            x = random.randint(100, 1000)
            width = random.randint(2, 6)
            self.all_plataformas.add(Plataforma(self.plat_dx+x,width,self.window))
        player=self.player.update(self.all_biscoitos,self.all_plataformas)
        if player == -1:
            return -1
        self.andando=player
        return self  
    
    def desenha(self):
        if self.andando:
            if abs(self.scroll)>self.fundo.get_width():
                self.scroll=0
            else: 
                self.scroll-=15
        for i in range(self.tiles):
            self.window.blit(self.fundo,(i*self.fundo.get_width()+self.scroll,0))
        self.all_biscoitos.draw(self.window)
        self.all_plataformas.draw(self.window)
        self.player.desenha()
        pygame.display.update()


class Jogo: 
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Cookie Chase')
        self.largura_tela=1300
        self.altura_tela=600
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
