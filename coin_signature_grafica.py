import random
import matplotlib.pyplot as plt

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

        #I = I + P2
        self.I.x += self.bank.P2.x
        self.I.y += self.bank.P2.y

        #Simplificado
        #Generar punto1         
        self.Q1 = self.bank.Q1

        #Generar punto2
        self.Q2 = self.bank.Q2

class Comercio:
    def __init__(self, bank):
        self.bank = bank
        self.user_vk = None

    def receive_verification_key(self, user_vk):
        self.user_vk = user_vk

    def receive_coin(self, coin):
        print("Comercio recibe moneda:")
        print("I:", coin[0].x, coin[0].y)
        print("Q2:", coin[1].x, coin[1].y)
        print("Signature:")
        print("C:", coin[2][0].x, coin[2][0].y)
        print("R:", coin[2][1].x, coin[2][1].y)
        print("S:", coin[2][2].x, coin[2][2].y)
        print("y:", coin[2][3])

#Funcion para visualizar puntos 
def visualize(bank, user, comercio):
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 8)

    plot_points(ax, [user.I.x, user.Q2.x], [user.I.y, user.Q2.y], label='User Public Keys', color='blue')
    plot_points(ax, [bank.Q.x, bank.Q1.x, bank.Q2.x], [bank.Q.y, bank.Q1.y, bank.Q2.y], label='Bank Public Keys', color='red')
    
    plot_lines(ax, [bank.Q.x, user.I.x], [bank.Q.y, user.I.y], color='black')
    
    ax.legend()
    plt.show()


def plot_points(ax, x_coords, y_coords, label, color):
    ax.scatter(x_coords, y_coords, label=label, color=color)

def plot_lines(ax, x_coords, y_coords, color, linestyle='dashed'):
    ax.plot(x_coords, y_coords, color=color, linestyle=linestyle)

def main():

    bank = Bank()
    user = User(bank, identity="User123")
    comercio = Comercio(bank)

    bank_point = (bank.Q.x, bank.Q.y)
    user_point = (user.I.x, user.I.y)
    C = Point(bank.z * user.I.x + user.Q1.x, bank.z * user.I.y + user.Q1.y)

    print("Bank Public Keys:")
    print("Q:", bank.Q.x, bank.Q.y)
    print("Q1:", bank.Q1.x, bank.Q1.y)
    print("Q2:", bank.Q2.x, bank.Q2.y)

    print("\nUser Public Keys:")
    print("I:", user.I.x, user.I.y)
    print("Q2:", user.Q2.x, user.Q2.y)

    print("\nCoin Generation:")
    print("C:", C.x, C.y)

    visualize(bank, user, comercio)

    ###########################################
    coin = (user.I, user.Q2)
    signature = generate_signature(coin, bank, C)
    received_coin = (user.I, user.Q2, signature)

    #Comercio recibe moneda
    comercio.receive_coin(received_coin)

def generate_signature(coin, bank, C):
    
    h = hash_function(coin)
    y = random.randint(1, 1000)
    R = Point(h * bank.Q.x + y * bank.P.x, h * bank.Q.y + y * bank.P.y)
    S = Point(h * C.x + y * coin[1].x, h * C.y + y * coin[1].y)

    return (C, R, S, y)

def hash_function(coin):
    ###
    return coin[0].x + coin[0].y + coin[1].x + coin[1].y

if __name__ == "__main__":
    main()
