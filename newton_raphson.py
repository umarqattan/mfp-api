def f(x):
	return x**3 - 6*x**2 + 11*x - 5

def f_prime(x):
	return 3*x**2-12*x+11


temp = 2
while f(temp) >= 1e-08:
	f_ = f(temp)
	f_prime_ = f_prime(temp)
	print(temp, f_, f_prime_, temp-f_/f_prime_)
	temp -= f_/f_prime_



