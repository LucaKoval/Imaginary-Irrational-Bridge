import random
import itertools

# sqrtList = [2, 3, 5]
sqrtList = [5]

# Three total terms
total_terms = 3


def to_string(
    coefNumerator, coefDenominator, powerNumerator, powerDenominator, plusMinus
):
    string = (
        f"({coefNumerator}/{coefDenominator})i^({powerNumerator}/{powerDenominator})"
    )

    if plusMinus == 1:
        string = "-" + string

    return string


# Generate the terms
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

combos = itertools.combinations_with_replacement(terms, total_terms)

for subset in combos:
    total = 0
    for term in subset:
        total += term[0]

    for num in sqrtList:
        if abs(total.imag) < 1e-10 and abs(pow(num, 1 / 2) - total.real) < 1e-10:
            print(f"Found for the square root of {num}.")
            term_string = ""
            for i, term in enumerate(subset):
                term_string += to_string(*term[1])
                if i < len(subset) - 1:
                    term_string += " + "
            print(term_string)
            print()
