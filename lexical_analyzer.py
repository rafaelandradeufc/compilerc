import sys
import os.path
import string


class LexicalAnalyzer():

    delimiters = ';,(){}[]'
    letters = string.ascii_letters
    digits = '0123456789'
    symbols = ''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHJKLMNOPQRSTUVXWYZ[\]^_`abcdefghijklmnopqrstuvxwyz{|}~'''
    operators = '+ - * / ++ -- == != > >= < <= && || ='.split()
    reserved_words  = '''if else switch int float long double char auto break case const continue default do enum extern goto register return short signed sizeof static volatile void unsigned union typedef struct printf scanf for while'''.split()


    def __init__(self):
        self.input_code = 'input-code.txt'
        self.output_lexical = 'output-lexical.txt'


    def is_delimiter(self, input):

        if input in self.delimiters:
            return True
        else:
            return False


    def identify_delimiter(self, input):

        position = self.delimiters.find(input)
        return 'token_delimiter_'+str(position)


    def is_letter(self, input):
        
        if input in self.letters:
            return True
        else:
            return False


    def is_digit(self, input):

        if input in self.digits:
            return True
        else:
            return False


    def is_symbol(self, input):

        if input in self.symbols:
            return True
        else:
            return False


    def is_operator(self, input):

        if input in self.operators:
            return True
        else:
            return False


    def identify_operator(self, input):

        position = 0

        for x in self.operators:
            if x == input:
                break
            position+=1
        
        if position > 5:
            return 'token_logical_operator_'+str(position)
        else:
            return 'token_mathematical_operator_'+str(position)
    

    def is_reserved_word(self, input):

        if input in reserved_words:
            return True
        else:
            return False


    def identify_reserved_word(self, input):

        for x in self.reserved_words:
            if x == input:
                break
            position+=1
        
        if position >= 0 and position <= 2:
            return 'token_reserved_word_conditional_'+str(position)

        elif position > 2 and position <= 7:
            return 'token_reserved_word_primitive_type_'+str(position)

        else:
            return 'token_reserved_word_'+str(position)


    def main(self):

        print('Iniciando analisador...')
        output_lexical = open(self.output_lexical, 'w')

        if not os.path.exists(self.input_code):
            output_lexical.write("Arquivo de entrada inexistente")
            return
        
        file = open(self.input_code, 'r')

        program_line = file.readline()
        line_num = 1

        while program_line:
            i=0

            line_len = len(program_line)
            while i < line_len:
                current_char = program_line[i]
                next_char = None

                if (i+1) < line_len:
                    next_char = program_line[i+1]

                # Delimitters
                if self.is_delimiter(current_char):
                    output_lexical.write(self.identify_delimiter(current_char)+' - '+current_char+' - '+str(line_num)+'\n')
                
                # Line Comments
                elif current_char == '/' and current_char == '/':
                    i = line_len

                # Block Comments
                elif current_char == '/' and current_char == '*':
                    cont = True
                    
                    line_start = line_num

                    while cont and not (current_char == '*' and current_char == '/'):

                        if (i+2) < line_len:

                            i+=1

                            current_char = program_line[i]
                            next_char = program_line[i+1]

                        else:

                            program_line = file.readline()
                            line_len = len(program_line)
                            line_num += 1
                            i=-1

                            if not program_line:
                                output_lexical.write('Erro Lexico - Comentario de bloco nao fechado - line: %d\n' %line_start)
                                cont = False
                    i += 1


                elif next_char != None and self.is_operator(current_char+next_char):
                    output_lexical.write(self.identify_operator(current_char+next_char)+' - '+current_char+next_char+' - '+str(line_num)+'\n')
                    i += 1
                
                elif self.is_operator(current_char):
                    output_lexical.write(self.identify_operator(current_char)+' - '+current_char+' - '+str(line_num)+'\n')

                
                i += 1

            program_line = file.readline()
            line_num+=1

        output_lexical.write('$')
        file.close()
        output_lexical.close()
    

lexical_analyzer = LexicalAnalyzer()
lexical_analyzer.main()