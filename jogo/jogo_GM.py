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
        self.all_monstros = pygame.sprite.Group()
        self.tiles=math.ceil(self.window.get_width()/self.fundo.get_width())+1
        self.scroll=0
        self.andando=False
        self.biscoito_dx = 0
        self.plat_dx=0
        self.all_biscoitos=pygame.sprite.Group()
        self.all_plataformas = pygame.sprite.Group()
        self.sound=pygame.mixer.Sound('jogo/Assets_jogo/jingle-bells-rock-energetic-positive-upbeat-happy-christmas-party-125676.mp3')
        self.musica_tocando=False
        for i in range(6):
            x = random.randint(100, 1000)
            width = random.randint(2, 6)
            self.all_plataformas.add(Plataforma(x,width,self.window))
        for i in range(10):
            y=random.randint(350,410)
            while not(250>y or y>370):
                y=random.randint(250,410)
            x = random.randint(self.biscoito_dx+500,1500 + self.biscoito_dx)
            biscoito=Biscoito(self.window,y,x)
            self.all_biscoitos.add(biscoito)
        self.monstro_dx = 0
        x=random.randint(self.monstro_dx,50+self.monstro_dx)
        monstro = Monstro(self.window, x)
        self.all_monstros.add(monstro)

    def atualiza(self):
        if not(self.musica_tocando):
            self.sound.play(-1)
            self.musica_tocando=True
        self.clock.tick(self.FPS)
        self.plat_dx+=1000
        for i in range(10):
            x = random.randint(100, 1000)
            width = random.randint(2, 6)
            self.all_plataformas.add(Plataforma(self.plat_dx+x,width,self.window))
        self.biscoito_dx += 1000
        for i in range(10):
            y=random.randint(350,410)
            while not(280>y or y>370):
                y=random.randint(250,410)
            x = random.randint(self.biscoito_dx+500,1500 + self.biscoito_dx)
            biscoito=Biscoito(self.window,y,x)
            while pygame.sprite.spritecollideany(biscoito,self.all_plataformas):
                y=random.randint(250,410)
                x = random.randint(self.biscoito_dx+500,1500 + self.biscoito_dx)
                biscoito=Biscoito(self.window,y,x)
            self.all_biscoitos.add(biscoito)
        self.monstro_dx += 500
        x=random.randint(self.monstro_dx,50+ self.monstro_dx)
        monstro = Monstro(self.window, x)
        self.all_monstros.add(monstro)
        player=self.player.update(self.all_biscoitos,self.all_plataformas,self.all_monstros)
        if player == -1:
            return -1
        self.andando=player
        return self  
    
    def desenha(self):
        if self.andando:
            if abs(self.scroll)>self.fundo.get_width():
                self.scroll=self.fundo.get_width()+self.scroll
            else: 
                self.scroll-=15
        for i in range(self.tiles):
            self.window.blit(self.fundo,(i*self.fundo.get_width()+self.scroll,0))
        self.all_biscoitos.draw(self.window)
        self.all_plataformas.draw(self.window)
        self.all_monstros.draw(self.window)
        self.player.desenha()
        pygame.display.update()


