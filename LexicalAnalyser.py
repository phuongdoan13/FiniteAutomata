from enum import Enum, auto
    
class NumberException(Exception):
    """
        Numbers will be in the following formats, otherwise the program throws error:
        1) A string of digits possibly followed by a decimal point and a non-empty string of digits. 
        2) If there is a decimal point, the string before the decimal point should consist only of 0.
        3) If the number starts with 0, it is either just 0, 
        or 0.[something] where the [something] is a string of digits.
    """
    pass

class ExpressionException(Exception):
    """
        Expressions will beee in the following formats, otherwise the program throws error:
        1) A valid number is a valid expression. 
        2) Any valid expression, followed by an operator, followed by a valid number.
        3) The operators and numbers may or may not be separated by white space.
    """
    pass


class TokenType(Enum):
    Number = auto()
    Plus = auto()
    Minus = auto()
    Times = auto()
    Divide = auto()

class Token:

    def __init__(self, valueOrType):
        if isinstance(valueOrType, float):
            self.value = valueOrType
            self.type = TokenType.Number
        else:
            self.value = -1.0
            self.type = valueOrType

    def isNumber(self):
        return self.type == TokenType.Number

    def getType(self):
        return self.type

    def getValue(self):
        if self.isNumber():
            return self.value
        else:
            return None

    def typeOf(symbol):
        types = {
            '+': TokenType.Plus,
            '-': TokenType.Minus,
            '*': TokenType.Times,
            '/': TokenType.Divide
        }
        return types.get(symbol, None)
    
    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        if self.isNumber():
            if other.isNumber():
                return self.value == other.value
            else:
                return False
        else:
            if other.isNumber():
                return False
            else:
                return self.type == other.type

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        strings = {
            TokenType.Number: str(self.value),
            TokenType.Plus: "+",
            TokenType.Minus: "-",
            TokenType.Times: "*",
            TokenType.Divide: "/"
        }
        return strings.get(self.type, None)

    def __repr__(self):
        return str(self)


