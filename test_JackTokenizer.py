import unittest
from JackTokenizer import JackTokenizer


class TestJackTokenizer(unittest.TestCase):
    
    def setUp(self) -> None:
        self.jackTokenizer = JackTokenizer('')
    

    def test_advance(self):
        self.jackTokenizer.tokens = ['class', '5', 'Main', '{']
        token = self.jackTokenizer.advance()
        self.assertEqual(token, 'class')
        token = self.jackTokenizer.advance()
        self.assertEqual(token, '5')


    def test_getTokenValue(self):
            token = "class"
            result = self.jackTokenizer.getTokenValue(token)
            self.assertEqual(result, ("class"))


    def test_gettokenType_keyword(self):
        token = "class"
        result = self.jackTokenizer.getTokenType(token)
        self.assertEqual(result, "keyword")

    
    def test_gettokenType_int(self):
        token = "5"
        result = self.jackTokenizer.getTokenType(token)
        self.assertEqual(result, "integerConstant")


    def test_gettokenType_symbol(self):
        token = "="
        result = self.jackTokenizer.getTokenType(token)
        self.assertEqual(result, "symbol")


    def test_gettokenType_string(self):
        token = '"hello"'
        result = self.jackTokenizer.getTokenType(token)
        self.assertEqual(result, "stringConstant")


    def test_gettokenType_identifier(self):
        token = "x"
        result = self.jackTokenizer.getTokenType(token)
        self.assertEqual(result, "identifier")


    def test_init_empty(self):
        actual_tokens = self.jackTokenizer.tokens
        self.assertEqual(actual_tokens, [])

    
    def test_hasMoreTokens_true(self):
        self.jackTokenizer.tokens = ['class', 'Main', '{']
        has_more_tokens = self.jackTokenizer.hasMoreTokens()
        self.assertEqual(has_more_tokens, True)
    

    def test_hasMoreTokens_false(self):
        self.jackTokenizer.tokens = []
        has_more_tokens = self.jackTokenizer.hasMoreTokens()
        self.assertEqual(has_more_tokens, False)

        
    def test_peek(self):
        self.jackTokenizer.tokens = ['class', 'Main', '{']
        self.assertEqual(self.jackTokenizer.peek(), 'class')
        self.assertEqual(self.jackTokenizer.peek(), 'class')

    def test_peek_empty(self):
        self.jackTokenizer.tokens = []
        self.assertEqual(self.jackTokenizer.peek(), None)


    