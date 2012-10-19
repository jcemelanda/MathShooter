#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
'''
#   Math Shooter.
#   A math scrolling arcade shooter.
#   This code is based in the one written by Tyler Gray & Chad Haley and
#   released under GPL
#
#   Copyleft (C) 2009  Julio Melanda
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
#	The song Stone Fortress use as background music of the game was taken from
#	http://opengameart.org/content/stone-fortress
# 
'''

#Import
import os, sys, pygame, random
from pygame.locals import RLEACCEL, KEYUP, K_LEFT, K_SPACE
from pygame.locals import K_RIGHT, K_UP, K_DOWN

class Game:
    
    def __init__(self):
        
        os.environ['SDL_VIDEO_CENTERED'] = "1"
        pygame.init()
        pygame.display.set_caption("Math Shooter")
        icon = pygame.image.load("data/Math Shooter.png")
        icon = pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((800, 600))
        pygame.mouse.set_visible(0)
        
        #Background      
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
            
        #Music
        try:
            self.music = pygame.mixer.music.load ("data/music/Stone Fortress.ogg")
            pygame.mixer.music.play(-1)
        except:
            'print the game will load without music'      
        
    def play_game(self):
        
        
        self.player = Player(self)
        self.score = Score()
        self.operation = Operation()
        self.fire = self.load_sound("sounds/laser.ogg")
        self.explode = self.load_sound("sounds/explosao.ogg")
        self.clock = pygame.time.Clock()
        #Arena
        self.arena = Arena(self)
        self.arena = pygame.sprite.RenderPlain((self.arena))
                
        #Game Groups
        
        #Player/Enemy
        
        self.player_sprite = pygame.sprite.RenderPlain((self.player))
        self.operation_sprite = pygame.sprite.Group(self.operation)
        
        self.enemy_sprites = pygame.sprite.RenderPlain(())
        self.enemy_sprites.add(Enemy(self))
        
        #Projectiles
        self.laser_sprites = pygame.sprite.RenderPlain(())
        
        self.explosion_sprites = pygame.sprite.RenderPlain(())
        
        #Score/and game over
        self.score_sprite = pygame.sprite.Group(self.score)
        self.game_over_sprite = pygame.sprite.RenderPlain(())
            
        keepGoing = True
        counter = 0
        loopCounter = 0
        dec = 1
        
        #Main Loop
        while keepGoing:
            self.clock.tick(30)
            #input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keepGoing = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        keepGoing = False
                    elif event.key == pygame.K_LEFT:
                        self.player.dx = -10
                    elif event.key == K_RIGHT:
                        self.player.dx = 10
                    elif event.key == K_UP:
                        self.player.dy = -10
                    elif event.key == K_DOWN:
                        self.player.dy = 10
                elif event.type == KEYUP:
                    if event.key == K_LEFT:
                        self.player.dx = 0
                    elif event.key == K_RIGHT:
                        self.player.dx = 0
                    elif event.key == K_UP:
                        self.player.dy = 0
                    elif event.key == K_DOWN:
                        self.player.dy = 0
                        
            #Update and draw on the self.screen
           
            #Update     
            self.screen.blit(self.background, (0,0))     
            self.player_sprite.update()
            self.enemy_sprites.update()
            self.laser_sprites.update()
            self.explosion_sprites.update()
            self.arena.update()
            self.score_sprite.update()
            self.operation_sprite.update()
            self.game_over_sprite.update()
            
            #Draw
            self.arena.draw(self.screen)
            self.player_sprite.draw(self.screen)
            self.enemy_sprites.draw(self.screen)
            self.laser_sprites.draw(self.screen)
            self.explosion_sprites.draw(self.screen)
            self.score_sprite.draw(self.screen)
            self.operation_sprite.draw(self.screen)
            self.game_over_sprite.draw(self.screen)
            pygame.display.flip()
            
            #Spawn new enemies
    
            counter += 1
            if (loopCounter % 90 == 0) and (dec < 35):
                dec += 1
            if counter >= 40 - dec:
                self.enemy_sprites.add(Enemy(self))
                counter = 0
            loopCounter += 1
            #Check for game over
            if self.score.score < -100:
                self.game_over_sprite.add(Gameover())
                self.game_over_sprite.add(Gameoveresc())
                self.player_sprite.remove(self.player)
    
    def train(self):
        
        self.player = Player(self)
        self.score = Score()
        self.teacher = Teacher(self)
        self.fire = self.load_sound( "sounds/laser.ogg")
        self.explode = self.load_sound("sounds/explosao.ogg")
        self.speech = Speech(self)
        self.speech_sprite = pygame.sprite.RenderPlain([self.speech]) 
        self.clock = pygame.time.Clock()
        #Arena
        self.arena = Arena(self)
        self.arena = pygame.sprite.RenderPlain((self.arena))
        
        self.op_train  = OperationTrain()
        self.big_op = Big_Operation(self)
        
        self.enemyL_sprites = pygame.sprite.RenderPlain(())
        self.enemyL_sprites.add(Enemy_Train(self))
        
        #shows Treinamento on the screen
        self.train_sprite = Menu(["Treinamento"])
        self.train_sprite.center_at(200, 250)
        self.train_sprite.set_font(pygame.font.Font("data/fonts/planet5.ttf",
                                                                        48))
        self.train_sprite.set_highlight_color((0, 255, 0))
        for i in range(30):
            self.clock.tick(30)
            self.screen.blit(self.background, (0,0))
            self.arena.update()
            self.arena.draw(self.screen)
            self.train_sprite.draw(self.screen)
            pygame.display.flip()
    
        self.teacher_sprite = pygame.sprite.RenderPlain((self.teacher))
        for i in range(70):
            self.show_message((460, 300), 'sprites/fala1.png')
            '''self.clock.tick(30)
            self.screen.blit(self.background, (0,0))
            self.arena.update()
            self.arena.draw(self.screen)
            self.speech_sprite.update('sprites/fala1.png')
            self.speech_sprite.draw(self.screen)
            self.teacher_sprite.update()
            self.teacher_sprite.draw(self.screen)
            pygame.display.flip()'''
            
        for i in range(70):
            self.show_message((460, 300), 'sprites/fala2.png')
            '''
            self.clock.tick(30)
            self.screen.blit(self.background, (0,0))
            self.arena.update()
            self.arena.draw(self.screen)
            self.speech_sprite.update('sprites/fala2.png', (460, 300))
            self.speech_sprite.draw(self.screen)
            self.teacher_sprite.update()
            self.teacher_sprite.draw(self.screen)
            pygame.display.flip()'''
            
        self.big_op_sprites = pygame.sprite.RenderPlain([self.big_op])
        for i in range(60):
            self.clock.tick(30)
            self.screen.blit(self.background, (0,0))
            self.arena.update()
            self.arena.draw(self.screen)
            self.big_op_sprites.update()
            self.big_op_sprites.draw(self.screen)
            self.teacher_sprite.update()
            self.teacher_sprite.draw(self.screen)
            pygame.display.flip()
            
        for i in range(70):
            self.show_message((460, 300), 'sprites/fala3.png')
            '''self.clock.tick(30)
            self.screen.blit(self.background, (0,0))
            self.arena.update()
            self.arena.draw(self.screen)
            self.speech_sprite.update('sprites/fala3.png', (460, 300))
            self.speech_sprite.draw(self.screen)
            self.teacher_sprite.update()
            self.teacher_sprite.draw(self.screen)
            pygame.display.flip()'''
            
        self.player_sprite = pygame.sprite.RenderPlain([self.player])
        self.operation_sprite = pygame.sprite.Group(self.op_train)
        
        self.enemyL_sprites = pygame.sprite.RenderPlain(())
        self.enemyL_sprites.add(Enemy_Train(self))
        
        #Projectiles
        self.laser_sprites = pygame.sprite.RenderPlain(())
        
        self.explosion_sprites = pygame.sprite.RenderPlain(())
            
        keepGoing = True
        counter = 0
        loopCounter = 0
        self.shots_counter = 0
        self.state = 0
        #Main Loop
        while keepGoing:
            self.clock.tick(30)
            
            if self.state == 1:
                for i in range(70):
                    self.clock.tick(30)
                    self.speech_sprite.update('sprites/fala5.png', (460, 300))
                    self.speech_sprite.draw(self.screen)
                    self.teacher_sprite.update()
                    self.teacher_sprite.draw(self.screen)
                    pygame.display.flip()
                    self.enemyL_sprites = pygame.sprite.RenderPlain(())
                    self.explosion_sprites = pygame.sprite.RenderPlain(())
                self.teacher_sprite.remove(self.teacher)
                self.state = 2
                  
            #input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keepGoing = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        keepGoing = False
                    elif event.key == pygame.K_LEFT:
                        self.player.dx = -10
                    elif event.key == K_RIGHT:
                        self.player.dx = 10
                    elif event.key == K_UP:
                        self.player.dy = -10
                    elif event.key == K_DOWN:
                        self.player.dy = 10
                elif event.type == KEYUP:
                    if event.key == K_LEFT:
                        self.player.dx = 0
                    elif event.key == K_RIGHT:
                        self.player.dx = 0
                    elif event.key == K_UP:
                        self.player.dy = 0
                    elif event.key == K_DOWN:
                        self.player.dy = 0
                        
            #Update and draw on the self.screen
            
            #Update     
            self.screen.blit(self.background, (0,0))     
            self.player_sprite.update()
            self.enemyL_sprites.update()
            self.laser_sprites.update()
            self.explosion_sprites.update()
            self.arena.update()
            self.operation_sprite.update()
            self.teacher_sprite.update()
            
            self.arena.draw(self.screen)
            self.player_sprite.draw(self.screen)
            self.enemyL_sprites.draw(self.screen)
            self.laser_sprites.draw(self.screen)
            self.explosion_sprites.draw(self.screen)
              
            if self.shots_counter == 1:
                for i in range(70):
                    self.clock.tick(30)
                    self.speech_sprite.update('sprites/fala4.png', (460, 300))
                    self.speech_sprite.draw(self.screen)
                    self.teacher_sprite.update()
                    self.teacher_sprite.draw(self.screen)
                    if loopCounter < 300:
                        self.shots_counter = 0
                        self.laser_sprites = pygame.sprite.RenderPlain(())
                    else:
                        self.state = 1
                        self.shots_counter += 1
                    pygame.display.flip()
                    self.enemyL_sprites = pygame.sprite.RenderPlain(())
                    self.explosion_sprites = pygame.sprite.RenderPlain(())
                if self.state == 0:    
                    for i in range(60):
                        self.clock.tick(30)
                        self.screen.blit(self.background, (0,0))
                        self.arena.update()
                        self.arena.draw(self.screen)
                        self.big_op_sprites.update()
                        self.big_op_sprites.draw(self.screen)
                        self.teacher_sprite.update()
                        self.teacher_sprite.draw(self.screen)
                        pygame.display.flip()    
            
                    
            #Draw
            self.arena.draw(self.screen)
            self.player_sprite.draw(self.screen)
            self.enemyL_sprites.draw(self.screen)
            self.laser_sprites.draw(self.screen)
            self.explosion_sprites.draw(self.screen)
            self.operation_sprite.draw(self.screen)
            self.teacher_sprite.draw(self.screen)
            pygame.display.flip()
            
                            
            #Spawn new enemies
    
            if (loopCounter % 50 == 0):
                self.enemyL_sprites.add(Enemy_Train(self))
            loopCounter += 1
            continuation = False
            
            if loopCounter > 1000:
                menu = Menu(
                        ['Para continuar treinando'], 
                        ['pressione qualquer tecla']
                        )
                #Menu settings
                menu.center_at(400, 400)
                menu.set_font(pygame.font.Font(
                                    "data/fonts/DejaVuLGCSansMono.ttf", 32))
                menu.set_highlight_color((0, 255, 0))
                menu.set_normal_color((0, 85, 0))
    
                
                if loopCounter % 500 == 0:
                    self.teacher_sprite.add(self.teacher)
                    for i in range(150):
                        #Events
                        events = pygame.event.get()
                        
                        for e in events:
                            if e.type == pygame.QUIT:
                                pygame.quit()
                                return
                        #Update Menu
                        self.show_message((460, 300), 'sprites/fala6.png', 
                                                                    menu)
                        
                        for e in events:
                            if e.type == pygame.KEYDOWN:
                                continuation = True
                    if continuation:
                        self.state = 5
                    else:
                        self.state = 6                        
                        
                if self.state == 5:
                    for i in range(70):
                        self.show_message((460, 300), 'sprites/fala7.png')
                    '''
                    for i in range(70):
                        self.clock.tick(30)
                        self.screen.blit(self.background, (0,0))
                        self.arena.update()
                        self.arena.draw(self.screen)
                        self.speech_sprite.update('sprites/fala7.png',
                                                                    (460, 300))
                        self.speech_sprite.draw(self.screen)
                        self.teacher_sprite.update()
                        self.teacher_sprite.draw(self.screen)
                        pygame.display.flip()
                        self.enemyL_sprites = pygame.sprite.RenderPlain(())
                        self.explosion_sprites = pygame.sprite.RenderPlain(())
                    '''
                    self.state = 4
                
                if self.state == 6:
                    for i in range(70):
                        self.show_message((460, 300), 'sprites/fala8.png')
                    return 1
                
        return 0
    
    def show_message(self, pos, image, menu = None):
        self.clock.tick(30)
        self.screen.blit(self.background, (0,0))
        self.arena.update()
        self.arena.draw(self.screen)
        self.speech_sprite.update(image, pos)
        self.speech_sprite.draw(self.screen)
        self.teacher_sprite.update()
        self.teacher_sprite.draw(self.screen)
        if menu != None:
            menu.draw(self.screen)
        pygame.display.flip()
        self.enemyL_sprites = pygame.sprite.RenderPlain(())
        self.explosion_sprites = pygame.sprite.RenderPlain(())
        self.laser_sprites = pygame.sprite.RenderPlain(())
    
    def mission_menu(self):
        
        #Arena
        arena = Arena(self)
        arena = pygame.sprite.RenderPlain((arena))
        
    
        #Title for Option Menu
        menuTitle = Menu(
            ["Math Shooter"])
    
        #Option Menu Text
        instructions = Menu(
            [""], 
            ["Você deve atirar nos números que são resposta para a operação"],
            [""],
            ["mostrada no canto superior esquerdo da tela"],
            [""],
            ["Navegue sua nave com as setas, e atire com o espaço."],
            [""],
            ["Ao acertar, a pontuação é acrescentada, e ao errar, a pontuação"],
            [""],
            ["Será decrementada"],
            [""],
            ["Ao chegar a -100 pontos, o jogo termina (Game Over)"],
            [""],
            [""],
            ["                   PRESSIONE ESC PARA RETORNAR                    "])
    
        #Title 
        menuTitle.center_at(150, 150)
        menuTitle.set_font(pygame.font.Font("data/fonts/planet5.ttf", 48))
        menuTitle.set_highlight_color((0, 255, 0))
            
    
        #Title Center
        instructions.center_at(440, 350)
    
        #Menu Font
        instructions.set_font(pygame.font.Font("data/fonts/arial.ttf", 22))
    
        #Highlight Color
        instructions.set_normal_color((0, 255, 0))
    
    
        #Set Clock
        clock = pygame.time.Clock()
        keepGoing = True
    
        while keepGoing:
            clock.tick(30)
            #input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keepGoing = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        keepGoing = False
            #Draw
            self.screen.blit(self.background, (0,0))
            arena.update()
            arena.draw(self.screen)
            menuTitle.draw(self.screen)
            instructions.draw(self.screen)
            pygame.display.flip()

    def about_menu(self):
     
        #Arena
        arena = Arena(self)
        arena = pygame.sprite.RenderPlain((arena))
        
        #About Menu Text
        #Title for Option Menu
        menuTitle = Menu(
            ["Math Shooter"])
    
        info = Menu(
            [""], 
            ["Versão de testes de Math Shooter."],
            [""],
            [" Distribuído sob a GPL"],
            [""],
            ["Desenvolvido por Júlio César Eiras Melanda"],
            [""],
            [""],
            ["            PRESSIONE ESC PARA RETORNAR            "])
            
    
        #About Title Font color, alignment, and font type
        menuTitle.center_at(150, 150)
        menuTitle.set_font(pygame.font.Font("data/fonts/planet5.ttf", 48))
        menuTitle.set_highlight_color((0, 255, 0))
    
        #About Menu Text Alignment
        info.center_at(400, 310)
    
        #About Menu Font
        info.set_font(pygame.font.Font("data/fonts/arial.ttf", 28))
    
        #About Menu Font Color
        info.set_normal_color((0, 255, 0))
    
    
        #Set Clock
        clock = pygame.time.Clock()
        keepGoing = True
    
        while keepGoing:
            clock.tick(30)
            #input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keepGoing = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        keepGoing = False
        #Draw
            self.screen.blit(self.background, (0,0))    
            arena.update()
            arena.draw(self.screen)
            menuTitle.draw(self.screen)
            info.draw(self.screen)
            pygame.display.flip()
    
    #Functions
    def option0(self):
        if self.train() == 1:
            self.option1()
    def option1(self):
        self.play_game()
    def option2(self):
        self.mission_menu()
    def option3(self):
        self.about_menu()   
    def option4(self):
        pygame.quit()
        sys.exit()
    def option5(self):
        self.state = 5
    def option6(self):
        self.state = 6
        
    #Main
    def main_menu(self):
            
        #Arena
        arena = Arena(self)
        arena = pygame.sprite.RenderPlain((arena))
    
       
        #Defines menu, option functions, and option display. For example,
        #Changing "Start" to "Begin" will display Begin, instead of start. 
        menuTitle = Menu(
            ["Math Shooter"])
            
        menu = Menu(
            ["Treinar", self.option0],
            ["Inicar", self.option1],
            ["Missão", self.option2],
            ["Sobre", self.option3],
            ["Sair", self.option4])
            
            
    
        #Title
        menuTitle.center_at(150, 150)
        menuTitle.set_font(pygame.font.Font("data/fonts/planet5.ttf", 48))
        menuTitle.set_highlight_color((0, 255, 0))
        
        #Menu settings
        menu.center_at(400, 320)
        menu.set_font(pygame.font.Font("data/fonts/DejaVuLGCSansMono.ttf", 32))
        menu.set_highlight_color((0, 255, 0))
        menu.set_normal_color((0, 85, 0))
        
        clock = pygame.time.Clock()
        keepGoing = True   
    
        while True:
            clock.tick(30)
    
            #Events
            events = pygame.event.get()
    
            #Update Menu
            menu.update(events)
    
            #Quit Event
            for e in events:
                if e.type == pygame.QUIT:
                    pygame.quit()
                    return
    
            #Draw
            self.screen.blit(self.background, (0,0))
            arena.update()
            arena.draw(self.screen)
            menu.draw(self.screen)
            menuTitle.draw(self.screen)
            pygame.display.flip()


    #Load Images
    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print 'Erro ao carregar a imagem:', fullname
            raise SystemExit, message
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()
    
    #Load Sounds
    def load_sound(self, name):
        class NoneSound:
            def play(self): pass
        if not pygame.mixer or not pygame.mixer.get_init():
            return NoneSound()
        fullname = os.path.join('data', name)
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error, message:
            print 'Erro ao carregar o som:', fullname
            raise SystemExit, message
        return sound
    
    #Modifies sprite_collide_any from the pygame api
    #(pygame.sprite.sprite_collide_any)
    def sprite_collide_any(self, sprite, group, collided = None): 
        """sprite_collide_any(sprite, group) -> sprite
           finds any sprites that collide
    
           given a sprite and a group of sprites, this will
           return return any single sprite that collides with
           with the given sprite. If there are no collisions
           this returns None.
    
           if you don't need all the features of the
           spritecollide function, this function will be a
           bit quicker.
    
           collided is a callback function used to calculate if
           two sprites are colliding. it should take two sprites
           as values, and return a bool value indicating if
           they are colliding. if collided is not passed, all
           sprites must have a "rect" value, which is a
           rectangle of the sprite area, which will be used
           to calculate the collision."""
           
        if collided is None:
            # Special case old behaviour for speed.
            spritecollide = sprite.rect.colliderect
            for s in group:
                if spritecollide(s.rect):
                    s.kill()
                    return s
        else:
            for s in group:
                if collided(sprite, s):
                    s.kill()
                    return s
        return None

