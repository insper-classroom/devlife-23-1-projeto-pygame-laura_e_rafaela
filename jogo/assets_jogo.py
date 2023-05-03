
import pygame 
class Player(pygame.sprite.Sprite):

    ''' 
    Essa classe é onde está tudo referente ao jogador
    ...
    Metodos(funções) da classe
    ---------------------
    update:
        atualiza se o jogador está andando, pulando ou caindo. 
        garante que ele não atrevessa as plataformas ou chão.
        chama as funcoes de update do grupo de sprites monstros, biscoitos e plataformas.
        muda as animações de acordo com o que está acontecendo no jogo
    desenha:
         desenha o personagem no local em que ele se encontra
         desenha o número de vidas do personagem
         desenha a quantidade de cookies coletados pelo jogador
    pegou_biscoito:
        checa se o personagem entrou em contato com algum biscoito
        muda o efeito sonoro
        aumenta a quantidade de pontos e de cookies coletados
        retira o biscoito da tela
    esta_na_plataforma:
        checa se o personagem está em cima de alguma plataforma
    '''

    def __init__(self,window, tela_jogo):
        '''
        Função que inicia a classe Player e define os valores do self
        ...
        Parâmetros:
        -------
        window:
            janela do jogo 
        tela_jogo:
            classe que controla a tela quando o jogo está rodando
        '''
        pygame.sprite.Sprite.__init__(self)
        self.window=window
        self.indice_img=0 #controla o indice da lista com a imagem das animações do personagem
        #carrega as imagens referentes as animações de andar, pular, cair e ser atacado
        self.images_animation=['jogo/Assets_jogo/Gingerman/gingerman_1.png','jogo/Assets_jogo/Gingerman/gingerman_2.png','jogo/Assets_jogo/Gingerman/gingerman_3.png','jogo/Assets_jogo/Gingerman/gingerman_4.png','jogo/Assets_jogo/Gingerman/gingerman_6.png']
        #carrega as imagens referente a 'dança' que o personagem faz quando se ganha o jogo
        self.images_dance=['jogo/Assets_jogo/Gingerman/gingerman_8.png','jogo/Assets_jogo/Gingerman/gingerman_10.png','jogo/Assets_jogo/Gingerman/gingerman_9.png','jogo/Assets_jogo/Gingerman/gingerman_7.png']
        #carrega a imagem da animação atual
        image=pygame.image.load(self.images_animation[self.indice_img])
        self.image=pygame.transform.scale(image, (60,60))
        self.vidas=3 
        self.h=self.image.get_height()
        self.radius=(self.h)/5
        self.rect=self.image.get_rect()
        self.rect.x=50
        self.rect.y=420
        self.pulo = False #incializa a variavel que controla o pulo
        self.vel_y = 0 #incicializa a velocidade no eixo vertical
        self.ace = 500 #inicialiaza a aceleração usada para o pulo e a caida
        self.tela_jogo = tela_jogo #inicializa a variavel da classe Tela_Jogo
        self.t0 = 0 #variavel usada no calculo do delta T para controlar o tempo do jogo
        self.chao=420 #altura do chão
        self.fonte=pygame.font.Font('jogo/Assets_jogo/fontes/OnlineWebFonts_COM_2486b26012f1198dc8c84cbf5c960f98/font_jogo/PressStart2P.ttf',16)
        cookie=pygame.image.load('jogo/Assets_jogo/biscoitos/biscoito_redondo.png')
        self.cookie=pygame.transform.scale(cookie,(20,20))
        self.cookies_coletados=0
        self.pegou_biscoito_som=pygame.mixer.Sound('jogo/Assets_jogo/collect_cookie.mp3')
        self.som_perdeu_vida=pygame.mixer.Sound('jogo/Assets_jogo/ginger_hurt.mp3')
        self.pontos=0
        self.vel_x=0 #velocidade no eixo x
        self.ace_x=0 #aceleração no eixo x
        self.indice_dance=0 #controla as animações da dança que ocorre no final do jogo
        self.win_sound=pygame.mixer.Sound('jogo/Assets_jogo/win.mp3')

    def update(self,all_biscoitos,all_plataformas,all_monstros,andando):
        
        '''
        Função responsável por:

        atualiza se o jogador está andando, pulando ou caindo. 
        garante que ele não atrevessa as plataformas ou chão.
        chama as funcoes de update do grupo de sprites monstros, biscoitos e plataformas.
        muda as animações de acordo com o que está acontecendo no jogo 
        '''

        #calcula o delta t entre um frame e outro
        tempo_frame = pygame.time.get_ticks()
        dt = (tempo_frame - self.t0)/1000
        self.t0 = tempo_frame

        #checa se o usario fechou o jogo
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                return -1,self.pontos
            if andando:
                if evento.type == pygame.KEYDOWN:
                    #controla o pulo e a animação de pulo
                    if evento.key == pygame.K_SPACE and not self.pulo:
                        self.pulo = True
                        self.vel_y=-450
                        image=pygame.image.load(self.images_animation[2])
                        self.image=pygame.transform.scale(image, (60,60))
                    #controla a descida acelerada
                    if evento.key == pygame.K_DOWN and self.pulo and self.vel_y<0:
                        self.vel_y*=-1
        if not andando: #verifica se o personagem está em movimento
            self.vel_x=200
            self.ace_x=50
        if self.rect.x>=600:
            self.vel_x=0
            self.ace_x=0
        #verifica se ele está na plataforma
        self.vel_x += self.ace_x * dt
        self.rect.x += self.vel_x * dt

        plataforma = self.esta_na_plataforma(all_plataformas)
        if plataforma and self.vel_y>0: #verifica se ele está caindo em cima da plataforma ou não
                self.chao=248 #atualiza a variavel chao
        else:
            self.chao=420 #atualiza a variavel chao
        self.vel_y += self.ace * dt
        self.rect.y += self.vel_y * dt

        #barreira pro boneco não atravessar o chão
        if self.rect.y >= self.chao:
            self.rect.y=self.chao
            self.pulo=False
            self.vel=0

        self.pegou_biscoito(all_biscoitos,self)

        #controla com a animação deve ser monstrada
        if self.rect.x<600:
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
        
        elif self.rect.x>=600:
                self.win_sound.play()
                self.indice_dance=(self.indice_dance+1)%4
                image=pygame.image.load(self.images_dance[self.indice_dance])
                self.image=pygame.transform.scale(image, (60,60))

        #atualiza as plataformas, monstros e biscoitos
        all_biscoitos.update()
        all_plataformas.update()
        all_monstros.update(self,True)
        if self.vidas==0:
            return False,self.pontos
        return True,self.pontos
            

    def desenha(self):
        '''
        Função responsavel por desenhar o personagem e as informações referentes a ele
        '''
        self.window.blit(self.image,self.rect)
        desenho_coracoes=self.fonte.render(chr(9829)*self.vidas,True,(255,0,0))
        self.window.blit(desenho_coracoes,(0,0))
        desenho_cookies=self.fonte.render(f' x {self.cookies_coletados}',True,(0,0,0))
        self.window.blit(desenho_cookies,(1202,5))
        self.window.blit(self.cookie,(1195,1))
        pygame.display.update()

    def pegou_biscoito(self,biscoitos,player):
        '''
        Função responsável por verificar se o personagem pegou os biscoitos ou não
        '''
        if pygame.sprite.spritecollideany(self,biscoitos)==None:
                return False
        else:
            player.cookies_coletados+=1
            player.pegou_biscoito_som.play()
            player.pontos+=5
            pygame.sprite.spritecollideany(self,biscoitos).kill()
            return True
    
    def esta_na_plataforma(self,all_plataformas):
        '''
        Função responsável por verificar se o pesonagem está colidindo com as plataformas
        '''
        return pygame.sprite.spritecollideany(self,all_plataformas)

