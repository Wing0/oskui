import unittest
from unittest.mock import patch, mock_open
from oskui import choice_menu, press_any_key, prompt, ask_float_int


class TestChoiceMenu(unittest.TestCase):

    @patch('builtins.input', side_effect=['1'])
    def test_choice_menu_valid_choice(self, mock_input):
        menu = ['Option 1', 'Option 2', 'Option 3']
        result = choice_menu(menu, "Choose an option:")
        self.assertEqual(result, 0)

    @patch('builtins.input', side_effect=['q'])
    def test_choice_menu_quit(self, mock_input):
        menu = ['Option 1', 'Option 2', 'Option 3']
        result = choice_menu(menu, "Choose an option:")
        self.assertFalse(result)


class TestPressAnyKey(unittest.TestCase):

    @patch('oskui.getch', return_value='a')
    def test_press_any_key(self, mock_getch):
        result = press_any_key("Press any key:")
        self.assertEqual(result, 'a')


class TestPrompt(unittest.TestCase):

    @patch('builtins.input', side_effect=['y'])
    def test_prompt_yes(self, mock_input):
        result = prompt("Are you sure?", default=None)
        self.assertTrue(result)

    @patch('builtins.input', side_effect=['n'])
    def test_prompt_no(self, mock_input):
        result = prompt("Are you sure?", default=None)
        self.assertFalse(result)

    @patch('builtins.input', side_effect=[''])
    def test_prompt_default(self, mock_input):
        result = prompt("Are you sure?", default=True)
        self.assertTrue(result)


class TestAskFloatInt(unittest.TestCase):

    @patch('builtins.input', side_effect=['10'])
    def test_ask_float_int_with_int(self, mock_input):
        result = ask_float_int("Enter an integer:", get_int=True)
        self.assertEqual(result, 10)

    @patch('builtins.input', side_effect=['10.5'])
    def test_ask_float_int_with_float(self, mock_input):
        result = ask_float_int("Enter a float:")
        self.assertEqual(result, 10.5)

    @patch('builtins.input', side_effect=['q'])
    def test_ask_float_int_cancel(self, mock_input):
        result = ask_float_int("Enter a value or q to cancel:")
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
