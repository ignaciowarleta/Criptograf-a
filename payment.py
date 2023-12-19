import random
from hashlib import sha256
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class User:
    def __init__(self, comercio, identity):
        self.comercio = comercio
        self.identity = identity
        self.generate_key_pair()

    def generate_key_pair(self):
        self.u1 = random.randint(1, 1000)
        self.s = random.randint(1, 1000)
        self.t1 = random.randint(1, 1000)
        self.t2 = random.randint(1, 1000)

    def payment_protocol(self, A, B, C, R, S, y):
        h0 = self.hash_function(A, B, self.comercio.account_number, self.comercio.transaction_datetime)

        y1 = (self.u1 * self.s) * h0 + self.t1
        y2 = self.s * h0 + self.t2

        print("\nValores obtenidos durante la ejecución:")
        print(f"h0: {h0}")
        print(f"y1: {y1}")
        print(f"y2: {y2}")

        if self.verify_relation(y1, y2, h0, A, B, self.comercio.P1, self.comercio.P2) and self.verify_signature(A, B, C, R, S, y, h0):
            print("Pago aceptado")
        else:
            print("Pago rechazado.")

    def verify_relation(self, y1, y2, h0, A, B, P1, P2):
        return y1 * P1.x + y2 * P2.x == h0 * A.x + B.x and y1 * P1.y + y2 * P2.y == h0 * A.y + B.y

    def verify_signature(self, A, B, C, R, S, y, h0):
        return (
            y * A.x == h0 * C.x + S.x and
            y * A.y == h0 * C.y + S.y and
            y * Point(1, 0).x == h0 * R.x + Point(1, 0).x and
            y * Point(1, 0).y == h0 * R.y + Point(1, 0).y
        )

    def hash_function(self, *args):
        concatenated_data = ''.join(str(arg.x) + str(arg.y) if isinstance(arg, Point) else str(arg) for arg in args).encode()
        return int(sha256(concatenated_data).hexdigest(), 16)

class Comercio:
    def __init__(self):
        self.P = Point(random.randint(1, 1000), random.randint(1, 1000))
        self.P1 = Point(random.randint(1, 1000), random.randint(1, 1000))
        self.P2 = Point(random.randint(1, 1000), random.randint(1, 1000))
        self.account_number = self.P.x
        self.transaction_datetime = "20230101120000" 
    def deposit(self, user, A, B, C, R, S, y):
        user.payment_protocol(A, B, C, R, S, y)

def main():
    comercio = Comercio()
    user = User(comercio, identity="User123")

    # Simular un pago
    A = Point(random.randint(1, 1000), random.randint(1, 1000))
    B = Point(random.randint(1, 1000), random.randint(1, 1000))
    C = Point(random.randint(1, 1000), random.randint(1, 1000))
    R = Point(random.randint(1, 1000), random.randint(1, 1000))
    S = Point(random.randint(1, 1000), random.randint(1, 1000))
    y = random.randint(1, 1000)

    comercio.deposit(user, A, B, C, R, S, y)

if __name__ == "__main__":
    main()

