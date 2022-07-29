
class bar:
    amount = 0
    of = 0
    def __init__(self, amount):
        self.of = amount

    def calc(self):
        sum = 0
        try:
            sum = int((self.amount/self.of)*100)
        finally:
            return sum

    def __str__(self):
        s = "["
        s += "".join("*" for i in range(self.calc()))
        s += "".join(" " for i in range(100 - self.calc()))
        if(self.calc() < 100):
            s += "] %" + str(self.calc())
        else:
            s += "] ok"
        return s

    def add(self):
        if self.amount != self.of:
            self.amount += 1