class Biscoito(pygame.sprite.Sprite):
    ''' 
    Essa classe é onde está tudo relacionado aos biscoitos do jogo
    ...
    Metodos(funções) da classe
    ---------------------
    update:
        garante que os cookies se movam junto com o resto da tela
    draw:
        desenha os biscoitos
    '''

    def __init__(self, window,y, x):
        '''
        Função que inicia a classe Biscoito e define os valores do self
        ...
        Parâmetros:
        -------
        window:
            janela do jogo 
        y:
            valor aleatório de y para a posição
        x:
            valor aleatório de x para a posição
        '''

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

    def update(self):
        '''
        Função responsável por movimentar os cookies de acordo com a velociade da tela e
        não deixa eles nascerem encima de plataformas
        '''
        v1=pygame.time.get_ticks()
        delta_t=(v1-self.last_updated)/1000
        self.last_updated=v1 
        self.rect.x=self.rect.x+(self.vel*delta_t)
        self.last_updated=v1
        if self.rect.x<(0-60):
            self.kill()

    def draw(self):
        '''
        Função resposável por desenhar os biscoitos
        '''
        self.window.blit(self.image,self.rect)


class Monstro(pygame.sprite.Sprite):
    ''' 
    Essa classe é onde está tudo relacionado aos monstros do jogo
    ...
    Metodos(funções) da classe
    ---------------------
    update:
        atualiza a posição e estados do monstro
    draw:
        desenha os monstros
    '''
    def __init__(self,window,x):
        '''
        Função que inicia a classe Monstro e define os valores do self
        ...
        Parâmetros:
        -------
        window:
            janela do jogo 
        x:
            valor aleatório de x para a posição
        '''

        pygame.sprite.Sprite.__init__(self)
        self.window=window
        self.indice_img=0
        self.images_animation=["jogo/Assets_jogo/snow_monster/snow_monster_4_esquerda.png", "jogo/Assets_jogo/snow_monster/snow_monster_2_esquerda.png"]
        image=pygame.image.load(self.images_animation[self.indice_img])
        self.image=pygame.transform.scale(image, (80,80))
        self.h=self.image.get_height()
        self.radius=(self.h)/2
        self.last_updated=0
        self.x=x
        self.y=420
        self.rect=pygame.Rect(self.x-20,self.y,40,80)
        self.vel=-120
        self.atacando=True
        self.som_esmaga=pygame.mixer.Sound('jogo/Assets_jogo/pula_no_monstro.mp3')

    def update(self, player, mexendo):

        '''
        Essa função é responsável por não deixar os monstros nascerem muito no começo do jogo,
        fazer com que eles se movem junto com a tela, 
        ver se o personagem está atacando eles ou eles estão atacando e mudar a animação de acordo
        '''

        if self.rect.x<(0-80):
            self.kill()

        v1=pygame.time.get_ticks()
        if mexendo:
            delta_t=(v1-self.last_updated)/1000
            self.last_updated=v1 
            self.rect.x=self.rect.x+(self.vel*delta_t)
        self.last_updated=v1
        machucando=True
        if pygame.sprite.collide_rect(player,self):
            if player.vel_y>0 and player.pulo:
                self.som_esmaga.play()
                self.kill()
                player.pontos+=10
                machucando=False
            elif self.atacando and not player.pulo:
                image=pygame.image.load(player.images_animation[4])
                player.image=pygame.transform.scale(image, (60,60))
                player.som_perdeu_vida.play()
                self.atacando=False
                player.vidas -= 1
                machucando=True 

            if machucando:
                image=pygame.image.load(player.images_animation[4])
                player.image=pygame.transform.scale(image, (60,60))
            self.indice_img=(self.indice_img+1)%len(self.images_animation)
            image=pygame.image.load(self.images_animation[self.indice_img])
            self.image=pygame.transform.scale(image, (80,80))
  
    def draw(self):
        '''
        Função responsável por desenhar o monstro
        '''
        self.window.blit(self.image,self.rect)