class LexicalAnalyser:
    class State(Enum):
        INIT = auto()
        DIGIT_0 = auto() # number start with 0;
        DIGIT = auto() # digit different from 0
        DEC_DIGIT = auto() # decimal digit
        DIGIT_WS = auto() # whitespace after digit
        OP = auto() # operator
        SINK = auto() # sink
    
    state = State.INIT

    @classmethod
    def analyse(cls, input):
        # Complete this method.
        # You will probably need to add more to this class.
        res = []
        arr = [c for c in input.strip()] # turn string into char array, striping all trailing and leading space
        buffer = '' #buffer for int digits
        dec_buffer = '0.' #buffer for dec digits
        isDecimal = False
        
        if(len(arr) == 0 or Token.typeOf(arr[0]) != None):
            #if the first char is an operator, 
            # or the array is empty
            #  throw error
            raise ExpressionException() 
        
        
        for i in range(0, len(arr)):
            char = arr[i]
            
            # 1) Current char is a digit
            if(char.isdigit()):
                # 1.1) Current digit is different from 0
                if(int(char) != 0):
                    if(cls.state == cls.State.INIT):
                        cls.state = cls.State.DIGIT
                        buffer += char
                        if(i + 1 == len(arr) or (not arr[i+1].isdigit() and arr[i+1] != '.')):
                            res.append(Token(float(buffer)))
                            buffer = ''
                    elif(cls.state == cls.State.DIGIT):
                        buffer += char
                        # if next element does not exist
                        if(i + 1 == len(arr) or not arr[i+1].isdigit()):
                            res.append(Token(float(buffer)))
                            buffer = ''
                    elif(cls.state == cls.State.DIGIT_0):
                        raise NumberException()
                    elif(cls.state == cls.State.DEC_DIGIT):
                        dec_buffer += char
                        if(i + 1 == len(arr) or not arr[i+1].isdigit()):
                            res.append(Token(float(dec_buffer)))
                            dec_buffer = '0.'
                    elif(cls.state == cls.State.DIGIT_WS):
                        raise ExpressionException()
                    elif(cls.state == cls.State.OP):
                        cls.state = cls.State.DIGIT
                        buffer += char
                        if(i + 1 == len(arr) or not arr[i+1].isdigit()):
                            res.append(Token(float(buffer)))
                            buffer = ''
                
                # 1.2) Current digit is 0            
                else:
                    if(cls.state == cls.State.INIT):
                        cls.state = cls.State.DIGIT_0
                        buffer += char
                        if(i + 1 == len(arr) or (not arr[i+1].isdigit() and arr[i+1] != '.')):
                            res.append(Token(float(buffer)))
                    elif(cls.state == cls.State.DIGIT):
                        buffer += char
                        # if next element does not exist
                        if(i + 1 == len(arr) or not arr[i+1].isdigit()):
                            res.append(Token(float(buffer)))
                            buffer = ''
                    elif(cls.state == cls.State.DIGIT_0):
                        raise NumberException()
                    elif(cls.state == cls.State.DEC_DIGIT):
                        dec_buffer += char
                        if(i + 1 == len(arr) or not arr[i+1].isdigit()):
                            res.append(Token(float(dec_buffer)))
                            dec_buffer = '0.'
                    elif(cls.state == cls.State.DIGIT_WS):
                        raise ExpressionException()
                    elif(cls.state == cls.State.OP):
                        cls.state = cls.State.DIGIT_0
                        buffer += char
                        if(i + 1 == len(arr) or (arr[i+1] != '.' and not arr[i+1].isdigit())):
                            res.append(Token(float(buffer)))
                            buffer = ''

            # 2) current char is an operator
            elif(Token.typeOf(char) != None):
                res.append(Token(Token.typeOf(char)))
                if(i + 1 == len(arr)):
                    raise ExpressionException()
                
                if(cls.state == cls.State.INIT):
                    raise ExpressionException()
                elif(cls.state == cls.State.DIGIT):
                    cls.state = cls.State.OP    
                elif(cls.state == cls.State.DIGIT_0):
                    cls.state = cls.State.OP 
                elif(cls.state == cls.State.DEC_DIGIT):
                    cls.state = cls.State.OP  
                elif(cls.state == cls.State.DIGIT_WS):
                    cls.state = cls.State.OP
                elif(cls.state == cls.State.OP):
                    raise ExpressionException()

            # 3) Current char is decimal point
            elif(char == '.'):
                if(cls.state == cls.State.INIT):
                    raise ExpressionException()
                if(cls.state == cls.State.DIGIT):
                    raise NumberException()    
                elif(cls.state == cls.State.DIGIT_0):
                    cls.state = cls.State.DEC_DIGIT 
                elif(cls.state == cls.State.DEC_DIGIT):
                    raise NumberException()
                elif(cls.state == cls.State.DIGIT_WS):
                    raise ExpressionException()
                elif(cls.state == cls.State.OP):
                    raise ExpressionException()

            # 4) current char is an whitespace
            elif(char == ' '):
                if(cls.state == cls.State.INIT):
                    pass # this will never happen since we strip before running
                if(cls.state == cls.State.DIGIT):
                    cls.state = cls.State.DIGIT_WS    
                elif(cls.state == cls.State.DIGIT_0):
                    cls.state = cls.State.DIGIT_WS 
                elif(cls.state == cls.State.DEC_DIGIT):
                    cls.state = cls.State.DIGIT_WS  
                elif(cls.state == cls.State.DIGIT_WS):
                    pass
                elif(cls.state == cls.State.OP):
                    pass

            # 5) Current char is not a valid input
            else:
                raise ExpressionException()
                
        return res


def main():
    #print(LexicalAnalyser.analyse("0.02+ 0 - 0.2346356346346 * 234234 / 0.234234"))
    print(LexicalAnalyser.analyse("ádfasdfasdf"))

if __name__ == "__main__":
    main()