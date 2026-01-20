"""
Configurações globais do jogo MathShooter.
Centraliza constantes para facilitar o ajuste fino e manutenção.
"""

# Tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

# Cores (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 85, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Gameplay - Jogador
PLAYER_START_POS = (400, 500)
PLAYER_SPEED = 10
LASER_SPEED = 25
LASER_COOLDOWN = 5

# Gameplay - Inimigos
ENEMY_MIN_SPEED = 3
ENEMY_MAX_SPEED = 6
ENEMY_SPAWN_DECREMENT_LIMIT = 35
ENEMY_SPAWN_RATE_BASE = 40
ENEMY_TRAIN_SPAWN_RATE = 50

# Pontuação
SCORE_CENTER = (400, 20)
OP_CENTER = (100, 20)
GAME_OVER_THRESHOLD = -100

# Estados do Jogo
class GameState:
    MENU = "menu"
    TRAINING = "training"
    PLAYING = "playing"
    MISSION = "mission"
    ABOUT = "about"
    GAMEOVER = "gameover"
    QUIT = "quit"
