import unittest
from SymbolTable import SymbolTable

class TestSymbolTable(unittest.TestCase):

   def setUp(self):
    self.symbolTable = SymbolTable()
    

   def test_define(self):
      self.symbolTable.define("x", "int", "static")
      self.symbolTable.define("y", "int", "static")
      self.symbolTable.define("u", "boolean", "field")

      self.assertEqual(self.symbolTable.scope,
          {
              "x": {"type": "int", "kind": "static", "index": 0},
              "y": {"type": "int", "kind": "static", "index": 1},
              "u": {"type": "boolean", "kind": "field", "index": 0},
          }
      )  


   def test_reset(self):
      self.symbolTable.define("x", "int", "static")
      self.symbolTable.reset()

      self.assertEqual(self.symbolTable.scope, {})
      self.assertEqual(self.symbolTable.count, { "static: 0", "field: 0", "argument: 0", "local: 0"})


   def test_varCount(self):
      self.symbolTable.define("x", "int", "static")
      self.assertEqual(self.symbolTable.var_count("static"), 1)


   def test_kindOf(self):
      self.symbolTable.define("x", "int", "static")
      self.assertEqual(self.symbolTable.kind_of('x'), 'static')


   def test_typeOf(self):
      self.symbolTable.define("x", "int", "static")
      self.assertEqual(self.symbolTable.type_of('x'), 'int')


   def test_indexOf(self):
      self.symbolTable.define("x", "int", "static")
      self.symbolTable.define("y", "int", "static")
      self.assertEqual(self.symbolTable.index_of('y'), 1)
