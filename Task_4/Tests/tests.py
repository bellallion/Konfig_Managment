import Task_4.interpreter as i
import unittest
from unittest.mock import patch, mock_open
from Task_4.assembler import Assembler


class Test(unittest.TestCase):
    def test_int_to_hex(self):
        assembler = Assembler("input.txt", "binary.bin", "log.csv")
        hex_bytes = assembler.int_to_hex(45, 905)
        expected_bytes = b'\xAD\xC4\x01'  # Ожидаемые байты в big-endian формате
        self.assertEqual(hex_bytes, expected_bytes)

        hex_bytes_without_b = assembler.int_to_hex(40)
        expected_bytes_without_b = b'\x28\x00\x00'  # Ожидаемые байты без B
        self.assertEqual(hex_bytes_without_b, expected_bytes_without_b)

    def setUp(self):
        self.binary_file = "mock_binary_file"
        self.result_file = "mock_result_file"
        self.memory_range = (0, 10)  # Задаем диапазон для тестирования
        self.interpreter = i.Interpreter(self.binary_file, self.result_file, self.memory_range)

    @patch("builtins.open", new_callable=mock_open, read_data=b'\x00\x00\x00')
    def test_run_empty_file(self, mock_open):
        self.interpreter.run()
        # Проверяем, что стек остается пустым
        self.assertEqual(self.interpreter.stack, [])
        # Проверяем, что память не изменилась
        self.assertEqual(self.interpreter.memory, [0] * 1024)


    @patch("builtins.open", new_callable=mock_open, read_data=b'\x28\x00\x00')  # Пример команды записи в память по адресу в стеке
    def test_run_write_to_memory_from_stack(self, mock_open) :
        self.interpreter.stack.append(5)  # Помещаем адрес в стек
        self.interpreter.run()
        self.assertEqual(self.interpreter.memory[5], 5)  # Проверяем, что значение записано в память

    @patch("builtins.open", new_callable=mock_open, read_data=b'\x55\x00\x00\x00\x00')  # Создаём команду для pop
    def test_run_invalid_stack_pop(self, mock_open):
        with self.assertRaises(IndexError):
            self.interpreter.run()  # Поскольку стек пуст, это вызовет исключение

if __name__ == '__main__':
    unittest.main()
