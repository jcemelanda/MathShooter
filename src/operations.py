import random
from typing import TYPE_CHECKING
import pygame
import assets
from config import CYAN, OP_CENTER

if TYPE_CHECKING:
    from game import Game

class Operation(pygame.sprite.Sprite):
    """Gera e exibe operações matemáticas aleatórias para o jogador resolver."""
    
    def __init__(self, game: "Game"):
        super().__init__()
        self.game = game
        self.setFont()
        self.rendered_text: str = ""
        self.text: str = ""
        self.generate()
                  
    def setFont(self) -> None:
        self.font = assets.fonts.operation

    def update(self) -> None:
        """Renderiza a operação apenas se o texto mudar."""
        if self.rendered_text != self.text:
            self.rendered_text = self.text
            self.image = self.font.render(self.text, True, CYAN)
            self.rect = self.image.get_rect(center=OP_CENTER)
            
    def generate(self) -> None:
        """Gera uma nova operação válida (evita divisão por zero e resultados negativos)."""
        valid = False
        while not valid:
            op = random.choice([' + ', ' - ', ' * ', ' / '])
            a, b = random.randrange(1, 10), random.randrange(1, 10)
            
            if op == ' / ':
                # Garante divisão exata e evita 1 / x
                a = b * random.randrange(1, 5)
                valid = a != b # Evita divisões triviais como 5/5
            elif op == ' - ':
                # Evita resultados negativos
                if a < b: a, b = b, a
                valid = a != b
            else:
                valid = True
                
            self.text = f"{a}{op}{b}"

class OperationTrain(Operation):
    """Versão da operação para o modo de treinamento."""
    
    def setFont(self) -> None:
        self.font = assets.fonts.op_train

    def update(self) -> None:
        self.text = self.game.op_train.text
        if self.rendered_text != self.text:
            self.rendered_text = self.text
            self.image = self.font.render(self.text, True, CYAN)
            self.rect = self.image.get_rect(center=(400, 300))

class Big_Operation(Operation):
    """Exibe a operação de forma ampliada no centro da tela."""

    def setFont(self) -> None:
        self.font = assets.fonts.op_large

    def update(self) -> None:
        self.text = self.game.op_train.text
        if self.rendered_text != self.text:
            self.rendered_text = self.text
            self.image = self.font.render(self.text, True, CYAN)
            self.rect = self.image.get_rect(center=(400, 300))
