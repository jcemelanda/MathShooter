import random
from typing import TYPE_CHECKING

import pygame
from pygame.locals import K_SPACE

import assets
from config import (
    ENEMY_MAX_SPEED,
    ENEMY_MIN_SPEED,
    LASER_COOLDOWN,
    LASER_SPEED,
    PLAYER_SPEED,
    PLAYER_START_POS,
)

if TYPE_CHECKING:
    from game import Game


class Arena(pygame.sprite.Sprite):
    """Controla o fundo da arena com efeito de rolagem infinita."""

    def __init__(self, game: "Game"):
        super().__init__()
        self.game = game
        assert assets.images is not None
        self.image = assets.images.arena
        self.rect = self.image.get_rect()
        self.dy = 5
        self.reset()

    def update(self) -> None:
        """Atualiza a posição do fundo para criar efeito de movimento."""
        self.rect.bottom += self.dy
        if self.rect.bottom >= 1200:
            self.reset()

    def reset(self) -> None:
        """Reinicia a posição do fundo no topo."""
        self.rect.top = -600


class Player(pygame.sprite.Sprite):
    """Representa a nave do jogador e controla seu movimento e tiro."""

    def __init__(self, game: "Game"):
        super().__init__()
        self.game = game
        assert assets.images is not None
        self.image = assets.images.player
        self.rect = self.image.get_rect()
        self.rect.center = PLAYER_START_POS
        self.dx = 0
        self.dy = 0
        self.laser_timer = 0
        self.laser_max = LASER_COOLDOWN
        self.reset()

    def update(self) -> None:
        """Processa entrada do teclado e atualiza posição da nave."""
        keys = pygame.key.get_pressed()
        self.dx = 0
        self.dy = 0

        if keys[pygame.K_LEFT]:
            self.dx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.dx = PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.dy = -PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.dy = PLAYER_SPEED

        self.rect.move_ip((self.dx, self.dy))

        # Atirar laser
        if keys[K_SPACE]:
            self.laser_timer += 1
            if self.laser_timer >= self.laser_max:
                self.game.laser_sprites.add(Laser(self.rect.midtop, self.game))
                assert assets.sounds is not None
                assets.sounds.laser.play()
                self.laser_timer = 0
        else:
            self.laser_timer = self.laser_max  # Permite atirar imediatamente no próximo clique

    def reset(self) -> None:
        """Reposiciona o jogador no ponto inicial."""
        self.rect.bottom = 600


class Laser(pygame.sprite.Sprite):
    """Representa o projétil disparado pelo jogador."""

    def __init__(self, pos: tuple[int, int], game: "Game"):
        super().__init__()
        self.game = game
        assert assets.images is not None
        self.image = assets.images.laser
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self) -> None:
        """Move o laser para cima e remove se sair da tela."""
        if self.rect.top < 0:
            self.kill()
        else:
            self.rect.move_ip(0, -LASER_SPEED)


class Enemy(pygame.sprite.Sprite):
    """Inimigo básico que carrega um valor numérico para o desafio matemático."""

    def __init__(self, game: "Game"):
        super().__init__()
        self.game = game
        if not assets.fonts:
            raise RuntimeError("Fonts NOT initialized")
        self.font = assets.fonts.enemy
        self.set_value()
        self.num = int(self.text)

        # Cor aleatória para o texto
        text_color = (
            random.randrange(50, 255),
            random.randrange(50, 255),
            random.randrange(50, 255),
        )

        self.image = self.font.render(self.text, True, text_color)
        self.rect = self.image.get_rect()
        self.dx: int = 0
        self.dy: int = 0
        self.reset()

    def set_value(self) -> None:
        """Define o valor do inimigo baseado na operação atual."""
        correct_val = int(eval(self.game.operation.text))
        if correct_val + 3 > 10:
            choices = list(range(int(1.5 * correct_val))) + [correct_val] * correct_val
            self.text = str(random.choice(choices))
        else:
            self.text = str(random.choice(list(range(10)) + [correct_val] * 10))

    def update(self) -> None:
        """Atualiza posição e verifica colisões."""
        self.rect.centerx += self.dx
        self.rect.centery += self.dy

        if self.rect.top > self.game.screen.get_height():
            self.kill()

        # Colisão com Laser
        if self.game.sprite_collide_any(self, self.game.laser_sprites):
            self.game.explosion_sprites.add(EnemyExplosion(self.rect.center, self.game))
            assert assets.sounds is not None
            assets.sounds.explosion.play()

            if eval(self.game.operation.text) == self.num:
                self.game.score.score += 10
                self.game.operation.generate()
            else:
                self.game.score.score -= 10
            self.kill()

    def reset(self) -> None:
        """Reseta posição do inimigo no topo da tela em local aleatório."""
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, self.game.screen.get_width())
        self.dy = random.randrange(ENEMY_MIN_SPEED + 2, ENEMY_MAX_SPEED + 4)
        self.dx = random.randrange(-2, 2)


class EnemyTrain(Enemy):
    """Inimigo específico para o modo treinamento."""

    def set_value(self) -> None:
        """No treino, o inimigo sempre carrega a resposta correta."""
        self.text = str(int(eval(self.game.op_train.text)))

    def update(self) -> None:
        """Atualiza posição e gera nova operação ao ser atingido."""
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.top > self.game.screen.get_height():
            self.kill()

        if self.game.sprite_collide_any(self, self.game.laser_sprites):
            self.game.explosion_sprites.add(EnemyExplosion(self.rect.center, self.game))
            assert assets.sounds is not None
            assets.sounds.explosion.play()
            self.kill()
            self.game.op_train.generate()
            self.game.shots_counter += 1


class EnemyExplosion(pygame.sprite.Sprite):
    """Efeito visual de explosão quando um inimigo é destruído."""

    def __init__(self, pos: tuple[int, int], game: "Game"):
        super().__init__()
        self.game = game
        assert assets.images is not None
        self.image = assets.images.explosion
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.counter = 0
        self.max_count = 10

    def update(self) -> None:
        """Controla o tempo de exibição da explosão."""
        self.counter += 1
        if self.counter == self.max_count:
            self.kill()
