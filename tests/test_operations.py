import pytest
import conftest # Sets up paths and mocks
from unittest.mock import MagicMock
from operations import Operation

class MockGame:
    def __init__(self):
        self.operation = MagicMock()
        self.op_train = MagicMock()

@pytest.fixture
def mock_game():
    return MockGame()

def test_operation_generation_validity(mock_game):
    """Testa se as operações geradas são strings válidas e computáveis."""
    op = Operation(mock_game)
    for _ in range(100): # Testa múltiplas gerações
        op.generate()
        assert isinstance(op.text, str)
        assert len(op.text) > 2
        # Verifica se o eval funciona (não deve disparar exceção)
        result = eval(op.text)
        assert isinstance(result, (int, float))

def test_no_division_by_zero(mock_game):
    """Garante que nunca ocorra divisão por zero."""
    op = Operation(mock_game)
    for _ in range(200):
        op.generate()
        if '/' in op.text:
            parts = op.text.split('/')
            divisor = int(parts[1].strip())
            assert divisor != 0

def test_subtraction_non_negative(mock_game):
    """Verifica se subtrações não resultam em números negativos (design do jogo)."""
    op = Operation(mock_game)
    for _ in range(200):
        op.generate()
        if '-' in op.text:
            result = eval(op.text)
            assert result >= 0

def test_division_is_integer(mock_game):
    """Garante que divisões sempre resultam em números inteiros exatos."""
    op = Operation(mock_game)
    for _ in range(200):
        op.generate()
        if '/' in op.text:
            result = eval(op.text)
            assert result == int(result)
