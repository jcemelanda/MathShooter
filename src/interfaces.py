from typing import Any, NamedTuple, Optional, Protocol, runtime_checkable

import pygame


@runtime_checkable
class Drawable(Protocol):
    """Protocol para objetos que podem ser desenhados em uma superfície."""

    def draw(self, surface: pygame.Surface) -> None: ...


@runtime_checkable
class Updatable(Protocol):
    """Protocol para objetos que possuem lógica de atualização por frame."""

    def update(self, *args: Any, **kwargs: Any) -> None: ...
