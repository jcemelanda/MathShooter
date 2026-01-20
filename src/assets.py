from pathlib import Path
from typing import Any, NamedTuple, Optional

import pygame

from config import MAGENTA

# Caminhos
ASSETS_DIR = Path(__file__).parent / "data"
FONTS_DIR = ASSETS_DIR / "fonts"
SOUNDS_DIR = ASSETS_DIR / "sounds"


class _DummySound:
    """Sound dummy para quando não há áudio"""

    def play(self, loops: int = 0) -> None:
        pass

    def stop(self) -> None:
        pass

    def set_volume(self, volume: float) -> None:
        pass


class ImageAssets(NamedTuple):
    player: pygame.Surface
    laser: pygame.Surface
    explosion: pygame.Surface
    arena: pygame.Surface
    teacher: pygame.Surface
    speech1: pygame.Surface
    speech2: pygame.Surface
    speech3: pygame.Surface
    speech4: pygame.Surface
    speech5: pygame.Surface
    speech6: pygame.Surface
    speech7: pygame.Surface
    speech8: pygame.Surface
    icon: pygame.Surface


class SoundAssets(NamedTuple):
    laser: pygame.mixer.Sound | _DummySound
    explosion: pygame.mixer.Sound | _DummySound
    background_music: Optional[Any]


class FontAssets(NamedTuple):
    score: pygame.font.Font
    operation: pygame.font.Font
    game_over: pygame.font.Font
    train: pygame.font.Font
    enemy: pygame.font.Font
    menu_title: pygame.font.Font
    menu_item: pygame.font.Font
    menu_info: pygame.font.Font
    menu_about: pygame.font.Font
    op_train: pygame.font.Font
    op_large: pygame.font.Font


# Globals
images: Optional[ImageAssets] = None
sounds: Optional[SoundAssets] = None
fonts: Optional[FontAssets] = None


def load_image(name: str, colorkey: int | pygame.Color | None = None) -> pygame.Surface:
    """Carrega uma imagem do diretório de sprites"""
    path = ASSETS_DIR / name
    try:
        image = pygame.image.load(str(path))
        if pygame.display.get_init() and pygame.display.get_surface():
            image = image.convert()

        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    except (pygame.error, FileNotFoundError):
        print(f"Erro ao carregar imagem: {path}")
        # Retorna imagem de fallback
        fallback = pygame.Surface((32, 32))
        fallback.fill(MAGENTA)
        return fallback


def load_sound(name: str) -> pygame.mixer.Sound | _DummySound:
    """Carrega asset de som"""
    path = SOUNDS_DIR / name
    if not pygame.mixer.get_init():
        return _DummySound()
    try:
        return pygame.mixer.Sound(str(path))
    except pygame.error:
        print(f"Erro ao carregar som: {path}")
        return _DummySound()


def load_music(name: str) -> Optional[Any]:
    """Carrega música para o mixer"""
    path = ASSETS_DIR / f"music/{name}"
    try:
        pygame.mixer.music.load(str(path))
        return pygame.mixer.music
    except pygame.error:
        print(f"Erro ao carregar música: {path}")
        return None


def get_font(name: str, size: int, bold: bool = False) -> pygame.font.Font:
    """Carrega asset de fonte"""
    try:
        font_path = FONTS_DIR / name
        return pygame.font.Font(font_path, size)
    except Exception:
        return pygame.font.SysFont(name, size, bold=bold)


def initialize() -> None:
    """Inicializa todos os assets globais. Deve ser chamado após pygame.init()"""
    global images, sounds, fonts

    # Imagens
    images = ImageAssets(
        player=load_image("sprites/jogador.png", -1),
        laser=load_image("sprites/laser.png", -1),
        explosion=load_image("sprites/explosao.png", -1),
        arena=load_image("menu/arena.jpg", -1),
        teacher=load_image("sprites/professor.png", -1),
        speech1=load_image("sprites/fala1.png", -1),
        speech2=load_image("sprites/fala2.png", -1),
        speech3=load_image("sprites/fala3.png", -1),
        speech4=load_image("sprites/fala4.png", -1),
        speech5=load_image("sprites/fala5.png", -1),
        speech6=load_image("sprites/fala6.png", -1),
        speech7=load_image("sprites/fala7.png", -1),
        speech8=load_image("sprites/fala8.png", -1),
        icon=load_image("Math Shooter.png", -1),
    )

    # Sons
    sounds = SoundAssets(
        laser=load_sound("laser.ogg"),
        explosion=load_sound("explosao.ogg"),
        background_music=load_music("Stone Fortress.ogg"),
    )

    # Fontes
    fonts = FontAssets(
        score=get_font("DejaVuLGCSansMono-Bold.ttf", 28),
        operation=get_font("DejaVuLGCSansMono-Bold.ttf", 28),
        game_over=get_font("planet5.ttf", 48),
        train=get_font("planet5.ttf", 48),
        enemy=get_font("arial.ttf", 36),
        menu_title=get_font("planet5.ttf", 48),
        menu_item=get_font("DejaVuLGCSansMono.ttf", 32),
        menu_info=get_font("arial.ttf", 22),
        menu_about=get_font("arial.ttf", 28),
        op_train=get_font("DejaVuLGCSansMono-Bold.ttf", 48),
        op_large=get_font("DejaVuLGCSansMono-Bold.ttf", 72),
    )
