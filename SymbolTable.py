class SymbolTable:
    def __init__(self):
        self.scope = {}
        self.count = { "static": 0, "field": 0, "argument": 0, "local": 0 }


    def reset(self):
        self.scope = {}
        self.count = {"static": 0, "field": 0, "argument": 0, "local": 0}


    def has(self, name):
        return name in self.scope

    def define(self, name, type, kind):
        if kind in self.count:  
            self.scope[name] = {
                'type': type,
                'kind': kind,
                'index': self.count[kind]
            }
            self.count[kind] += 1  



    def var_count(self, kind):
        return self.count[kind]


    def kind_of(self, name):
        if name in self.scope:
            return self.scope[name]['kind']
        return None


    def type_of(self, name):
        if name in self.scope:
            return self.scope[name]['type']
        return None


    def index_of(self, name):
        if name in self.scope:
            return self.scope[name]['index']
        return None
        
