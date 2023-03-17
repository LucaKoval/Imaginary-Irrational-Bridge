import random
import itertools

# List of primes for which we wish to find imaginary sum representations
sqrtList = [2, 3, 5]

# Number of terms in the imaginary sum
total_terms = 3


# Helper function that ingests the numbers representing a term in the sum
# and outputs the corresponding, formatted string
def to_string(
    coefNumerator, coefDenominator, powerNumerator, powerDenominator, plusMinus
):
    string = (
        f"({coefNumerator}/{coefDenominator})i^({powerNumerator}/{powerDenominator})"
    )

    if plusMinus == 1:
        string = "-" + string

    return string


# Generate (representations for) all terms/powers of i for which we wish to use
# in the sums
terms = set()
for coefNumerator in range(0, 7):
    for coefDenominator in range(1, 7):
        for powerNumerator in range(0, 7):
            for powerDenominator in range(1, 7):
                termNotFinalized = (coefNumerator / coefDenominator) * pow(
                    1j, powerNumerator / powerDenominator
                )
                for plusMinus in range(2):
                    if plusMinus == 0:
                        terms.add(
                            (
                                termNotFinalized,
                                (
                                    coefNumerator,
                                    coefDenominator,
                                    powerNumerator,
                                    powerDenominator,
                                    plusMinus,
                                ),
                            )
                        )
                    else:
                        terms.add(
                            (
                                -termNotFinalized,
                                (
                                    coefNumerator,
                                    coefDenominator,
                                    powerNumerator,
                                    powerDenominator,
                                    plusMinus,
                                ),
                            )
                        )

# Generate all combinations based on the above terms
combos = itertools.combinations_with_replacement(terms, total_terms)

"""
Loop through all combinations and evaluate them. If they
are sufficiently close (within rounding error) to the
square root of a prime at which we are looking, we have
found a valid imaginary representation of our prime!
"""
for subset in combos:
    # Add up all the terms in our combination
    total = 0
    for term in subset:
        total += term[0]

    # For each prime we want to examine, check the imaginary representation
    for num in sqrtList:
        # Check the imaginary representation
        if abs(total.imag) < 1e-10 and abs(pow(num, 1 / 2) - total.real) < 1e-10:
            print(f"Found for the square root of {num}.")

            # Format the string representation of the imaginary representation
            term_string = ""
            for i, term in enumerate(subset):
                term_string += to_string(*term[1])
                if i < len(subset) - 1:
                    term_string += " + "

            # Output the string
            print(term_string)
            print()
