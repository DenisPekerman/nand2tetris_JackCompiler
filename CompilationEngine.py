#!/usr/bin/env python3

from JackTokenizer import JackTokenizer
from VmWriter import VmWriter
from SymbolTable import SymbolTable


class CompilationEngine:

    def __init__(self, input: str, output_file):
        self.output_file = output_file

        self.tokenizer = JackTokenizer(input)
        
        self.st_class = SymbolTable()  # St = symbol table 
        self.st_subroutine = SymbolTable()

        self.writeVm = VmWriter(output_file)

        self.class_name = ''
        self.stackMachine = [[]]

    
    def _saveVarDetail(self, token):
        token_type = self.tokenizer.getTokenType(token)
        name = token
        if token_type == 'opSymbol':
            name = self.tokenizer.getSymbolValue(token)
            kind = 'opSymbol'
            type = None
            index = None
        
        elif token_type == 'integerConstant':
            kind = 'constant'
            type = None
            index = None

        elif self.st_subroutine.has(token):
            kind = self.st_subroutine.kind_of(token)
            type = self.st_subroutine.type_of(token)
            index = self.st_subroutine.index_of(token)

        elif self.st_class.has(token):
            kind = self.st_class.kind_of(token)
            type = self.st_class.type_of(token)
            index = self.st_class.index_of(token)

        self.stackMachine[-1].append({
            'name': name,
            'kind': kind,
            'type': type,
            'index': index
        })


    def _subroutineHelper(self):
        self.tokenizer.advance() # consume 'subroutine'
        subroutine_type = self.tokenizer.advance()
        subroutine_name = self.tokenizer.advance()
        self.tokenizer.advance() # consume '('

        if self.tokenizer.peek() != ')':
            self.compileParameterList()
        self.tokenizer.advance() # consume ')'
        self.tokenizer.advance() # consume '{'
    
        return (subroutine_type, subroutine_name)


    def compileClass(self):
        self.st_class = {} # reset class symbolTable

        while self.tokenizer.peek() != '}':
            self.tokenizer.advance() # 'class'
            self.class_name = self.tokenizer.advance() # class name
            self.tokenizer.advance() # {
            
            if self.tokenizer.peek() in ['static', 'field']:
                self.compileClassVarDec()

            if self.tokenizer.peek() in ['constructor', 'method', 'function']:
                self.compileSubroutine()

        self.tokenizer.advance() # consume '}'
        self.writeVm.close()

    def compileClassVarDec(self):
        while self.tokenizer.peek() in ('static', 'field'):
            kind = self.tokenizer.advance()
            type = self.tokenizer.advance()
            name = self.tokenizer.advance()
            self.st_class.define(name, type, kind)

            while self.tokenizer.peek() == ',':
                self.tokenizer.advance() # consume ','
                name = self.tokenizer.advance() # get next var name
                self.st_class.define(name, type, kind)

            self.tokenizer.advance() # consume ';'
                

    def compileSubroutine(self):
        self.st_subroutine = {} # reset subroutine symbolTable 

        while self.tokenizer.peek() in ['constructor', 'method', 'function']:
            if self.tokenizer.peek() == 'constructor':
                self.tokenizer.advance() # consume 'constructor'
                self.tokenizer.advance() # consume name
                self.tokenizer.advance() # consume type
                self.tokenizer.advance() # consume '('
                
                if self.tokenizer.peek() != ')':
                    self.compileParameterList()    
                self.tokenizer.advance() # consume ')'
                self.tokenizer.advance() # consume '{'

                nVars = self.st_subroutine.index_of('argument')
                self.writeVm.writeFunction(f'{self.class_name}.new', nVars)
            
            elif self.tokenizer.peek() == 'method':
                name = 'this'
                type = self.class_name
                kind = 'argument'
                self.st_subroutine.define(name, type, kind)

                method_type, method_name = self._subroutineHelper()

                nVars = self.st_subroutine.index_of('argument')
                self.writeVm.writeFunction(f'{self.class_name}.{method_name}', nVars)

            elif self.tokenizer.peek() == 'function':
                function_type, function_name = self._subroutineHelper()

                nVars = self.st_subroutine.index_of('argument')
                self.writeVm.writeFunction(f'{self.class_name}.{function_name}', nVars)

        self.compileSubroutineBody()


    def compileParameterList(self):
        kind = 'argument'
        while self.tokenizer.peek() != ')':
            type = self.tokenizer.advance()
            name = self.tokenizer.advance()
            self.st_subroutine .define(name, type, kind)
            if self.tokenizer.peek() == ',':
                self.tokenizer.advance()
            else:
                break
        

    def compileSubroutineBody(self):
        if self.tokenizer.peek() == 'var':
                self.compileVarDec()
        self.compileStatements()
        

    def compileVarDec(self):
        kind = 'local'
        while self.tokenizer.peek() == 'var':
            self.tokenizer.advance()  # consume 'var'
            type = self.tokenizer.advance()  # get type

            while self.tokenizer.peek() != ';':
                name = self.tokenizer.advance()  # get variable name
                self.st_subroutine.define(name, type, kind)

                if self.tokenizer.peek() == ',':
                    self.tokenizer.advance()  # consume ','
                else:
                    break
            self.tokenizer.advance()  # consume ';'

        
    def compileStatements(self):
        while self.tokenizer.peek() != '}':
            if self.tokenizer.peek() == 'let':
                self.compileLet()
            elif self.tokenizer.peek() == 'do':
                self.compileDo()
            elif self.tokenizer.peek() == 'if':
                self.compileIf()
            elif self.tokenizer.peek() == 'while':
                self.compileWhile()
            elif self.tokenizer.peek() == 'return':
                self.compileReturn()
        self.tokenizer.advance() # consume '}'


    def compileLet(self):
        self.tokenizer.advance() # consume 'let'
        self.compileTerm()
        self.tokenizer.advance() # consume '='
        self.compileExpression()
        self.compileExpression() # consume ';'
    
    def compileDo(self):
        self.tokenizer.advance() # consume 'do'
        self.compileExpression()
        self.tokenizer.advance() # consume ';'
        

    def compileIf(self):
        self.tokenizer.advance() # consume 'if'
        self.tokenizer.advance()# consume '('
        self.compileExpression()
        self.tokenizer.advance() # consume ')'
        self.tokenizer.advance() # consume '{'
        self.compileStatements()
        self.tokenizer.advance() # consume '}'

        if self.tokenizer.peek() == 'else':
            self.tokenizer.advance() # consume 'else'
            self.tokenizer.advance() # consume "{"
            self.compileStatements()
            self.tokenizer.advance() # consume "}"


    def compileWhile(self):
        self.tokenizer.advance() # consume 'while'
        self.tokenizer.advance()# consume '('
        self.compileExpression()
        self.tokenizer.advance() # consume ')'
        self.tokenizer.advance() # consume '{'
        self.compileStatements()
        self.tokenizer.advance() # consume '}'


    def compileReturn(self):
        pass

    def compileExpressionList(self):
        pass

    def compileExpression(self):
        self.stackMachine.append([])
        while self.tokenizer.peek() not in [')', ';', ']']:
            self.compileTerm() # term left to the '='

            # handles if/while condition.
            if self.tokenizer.peek() in [ '=', '<', '>']: 
                if self.tokenizer.peek() == '=':
                    self.tokenizer.advance() # consume '='
                    self.compileTerm() # term right to the '='
                                    
                    token = self.tokenizer.peek()
                    token_type = self.tokenizer.getTokenType(token)

                    if token_type == 'opSymbol':
                        op = self.tokenizer.advance() # get the op
                        self.compileTerm()  # term right to the op
                        self._saveVarDetail(op)
        self.stackMachine.pop()
                        
                    
    # let x = y + z + 1
    # 
    # while (x=5)
    
    def compileTerm(self):
        token = self.tokenizer.advance() # term's first token
        token_type = self.tokenizer.getTokenType(token)

        if self.tokenizer.peek() == '=':
            self._saveVarDetail(token)

        elif token_type == 'integerConstant':
            self.writeVm.writePush('constant', token)
        
        elif token == '(':
            self.tokenizer.advance() # consume '('
            self.compileExpression()
            self.tokenizer.advance() # consume ')'

        elif token_type == 'unaryOp':
            self.compileTerm()
            if token == '-':
                self.writeVm.writeArithmetic('neg')
            else:
                self.writeVm.writeArithmetic('not')
        
        elif token_type == 'identifier':
            self._saveVarDetail(token)
        
        
# let x = y + z