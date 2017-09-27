#!/usr/bin/env python3

import sys
import re
import os


MACRO_START="<<<"
MACRO_END=">>>"
class SimplePreprocessor(object):
    def __init__(self):
        self.symbols_table=dict()
        self.re_define=re.compile("define\s+(?P<id>[a-zA-Z0-9_]+)\s+(?P<value>[a-zA-Z0-9 ]+)")
        self.re_include=re.compile("include\s+(?P<filename>(\S+))")
        
    def get_lines(self, filename):
        with open(filename, "r") as f:
            lines=f.readlines()
            lines_without_end_of_line=[]
            for l in lines:
                lines_without_end_of_line.append(l.strip(os.linesep))
            line=os.linesep.join(lines_without_end_of_line)
            return line + os.linesep
        return "Unable to read " + filename
    
    def run_macro(self, line, pos_macro_start, pos_macro_end):
        #print(line, self.re_define.match(line), end="")
        search_results=self.re_define.search(line)
        if self.re_define.search(line)!=None:
            #print("Encontre un define :"+line)
            id=search_results.group("id")
            value=search_results.group("value")
            #print (id, value)
            self.symbols_table[id]=value
            return ""
        include_results=self.re_include.search(line[pos_macro_start:pos_macro_end])
        if include_results!=None:
            filename=include_results.group("filename")
            line=self.get_lines(filename)
            return line
        return line
    
    
    def parse_line(self, line):
        pos_macro_start=line.find(MACRO_START)
        pos_macro_end=line.find(MACRO_END)
        line_has_macro= pos_macro_start!=-1 and pos_macro_end!=-1
        if line_has_macro:
            #print("Macro en:"+line)
            line_with_macro_executed=self.run_macro(line, pos_macro_start, pos_macro_end)
            return line_with_macro_executed
        else:
            return line
    
    
    def process(self, file_path):
        
        with open(file_path, "r") as f:
            for line in f.readlines():
                processed_line=self.parse_line(line)
                print (processed_line, end="")
        
        
if __name__ == '__main__':
    try:
        
        SimplePreprocessor().process(sys.argv[1])
    except Exception as e:
        print (e)
        #print("""\n\tUsage:  simple_preprocessor.py <file>""")