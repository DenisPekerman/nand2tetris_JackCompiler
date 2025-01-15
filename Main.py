#!/usr/bin/env python3
import os
import sys
from CompilationEngine import CompilationEngine

class JackAnalyzer:
    
    def __init__(self, input_file_or_folder):
        self.input_file_or_folder = input_file_or_folder
        self.output_file = JackAnalyzer.getOutputPath(input_file_or_folder)


    @staticmethod
    def getOutputPath(input_file_or_folder):      
        return input_file_or_folder.replace('.jack', '.vm')
    

    @staticmethod
    def getAllJackFiles(input_file_or_folder):
        isFile = os.path.isfile(input_file_or_folder)
        if isFile:
            if input_file_or_folder.endswith('.jack'):
                return [input_file_or_folder]

        else: 
            files = os.listdir(input_file_or_folder) 
            files = [file for file in files if file.endswith('.jack')]
            files = [os.path.join(input_file_or_folder, file ) for file in files]
            return files
    

    def run(self):
        for file in JackAnalyzer.getAllJackFiles(self.input_file_or_folder):
            print(file)
            compileEngine = CompilationEngine(file, JackAnalyzer.getOutputPath(file))
            compileEngine.compileClass()



if __name__ == "__main__":

    input = sys.argv[1]
    main = JackAnalyzer(input)
    main.run()
    
    
    