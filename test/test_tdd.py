import sys
from pathlib import Path

# Agregar la raíz del proyecto al sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from source.server import parse_buffer
from source.client import is_valid_message

# ==========================================
# FASE RED (TDD): Máximo 100 caracteres

def test_is_valid_message_exceeds_max_length():
    """RED: Validar que mensajes de más de 100 caracteres sean rechazados."""
    long_message = "A" * 101
    valid_message = "A" * 100
    
    # Esta aserción FALLARÁ con la implementación actual de is_valid_message
    assert is_valid_message(long_message) is False
    assert is_valid_message(valid_message) is True


def test_parse_buffer_ignores_overly_long_messages():
    """RED: Validar que el buffer ignore líneas que superen 100 caracteres."""
    long_line = "B" * 105 + "\n"
    normal_line = "Hola mundo\n"
    buffer_input = long_line + normal_line
    
    messages, remainder = parse_buffer(buffer_input)
    
    # Esta aserción FALLARÁ porque actualmente parse_buffer procesa cadenas de cualquier longitud
    assert messages == ["Hola mundo"]
    assert remainder == ""

