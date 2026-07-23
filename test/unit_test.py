import importlib.util
import pathlib

import pytest

# Cargar los módulos
ROOT = pathlib.Path(__file__).resolve().parent.parent
SERVER_PATH = ROOT / "source" / "server.py"
CLIENT_PATH = ROOT / "source" / "client.py"

def _load_module_from_path(name: str, path: pathlib.Path):
	spec = importlib.util.spec_from_file_location(name, str(path))
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module

server_mod = _load_module_from_path("server_mod", SERVER_PATH)
client_mod = _load_module_from_path("client_mod", CLIENT_PATH)

# Funciones a probar
parse_buffer = server_mod.parse_buffer
is_valid_message = client_mod.is_valid_message


class TestParseBuffer:
	"""Pruebas unitarias para `parse_buffer`."""

	def test_parse_buffer_single_complete_message(self):
		buf = "hello world\n"
		messages, residue = parse_buffer(buf)
		
		# Assert
		assert messages == ["hello world"]
		assert residue == ""

	def test_parse_buffer_multiple_messages(self):
		buf = "one\ntwo\nthree\n"
		messages, residue = parse_buffer(buf)

		# Assert
		assert messages == ["one", "two", "three"]
		assert residue == ""

	def test_parse_buffer_fragmented_message_keeps_residue(self):
		buf = "incomplete"
		messages, residue = parse_buffer(buf)

		# Assert
		assert messages == []
		assert residue == "incomplete"

	def test_parse_buffer_fragmentation_plus_concatenation(self):
		# Simula un residuo previo que se concatena con un nuevo paquete entrante
		residue_prev = "incom"
		new_chunk = "plete\nnext\npartial"
		buf = residue_prev + new_chunk

		messages, residue = parse_buffer(buf)

		# Assert
		assert messages == ["incomplete", "next"]
		assert residue == "partial"

	def test_parse_buffer_discards_empty_and_whitespace_lines(self):
		buf = "\n\n   \nmsg\n"
		messages, residue = parse_buffer(buf)

		# Assert
		assert messages == ["msg"]
		assert residue == ""


class TestIsValidMessage:
	"""Pruebas unitarias para `is_valid_message` """
	def test_is_valid_message_with_normal_text(self):
		msg = "hello"
		result = is_valid_message(msg)

		# Assert
		assert result is True

	def test_is_valid_message_with_empty_string(self):
		msg = ""
		result = is_valid_message(msg)

		# Assert
		assert result is False

	def test_is_valid_message_with_whitespace_only(self):
		msg = "   "
		result = is_valid_message(msg)

		# Assert
		assert result is False