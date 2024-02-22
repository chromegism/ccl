import argparse
import string
import re

class IncludeError(Exception):
    def __init__(self, *args):
        self.args = args

class Include:
    def __init__(self, span, inc_type, value):
        self.span = span
        self.type = inc_type
        self.value = value
        
    def __repr__(self):
        return f'<Include object; span=({self.span[0]}, {self.span[1]}), type={self.type}, value=\"{self.value}\"'

class Function:
    def __init__(self, span, name, args, content_span, content):
        self.span = span
        self.name = name
        self.args = args
        self.content_span = content_span
        self.content = content

    def __repr__(self):
        return f'<Function object; span=({self.span[0]}, {self.span[1]}), name={self.name}, args={self.args}, content span=({self.content_span[0]}, {self.content_span[1]})'

def get_line_number(character_number, data):
    return data[:character_number].count('\n')

def parse_include(match):
    inc = Include(match.span(), 
        match.group().split()[1], 
        match.group().split('"')[1])
        
    if len(match.group(0).split()) != 3:
        raise IncludeError(f'\n\nError: \nline {get_line_number(inc.span[0], data_with_newlines)}: Include statement either has too many arguments ({len(match.group().split())}) or the file name has a space\n{match.group(0)}')
    
    return inc

def lex(data, lexinf):
    data_with_newlines = data
    data = ' '.join(data.split())
    #lexinf['includes'] = [Include(x.span(), x.group().split()[1], x.group().split('"')[1]) for x in re.finditer('include.*;', data)]
    includes = re.finditer('(include.*?;)', data)
    
    lexinf['includes'] = []
    
    for i in includes:
        inc = parse_include(i)
        
        lexinf['includes'].append(inc)
    
    lexinf['functions'] = [x for x in re.finditer('function.*?{.*?}', data)]

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                        prog='ProgramName',
                        description='What the program does',
                        epilog='Text at the bottom of help')

    parser.add_argument('file_in')
    parser.add_argument('-o', '--output', 
                        required=True)
    parser.add_argument('-f', '--format',
                        choices=['efi', 'EFI', 'os', 'OS'])

    args = parser.parse_args()
    lexer_info = {}
    
    with open(args.file_in, 'r') as f:
        file_dat = f.read()
        
        lex(file_dat, lexer_info)
    
    for i in range(len(lexer_info)):
        print(f'{list(lexer_info.keys())[i]} - {list(lexer_info.values())[i]}')