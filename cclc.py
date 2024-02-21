import argparse

class Token:
    def __init__(self, id, value, lineNum, charNum):
        self.id = id
        self.value = value
        self.lineNum = lineNum
        self.charNum = charNum
        
    def __repr__(self):
        return f'Token - id: {self.id}, value: {self.value}, line number: {self.lineNum}, character number: {self.charNum}'

def lex(dat):
    pass

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