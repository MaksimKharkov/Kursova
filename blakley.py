import random
from sympy import Matrix

def generate_polynomial(degree, prime):
    polynomial = [random.randint(1, prime - 1) for _ in range(degree)]
    polynomial.append(random.randint(1, prime - 1))  
    return polynomial

def evaluate_polynomial(polynomial, x, prime):
    y = 0
    for i, coef in enumerate(polynomial):
        y += coef * (x ** i)
    return y % prime

def share_secret(secret, num_shares, prime, degree):
    polynomial = generate_polynomial(degree, prime)
    shares = []
    for i in range(1, num_shares + 1):
        x = random.randint(1, prime - 1)
        y = evaluate_polynomial(polynomial, x, prime)
        shares.append((x, y))
    return shares

def reconstruct_secret(shares, prime):
    num_shares = len(shares)
    x_values = [share[0] for share in shares]
    y_values = [share[1] for share in shares]
    x_matrix = Matrix(num_shares, num_shares, lambda i, j: x_values[i] ** j)
    y_vector = Matrix(y_values)
    coefficients = x_matrix.inv_mod(prime) * y_vector
    secret = coefficients[-1] % prime
    return secret

prime = 257  
degree = 2   

secret = 123  
num_shares = 5  
shares = share_secret(secret, num_shares, prime, degree)
print("Shares:", shares)

reconstructed_secret = reconstruct_secret(shares[:degree + 1], prime)
print("Reconstructed Secret:", reconstructed_secret)
