import pygame 
from assets_jogo import * 

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
