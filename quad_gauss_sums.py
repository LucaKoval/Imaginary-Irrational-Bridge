import math
from sympy import legendre_symbol

# The number up to which we check for primes
UPPER = 100

"""
Naively generate a list of primes from 3 to UPPER
2 is not included because the calculating the Legendre symbol
of some integer k < p and p, where p is prime, requires p
to be an *odd* prime. The equation representing the square
root of two can be be found using Euler's formula evaluated
at theta = pi/4. We get sqrt(2) = i^(7/2) + i^(1/2).
"""
primes = []
for num in range(3, UPPER, 2):
    if all(num % i != 0 for i in range(3, int(math.sqrt(num)) + 1, 2)):
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
for p in primes:
    """
    Keep track of the counts of Legendre symbols. Note that zero
    is not a possible value as we will only be calculating
    Legendre symbols of some integer k < p and p, where p
    is an odd prime
    """
    legendre_counts = {-1: 0, 1: 0}

    # Initialize the output string
    op_string = ""
    total_coef = (-1) ** ((p - 1) / 2)
    root_sum = 0
    root_sum_string = ""

    # Loop through all integers k < p
    for k in range(1, p):
        # Calculate the Legendre symbol
        coef = legendre_symbol(k, p)

        # Keep track of the Legendre symbol counts
        legendre_counts[coef] += 1

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

        # Add the current term string to the sum
        op_string += op

    # Strip the complete string of the very first operation.
    # Otherwise, the result will begin with a + or - sign
    root_sum_string = root_sum_string[3:]

    # Print the result
    print(f"sqrt({p}) = {root_sum_string}\n")