#This class controls the arena background
class Arena(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image, self.rect = game.load_image("menu/arena.jpg", -1)
        self.dy = 5
        self.reset()
    
    def update(self):
        self.rect.bottom += self.dy
        if self.rect.bottom >= 1200:
            self.reset()
            
    def reset(self):
        self.rect.top = -600
        
#Player
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image, self.rect = game.load_image("sprites/jogador.png", -1)
        self.rect.center = (400,500)
        self.dx = 0
        self.dy = 0
        self.reset()
        self.laser_timer = 0
        self.laser_max = 5
        
        
        
    def update(self):
        self.rect.move_ip((self.dx, self.dy))
        
        #Fire the laser
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.laser_timer = self.laser_timer + 1
            if self.laser_timer == self.laser_max:
                game.laser_sprites.add(Laser(self.rect.midtop, game))
                game.fire.play()
                self.laser_timer = 0
        
    def reset(self):
        self.rect.bottom = 600  

#Laser class
class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image, self.rect = game.load_image("sprites/laser.png", -1)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    
    def update(self):
        if self.rect.top < 0:
            self.kill()
        else:    
            self.rect.move_ip(0, -25)  

#Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.font = pygame.font.Font("data/fonts/arial.ttf", 36)
        self.setValue()
        self.num = int(self.text)
        self.image = self.font.render(self.text, 1, (random.randrange(0, 255),
                                                     random.randrange(0, 255),
                                                     random.randrange(0, 255)))
        self.rect = self.image.get_rect()
        self.dy = random.randrange(3, 6)
        self.reset()
        
    def setValue(self):
        val = eval(game.operation.text)
        if val + 3 > 10:
            self.text = str(random.choice(range(int(1.5 *val)) + [val] * val))
        else:
            self.text = str(random.choice(range(10)+ [val] * 10))
            
    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.top > game.screen.get_height():
            self.kill()
           
        #Laser Collisions    
        if game.sprite_collide_any(self, game.laser_sprites):
            game.explosion_sprites.add(EnemyExplosion(self.rect.center, game))
            game.explode.play()
            if eval(game.operation.text) == self.num:
                print "Acertou!!!" 
                game.score.score += 10
                game.operation.generate()
            else:
                print "Errou..."
                game.score.score -= 10
            self.kill()
           
    def reset(self):
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, game.screen.get_width())
        self.dy = random.randrange(5, 10)
        self.dx = random.randrange(-2, 2)
    
