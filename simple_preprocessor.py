#!/usr/bin/env python3

import sys
import re


MACRO_START="<<<"
MACRO_END=">>>"
class SimplePreprocessor(object):
    def __init__(self):
        self.symbols_table=dict()
        self.re_define=re.compile("define\s+(?P<id>[a-zA-Z0-9_]+)\s+(?P<value>[a-zA-Z0-9 ]+)")
        
    
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
                print (line, end="")
        
        
if __name__ == '__main__':
    try:
        
        SimplePreprocessor().process(sys.argv[1])
    except Exception as e:
        print (e)
        #print("""\n\tUsage:  simple_preprocessor.py <file>""")