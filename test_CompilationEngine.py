import unittest
from CompilationEngine import CompilationEngine
 
class TestCompilationEngine(unittest.TestCase):
    
    def setUp(self) -> None:
        self.compilationEngine = CompilationEngine('', "temp.xml")
        self.jackTokenizer = self.compilationEngine.tokenizer
    
    def test_compileClassVarDec_oneVar(self):
        self.jackTokenizer.tokens = ['static', 'int', 'x', ',', 'y', ',', 'z', ';']
        self.compilationEngine.compileClassVarDec()
        st_class = self.compilationEngine.st_class

        self.assertEqual(st_class.var_count('static'), 3)

        self.assertEqual(st_class.kind_of('x'), 'static')
        self.assertEqual(st_class.type_of('x'), 'int')
        self.assertEqual(st_class.index_of('x'), 0)

        self.assertEqual(st_class.kind_of('y'), 'static')
        self.assertEqual(st_class.type_of('y'), 'int')
        self.assertEqual(st_class.index_of('y'), 1)

        self.assertEqual(st_class.kind_of('z'), 'static')
        self.assertEqual(st_class.type_of('z'), 'int')
        self.assertEqual(st_class.index_of('z'), 2)


    def test_compileClassVarDec_twoVar(self):
        self.jackTokenizer.tokens = [
            'static', 'int', 'x', ',', 'y', ',', 'z', ';',
            'field', 'boolean', 'a', ',', 'b', ',', 'c', ';'
        ]

        st_class = self.compilationEngine.st_class
        self.compilationEngine.compileClassVarDec()
        
        self.assertEqual(st_class.var_count('static'), 3)
        self.assertEqual(st_class.kind_of('x'), 'static')
        self.assertEqual(st_class.type_of('x'), 'int')
        self.assertEqual(st_class.index_of('x'), 0)
        self.assertEqual(st_class.kind_of('y'), 'static')
        self.assertEqual(st_class.type_of('y'), 'int')
        self.assertEqual(st_class.index_of('y'), 1)
        self.assertEqual(st_class.kind_of('z'), 'static')
        self.assertEqual(st_class.type_of('z'), 'int')
        self.assertEqual(st_class.index_of('z'), 2)

        self.assertEqual(st_class.var_count('field'), 3)
        self.assertEqual(st_class.kind_of('a'), 'field')
        self.assertEqual(st_class.type_of('a'), 'boolean')
        self.assertEqual(st_class.index_of('a'), 0)
        self.assertEqual(st_class.kind_of('b'), 'field')
        self.assertEqual(st_class.type_of('b'), 'boolean')
        self.assertEqual(st_class.index_of('b'), 1)
        self.assertEqual(st_class.kind_of('c'), 'field')
        self.assertEqual(st_class.type_of('c'), 'boolean')
        self.assertEqual(st_class.index_of('c'), 2)








 