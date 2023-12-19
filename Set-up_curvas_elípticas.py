import random
import pygame
from pygame.locals import QUIT
import matplotlib.pyplot as plt
from Crypto.PublicKey import ECC

class Bank:
    def __init__(self):
        self.sk = ECC.generate(curve='P-256')
        self.vk = self.sk.public_key()

class User:
    def __init__(self, bank, identity):
        self.bank = bank
        self.identity = identity
        self.generate_key_pair()

    def generate_key_pair(self):
        self.sk = ECC.generate(curve='P-256')
        self.vk = self.sk.public_key()

class Merchant:
    def __init__(self, bank):
        self.bank = bank

    def receive_verification_key(self, user_vk):
        self.user_vk = user_vk


###################################

def plot_points(ax, x_coords, y_coords, label, color):
    ax.scatter(x_coords, y_coords, label=label, color=color)

def plot_lines(ax, x_coords, y_coords, color, linestyle='dashed'):
    ax.plot(x_coords, y_coords, color=color, linestyle=linestyle)

##################################    

bank = Bank()
user = User(bank, identity="User123")
merchant = Merchant(bank)

###################################

num_points = 200
x_coords, y_coords = [], []

for i in range(num_points):
    point = ECC.generate(curve='P-256').public_key()
    x_coords.append(point.pointQ.x)
    y_coords.append(point.pointQ.y)

###################################

fig, ax = plt.subplots()
fig.set_size_inches(8, 8)

###################################

plot_points(ax, x_coords, y_coords, label='Curva Elíptica', color='blue')

###################################

bank_point = (bank.vk.pointQ.x, bank.vk.pointQ.y)
user_point = (user.vk.pointQ.x, user.vk.pointQ.y)

merchant.receive_verification_key(user.vk)

merchant_point = (merchant.user_vk.pointQ.x, merchant.user_vk.pointQ.y)

###################################

plot_points(ax, [bank_point[0], user_point[0], merchant_point[0]],
            [bank_point[1], user_point[1], merchant_point[1]],
            label='Public Keys', color='red')

plot_lines(ax, [bank_point[0], user_point[0]], [bank_point[1], user_point[1]], color='black')
plot_lines(ax, [bank_point[0], merchant_point[0]], [bank_point[1], merchant_point[1]], color='black')

ax.legend()
plt.show()

pygame.quit()
