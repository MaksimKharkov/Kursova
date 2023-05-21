import random
from sympy import Symbol, mod_inverse
from functools import reduce

def generate_polynomial(coefs, secret):
    polynomial = [secret] + [random.randint(1, prime - 1) for _ in range(coefs - 1)]
    return polynomial

def evaluate_polynomial(polynomial, x, prime):
    y = 0
    for i, coef in enumerate(polynomial):
        y += coef * (x ** i)
    return y % prime

def lagrange_basis_polynomial(j, x_values, prime):
    x = Symbol('x')
    numerator = [(x - x_values[m]) % prime for m in range(len(x_values))]
    denominator = [(x_values[j] - x_values[m]) % prime for m in range(len(x_values)) if m != j]
    basis_polynomial = reduce(lambda a, b: (a * b) % prime, numerator) * mod_inverse(reduce(lambda a, b: (a * b) % prime, denominator), prime) % prime
    return basis_polynomial

def share_secret(secret, num_shares, threshold, prime):
    polynomial = generate_polynomial(threshold, secret)
    x_values = list(range(1, num_shares + 1))
    shares = [(x, evaluate_polynomial(polynomial, x, prime)) for x in x_values]
    return shares

def reconstruct_secret(shares, threshold, prime):
    x_values = [share[0] for share in shares[:threshold]]
    y_values = [share[1] for share in shares[:threshold]]
    secret = sum([y * lagrange_basis_polynomial(j, x_values, prime) % prime for j, y in enumerate(y_values)]) % prime
    return secret

prime = 257  
threshold = 2 

secret = 123  
num_shares = 5  
shares = share_secret(secret, num_shares, threshold, prime)
print("Shares:", shares)

reconstructed_secret = reconstruct_secret(shares[:threshold], threshold, prime)
print("Reconstructed Secret:", reconstructed_secret)
