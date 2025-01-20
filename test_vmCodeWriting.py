import unittest
from unittest.mock import mock_open, patch
from CompilationEngine import CompilationEngine
from VmWriter import VmWriter

class Test2CompilationEngine(unittest.TestCase):
    
    def setUp(self):
        self.input_file = "dummy_input.jack"
        self.output_file = "dummy_output.vm"

        self.mocked_open = mock_open()
        self.patcher = patch("builtins.open", self.mocked_open)
        self.patcher.start()

        self.engine = CompilationEngine(self.input_file, self.output_file)

        self.engine.tokenizer.tokens = []  # Initialize with an empty token list.
        self.engine.writeVm = VmWriter(self.output_file)

    def tearDown(self):
        self.patcher.stop()

    def test_compile_term(self):
        self.engine.tokenizer.tokens = ["some", "tokens", "for", "term"]

        self.engine.compileTerm()
        self.engine.writeVm.close()

        handle = self.mocked_open()
        handle.write.assert_not_called()


