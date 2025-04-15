import argparse
import math
import sys
from collections import defaultdict
from colorama import Fore, Style
from sympy import legendre_symbol

parser = argparse.ArgumentParser(
	description="A bridge from the irrationals to the imaginaries."
)
parser.add_argument(
	"-u",
	"--upper",
	type=str,
	help="We will not map from the square roots of any primes greater than this upper limit.",
)
args = parser.parse_args()

upper = args.upper
if not upper:
	print(
		f'Please provide an upper bound using "-u" or "--upper". We will not map from the square roots of any primes greater than this upper limit.'
	)
	sys.exit(1)

try:
	upper = int(upper)
except:
	print(f"The upper bound must be an integer greater than three.")
	sys.exit(1)

if upper < 4:
	print(f"The upper bound must be an integer greater than three.")
	sys.exit(1)


# Checks if a number is prime
def is_prime(n: int) -> bool:
	if n == 1:
		return False
	return all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1))


# Checks if a number is prime, skipping checks of even factors and starting at 3
def is_prime_skip_even_start_at_three(n: int) -> bool:
	return all(n % i != 0 for i in range(3, int(math.sqrt(n)) + 1, 2))


# Checks if a number is a perfect square
def is_square(n: int) -> bool:
	return n == math.isqrt(i) ** 2


"""
Naively generate a list of primes from 3 to upper.
2 is not included because the calculating the Legendre symbol
of some integer k < p and p, where p is prime, requires p
to be an *odd* prime. The equation representing the square
root of two can be be found using Euler's formula evaluated
at theta = pi/4. We get sqrt(2) = i^(7/2) + i^(1/2).
"""
primes = []
for num in range(3, upper, 2):
	if is_prime_skip_even_start_at_three(num):
		# The odd integer is a prime if and only if all numbers from 3
		# through the square root of the odd integer are not factors
		primes.append(num)

"""
We now loop through our primes. We go about calculating a variant of 
quadratic Gauss sums as documented by David E Speyer here:
https://mathoverflow.net/questions/287947/is-every-square-root-of-an-integer-a-linear-combination-of-cosines-of-pi-rati?rq=1

As a side note, we are guaranteed that the square root of every prime
can be mapped to the imaginaries through a side effect of the
Kronecker-Weber theorem: https://en.wikipedia.org/wiki/Kronecker%E2%80%93Weber_theorem

The logic in the loop below is geared around outputing the string
representation of the sum of powers of i representation of the 
square root of an odd prime p. This allows the user to validate the
representation by, for example, directly taking the output of this
program and putting into Wolfram Alpha.
"""
legendre_position_counts = defaultdict(lambda: 0)
for p in primes:
	"""
	Keep track of the counts of Legendre symbols. Note that zero
	is not a possible value as we will only be calculating
	Legendre symbols of some integer k < p and p, where p
	is an odd prime
	"""
	legendre_counts = {-1: 0, 1: 0}

	# Initialize the output string
	total_coef = (-1) ** ((p - 1) / 2)
	root_sum = 0
	root_sum_string = ""

	# Loop through all integers k < p
	for k in range(1, p):
		# Calculate the Legendre symbol
		coef = legendre_symbol(k, p)

		# Keep track of the Legendre symbol counts
		legendre_counts[coef] += 1

		legendre_position_counts[k] += coef

		# Here we deal with the sign of the current term
		op = "+"
		if coef == -1:
			op = "-"

		# Initialize the numerator of the fraction to which i
		# is raised
		pow_numerator = 4 * k

		# To account for the possibility of a -1 appearing in
		# the square root of the prime p in the Gauss sum formula,
		# we must adjust to numerator of the fraction to which i
		# is raised accordingly
		if total_coef == -1:
			pow_numerator = 4 * k - p

		# Set the denominator of the fraction to which i
		# is raised
		pow_denominator = p

		# Format the string corresponding to the current term in the sum
		root_sum_string += f" {op} i^({pow_numerator}/{pow_denominator})"
		# root_sum_string += f"{op}"

	# Strip the complete string of the very first operation.
	# Otherwise, the result will begin with a + or - sign
	root_sum_string = root_sum_string[3:]

	# Print the result
	print(f"sqrt({p}) = {root_sum_string}\n")

legendre_position_counts_pairs = sorted(
	list(legendre_position_counts.items()), key=lambda pair: pair[1], reverse=True
)

# for i, val in legendre_position_counts_pairs:
# 	text = f"{i}: {val}"
# 	if is_prime(i):
# 		print(Fore.RED + text)
# 	elif is_square(i):
# 		print(Fore.GREEN + text)
# 	else:
# 		print(Style.RESET_ALL + text)