class Plataforma (pygame.sprite.Sprite):
    ''' 
    Essa classe é onde está tudo relacionado ás platFformas do jogo
    ...
    Metodos(funções) da classe
    ---------------------
    update:
        atualiza a posição da plataforma
    draw:
        desenha as plataformas
    '''
    def __init__(self, x, width,window):
        '''
        Função que inicia a classe Monstro e define os valores do self
        ...
        Parâmetros:
        -------
        window:
            janela do jogo 
        x:
            valor aleatório de x para a posição
        width:
            valor aleatório para a largura da pplataforma    
        
        '''

        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("jogo/Assets_jogo/snow_ground.png")
        self.image = pygame.transform.scale(image, (80,60))
        self.h=20
        self.x=x
        self.y=300
        self.width =width
        self.rect =pygame.Rect(self.x+15,self.y,self.width+40,self.h)
        self.window=window
        self.last_updated=0
        self.vel=-120
        self.radius=self.h/2

    def draw(self):
        '''
        Função responsável por desenhar as plataformas
        '''
        self.window.blit(self.image, self.rect.y)

    def update(self):
        '''
        Função responsável por movimentar as plataformas de acordo com a velociade da tela e
        não deixa elas nascerem uma encima da outra
        '''
        v1=pygame.time.get_ticks()
        delta_t=(v1-self.last_updated)/1000
        self.last_updated=v1 
        self.rect.x=self.rect.x+(self.vel*delta_t)
        self.last_updated=v1
        if self.rect.x<(0-self.width-80):
            self.kill()

    
class Casa (pygame.sprite.Sprite):
    ''' 
    Essa classe é onde está referente a Casa
    ...
    Metodos(funções) da classe
    ---------------------
    desenha:
        desenha a casa
    update:
        controla a entrada da casa no jogo
    '''
    def __init__(self,window):
       
        '''
        Função que inicia a classe Casa e define os valores do self
        ...
        Parâmetros:
        -------
        window:
            janela do jogo 
        '''
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("jogo/Assets_jogo/Gingerbread_house/casa_gingerbread.png")
        self.image = pygame.transform.scale(image, (300,200))
        self.rect =self.image.get_rect()
        self.rect.x=1300
        self.rect.y=300 
        self.window=window
        self.last_updated=0
        self.vel_x=2
        self.ace_x=1

    def desenha(self):
        '''Função resposável por desenhar a casa
        '''
        self.window.blit(self.image,self.rect)

    def update(self):
        '''Função resposável por controlar a aceleração e velocidade da casa
        '''
        self.vel_x += self.ace_x
        self.rect.x -= self.vel_x
        