class Enemy_Train(Enemy):
    def __init__(self, game):
        Enemy.__init__(self, game)
        
    def setValue(self):
        self.text = str(eval(self.game.op_train.text))
        
    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.top > game.screen.get_height():
            self.kill()
           
        #Laser Collisions    
        if game.sprite_collide_any(self, game.laser_sprites):
            game.explosion_sprites.add(EnemyExplosion(self.rect.center, game))
            game.explode.play()
            self.kill()
            game.op_train.generate()
            game.shots_counter += 1
        
class EnemyExplosion(pygame.sprite.Sprite):
    def __init__(self, pos, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image, self.rect = game.load_image("sprites/explosao.png", -1)
        self.rect.center = pos        
        self.counter = 0
        self.max_count = 10
    def update(self):
        self.counter = self.counter + 1
        if self.counter == self.max_count:
            self.kill()
            
class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.font = pygame.font.Font("data/fonts/DejaVuLGCSansMono-Bold.ttf", 28)
        
    def update(self):
        self.text = "Pontos: %d" % (self.score,)
        self.image = self.font.render(self.text, 1, (0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (400,20)

class Operation(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.setFont()
        self.generate()
                  
    def setFont(self):
        self.font = pygame.font.Font(
                                "data/fonts/DejaVuLGCSansMono-Bold.ttf", 28)
    def update(self):
        self.image = self.font.render(self.text, 1, (0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (100,20)
            
    def generate(self):
        ok = False
        while not ok:
            operator = [' + ', ' - ', ' * ', ' / ']
            random.shuffle(operator)
            self.op = operator.pop()
            self.first = str(random.randrange(0, 10))
            self.second = str(random.randrange(0, 10))
            self.text =  self.first + self.op + self.second
            if (self.op == ' / ') and (self.second != '0')\
                                    and (self.first != '0'):
                if int(self.first) % int(self.second) == 0:
                	if (int(self.first) > int(self.second)):
                		ok = True
                	else:
                		ok = False
            elif (self.op == ' - ') and (int(self.first) < int(self.second)):
                ok = False 
            elif(self.first != '0') and (self.second != '0'):
                ok = True
            else:
            	ok = False

class OperationTrain(Operation):
    def __init__(self):
        Operation.__init__(self)                   
        self.generate()
    
    def setFont(self):
        self.font = pygame.font.Font(
                                "data/fonts/DejaVuLGCSansMono-Bold.ttf", 48)                    
    def update(self):
        self.image = self.font.render(self.text, 1, (0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (400,20)
                        
class Gameover(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font("data/fonts/planet5.ttf", 48)
        
    def update(self):
        self.text = ("GAME OVER")
        self.image = self.font.render(self.text, 1, (0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (400,300)
        
class Gameoveresc(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(
                                "data/fonts/DejaVuLGCSansMono-Bold.ttf", 28)
        
    def update(self):
        self.text = "PRESSIONE ESC PARA RETORNAR"
        self.image = self.font.render(self.text, 1, (0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (400,400)
                    

#Class Module
class Menu:

#Define the initalize self options
    def __init__(self, *options):

        self.options = options
        self.x = 0
        self.y = 0
        self.font = pygame.font.Font(None, 32)
        self.option = 0
        self.width = 1
        self.color = [0, 0, 0]
        self.hcolor = [0, 0, 0]
        self.height = len(self.options)*self.font.get_height()
        for o in self.options:
            text = o[0]
            ren = self.font.render(text, 1, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()

#Draw the menu
    def draw(self, surface):
        i=0
        for o in self.options:
            if i==self.option:
                clr = self.hcolor
            else:
                clr = self.color
            text = o[0]
            ren = self.font.render(text, 1, clr)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            surface.blit(ren, (self.x, self.y + i*self.font.get_height()))
            i+=1

#Menu Input            
    def update(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    self.option += 1
                if e.key == pygame.K_UP:
                    self.option -= 1
                if e.key == pygame.K_RETURN:
                    self.options[self.option][1]()
        if self.option > len(self.options)-1:
            self.option = 0
        if self.option < 0:
            self.option = len(self.options)-1
            
#Position Menu
    def set_pos(self, x, y):
        self.x = x
        self.y = y

#Font Style        
    def set_font(self, font):
        self.font = font

#Highlight Color        
    def set_highlight_color(self, color):
        self.hcolor = color

#Font Color        
    def set_normal_color(self, color):
        self.color = color

#Font position        
    def center_at(self, x, y):
        self.x = x-(self.width/2)
        self.y = y-(self.height/2)
        
class Teacher(pygame.sprite.Sprite):
    
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image, self.rect = game.load_image("sprites/professor.png", -1)
        self.rect = self.image.get_rect()
        self.rect.center = (700, 300)

    
    def update(self):
        pass
    
class Speech(pygame.sprite.Sprite):  
      
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
    
    def update(self, image, pos = (500, 300)):
        self.image, self.rect = game.load_image(image, -1)
        self.rect = self.image.get_rect()
        self.rect.center = pos
    
class Big_Operation(Operation):
    def __init__(self, game):
        Operation.__init__(self)                   
        self.game = game
    def setFont(self):
        self.font = pygame.font.Font(
                                "data/fonts/DejaVuLGCSansMono-Bold.ttf", 72)                    
    def update(self):
        self.text = game.op_train.text
        self.image = self.font.render(self.text, 1, (0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (400,300)
        
if __name__ == "__main__":
    game = Game()
    game.main_menu()
