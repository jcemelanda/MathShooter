import os
import sys
from typing import List, Optional, Generator, Any
import pygame

import assets
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, DARK_GREEN, GREEN,
    GAME_OVER_THRESHOLD, ENEMY_SPAWN_DECREMENT_LIMIT, ENEMY_SPAWN_RATE_BASE,
    GameState
)
from entities import Player, Arena, Enemy, Laser, EnemyExplosion, Enemy_Train
from ui import Score, Menu, Gameover, Gameoveresc, Teacher, Speech
from operations import Operation, OperationTrain, Big_Operation
from interfaces import Updatable, Drawable

class Game:
    """Controlador principal do jogo MathShooter.
    
    Gerencia o loop principal, transições de estado, processamento de entradas
    e coordenação entre entidades e UI.
    """

    def __init__(self) -> None:
        """Inicializa o motor de jogo, assets e configurações básicas."""
        os.environ['SDL2_VIDEO_CENTERED'] = "1"
        pygame.init()
        assets.initialize()
        
        pygame.display.set_caption("Math Shooter")
        if assets.images.icon:
            pygame.display.set_icon(assets.images.icon)
            
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
        pygame.mouse.set_visible(False)
        
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(BLACK)
        
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        
        # Singleton-like music initialization
        if assets.sounds.background_music:
            assets.sounds.background_music.play(-1)

    def _reset_groups(self) -> None:
        """Limpa todos os grupos de sprites para um novo estado de jogo."""
        self.arena = pygame.sprite.RenderPlain(Arena(self))
        self.player_sprite = pygame.sprite.RenderPlain()
        self.enemy_sprites = pygame.sprite.RenderPlain()
        self.laser_sprites = pygame.sprite.RenderPlain()
        self.explosion_sprites = pygame.sprite.RenderPlain()
        self.ui_sprites = pygame.sprite.RenderPlain()
        self.operation_sprite = pygame.sprite.Group()

    def main_loop(self) -> None:
        """Loop de gerenciamento de estados principal."""
        while self.state != GameState.QUIT:
            if self.state == GameState.MENU:
                self.main_menu()
            elif self.state == GameState.TRAINING:
                self.run_training()
            elif self.state == GameState.PLAYING:
                self.run_gameplay()
            elif self.state == GameState.MISSION:
                self.show_static_screen(GameState.MISSION)
            elif self.state == GameState.ABOUT:
                self.show_static_screen(GameState.ABOUT)
        
        pygame.quit()
        sys.exit()

    def main_menu(self) -> None:
        """Exibe e gerencia o menu principal."""
        self._reset_groups()
        
        title = Menu(["Math Shooter"])
        title.center_at(150, 150)
        title.font = assets.fonts.menu_title
        title.highlight_color = GREEN
        
        menu = Menu(
            ["Treinar", lambda: setattr(self, 'state', GameState.TRAINING)],
            ["Iniciar", lambda: setattr(self, 'state', GameState.PLAYING)],
            ["Missão", lambda: setattr(self, 'state', GameState.MISSION)],
            ["Sobre", lambda: setattr(self, 'state', GameState.ABOUT)],
            ["Sair", lambda: setattr(self, 'state', GameState.QUIT)]
        )
        menu.center_at(400, 320)
        menu.highlight_color = GREEN
        menu.normal_color = DARK_GREEN

        while self.state == GameState.MENU:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.state = GameState.QUIT
            
            menu.update(events)
            
            self.screen.blit(self.background, (0, 0))
            self.arena.update()
            self.arena.draw(self.screen)
            title.draw(self.screen)
            menu.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

    def run_gameplay(self) -> None:
        """Executa o loop principal de gameplay."""
        self._reset_groups()
        self.player = Player(self)
        self.score = Score()
        self.operation = Operation(self)
        
        self.player_sprite.add(self.player)
        self.ui_sprites.add(self.score)
        self.operation_sprite.add(self.operation)
        
        counter = 0
        loop_counter = 0
        difficulty_dec = 1
        
        playing = True
        while playing and self.state == GameState.PLAYING:
            self.clock.tick(FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.state = GameState.QUIT
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = GameState.MENU
                    playing = False

            # Lógica de Spawn
            loop_counter += 1
            counter += 1
            if loop_counter % 90 == 0 and difficulty_dec < ENEMY_SPAWN_DECREMENT_LIMIT:
                difficulty_dec += 1
            
            if counter >= ENEMY_SPAWN_RATE_BASE - difficulty_dec:
                self.enemy_sprites.add(Enemy(self))
                counter = 0

            # Updates & Drawing
            groups = [self.arena, self.player_sprite, self.enemy_sprites, 
                     self.laser_sprites, self.explosion_sprites, self.ui_sprites, 
                     self.operation_sprite]
            self.screen.blit(self.background, (0, 0))
            for group in groups:
                group.update()
                group.draw(self.screen)
            
            pygame.display.flip()

            if self.score.score < GAME_OVER_THRESHOLD:
                self.run_gameover()
                playing = False

    def run_gameover(self) -> None:
        """Exibe a tela de Game Over e aguarda retorno ao menu."""
        go_title = Gameover()
        go_esc = Gameoveresc()
        go_group = pygame.sprite.RenderPlain(go_title, go_esc)
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = GameState.QUIT
                    waiting = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = GameState.MENU
                    waiting = False
            
            self.screen.blit(self.background, (0, 0))
            self.arena.draw(self.screen)
            go_group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

    def _tutorial_script(self) -> Generator[List[pygame.sprite.Group], None, None]:
        """Gerador que define a sequência de eventos do tutorial."""
        self.teacher = Teacher()
        self.speech = Speech()
        self.op_train = OperationTrain(self)
        self.big_op = Big_Operation(self)
        
        teacher_group = pygame.sprite.RenderPlain(self.teacher)
        speech_group = pygame.sprite.RenderPlain(self.speech)
        big_op_group = pygame.sprite.RenderPlain(self.big_op)
        
        # Introdução
        for msg in ['speech1', 'speech2']:
            for _ in range(70):
                self.speech.update(msg)
                yield [self.arena, teacher_group, speech_group]
        
        # Operação Grande
        for _ in range(60):
            yield [self.arena, big_op_group, teacher_group]
            
        # Instrução de tiro
        for _ in range(70):
            self.speech.update('speech3')
            yield [self.arena, teacher_group, speech_group]
            
        # Treino Ativo
        self.player_sprite.add(self.player)
        self.operation_sprite.add(self.op_train)
        self.shots_counter = 0
        loop_counter = 0
        
        while self.shots_counter < 10:
            if loop_counter % 50 == 0:
                self.enemy_sprites.add(Enemy_Train(self))
            loop_counter += 1
            yield [self.arena, self.player_sprite, self.enemy_sprites, 
                   self.laser_sprites, self.explosion_sprites, self.operation_sprite]

        # Finalização
        for msg in ['speech5', 'speech7']:
            for _ in range(70):
                self.speech.update(msg)
                yield [self.arena, teacher_group, speech_group]

    def run_training(self) -> None:
        """Modo tutorial/treinamento gerenciado por um script gerador."""
        self._reset_groups()
        self.player = Player(self)
        script = self._tutorial_script()
        
        training = True
        while training and self.state == GameState.TRAINING:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.state = GameState.QUIT
                    training = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = GameState.MENU
                    training = False

            try:
                groups = next(script)
                self.screen.blit(self.background, (0, 0))
                for group in groups:
                    group.update()
                    group.draw(self.screen)
                pygame.display.flip()
                self.clock.tick(FPS)
            except StopIteration:
                self.state = GameState.PLAYING
                training = False

    def _show_tutorial_messages(self, messages: List[str], sprites: pygame.sprite.Group) -> None:
        """Helper para exibir sequência de falas no treinamento."""
        for msg in messages:
            for _ in range(70):
                self.speech.update(msg)
                if not self._tutorial_step([self.arena, sprites, pygame.sprite.RenderPlain(self.speech)]):
                    return

    def _tutorial_step(self, groups: List[pygame.sprite.Group]) -> bool:
        """Um único frame de atualização e desenho para o modo tutorial."""
        self.clock.tick(FPS)
        self.screen.blit(self.background, (0, 0))
        for group in groups:
            group.update()
            group.draw(self.screen)
        pygame.display.flip()
        return self.state == GameState.TRAINING

    def show_static_screen(self, screen_type: str) -> None:
        """Exibe telas estáticas como Mission e About."""
        self._reset_groups()
        
        title = Menu(["Math Shooter"])
        title.center_at(150, 150)
        title.font = assets.fonts.menu_title
        title.highlight_color = GREEN
        
        content_text = []
        if screen_type == GameState.MISSION:
            content_text = [
                "Você deve atirar nos números que são resposta para a operação",
                "mostrada no canto superior esquerdo da tela.",
                "Navegue com as setas, atire com ESPAÇO.",
                "Acertos: +10 pontos | Erros: -10 pontos.",
                "Game Over ao chegar em -100 pontos.",
                "", "PRESSIONE ESC PARA RETORNAR"
            ]
            font = assets.fonts.menu_info
        else: # ABOUT
            content_text = [
                "Versão de testes de Math Shooter.",
                "Distribuído sob a GPL.",
                "Desenvolvido por Júlio César Eiras Melanda.",
                "", "PRESSIONE ESC PARA RETORNAR"
            ]
            font = assets.fonts.menu_about

        content = Menu(*[[line] for line in content_text])
        content.center_at(400, 310 if screen_type == GameState.ABOUT else 350)
        content.font = font
        content.normal_color = GREEN

        while self.state == screen_type:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = GameState.QUIT
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = GameState.MENU

            self.screen.blit(self.background, (0, 0))
            self.arena.update()
            self.arena.draw(self.screen)
            title.draw(self.screen)
            content.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

    def sprite_collide_any(self, sprite: pygame.sprite.Sprite, group: pygame.sprite.Group) -> Optional[pygame.sprite.Sprite]:
        """Versão simplificada e pythonic de colisão."""
        collisions = pygame.sprite.spritecollide(sprite, group, True)
        return collisions[0] if collisions else None
