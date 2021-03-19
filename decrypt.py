class one:

    def __init__(self, a=0, b=0):
        self.a = a
        self.b = b
        print("Class one constructor")
        print(f"a = {self.a}\nb = {self.b}")

    def do_stuff_inline(self):
        return self.a + self.b

    def create_object_two(self):
        return two(self.a, self.b)

    @staticmethod
    def do_stuff(a1, b1):
        return a1+b1


class two:

    def __init__(self, a=0, b=0):
        self.a = a
        self.b = b
        print("Class two constructor")
        print(f"a = {self.a}\nb = {self.b}")

    def do_stuff_inline(self):
        return self.a - self.b

    @property
    def one_cha_object(self):
        return one(self.a, self.b)
