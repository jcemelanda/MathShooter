"""
Módulo de gerenciamento de assets do jogo.

Usa LRU Cache para otimizar o carregamento e armazenamento de assets frequentemente usados.
"""

from pathlib import Path
from typing import Tuple
import pygame

# Caminhos
ASSETS_DIR = Path("data")
FONTS_DIR = ASSETS_DIR / "fonts"
SPRITES_DIR = ASSETS_DIR / "sprites"
SOUNDS_DIR = ASSETS_DIR / "sounds"


class _DummySound:
    """Sound dummy para quando não há áudio"""
    def play(self): pass
    def stop(self): pass
    def set_volume(self, volume): pass


def load_image(name: str, colorkey= None) -> Tuple[pygame.Surface, pygame.Rect]:
    """Carrega uma imagem do diretório de sprites"""
    path = ASSETS_DIR / name
    try:
        image = pygame.image.load(path).convert()
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image, image.get_rect()
    except (pygame.error, FileNotFoundError) as e:
        print(f"Erro ao carregar: {path}")
        # Retorna imagem de fallback
        fallback = pygame.Surface((32, 32))
        fallback.fill((255, 0, 255))  # Magenta para indicar erro
        return fallback, fallback.get_rect()
    

def load_sound(name: str) -> pygame.mixer.Sound:
    """Carrega asset de som"""
    path = SOUNDS_DIR / name
    if not pygame.mixer.get_init():
        return _DummySound()
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        return _DummySound()
    

def get_font(name: str, size: int, bold: bool = False) -> pygame.font.Font:
    """Carrega asset de fonte"""
    try:
        font_path = FONTS_DIR / name
        return pygame.font.Font(font_path, size)
    except:
        return pygame.font.SysFont(name, size, bold=bold)
