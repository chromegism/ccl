import argparse
import string
import re
import sys

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class error_bases:
    SYNTAX = f'{color.BOLD}{color.RED}Fatal Syntax Error{color.END}'
    ASSEMBLER = f'{color.BOLD}{color.RED}Fatal Assembler Error{color.END}'
    COMPILER = f'{color.BOLD}{color.RED}Fatal Compiler Error{color.END}'
    LINKER = f'{color.BOLD}{color.RED}Fatal Linker Error{color.END}'
    WARNING = f'{color.BOLD}{color.YELLOW}Warning{color.END}'
    NOTICE = f'{color.BOLD}{color.CYAN}Notice{color.END}'

class IncludeError(Exception):
    def __init__(self, *args):
        self.args = args

class Include:
    def __init__(self, span, inc_type, value):
        self.span = span
        self.type = inc_type
        self.value = value
        
    def __repr__(self):
        return f'<Include object; span=({self.span[0]}, {self.span[1]}), type={self.type}, value=\"{self.value}\">'
    
class Constant:
    def __init__(self, name, const_type, value):
        self.name = name
        self.type = const_type
        self.value = value

    def __repr__(self):
        return f'<Constant object; name="{self.name}", type={self.type}, value={self.value}'


class Function:
    def __init__(self, span, name, args, content_span, content):
        self.span = span
        self.name = name
        self.args = args
        self.content_span = content_span
        self.content = content

    def __repr__(self):
        return f'<Function object; span=({self.span[0]}, {self.span[1]}), name={self.name}, args={self.args}, content span=({self.content_span[0]}, {self.content_span[1]})>'

def get_line_number(character_number, data):
    return data[:character_number].count('\n')

def lex_include(match, data_with_newlines):
    
    # getting values from the match
    span = match.span()
    grouped = match.group()
    
    # getting include type
    inc_type = re.search('(file)|(library)', grouped)
    if inc_type is None:
        try:
            line_num = get_line_number(span[0], data_with_newlines)
            error_text = grouped
            raise SyntaxError(f'{error_bases.SYNTAX}\nInclude statement does not contain a valid type.\n\nline {line_num}: \t{error_text}\n\nValid types are:\nlibrary - include a standard library\nfile - include a file from the same directory. These end with .ccli')
        except Exception as e:
            print(e)
            quit()
    else:
        inc_type = inc_type.group()
        
    # getting include location
    value = re.search('".+?"', grouped)
    if value is None:
        try:
            line_num = get_line_number(span[0], data_with_newlines)
            error_text = grouped
            raise SyntaxError(f'{error_bases.SYNTAX}\nInclude statement does not contain a file\n\nline {line_num}: \t{error_text}')
        except Exception as e:
            print(e)
            quit()
    else:
        value = value.group()
        value = value.lstrip('"').rstrip('"')
        
    # checking for multiple locations
    if len(re.findall('".+?"', grouped)) > 1:
        try:
            line_num = get_line_number(span[0], data_with_newlines)
            error_text = grouped
            raise SyntaxError(f'{error_bases.SYNTAX}\nInclude statements don\'t support multiple includes per line yet\n\nline {line_num}: \t{error_text}')
        except Exception as e:
            print(e)
            quit()
    
    inc = Include(span, inc_type, value)
    
    return inc

def lex_constants(match, data_with_newlines):
    return match

def lex(data, lexinf):
    data_with_newlines = data
    data = ' '.join(data.split())
    
    # checking for includes
    includes = re.finditer('include.+?;', data)
    lexinf['includes'] = []
    
    for i in includes:
        k = lex_include(i, data_with_newlines)
        lexinf['includes'].append(k)
    
    # checking for constants
    constants = re.finditer('constant.+?;', data)
    lexinf['constants'] = []
    
    for i in constants:
        k = lex_constants(i, data_with_newlines)
        lexinf['constants'].append(k)

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