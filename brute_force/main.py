from random import randint
from math import gcd

import itertools
from multiprocessing import Pool

# from numba import njit, prange


# sqrtList = [2, 3, 5, 7, 11, 13]
# sqrtList = [5, 7, 11, 13]
sqrtList = [2]
max_list_elt = max(sqrtList)

# Five total terms
total_terms = 2
# num_tries = 100000
# for _ in range(total_terms):
# 	current_term = 0
# 	for coef in range()

# 	total += current_term


def to_string(coefNumerator, coefDenominator, powerNumerator, powerDenominator, plusMinus):
	string = f"({coefNumerator}/{coefDenominator})i^({powerNumerator}/{powerDenominator})"

	if plusMinus == 1:
		string = "-" + string

	return string


# Generate the terms
terms = set()
termsToParams = {}

def gen_terms():
	for coefNumerator in range(0, max_list_elt + 1):
		for coefDenominator in range(1, max_list_elt + 1):
			for powerNumerator in range(1, max_list_elt + 1):
				for powerDenominator in range(1, max_list_elt + 1):
					if gcd(coefNumerator, coefDenominator) == 1 and gcd(powerNumerator, powerDenominator) == 1:
						termNotFinalized = (coefNumerator/coefDenominator) * pow(1j, powerNumerator/powerDenominator)
						terms.add(coefNumerator * 1j)
						for plusMinus in range(2):
							if plusMinus == 0:
								terms.add(termNotFinalized)
								termsToParams[termNotFinalized] = (coefNumerator, coefDenominator, powerNumerator, powerDenominator, plusMinus)
							else:
								terms.add(-termNotFinalized)
								termsToParams[-termNotFinalized] = (coefNumerator, coefDenominator, powerNumerator, powerDenominator, plusMinus)

	return terms, termsToParams

terms, termsToParams = gen_terms()
print(len(terms))


# subsets = []
# for subset in itertools.combinations_with_replacement(terms, total_terms):
# 	subsets.append(subset)
# num_subsets = len(subsets)

def comb_with_replacement(n): # the argument n is the number of items to select
	res = list(itertools.combinations_with_replacement(terms, n)) # create a list from the iterator
	return res


def main():
	p = Pool(4)
	times = range(0, len(terms)+1)
	values = p.map(comb_with_replacement, times) # pass the range as the sequence of arguments!
	print(values)
	p.close()
	p.join()
	# print(values)


if __name__ == '__main__':
	main()


# @njit(parallel=True)
def compute_bridge():
	# for subset in itertools.combinations_with_replacement(terms, total_terms):
	for derp in prange(num_subsets):
		subset = subsets[derp]
		total = 0
		for term in subset:
			# total += term[0]
			total += term

		for num in sqrtList:
			if abs(pow(num, 1/2) - total.real) < 1e-10:
				if num == 7:
					print(f"Found near the square root of {num}.")
					print()
				# term_string = ""
				# for i, term in enumerate(subset):
				# 	term_string += to_string(*termsToParams[term])
				# 	if i < len(subset) - 1:
				# 		term_string += " + "
				# print(term_string, total)
				# print()
			if abs(total.imag) < 1e-10 and abs(pow(num, 1/2) - total.real) < 1e-10:
				print(f"Found for the square root of {num}.")
				term_string = ""
				for i, term in enumerate(subset):
					term_string += to_string(*termsToParams[term])
					if i < len(subset) - 1:
						term_string += " + "
				print(term_string)
				print()




# terms_list = list(terms)
# for _ in range(num_tries):
# 	for _ in range(total_terms):
# 		index_to_choose = randint(0, len(terms_list) - 1)
# 		total += terms_list[index_to_choose]
# 		del terms_list[index_to_choose]

# 	for num in sqrtList:
# 		if abs(total.imag) < 1e-10 and abs(pow(num, 1/2) - total.real) < 1e-10:
# 			print(f"Found for the square root of {num}.")


# for term1 in terms:
# 	for term2 in terms:
# 		for term3 in terms:
# 			for term4 in terms:
# 				for term5 in terms:
# 					total = term1 + term2 + term3 + term4 + term5
# 					for num in sqrtList:
# 						if abs(total.imag) < 1e-10 and abs(pow(num, 1/2) - total.real) < 1e-10:
# 							print(f"Found for the square root of {num}.")


# for _ in range(1000000):
# 	total = complex(0, 0)
# 	for _ in range(total_terms):
# 		coefNumerator = randint(-7, 7)
# 		coefDenominator = randint(1, 7)

# 		powerNumerator = randint(-7, 7)
# 		powerDenominator = randint(1, 7)

# 		total += (coefNumerator/coefDenominator) * pow(1j, powerNumerator/powerDenominator)

# 	for num in sqrtList:
# 		if abs(total.imag) < 1e-10 and abs(pow(num, 1/2) - total.real) < 1e-10:
# 			print(f"Found for the square root of {num}.")