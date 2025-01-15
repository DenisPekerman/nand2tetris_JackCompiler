#!/usr/bin/env python3

import re

class JackTokenizer:

    KeywordsCodes = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]
    
    SymbolsCodes = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', 
                    '<', '>', '=', '~']

    #  negation is handled in getTokenType()
    symbolDict = { '+': 'add', '-': 'sub', '*': 'mult', '/': 'div', '&': 'and', 
                   '<': 'lt', '>': 'gt', '=': 'eq', '~': 'not' }


    keyword_Pattern = '(?!\w)|'.join(KeywordsCodes) + '(?!\w)'
    symbol_pattern = '[' + re.escape('|'.join(SymbolsCodes)) + ']'
    int_pattern = r'\d+'
    str_pattern = r'"[^"\n]*"'
    identifier_pattern = r'[a-zA-Z_]\w*'
    token = re.compile(keyword_Pattern + '|' + symbol_pattern + '|' + int_pattern + '|' + str_pattern + '|' + identifier_pattern)

    

    def __init__(self, input_file: str):
        self.currentToken = ""
        self.prevToken = ""
        self.data = ''
        if input_file:
            self.input_file = open(input_file, "r")
            self.data = self.input_file.read()

        self.data = re.sub(r'(//.*|/\*[\s\S]*?\*/)', '\n', self.data)   # remove all comments 
        self.data = self.data.strip()
        self.tokens = self.token.findall(self.data) # Find all tokens


    def advance(self):
        if self.hasMoreTokens():
            self.prevToken = self.currentToken if self.currentToken else None
            self.prevTokenType = self.getTokenType(self.prevToken) if self.prevToken else None

            self.currentToken = self.tokens.pop(0)
        return self.getTokenValue(self.currentToken) if self.currentToken else None

    
    def getTokenValue(self, tokenValue):
        if re.match(self.str_pattern, tokenValue) is not None:
            return tokenValue.strip('"')  
        return tokenValue


    def _UnaryOrSymbol(self, tokenValue):
        if tokenValue == '~':
            return 'unaryOp'
        elif tokenValue == '-':
            if self.prevTokenType in ['symbol', 'keyword'] and self.prevToken not in [')', ']']:
                return 'unaryOp'
        return 'symbol'
    
                        
    def getTokenType(self, tokenValue):
        if re.match(self.symbol_pattern, tokenValue) is not None:  # matches unaryOp as well
            if tokenValue in ['-', '~']:
                return self._UnaryOrSymbol(tokenValue)
            else:
                return 'symbol'
        elif re.match(self.keyword_Pattern, tokenValue) is not None:
            return "keyword"
        elif re.match(self.int_pattern, tokenValue) is not None:
            return "integerConstant"
        elif re.match(self.str_pattern, tokenValue) is not None:
            return "stringConstant"
        elif re.match(self.identifier_pattern, tokenValue) is not None:
            return "identifier"
        return None


    def getSymbolValue(self, token):
        return self.symbolDict.get(token)


    def hasMoreTokens(self):
        return len(self.tokens) > 0


    def peek(self, index: int = 0):
        return self.tokens[index] if len(self.tokens) > index else None
         
        




