import difflib
import unittest
from CompilationEngine import CompilationEngine
from SymbolTable import SymbolTable  

class TestCompilationEngine(unittest.TestCase):
    
    def setUp(self) -> None:
        self.maxDiff = None
        self.compilationEngine = CompilationEngine('', "temp.vm")

        self.st_sub = self.compilationEngine.st_subroutine
        self.st_class = self.compilationEngine.st_class

        self.jackTokenizer = self.compilationEngine.tokenizer


    def test_compileClassVarDec_oneVar(self):
        self.jackTokenizer.tokens = ['static', 'int', 'x', ',', 'y', ',', 'z', ';']
        self.compilationEngine.compileClassVarDec()

        self.assertEqual(self.st_class.var_count('static'), 3)

        self.assertEqual(self.st_class.kind_of('x'), 'static')
        self.assertEqual(self.st_class.type_of('x'), 'int')
        self.assertEqual(self.st_class.index_of('x'), 0)

        self.assertEqual(self.st_class.kind_of('y'), 'static')
        self.assertEqual(self.st_class.type_of('y'), 'int')
        self.assertEqual(self.st_class.index_of('y'), 1)

        self.assertEqual(self.st_class.kind_of('z'), 'static')
        self.assertEqual(self.st_class.type_of('z'), 'int')
        self.assertEqual(self.st_class.index_of('z'), 2)


    def test_compileClassVarDec_twoVar(self):
        self.jackTokenizer.tokens = [
            'static', 'int', 'x', ',', 'y', ',', 'z', ';',
            'field', 'boolean', 'a', ',', 'b', ',', 'c', ';'
        ]

        self.compilationEngine.compileClassVarDec()
        
        self.assertEqual(self.st_class.var_count('static'), 3)
        self.assertEqual(self.st_class.kind_of('x'), 'static')
        self.assertEqual(self.st_class.type_of('x'), 'int')
        self.assertEqual(self.st_class.index_of('x'), 0)

        self.assertEqual(self.st_class.kind_of('y'), 'static')
        self.assertEqual(self.st_class.type_of('y'), 'int')
        self.assertEqual(self.st_class.index_of('y'), 1)

        self.assertEqual(self.st_class.kind_of('z'), 'static')
        self.assertEqual(self.st_class.type_of('z'), 'int')
        self.assertEqual(self.st_class.index_of('z'), 2)

        self.assertEqual(self.st_class.var_count('field'), 3)
        self.assertEqual(self.st_class.kind_of('a'), 'field')
        self.assertEqual(self.st_class.type_of('a'), 'boolean')
        self.assertEqual(self.st_class.index_of('a'), 0)

        self.assertEqual(self.st_class.kind_of('b'), 'field')
        self.assertEqual(self.st_class.type_of('b'), 'boolean')
        self.assertEqual(self.st_class.index_of('b'), 1)
        
        self.assertEqual(self.st_class.kind_of('c'), 'field')
        self.assertEqual(self.st_class.type_of('c'), 'boolean')
        self.assertEqual(self.st_class.index_of('c'), 2)


    def test_compileParameterList_single(self):
        self.jackTokenizer.tokens = ['int', 'x', ')']

        self.compilationEngine.compileParameterList()

        self.assertEqual(self.st_sub.var_count('argument'), 1)
        self.assertEqual(self.st_sub.kind_of('x'), 'argument')
        self.assertEqual(self.st_sub.type_of('x'), 'int')
        self.assertEqual(self.st_sub.index_of('x'), 0)


    def test_compileParameterList_threeParams(self):
        self.jackTokenizer.tokens = [
            'int', 'x', 
            ',', 'int', 'y', 
            ',', 'int', 'z', 
            ')'
        ]

        self.compilationEngine.compileParameterList()

        self.assertEqual(self.st_sub.var_count('argument'), 3)

        self.assertEqual(self.st_sub.kind_of('x'), 'argument')
        self.assertEqual(self.st_sub.type_of('x'), 'int')
        self.assertEqual(self.st_sub.index_of('x'), 0)

        self.assertEqual(self.st_sub.kind_of('y'), 'argument')
        self.assertEqual(self.st_sub.type_of('y'), 'int')
        self.assertEqual(self.st_sub.index_of('y'), 1)

        self.assertEqual(self.st_sub.kind_of('z'), 'argument')
        self.assertEqual(self.st_sub.type_of('z'), 'int')
        self.assertEqual(self.st_sub.index_of('z'), 2)

    
    def test_compileVarDec_simple(self):
        self.jackTokenizer.tokens = ['var', 'int', 'x', ',', 'y', ';']

        self.compilationEngine.compileVarDec()

        self.assertEqual(self.st_sub.var_count('local'), 2)

        self.assertEqual(self.st_sub.kind_of('x'), 'local')
        self.assertEqual(self.st_sub.type_of('x'), 'int')
        self.assertEqual(self.st_sub.index_of('x'), 0)
        
        # self.assertEqual(self.st_sub.kind_of('y'), 'local')
        # self.assertEqual(self.st_sub.type_of('y'), 'int')
        # self.assertEqual(self.st_sub.index_of('y'), 1)


    def test_compileVarDec_complex(self):
        self.jackTokenizer.tokens = [
            'var', 'int', 'x', ',', 'y', ';', 
            'var', 'Banana', 'b', ';', 
            'var', 'boolean', 'flag', ',', 'check', ';'
        ]
        self.compilationEngine.compileVarDec()

        self.assertEqual(self.st_sub.var_count('local'), 5)

        self.assertEqual(self.st_sub.kind_of('x'), 'local')
        self.assertEqual(self.st_sub.type_of('x'), 'int')
        self.assertEqual(self.st_sub.index_of('x'), 0)

        self.assertEqual(self.st_sub.kind_of('y'), 'local')
        self.assertEqual(self.st_sub.type_of('y'), 'int')
        self.assertEqual(self.st_sub.index_of('y'), 1)

        self.assertEqual(self.st_sub.kind_of('b'), 'local')
        self.assertEqual(self.st_sub.type_of('b'), 'Banana')
        self.assertEqual(self.st_sub.index_of('b'), 2)

        self.assertEqual(self.st_sub.kind_of('flag'), 'local')
        self.assertEqual(self.st_sub.type_of('flag'), 'boolean')
        self.assertEqual(self.st_sub.index_of('flag'), 3)

        self.assertEqual(self.st_sub.kind_of('check'), 'local')
        self.assertEqual(self.st_sub.type_of('check'), 'boolean')
        self.assertEqual(self.st_sub.index_of('check'), 4)

    def test_saveStateVar_scopeCheck(self):
        self.compilationEngine.st_subroutine.define('y', 'int', 'local')
        self.compilationEngine.st_class.define('x', 'int', 'static')
        self.compilationEngine.st_class.define('z', 'int', 'static')
        self.compilationEngine._saveVarDetail('z')

        expected_stateVar = [
            {'name': 'z', 'kind': 'static', 'type': 'int', 'index': 1}
        ]

        self.assertEqual(self.compilationEngine.stackMachine[0], expected_stateVar)
    

    def test_compileVarDec_single_line(self):
        self.jackTokenizer.tokens = ['var', 'int', 'x', ',', 'y', ',', 'z', ';']
        self.compilationEngine.compileVarDec()

        # Assert that the variables were added to st_subroutine
        self.assertEqual(self.st_sub.var_count('local'), 3)
        self.assertEqual(self.st_sub.kind_of('x'), 'local')
        self.assertEqual(self.st_sub.type_of('x'), 'int')
        self.assertEqual(self.st_sub.index_of('x'), 0)
        self.assertEqual(self.st_sub.kind_of('y'), 'local')
        self.assertEqual(self.st_sub.type_of('y'), 'int')
        self.assertEqual(self.st_sub.index_of('y'), 1)
        self.assertEqual(self.st_sub.kind_of('z'), 'local')
        self.assertEqual(self.st_sub.type_of('z'), 'int')
        self.assertEqual(self.st_sub.index_of('z'), 2)


    def test_getStateVar(self):
        # Define variables in subroutine and class symbol tables
        self.compilationEngine.st_subroutine.define('x', 'int', 'local')
        self.compilationEngine.st_class.define('y', 'char', 'field')

        # Test for a variable in subroutine symbol table
        result_x = self.compilationEngine._getVarDetail('x')
        expected_x = {
            'name': 'x',
            'kind': 'local',
            'type': 'int',
            'index': 0
        }
        self.assertEqual(result_x, expected_x)

        # Test for a variable in class symbol table
        result_y = self.compilationEngine._getVarDetail('y')
        expected_y = {
            'name': 'y',
            'kind': 'field',
            'type': 'char',
            'index': 0
        }
        self.assertEqual(result_y, expected_y)

        # Test for a variable that does not exist
        result_z = self.compilationEngine._getVarDetail('z')
        self.assertIsNone(result_z)



    def test_stackMachine(self):
        self.compilationEngine.st_class.define("x", "int", "static")
        self.compilationEngine.st_class.define("y", "int", "static")

        self.jackTokenizer.tokens = ['x', '=', 'y', ';']

        self.compilationEngine.compileExpression()

        # The second item in stackMachine (index 1), 'name' field
        actual = self.compilationEngine.stackMachine[1]['name']
        expected = 'y'
        self.assertEqual(expected, actual)

    
    def test_stackMachine_1(self):
        self.compilationEngine.st_class.define("x", "int", "static")
        self.compilationEngine.st_class.define("y", "int", "static")

        self.jackTokenizer.tokens = ['x', '=', 'y', ';']

        self.compilationEngine.stackMachine = []

        self.compilationEngine.compileExpression()

        # The second item in stackMachine (index 1), 'name' field
        actual = self.compilationEngine.stackMachine[1]['name']
        expected = 'y'
        self.assertEqual(expected, actual)
