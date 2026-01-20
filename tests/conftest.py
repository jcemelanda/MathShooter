import sys
import os
from unittest.mock import MagicMock
import pygame

# Set up paths
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

def mock_pygame_and_assets():
    """Mocks common pygame modules and asset singletons."""
    # Mocking display and mixer
    pygame.display.init = MagicMock()
    pygame.display.set_mode = MagicMock(return_value=MagicMock(spec=pygame.Surface))
    pygame.mixer.init = MagicMock()
    pygame.mixer.Sound = MagicMock(return_value=MagicMock())
    
    # Mocking font
    pygame.font.init = MagicMock()
    mock_font = MagicMock()
    mock_font.get_height.return_value = 30
    mock_font.render.return_value = MagicMock(spec=pygame.Surface)
    pygame.font.Font = MagicMock(return_value=mock_font)

    # Initialize assets with Mocks to avoid NoneType errors
    import assets
    assets.images = MagicMock()
    assets.sounds = MagicMock()
    assets.fonts = MagicMock()
    
    # Pre-populate some fonts that are accessed during __init__
    assets.fonts.score = mock_font
    assets.fonts.operation = mock_font
    assets.fonts.menu_item = mock_font
    assets.fonts.menu_title = mock_font
    assets.fonts.op_train = mock_font
    assets.fonts.op_large = mock_font

# Apply mocks immediately
mock_pygame_and_assets()
