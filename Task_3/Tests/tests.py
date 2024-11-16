import unittest
import Task_3.main as m
from Task_3.main import parse_text


class TestConstantParser(unittest.TestCase):

    def setUp(self):
        # Сброс глобальных переменных перед каждым тестом
        m.constants = {}
        m.result = ""
        m.kol_bracket = 0
        m.kol_array = 0
        m.in_dict = False
        m.in_array = False
        m.cur_value = ''
        m.cur_name = ''

    def test_repository_functionality(self):
        # Тестируем добавление константы
        m.cur_name = "TEST_CONSTANT"
        m.parse_value('"My Const";', "Line with a constant", 0,m.cur_name)

        self.assertIn("TEST_CONSTANT", m.constants)
        self.assertEqual(m.constants["TEST_CONSTANT"], '"My Const"')

    def test_empty_value(self):
        # Тестируем пустое значение
        with self.assertRaises(SyntaxError):
            m.parse_value("", "Line with an empty value", 0, "EMPTY")

    def test_brace_syntax_error(self):
        # Тестируем ситуацию с неправильным количеством скобок
        m.parse_value("{", "Line with unbalanced brackets", 0, "UNBALANCED")
        with self.assertRaises(SyntaxError):
            m.parse_value("}", "Line without opening bracket", 0, "UNBALANCED")

    def test_array_value(self):
        # global cur_name
        m.cur_name = "ARRAY_CONST"
        m.parse_value("'( 1 2 3 );", "let A = '( 1 2 3 );", 0, m.cur_name)

        self.assertIn("ARRAY_CONST", m.constants)
        self.assertTrue("[ 1, 2, 3 ]" in m.constants["ARRAY_CONST"])

    def test_invalid_expression(self):
        # Тестируем неверное выражение
        m.cur_name = "INVALID_EXPR"
        with self.assertRaises(SyntaxError):
            m.parse_value(".INVALID.", "Invalid expression in line", 0, m.cur_name)

    def test_parse_config_with_dict(self):
        file_content = """
        let A = {
            X = 1;
            Y = 2;
        };
        """
        expected_output = '{\n  "A": {\n    "X": 1,\n    "Y": 2\n  }\n}\n'
        result = parse_text(file_content)
        self.assertEqual(result, expected_output)

if __name__ == "__main__":
    unittest.main()
