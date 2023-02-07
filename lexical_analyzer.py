import re
from buffer import Buffer
import datetime


class LexicalAnalyzer:
    """!The statement LexicalAnalyzer class.
    Tokenize C/C++ language source code.
    """

    def __init__(self):
        """!The LexicalAnalyzer class initializer."""
        # Array of tokens
        self.tokens = []
        # Token row
        self.line_number = 1
        # Buffer to read file content
        self.buffer = Buffer()

    def tokenize(self, code):
        """! Tokenize the input code.
        @param code  C/C++ source code.
        @return  An array compounded by token, lexeme, row, column and raw_output(used to populate the output JSON file).
        """
        rules = [
            ('MAIN', r'main'),  # main
            ('INT', r'int'),  # int
            ('FLOAT', r'float'),  # float
            ('IF', r'if'),  # if
            ('ELSE', r'else'),  # else
            ('WHILE', r'while'),  # while
            ('FOR', r'for'),  # for
            ('READ', r'read'),  # read
            ('PRINT', r'print'),  # print
            ('LBRACKET', r'\('),  # (
            ('RBRACKET', r'\)'),  # )
            ('LBRACE', r'\{'),  # {
            ('RBRACE', r'\}'),  # }
            ('COMMA', r','),  # ,
            ('PCOMMA', r';'),  # ;
            ('EQ', r'=='),  # ==
            ('NE', r'!='),  # !=
            ('LE', r'<='),  # <=
            ('GE', r'>='),  # >=
            ('OR', r'\|\|'),  # ||
            ('AND', r'&&'),  # &&
            ('ATTR', r'\='),  # =
            ('LT', r'<'),  # <
            ('GT', r'>'),  # >
            ('PLUS', r'\+'),  # +
            ('MINUS', r'-'),  # -
            ('MULT', r'\*'),  # *
            ('DIV', r'\/'),  # /
            ('ID', r'[a-zA-Z]\w*'),  # IDENTIFIERS
            ('FLOAT_CONST', r'\d(\d)*\.\d(\d)*'),  # FLOAT
            ('INTEGER_CONST', r'\d(\d)*'),  # INT
            ('NEWLINE', r'\n'),  # NEW LINE
            ('SKIP', r'[ \t]+'),  # SPACE and TABS
            ('MISMATCH', r'.'),  # ANOTHER CHARACTER
        ]

        tokens_join = '|'.join('(?P<%s>%s)' % x for x in rules)
        lin_start = 0

        # Lists of output for the program
        token = []
        lexeme = []
        row = []
        column = []
        raw_output = []

        # It analyzes the code to find the lexemes and their respective Tokens
        for m in re.finditer(tokens_join, code):
            token_type = m.lastgroup
            token_lexeme = m.group(token_type)

            if token_type == 'NEWLINE':
                lin_start = m.end()
                self.line_number += 1
            elif token_type == 'SKIP':
                continue
            elif token_type == 'MISMATCH':
                raise RuntimeError('%r unexpected on line %d' % (token_lexeme, self.line_number))
            else:
                col = m.start() - lin_start
                column.append(col)
                token.append(token_type)
                lexeme.append(token_lexeme)
                row.append(self.line_number)
                self.tokens.append({
                    'type': token_type,
                    'value': token_lexeme
                })
                raw = 'Token = {0}, Lexeme = \'{1}\', Row = {2}, Column = {3}'.format(token_type, token_lexeme,
                                                                                      self.line_number, col)
                raw_output.append(raw)

        return token, lexeme, row, column, raw_output

    def get_tokens(self, input_file: str, output_file: str = None) -> list:
        """! Tokenize the input code.
        @param input_file  The input C/C++ file.
        @param output_file  The output JSON file.
        @return  A list of tokens.
        """

        raw_output = []
        # Tokenize and reload of the buffer
        for i in self.buffer.load_buffer(input_file):
            t, lex, lin, col, raw = self.tokenize(i)
            raw_output.extend(raw)

        if output_file:
            f = open(output_file, "w")
            f.write('\n **** Syntactic analyzer : output data ****' + '\n**** Generation date: {0} ****'
                    .format(datetime.datetime.now().strftime("%x %X"))
                    + '\n\n')
            for i in raw_output:
                f.write('\n' + i)
                print(i)

            f.close()
            print('\nTokens/Lexemes file created with success.')

        return self.tokens


analyzer = LexicalAnalyzer()
analyzer.get_tokens("program.c", "lexemes_tokens.txt")
