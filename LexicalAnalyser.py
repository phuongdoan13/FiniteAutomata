from enum import Enum, auto


class NumberException(Exception):
    


class ExpressionException(Exception):
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

    @classmethod
    def analyse(cls, input):
        # Complete this method.
        # You will probably need to add more to this class.
        return []


def main():
    print(LexicalAnalyser.analyse("Put something here to test"))


if __name__ == "__main__":
    main()