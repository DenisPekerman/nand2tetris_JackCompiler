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

        self.writeVm = VmWriter(self.output_file)

        self.class_name = ''
        

    def _getVarDetail(self, token):
        name = token
        if self.st_subroutine.has(token):
            kind = self.st_subroutine.kind_of(token)
            type = self.st_subroutine.type_of(token)
            index = self.st_subroutine.index_of(token)

        elif self.st_class.has(token):
            kind = self.st_class.kind_of(token)
            type = self.st_class.type_of(token)
            index = self.st_class.index_of(token)

            var_details = {
                'name': name,
                'kind': kind,
                'type': type,
                'index': index
            }
        return var_details
    

    def _handleArray(self, token):
        var_detail = self._getVarDetail(token)
        if var_detail['kind'] == 'field':
            self.writeVm.writePush('this', var_detail['index'])
        else:
            self.writeVm.writePush(var_detail['kind'], var_detail['index'])
        self.writeVm.writeArithmetic('add')
        self.writeVm.writePop('pointer', '1')
        self.writeVm.writePush('that', '0')


    def _subroutineHelper(self):
        self.tokenizer.advance()  # consume 'subroutine'
        subroutine_type = self.tokenizer.advance()
        subroutine_name = self.tokenizer.advance()
        self.tokenizer.advance()  # consume '('

        if self.tokenizer.peek() != ')':
            nVars = self.compileParameterList()
        else:
            nVars = 0  

        self.tokenizer.advance()  # consume ')'
        self.tokenizer.advance()  # consume '{'

        return subroutine_type, subroutine_name, nVars



    def compileClass(self):
        self.st_class.reset() # reset class symbolTable

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
        self.st_subroutine.reset()# reset subroutine symbolTable 

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

                method_type, method_name, nVars = self._subroutineHelper()

                self.writeVm.writeFunction(f'{self.class_name}.{method_name}', nVars)

            elif self.tokenizer.peek() == 'function':
                function_type, function_name, nVars = self._subroutineHelper()

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
                self.writeVm.writePop('temp', 0) # discards the dummy value
            elif self.tokenizer.peek() == 'if':
                self.compileIf()
            elif self.tokenizer.peek() == 'while':
                self.compileWhile()
            elif self.tokenizer.peek() == 'return':
                self.compileReturn()
        self.tokenizer.advance() # consume '}'


    def compileLet(self):
        self.tokenizer.advance() # consume 'let'
        first_term = self.tokenizer.advance()
        var_detail = self._getVarDetail(first_term)
        self.tokenizer.advance() # consume '='
        self.compileExpression()
        self.writeVm.writePop(var_detail['kind'], var_detail['index'])
        self.tokenizer.advance() # consume ';'


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
        self.tokenizer.advance() # consume 'return'
        if self.tokenizer.peek() == ';':
            self.writeVm.writePush('constant', 0)
        else:
            self.compileExpression()

        self.writeVm.writeReturn()
        self.tokenizer.advance()  # consume ';'


    def compileExpressionList(self):
        var_count = 0
        while self.tokenizer.peek() != ')':
            self.compileExpression()
            var_count += 1
            if self.tokenizer.peek() == ',':
                self.tokenizer.advance() # consume ','
            else:
                break
        return var_count
    

    def compileExpression(self):
        self.compileTerm() 
        token = self.tokenizer.peek()
        token_type = self.tokenizer.getTokenType(token)

        while token_type == 'opSymbol':
            op = self.tokenizer.advance() # get operator
            self.compileTerm() # get next term

            if op == '+':
                self.writeVm.writeArithmetic('add')
            elif op == '-':
                self.writeVm.writeArithmetic('sub')
            elif op == '*':
                self.writeVm.writeCall('Math.multiply', 2)
            elif op == '/':
                self.writeVm.writeCall('Math.divide', 2)
            elif op == '|':
                self.writeVm.writeArithmetic('or')
            elif op == '&':
                self.writeVm.writeArithmetic('and')
            elif op == '=':
                self.writeVm.writeArithmetic('eq')
            elif op == '<':
                self.writeVm.writeArithmetic('lt')
            elif op == '>':
                self.writeVm.writeArithmetic('gt')
            
            token = self.tokenizer.peek()
            token_type = self.tokenizer.getTokenType(token)
        
        

    def compileTerm(self):
        token = self.tokenizer.peek() # term's first token
        token_type = self.tokenizer.getTokenType(token)
        
        if token == '(':
            self.tokenizer.advance() # consume '('
            self.compileExpression()
            self.tokenizer.advance() # consume ')'

        elif token_type == 'unaryOp':
            op = self.tokenizer.advance() # get the unary op
            self.compileTerm()
            if op == '-':
                self.writeVm.writeArithmetic('neg')
            else:
                self.writeVm.writeArithmetic('not')

        elif token_type == 'integerConstant':
            int_token = self.tokenizer.advance()
            self.writeVm.writePush('constant', int_token)

        elif token_type == 'stringConstant':
            str_token = self.tokenizer.advance()
            self.writeVm.writePush('constant', len(str_token)) 
            self.writeVm.writeCall('string.new', 1)   
            for letter in str_token:
                self.writer.writePush('constant', ord(letter))
                self.writer.writeCall('String.appendChar', 2)

        elif token in ['true', 'false', 'null', 'this']:
            key_token = self.tokenizer.advance()
            if key_token == 'this':
                self.writeVm.writePush('pointer', 0)
            else:
                self.writeVm.writePush('constant', 0)
                if key_token == "true":
                    self.writeVm.writeArithmetic('not')

        elif token_type == 'identifier':
            ident_token = self.tokenizer.advance()

            if self.tokenizer.peek() == '[':
                self.tokenizer.advance() # consume '['
                self.compileExpression()
                self.tokenizer.advance() # consume ']'
                self._handleArray(ident_token)

            if self.tokenizer.peek() == '(':
                self.tokenizer.advance() # consume '('
                nVars = self.compileExpressionList()
                self.tokenizer.advance() # consume ')'
                self.writeVm.writeCall(ident_token, nVars)

            if self.tokenizer.peek() == '.':
                self.tokenizer.advance() # consume '.'
                class_name = ident_token
                subroutine_name = self.tokenizer.advance() # get subroutine name
                self.tokenizer.advance() # consume '('
                nVars = self.compileExpressionList()
                self.tokenizer.advance() # consume ')'
                self.writeVm.writeCall(f'{class_name}.{subroutine_name}',nVars)


            

        