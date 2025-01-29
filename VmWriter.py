

class VmWriter:
    
    def __init__(self, output_file):
        self.output_file = open(output_file, 'w')        


    def _writeToFile(self, input):
        self.output_file.write(input + '\n')
        self.output_file.flush()


    def writePush(self, segment, index):
        self._writeToFile(f'push {segment} {index}')
        

    def writePop(self, segment, index):
        self._writeToFile(f'pop {segment} {index}')


    def writeArithmetic(self, command):
          self._writeToFile(command)


    def writeLabel(self, label):
        self._writeToFile(f"label {label}")


    def writeGoto(self, label):
        self._writeToFile(f"goto {label}")


    def writeIf(self, label):
        self._writeToFile(f"if-goto {label}")
        

    def writeCall(self, name, nArgs):
        self._writeToFile(f"call {name} {nArgs}")


    def writeFunction(self, name, nVars):
        self._writeToFile(f"function {name} {nVars}")


    def writeReturn(self):
        self._writeToFile("return")
        

    def close(self):
        self.output_file.close()
        