class Tela_Inicial():
    def __init__(self,window):
        pygame.init()
        self.window=window
        self.largura_tela =1300
        self.altura_tela =600
        fundo=pygame.image.load('jogo/Assets_jogo/img_fundo.png'). convert()
        self.fundo=pygame.transform.scale(fundo, (800, 600))
        self.tiles=math.ceil(self.window.get_width()/self.fundo.get_width())+1
        self.scroll=0
        self.clock=pygame.time.Clock()
        self.FPS=15
        self.fundo_jogar = pygame.Rect(self.largura_tela//2-150,self.altura_tela//2-100,300,100)
        self.fonte_jogar = pygame.font.Font("jogo/Assets_jogo/fontes/OnlineWebFonts_COM_2486b26012f1198dc8c84cbf5c960f98/Architype Aubette W90/Architype Aubette W90.ttf", 80)
        self.jogar = False
        self.fundo_regras = pygame.Rect(self.largura_tela//2 - 150,self.altura_tela//2 + 40,120,40)
        self.fonte_regras = pygame.font.Font("jogo/Assets_jogo/fontes/OnlineWebFonts_COM_2486b26012f1198dc8c84cbf5c960f98/Architype Aubette W90/Architype Aubette W90.ttf", 30)
        self.regras = False
        self.fundo_info = pygame.Rect(self.largura_tela//2 + 30,self.altura_tela//2 + 40,120,40)
        self.fonte_info = pygame.font.Font("jogo/Assets_jogo/fontes/OnlineWebFonts_COM_2486b26012f1198dc8c84cbf5c960f98/Architype Aubette W90/Architype Aubette W90.ttf", 30)
        self.info = False
        self.logo = pygame.image.load("jogo/Assets_jogo/cookie_chase_vermelho.png")
        self.logo = pygame.transform.scale(self.logo, (911.25, 109.5))
    def desenha(self):

        if abs(self.scroll)>self.fundo.get_width():
                self.scroll=0
        else: 
            self.scroll-=15
        for i in range(self.tiles):
            self.window.blit(self.fundo,(i*self.fundo.get_width()+self.scroll,0))
        if self.jogar:
            texto_jogar = self.fonte_jogar.render("JOGAR",True,(184, 55, 38))
            pygame.draw.rect(self.window, (240, 248, 255),self.fundo_jogar,0,15)
        else:
            texto_jogar = self.fonte_jogar.render("JOGAR",True,(240, 248, 255))
            pygame.draw.rect(self.window, (184, 55, 38),self.fundo_jogar,0,15)
        
        if self.regras:
            texto_regras = self.fonte_regras.render("REGRAS", True, (184, 55, 38))
            pygame.draw.rect(self.window,(240, 248, 255), self.fundo_regras,0 ,15)
        else:
            texto_regras = self.fonte_regras.render("REGRAS", True, (240, 248, 255))
            pygame.draw.rect(self.window,(184, 55, 38), self.fundo_regras,0 ,15)
        if self.info:
            texto_info = self.fonte_info.render("INFO", True, (184, 55, 38))
            pygame.draw.rect(self.window, (240, 248, 255), self.fundo_info, 0, 15)
        else:
            texto_info = self.fonte_info.render("INFO", True, (240, 248, 255))
            pygame.draw.rect(self.window, (184, 55, 38), self.fundo_info, 0, 15)
        self.window.blit(self.logo, (190,40))
        self.window.blit(texto_info, (self.largura_tela//2 + 65,self.altura_tela//2 + 40))
        self.window.blit(texto_regras, (self.largura_tela//2 - 140 ,self.altura_tela//2 + 40))
        self.window.blit(texto_jogar, (self.largura_tela//2-115,self.altura_tela//2-100))
        pygame.display.update()
    def atualiza(self):
        self.clock.tick(self.FPS)
        pos_mouse = pygame.mouse.get_pos()
        if self.checa_colisao(self.fundo_jogar.x, self.fundo_jogar.y, self.fundo_jogar.width, self.fundo_jogar.height,pos_mouse[0],pos_mouse[1]):
            self.jogar = True
        else:
            self.jogar= False
        if self.checa_colisao (self.fundo_regras.x, self.fundo_regras.y, self.fundo_regras.width, self.fundo_regras.height,pos_mouse[0],pos_mouse[1]):
            self.regras = True
        else:
            self.regras = False
        if self.checa_colisao (self.fundo_info.x, self.fundo_regras.y, self.fundo_info.width, self.fundo_info.height,pos_mouse[0],pos_mouse[1]):
            self.info = True
        else:
            self.info = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN and self.jogar:
                return Tela_Jogo(self.window)
            elif event.type == pygame.MOUSEBUTTONDOWN and self.regras:
                return Tela_Regras(self.window)
            elif event.type == pygame.MOUSEBUTTONDOWN and self.info:
                return Tela_Info(self.window)
            
        return self
    
    def checa_colisao(self,ret_x, ret_y, ret_largura, ret_altura, p_x, p_y):
        if (
            ret_x <= p_x and 
            p_x <= ret_x + ret_largura and 
            ret_y <= p_y and 
            p_y <= ret_y + ret_altura
        ):
            return True
        else:
            return False
        

class Tela_Regras ():
    def __init__(self,window):
        pygame.init()
        self.window=window
        fundo=pygame.image.load('jogo/Assets_jogo/img_fundo_regras.png').convert()
        self.fundo=pygame.transform.scale(fundo,(1300,600))
        self.fundo_jogar = pygame.Rect(380,366,185,60)
        self.fonte_jogar = pygame.font.Font("jogo/Assets_jogo/fontes/OnlineWebFonts_COM_2486b26012f1198dc8c84cbf5c960f98/Architype Aubette W90/Architype Aubette W90.ttf", 60)
        self.jogar = False
        self.fundo_voltar = pygame.Rect(670,366,205,60)
        self.fonte_voltar = pygame.font.Font("jogo/Assets_jogo/fontes/OnlineWebFonts_COM_2486b26012f1198dc8c84cbf5c960f98/Architype Aubette W90/Architype Aubette W90.ttf", 60)
        self.voltar = False
        self.FPS=15
        self.clock=pygame.time.Clock()

    def desenha(self):
        self.window.blit(self.fundo,(0,0))
        if self.jogar:
            texto_jogar = self.fonte_jogar.render("JOGAR",True,(184, 55, 38))
            pygame.draw.rect(self.window, (240, 248, 255),self.fundo_jogar,0,15)
        else:
            texto_jogar = self.fonte_jogar.render("JOGAR",True,(240, 248, 255))
            pygame.draw.rect(self.window, (184, 55, 38),self.fundo_jogar,0,15)
        self.window.blit(texto_jogar, (380,360))
        if self.voltar:
            texto_voltar = self.fonte_voltar.render("VOLTAR",True,(184, 55, 38))
            pygame.draw.rect(self.window, (240, 248, 255),self.fundo_voltar,0,15)
        else:
            texto_voltar = self.fonte_voltar.render("VOLTAR",True,(240, 248, 255))
            pygame.draw.rect(self.window, (184, 55, 38),self.fundo_voltar,0,15)
        self.window.blit(texto_voltar, (670,360))
        pygame.display.update()


    def atualiza(self):
        self.clock.tick(self.FPS)
        pos_mouse = pygame.mouse.get_pos()
        if self.checa_colisao(self.fundo_jogar.x, self.fundo_jogar.y, self.fundo_jogar.width, self.fundo_jogar.height,pos_mouse[0],pos_mouse[1]):
            self.jogar = True
        else:
            self.jogar= False
        if self.checa_colisao(self.fundo_voltar.x, self.fundo_voltar.y, self.fundo_voltar.width, self.fundo_voltar.height,pos_mouse[0],pos_mouse[1]):
            self.voltar = True
        else:
            self.voltar= False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN and self.jogar:
                return Tela_Jogo(self.window)
            if event.type == pygame.MOUSEBUTTONDOWN and self.voltar:
                return Tela_Inicial(self.window)
        return self

    def checa_colisao(self,ret_x, ret_y, ret_largura, ret_altura, p_x, p_y):
        if (
            ret_x <= p_x and 
            p_x <= ret_x + ret_largura and 
            ret_y <= p_y and 
            p_y <= ret_y + ret_altura
        ):
            return True
        else:
            return False


class Tela_Info ():
    pass

class Jogo: 
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Cookie Chase')
        self.largura_tela=1300
        self.altura_tela=600
        self.window=pygame.display.set_mode((self.largura_tela,self.altura_tela))
        self.tela_atual=Tela_Inicial(self.window)

        
    
    def game_loop(self):
        rodando=True 
        while rodando:
            self.tela_atual=self.tela_atual.atualiza()
            if self.tela_atual==-1:
                rodando=False
            else:self.tela_atual.desenha()



if __name__ == '__main__':
    Jogo().game_loop()   

