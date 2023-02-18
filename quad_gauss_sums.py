import math
from sympy import legendre_symbol

UPPER = 100

primes = []
for num in range(3, UPPER, 2):
    if all(num%i!=0 for i in range(3,int(math.sqrt(num))+1, 2)):
    	primes.append(num)

for p in primes:
	legendre_counts = {-1: 0, 1: 0}
	op_string = ''
	total_coef = (-1)**((p - 1)/2)
	root_sum = 0
	root_sum_string = ''
	for k in range(1, p):
		coef = legendre_symbol(k, p)
		legendre_counts[coef] += 1
		op = '+'
		if coef == -1:
			op = '-'
		pow_numerator = 4*k
		pow_denominator = p
		if total_coef == -1:
			pow_numerator = 4*k - p
		root_sum_string += f' {op} i^({pow_numerator}/{pow_denominator})'
		op_string += op

	root_sum_string = root_sum_string[3:]
	print(f'sqrt({p}) = {root_sum_string}\n')
	# print(op_string)
	# print(f'for {p}, legendre_counts: {legendre_counts}')