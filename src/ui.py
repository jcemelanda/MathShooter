from typing import Any, List, Optional, Tuple, TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from game import Game

import assets
from config import GREEN, SCORE_CENTER


class Score(pygame.sprite.Sprite):
    """Exibe a pontuação atual do jogador na tela."""

    def __init__(self) -> None:
        super().__init__()
        self._score = 0
        assert assets.fonts is not None
        self.font = assets.fonts.operation
        self.text: str = ""
        self._render()

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, value: int) -> None:
        if self._score != value:
            self._score = value
            self._render()

    def _render(self) -> None:
        """Renderiza o texto da pontuação."""
        self.text = f"Pontos: {self._score}"
        self.image = self.font.render(self.text, True, GREEN)
        self.rect = self.image.get_rect(center=SCORE_CENTER)

    def update(self) -> None:
        pass  # Renders are now reactive via the setter


class Gameover(pygame.sprite.Sprite):
    """Exibe a mensagem 'GAME OVER' na tela."""

    def __init__(self) -> None:
        super().__init__()
        assert assets.fonts is not None
        self.font = assets.fonts.game_over
        self.text = "GAME OVER"
        self.image = self.font.render(self.text, True, GREEN)
        self.rect = self.image.get_rect(center=(400, 300))

    def update(self) -> None:
        pass


class Gameoveresc(pygame.sprite.Sprite):
    """Exibe instruções para retornar ao menu após o Game Over."""

    def __init__(self) -> None:
        super().__init__()
        assert assets.fonts is not None
        self.font = assets.fonts.score
        self.text = "PRESSIONE ESC PARA RETORNAR"
        self.image = self.font.render(self.text, True, GREEN)
        self.rect = self.image.get_rect(center=(400, 400))

    def update(self) -> None:
        pass


class Menu:
    """Sistema de menu genérico com suporte a navegação e callbacks."""

    def __init__(self, *options: List[Any]) -> None:
        self.options = options
        self.x = 0
        self.y = 0
        assert assets.fonts is not None
        self._font = assets.fonts.menu_item
        self._option = 0
        self.width = 1
        self._color = (0, 0, 0)
        self._hcolor = (0, 0, 0)
        self.height = len(self.options) * self._font.get_height()
        self.dirty = True
        self.cache_normal: list[pygame.Surface] = []
        self.cache_highlight: list[pygame.Surface] = []

    @property
    def option(self) -> int:
        return self._option

    @option.setter
    def option(self, value: int) -> None:
        # Garante que o índice esteja dentro dos limites
        self._option = value % len(self.options)

    @property
    def font(self) -> pygame.font.Font:
        return self._font

    @font.setter
    def font(self, value: pygame.font.Font) -> None:
        self._font = value
        self.height = len(self.options) * self._font.get_height()
        self.dirty = True

    @property
    def normal_color(self) -> tuple[int, int, int]:
        return self._color

    @normal_color.setter
    def normal_color(self, color: tuple[int, int, int]) -> None:
        self._color = color
        self.dirty = True

    @property
    def highlight_color(self) -> tuple[int, int, int]:
        return self._hcolor

    @highlight_color.setter
    def highlight_color(self, color: tuple[int, int, int]) -> None:
        self._hcolor = color
        self.dirty = True

    def _render_cache(self) -> None:
        """Prerenderiza as opções do menu para otimizar o desenho."""
        self.cache_normal = []
        self.cache_highlight = []
        self.width = 1

        for o in self.options:
            text = str(o[0])
            # Normal
            ren = self._font.render(text, True, self._color)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            self.cache_normal.append(ren)

            # Highlight
            ren_h = self._font.render(text, True, self._hcolor)
            if ren_h.get_width() > self.width:
                self.width = ren_h.get_width()
            self.cache_highlight.append(ren_h)

    def draw(self, surface: pygame.Surface) -> None:
        """Desenha o menu na superfície fornecida."""
        if self.dirty:
            self._render_cache()
            self.dirty = False

        for i, _ in enumerate(self.options):
            ren = self.cache_highlight[i] if i == self._option else self.cache_normal[i]
            surface.blit(ren, (self.x, self.y + i * self._font.get_height()))

    def update(self, events: list[pygame.event.Event]) -> None:
        """Processa eventos de navegação e seleção do menu."""
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    self.option += 1  # Setter handles modulo
                elif e.key == pygame.K_UP:
                    self.option -= 1
                elif e.key == pygame.K_RETURN:
                    if len(self.options[self._option]) > 1:
                        self.options[self._option][1]()

    def set_pos(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    def center_at(self, x: int, y: int) -> None:
        """Centraliza o menu em relação às coordenadas X e Y."""
        if self.dirty:
            self._render_cache()
            self.dirty = False
        self.x = int(x - (self.width / 2))
        self.y = int(y - (self.height / 2))


class Teacher(pygame.sprite.Sprite):
    """Sprite do professor no modo treinamento."""

    def __init__(self, game: "Game"):
        super().__init__()
        self.game = game
        assert assets.images is not None
        self.image = assets.images.teacher
        self.rect = self.image.get_rect(center=(700, 300))

    def update(self) -> None:
        pass


class Speech(pygame.sprite.Sprite):
    """Exibe balões de fala do professor."""

    def __init__(self) -> None:
        super().__init__()

    def update(self, image_name: str, pos: tuple[int, int] = (500, 300)) -> None:
        """Atualiza a imagem e posição do balão de fala."""
        self.image = getattr(assets.images, image_name)
        self.rect = self.image.get_rect(center=pos)
