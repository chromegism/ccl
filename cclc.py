import argparse
import string

class Token:
    def __init__(self, value, lineNum, charNum):
        self.value = value
        self.lineNum = lineNum
        self.charNum = charNum
        
    def __repr__(self):
        return f'Token - value: {self.value}, line number: {self.lineNum}, character number: {self.charNum}'

def lex(dat):
    word = ''
    token_stack = []
    line_count = 1
    char_count = 1
    
    
    
    for letter in dat:
        if letter in string.ascii_letters or letter in ['_', '"', "'"]:
            word += letter
            
        else:
            token_stack.append(Token(word, line_count, char_count))
            word = ''
            if letter == '\n':
                char_count = 0
                line_count += 1
            
        char_count += 1
        
    for i in token_stack:
        print(i)
            

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
    
    with open(args.file_in, 'r') as f:
        file_dat = f.read()
        
        lex(file_dat)