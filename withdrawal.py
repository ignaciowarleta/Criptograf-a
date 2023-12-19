import random
from hashlib import sha256
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Bank:
    def __init__(self):
        self.P = self.generate_random_element()
        self.P1 = self.generate_random_element()
        self.P2 = self.generate_random_element()
        self.z = random.randint(1, 1000)
        self.Q = Point(self.z * self.P.x, self.z * self.P.y)
        self.Q1 = Point(self.z * self.P1.x, self.z * self.P1.y)
        self.Q2 = Point(self.z * self.P2.x, self.z * self.P2.y)

    def generate_random_element(self):
        return Point(random.randint(1, 1000), random.randint(1, 1000))

class User:
    def __init__(self, bank, identity):
        self.bank = bank
        self.identity = identity
        self.generate_key_pair()

    def generate_key_pair(self):
        self.u1 = random.randint(1, 1000)
        self.I = Point(self.u1 * self.bank.P1.x, self.u1 * self.bank.P1.y)
        self.I.x += self.bank.P2.x
        self.I.y += self.bank.P2.y
        self.Q1 = Point(self.u1 * self.bank.P.x, self.u1 * self.bank.P.y)
        self.ip = Point(self.u1 * self.bank.P2.x, self.u1 * self.bank.P2.y)

    def withdrawal_protocol(self):
        #Banco
        w = random.randint(1, 1000)
        R = Point(w * self.bank.P.x, w * self.bank.P.y)
        S = Point(w * self.I.x, w * self.I.y)

        #User
        s = random.randint(1, 1000)
        t1 = random.randint(1, 1000)
        t2 = random.randint(1, 1000)
        A = Point(s * self.I.x, s * self.I.y)
        B = Point(t1 * self.bank.P1.x + t2 * self.bank.P2.x, t1 * self.bank.P1.y + t2 * self.bank.P2.y)
        h = self.hash_function(A, B)
        

        #Comercio
        u = random.randint(1, 1000)
        while math.gcd(u, self.bank.z) != 1:
            u = random.randint(1, 1000)
        v = random.randint(1, 1000)
        C = Point(s * self.bank.Q.x, s * self.bank.Q.y)
        R = Point(u * R.x + v * self.bank.P.x, u * R.y + v * self.bank.P.y)
        S = Point(s * u * S.x + v * A.x, s * u * S.y + v * A.y)
        r = pow(u, -1, self.bank.z) * self.hash_function(A, B, C, R, S)

        #Banco
        y_received = r * self.bank.z + w

        print("\nValores generados durante el proceso:")
        print(f"s: {s}")
        print(f"t1: {t1}, t2: {t2}")
        print(f"A: ({A.x}, {A.y})")
        print(f"B: ({B.x}, {B.y})")
        print(f"h: {h}")
        print(f"w: {w}")
        print(f"R: ({R.x}, {R.y})")
        print(f"S: ({S.x}, {S.y})")
        print(f"u: {u}")
        print(f"v: {v}")
        print(f"C: ({C.x}, {C.y})")
        print(f"r: {r}")
        print(f"y_received: {y_received}")

        if self.verify_quasi_signature(y_received, A, B, C, R, S):
            print("Retiro completado con éxito.")
            return A, B, C, R, S, y_received
        else:
            print("Retiro fallido.")
            return None

    def verify_quasi_signature(self, y, A, B, C, R, S):
        h = self.hash_function(A, B, C, R, S)
        return (
            y * self.bank.P.x == h * self.bank.Q.x + R.x and
            y * self.bank.P.y == h * self.bank.Q.y + R.y and
            y * A.x == h * C.x + S.x and
            y * A.y == h * C.y + S.y
        )

    def hash_function(self, *args):
        concatenated_data = ''.join(str(arg.x) + str(arg.y) for arg in args).encode()
        return int(sha256(concatenated_data).hexdigest(), 16)

class Comercio:
    def __init__(self, bank):
        self.bank = bank

    def deposit_coin(self, coin):
        print("\Comercio recibe moneda:")
        print(f"A: ({coin[0].x}, {coin[0].y})")
        print(f"B: ({coin[1].x}, {coin[1].y})")
        print(f"C: ({coin[2].x}, {coin[2].y})")
        print(f"R: ({coin[3].x}, {coin[3].y})")
        print(f"S: ({coin[4].x}, {coin[4].y})")
        print(f"y: {coin[5]}")

def main():
    bank = Bank()
    user = User(bank, identity="User123")
    comercio = Comercio(bank)

    coin = user.withdrawal_protocol()

    if coin:
        comercio.deposit_coin(coin)

if __name__ == "__main__":
    main()

