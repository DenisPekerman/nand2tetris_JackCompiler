#!/usr/bin/env python3

from JackTokenizer import JackTokenizer
from VmWriter import VMWriter
from SymbolTable import SymbolTable


class CompilationEngine:

    def __init__(self, input: str, output_file):
        self.output_file = output_file

        self.tokenizer = JackTokenizer(input)
        # St = symbol table 
        self.st_class = SymbolTable()
        self.st_subroutine = SymbolTable()

        self.writeVm = VMWriter(output_file)

        self.class_name = ''

            
    def _subroutineHelper(self):
        self.tokenizer.advance() # consume 'method'
        subroutine_type = self.tokenizer.advance()
        subroutine_name = self.tokenizer.advance()
        self.tokenizer.advance() # consume '('

        if self.tokenizer.peek() == ')':
            self.tokenizer.advance() # consume ')'
            self.tokenizer.advance() # consume '{'
        else:
            self.compileParameterList()

        return (subroutine_type, subroutine_name)

    def compileClass(self):
        self.tokenizer.advance() # 'class'
        self.class_name = self.tokenizer.advance() # class name
        self.tokenizer.advance() # {
        
        if self.tokenizer.peek() in ['static', 'field']:
            self.compileClassVarDec()

        if self.tokenizer.peek() in ['constructor', 'method', 'function']:
            self.compileSubroutine()


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

        if self.tokenizer.peek() == 'constructor':
            while self.tokenizer.peek() != '(':
                self.tokenizer.advance()
            self.tokenizer.advance() # consume '('
            
            if self.tokenizer.peek() == ')':
                self.tokenizer.advance() # consume ')'
                self.tokenizer.advance() # consume '{'
            else:
                self.compileParameterList()
            
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

            

    def compileVarDec(self):
        pass
        
    

    def compileParameterList(self):
        pass

    def compileSubroutineBody(self):
        pass

    def compileStatements(self):
        pass

    def compileLet(self):
        pass

    def compileIf(self):
        pass

    def compileWhile(self):
        pass

    def compileDo(self):
        pass

    def compileReturn(self):
        pass

    def compileExpressionList(self):
        pass

    def compileExpression(self):
        pass

    def compileTerm(self):
        first_var = self.tokenizer.advance()
        if self.tokenizer.peek() == '[':
            self.tokenizer.advance() # consume '['
            arr_index = self.tokenizer.advance() # get index
            self.tokenizer.advance() # consume ']'

        self.tokenizer.advance() # consume '='

        if self.tokenizer.peek() == '(':
            pass
        
