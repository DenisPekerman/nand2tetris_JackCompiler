import unittest
from CompilationEngine import CompilationEngine
from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable

 
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








    def assertXml(self, node, expected_str):
        ET.indent(node)
        received_str = self.getXmlFmtStr(node)

        expected_node = ET.fromstring(expected_str)
        expected_fmt_str = self.getXmlFmtStr(expected_node)

        if received_str != expected_fmt_str:
            msg = f"""
------------------
Expected:
{expected_fmt_str}
------------------
Received:
{received_str}
------------------
                """
            self.fail(msg)



    def test_compileReturn(self):
        self.compilationEngine.tokenizer.tokens = ["return", "x", ";"]
        root = ET.Element("test") 
        self.compilationEngine.compileReturn(root)
        expected = """
            <test>
                <returnStatement>
                    <keyword>return</keyword>
                        <expression>
                            <term>
                                <identifier>x</identifier>   
                            </term>
                        </expression>
                    <symbol>;</symbol>
                </returnStatement>
            </test>
        """

        self.assertXml(root, expected)



    def test_compileDo_empty(self):
        compilationEngine = CompilationEngine('', "temp.xml")
        compilationEngine.tokenizer.tokens = ["do", "someFunc", "(", ")", ';']
        root = ET.Element("test") 
        compilationEngine.compileDo(root)
        expected = """
            <test>
                <doStatement>
                    <keyword>do</keyword>
                    <identifier>someFunc</identifier>
                    <symbol>(</symbol>
                    <expressionList></expressionList>
                    <symbol>)</symbol>
                    <symbol>;</symbol>
                </doStatement>
            </test>
        """

        self.assertXml(root, expected)



    def test_compileDo_one_param(self):
        self.compilationEngine.tokenizer.tokens = ["do", "someFunc", "(", "x", ")", ';']
        root = ET.Element("test") 
        self.compilationEngine.compileDo(root)
        expected = """
        <test>
            <doStatement>
                <keyword>do</keyword>
                <identifier>someFunc</identifier>
                <symbol>(</symbol>
                <expressionList> 
            <expression>
              <term>
                    <identifier>x</identifier>   
              </term>
            </expression>            
                </expressionList>
                <symbol>)</symbol>
                <symbol>;</symbol>
            </doStatement>
        </test>
        """

        self.assertXml(root, expected)



    def test_compileDo_multi_param(self):
        self.compilationEngine.tokenizer.tokens = ["do", "someFunc", "(", "x", ",", "y",
                                                    ",", "3", ")", ';', '{', '}']
        root = ET.Element("test") 
        self.compilationEngine.compileDo(root)
        expected = """
        <test>
            <doStatement>
                <keyword>do</keyword>
                <identifier>someFunc</identifier>
                <symbol>(</symbol>
                <expressionList>
                <expression>
                    <term>
                    <identifier>x</identifier>
                    </term>
                </expression>
                <symbol>,</symbol>
                <expression>
                    <term>
                    <identifier>y</identifier>
                    </term>
                </expression>
                <symbol>,</symbol>
                <expression>
                    <term>
                    <integerConstant>3</integerConstant>
                    </term>
                </expression>
                </expressionList>
                <symbol>)</symbol>
                <symbol>;</symbol>
            </doStatement>
        </test>
        """

        self.assertXml(root, expected)



    def test_compileParameterList(self):
        self.compilationEngine.tokenizer.tokens = ['int', 'y', ',', 'int', 'x', ')' ]
        root = ET.Element("test") 
        self.compilationEngine.compileParameterList(root)
        expected = """
            <test>
            <parameterList>
                <keyword>int</keyword>
                <identifier>y</identifier>
                <symbol>,</symbol>
                <keyword>int</keyword>
                <identifier>x</identifier>
            </parameterList>
            </test>
        """

        self.assertXml(root, expected)



    def test_compileIf_complex(self):
        # if ((x>4) & (y = 8))
        self.compilationEngine.tokenizer.tokens = ['if', '(', '(', 'x', '>', '4', ')', '&', 
                                                   '(', 'y', '=', '8', ')', ')', '{', '}' ]
        root = ET.Element("test") 
        self.compilationEngine.compileIf(root)
        expected = """
        <test>
            <ifStatement>
                <keyword>if</keyword>
                <symbol>(</symbol>
                <expression>
                    <term>
                        <symbol>(</symbol>
                        <expression>
                            <term>
                                <identifier>x</identifier>
                            </term>
                            <symbol>></symbol>
                            <term>
                                <integerConstant>4</integerConstant>
                            </term>
                        </expression>
                        <symbol>)</symbol>
                    </term>
                    <symbol>&amp;</symbol>
                    <term>
                        <symbol>(</symbol>
                        <expression>
                            <term>
                                <identifier>y</identifier>
                            </term>
                            <symbol>=</symbol>
                            <term>
                                <integerConstant>8</integerConstant>
                            </term>
                        </expression>
                        <symbol>)</symbol>
                    </term>
                </expression>
                <symbol>)</symbol>
                <symbol>{</symbol>
                <statements></statements> 
                <symbol>}</symbol>
            </ifStatement>
            
        </test>

        """

        self.assertXml(root, expected)

    

    def test_compileIf_simple(self):
        # if (x>4)
        self.compilationEngine.tokenizer.tokens = ['if', '(', 'x', '>', '4', ')'
                                                   , '{', '}']
        root = ET.Element("test") 
        self.compilationEngine.compileIf(root)
        expected = """
        <test>
            <ifStatement>
                <keyword>if</keyword>
                <symbol>(</symbol>
                <expression>
                    <term>
                        <identifier>x</identifier>
                    </term>
                    <symbol>></symbol>
                    <term>
                        <integerConstant>4</integerConstant>
                    </term>
                </expression>
                <symbol>)</symbol>
                <symbol>{</symbol>
                <statements></statements>
                <symbol>}</symbol>
            </ifStatement>
        </test>
        """

        self.assertXml(root, expected)



    def test_compileIf_ifElse(self):
        self.compilationEngine.tokenizer.tokens = ['if', '(', 'x', '>', '4', ')'
                                                   , '{', '}', 'else', '{', '}' ]
        root = ET.Element("test") 
        self.compilationEngine.compileIf(root)
        expected = """
        <test>
            <ifStatement>
                <keyword>if</keyword>
                <symbol>(</symbol>
                <expression>
                    <term>
                        <identifier>x</identifier>
                    </term>
                    <symbol>></symbol>
                    <term>
                        <integerConstant>4</integerConstant>
                    </term>
                </expression>
                <symbol>)</symbol>
                <symbol>{</symbol>
                <statements></statements>
                <symbol>}</symbol>
                <keyword>else</keyword>
                <symbol>{</symbol>
                <statements></statements>
                <symbol>}</symbol>
            </ifStatement>
        </test>
        """

        self.assertXml(root, expected)



    def test_compileWhile(self):
        # if (x>4)
        self.compilationEngine.tokenizer.tokens = ['while', '(', 'x', '>', '4', ')'
                                                   , '{', '}']
        root = ET.Element("test") 
        self.compilationEngine.compileWhile(root)
        expected = """
        <test>
            <whileStatement>
                <keyword>while</keyword>
                <symbol>(</symbol>
                <expression>
                    <term>
                        <identifier>x</identifier>
                    </term>
                    <symbol>></symbol>
                    <term>
                        <integerConstant>4</integerConstant>
                    </term>
                </expression>
                <symbol>)</symbol>
                <symbol>{</symbol>
                <statements></statements>
                <symbol>}</symbol>
            </whileStatement>
        </test>
        """

        self.assertXml(root, expected)



    def test_compileExpression_simple(self):
        self.compilationEngine.tokenizer.tokens = ['x', '+', '2']
                                                  
        root = ET.Element("test") 
        self.compilationEngine.compileExpression(root)
        expected = """
        <test>
            <expression>
                <term>
                    <identifier>x</identifier>
                </term>
                <symbol>+</symbol>
                <term>
                    <integerConstant>2</integerConstant>
                </term>
            </expression>
        </test>
        """

        self.assertXml(root, expected)



    def test_compileExpression_simple1(self):
        self.compilationEngine.tokenizer.tokens = ['x', '+', '2', '*', '7']
                                                  
        root = ET.Element("test") 
        self.compilationEngine.compileExpression(root)
        expected = """
        <test>
            <expression>
                <term>
                    <identifier>x</identifier>
                </term>
                <symbol>+</symbol>
                <term>
                    <integerConstant>2</integerConstant>
                </term>
                <symbol>*</symbol>
                <term>
                    <integerConstant>7</integerConstant>
                </term>
            </expression>
        </test>
        """

        self.assertXml(root, expected)



    def test_compileExpression_brackets(self):
        self.compilationEngine.tokenizer.tokens = ['x', '+','(', '2', '*', '7',')']
                                                  
        root = ET.Element("test") 
        self.compilationEngine.compileExpression(root)
        expected = """
        <test>
            <expression>
                <term>
                    <identifier>x</identifier>
                </term>
                <symbol>+</symbol>
                <term>
                    <symbol>(</symbol>
                    <expression>
                        <term>
                            <integerConstant>2</integerConstant>
                        </term>
                        <symbol>*</symbol>
                        <term>
                            <integerConstant>7</integerConstant>
                        </term>
                    </expression>
                    <symbol>)</symbol>
                </term>
            </expression>
        </test>
        """

        self.assertXml(root, expected)



    def test_compileTerm_varName(self):
        self.compilationEngine.tokenizer.tokens = ['x']
                                                  
        root = ET.Element("test") 
        self.compilationEngine.compileTerm(root)
        expected = """
        <test>
            <term>
                <identifier>x</identifier>
            </term>
        </test>
        """

        self.assertXml(root, expected)



    def test_compileTerm_boolean(self):
        self.compilationEngine.tokenizer.tokens = ['false']
                                                  
        root = ET.Element("test") 
        self.compilationEngine.compileTerm(root)
        expected = """
        <test>
            <term>
                <keyword>false</keyword>
            </term>
        </test>
        """

        self.assertXml(root, expected)



    def test_compileTerm_listItem(self):
        # x[1+2]
        self.compilationEngine.tokenizer.tokens = ['x', '[', '1', '+', '2', ']']
                                                  
        root = ET.Element("test") 
        self.compilationEngine.compileTerm(root)
        expected = """
        <test>
            <term>
                <identifier>x</identifier>
                <symbol>[</symbol>
                <expression>
                    <term>
                        <integerConstant>1</integerConstant>
                    </term>
                    <symbol>+</symbol>
                    <term>
                        <integerConstant>2</integerConstant>
                    </term>
                </expression>
                <symbol>]</symbol>
            </term>
        </test>
        """

        self.assertXml(root, expected)



    def test_compileTerm_subroutineCall(self):
        # foo(1)
        self.compilationEngine.tokenizer.tokens = ['foo', '(', '1', ')']
                                                  
        root = ET.Element("test") 
        self.compilationEngine.compileTerm(root)
        expected = """
        <test>
            <term>
                <identifier>foo</identifier>
                <symbol>(</symbol>
                <expressionList>
                    <expression>
                        <term>
                            <integerConstant>1</integerConstant>
                        </term>
                    </expression>
                </expressionList>
                <symbol>)</symbol>
            </term>
        </test>
        """

        self.assertXml(root, expected)



    def test_compileTerm_classSubroutine(self):
        self.compilationEngine.tokenizer.tokens = ['x', '.', 'foo', '(', '1', '+', '2', ')']
                                                  
        root = ET.Element("test") 
        self.compilationEngine.compileTerm(root)
        expected = """
        <test>
            <term>
                <identifier>x</identifier>
                <symbol>.</symbol>
                <identifier>foo</identifier>
                <symbol>(</symbol>
                <expressionList>
                    <expression>
                        <term>
                            <integerConstant>1</integerConstant>
                        </term>
                        <symbol>+</symbol>
                        <term>
                            <integerConstant>2</integerConstant>
                        </term>
                    </expression>
                </expressionList>
                <symbol>)</symbol>
            </term>
        </test>
        """

        self.assertXml(root, expected)



    def test_compileTerm_expression(self):
        self.compilationEngine.tokenizer.tokens = ['(', '1', '+', '2', ')'] 
                                                  
        root = ET.Element("test") 
        self.compilationEngine.compileTerm(root)
        expected = """
        <test>
            <term>
                <symbol>(</symbol>
                <expression>
                    <term>
                        <integerConstant>1</integerConstant>
                    </term>
                    <symbol>+</symbol>
                    <term>
                        <integerConstant>2</integerConstant>
                    </term>
                </expression>
                <symbol>)</symbol>
            </term>
        </test>
        """

        self.assertXml(root, expected)



    def test_compileTerm_unaryOp(self):
        # ~(x)
        self.compilationEngine.tokenizer.tokens = ['~', '(', 'x', ')']                                   
        root = ET.Element("test") 
        self.compilationEngine.compileTerm(root)
        expected = """
        <test>
            <term>
                <symbol>~</symbol>
                <term>
                    <symbol>(</symbol>
                    <expression>
                        <term>
                            <identifier>x</identifier>
                        </term>
                    </expression>
                    <symbol>)</symbol>
                </term>
            </term>
        </test>
        """

        self.assertXml(root, expected)

    
