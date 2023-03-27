use itertools::Itertools;
use num::complex::Complex;
use num_modular::ModularSymbols;
use ordered_float::OrderedFloat;
use std::collections::HashMap;
use std::collections::HashSet;

// Helper function that ingests the numbers representing a term in the sum
// and outputs the corresponding, formatted string
fn format_string(
	(coef_numerator, coef_denominator, power_numerator, power_denominator, plus_minus): (
		OrderedFloat<f32>,
		OrderedFloat<f32>,
		OrderedFloat<f32>,
		OrderedFloat<f32>,
		OrderedFloat<f32>,
	),
) -> String {
	let minus = "-".to_string();
	let mut formatted =
		format!("({coef_numerator}/{coef_denominator})i^({power_numerator}/{power_denominator})");

	if plus_minus == 1.0 {
		formatted = minus + &formatted;
	}

	return formatted;
}

fn brute_force() {
	// Error bounds used later during calculations
	const ERROR: f32 = 1e-10;

	// List of primes for which we wish to find imaginary sum representations
	let mut sqrt_list: Vec<i32> = Vec::new();
	sqrt_list.push(2);
	sqrt_list.push(3);
	sqrt_list.push(5);

	// Number of terms in the imaginary sum
	const TOTAL_TERMS: usize = 3;

	// Generate (representations for) all terms/powers of i for which we wish to use
	// in the sums
	let mut terms: HashSet<(
		OrderedFloat<f32>,
		Complex<OrderedFloat<f32>>,
		(
			OrderedFloat<f32>,
			OrderedFloat<f32>,
			OrderedFloat<f32>,
			OrderedFloat<f32>,
			OrderedFloat<f32>,
		),
	)> = HashSet::new();
	for coef_numerator in 0..7 {
		for coef_denominator in 1..7 {
			for power_numerator in 0..7 {
				for power_denominator in 1..7 {
					let term_not_finalized_coef: OrderedFloat<f32> =
						OrderedFloat(coef_numerator as f32 / coef_denominator as f32);
					let term_not_finalized: Complex<OrderedFloat<f32>> =
						Complex::new(OrderedFloat(0.0), OrderedFloat(1.0)).powf(OrderedFloat(
							power_numerator as f32 / power_denominator as f32,
						));

					for plus_minus in 0..2 {
						if plus_minus == 0 {
							terms.insert((
								term_not_finalized_coef,
								term_not_finalized,
								(
									OrderedFloat(coef_numerator as f32),
									OrderedFloat(coef_denominator as f32),
									OrderedFloat(power_numerator as f32),
									OrderedFloat(power_denominator as f32),
									OrderedFloat(plus_minus as f32),
								),
							));
						} else {
							terms.insert((
								-term_not_finalized_coef,
								term_not_finalized,
								(
									OrderedFloat(coef_numerator as f32),
									OrderedFloat(coef_denominator as f32),
									OrderedFloat(power_numerator as f32),
									OrderedFloat(power_denominator as f32),
									OrderedFloat(plus_minus as f32),
								),
							));
						}
					}
				}
			}
		}
	}

	// Generate all combinations based on the above terms
	let combos = terms.into_iter().combinations_with_replacement(TOTAL_TERMS);

	/*
	 * Loop through all combinations and evaluate them. If they
	 * are sufficiently close (within rounding error) to the
	 * square root of a prime at which we are looking, we have
	 * found a valid imaginary representation of our prime!
	 */
	for subset in combos {
		// Add up all the terms in our combination
		let mut total_re: OrderedFloat<f32> = OrderedFloat(0.0);
		let mut total_im: OrderedFloat<f32> = OrderedFloat(0.0);
		for term in &subset {
			total_re += term.0 * term.1.re;
			total_im += term.0 * term.1.im;
		}

		// For each prime we want to examine, check the imaginary representation
		for num in &sqrt_list {
			// Check the imaginary representation
			if total_im.abs() < ERROR
				&& (OrderedFloat((*num as f32).sqrt()) - total_re).abs() < ERROR
			{
				println!("Found for the square root of {num}.");
				// println!("{:#?}, {:#?}", total_im, total_im.abs());

				// Format the string representation of the imaginary representation
				let mut term_string = "".to_string();
				for (i, term) in subset.clone().into_iter().enumerate() {
					term_string += &format_string(term.2);
					if i < TOTAL_TERMS - 1 {
						term_string.push_str(" + ");
					}
				}

				// Output the string
				println!("{}", term_string);
			}
		}
	}
}

fn quad_gauss_sums() {
	// The number up to which we check for primes
	const UPPER: i32 = 100;

	/*
	 * Naively generate a list of primes from 3 to UPPER.
	 * 2 is not included because the calculating the Legendre symbol
	 * of some integer k < p and p, where p is prime, requires p
	 * to be an *odd* prime. The equation representing the square
	 * root of two can be be found using Euler's formula evaluated
	 * at theta = pi/4. We get sqrt(2) = i^(7/2) + i^(1/2).
	 */
	let mut primes: Vec<i32> = Vec::new();
	for num in (3..UPPER).step_by(2) {
		let mut is_prime = true;
		for i in (3..=((num as f64).sqrt() as i32)).step_by(2) {
			if num % i == 0 {
				is_prime = false;
				break;
			}
		}

		// The odd integer is a prime if and only if all numbers from 3
		// through the square root of the odd integer are not factors
		if is_prime {
			primes.push(num);
		}
	}

	/*
	 * We now loop through our primes. We go about calculating a variant of
	 * quadratic Gauss sums as documented by David E Speyer here:
	 * https://mathoverflow.net/questions/287947/is-every-square-root-of-an-integer-a-linear-combination-of-cosines-of-pi-rati?rq=1
	 *
	 * As a side note, we are guaranteed that the square root of every prime
	 * can be mapped to the imaginaries through a side effect of the
	 * Kronecker-Weber theorem: https://en.wikipedia.org/wiki/Kronecker%E2%80%93Weber_theorem
	 *
	 * The logic in the loop below is geared around outputing the string
	 * representation of the sum of powers of i representation of the
	 * square root of an odd prime p. This allows the user to validate the
	 * representation by, for example, directly taking the output of this
	 * program and putting into Wolfram Alpha.
	 */
	for p in primes {
		/*
		 * Keep track of the counts of Legendre symbols. Note that zero
		 * is not a possible value as we will only be calculating
		 * Legendre symbols of some integer k < p and p, where p
		 * is an odd prime
		 */
		let mut legendre_counts: HashMap<i32, i32> = HashMap::new();

		// Initialize the output string
		let mut op_string = "".to_string();
		let mut total_coef: i32 = (-1 as i32).pow(((p - 1) / 2) as u32);
		let mut root_sum: i32 = 0;
		let mut root_sum_string = "".to_string();

		// Loop through all integers k < p
		for k in 1..p {
			// Calculate the Legendre symbol
			let coef: i32 = k.legendre(&p) as i32;

			// Keep track of the Legendre symbol counts
			*legendre_counts.entry(coef).or_insert(0) += 1;

			// Here we deal with the sign of the current term
			let op = if coef == -1 { "-" } else { "+" };

			/*
			 * Initialize the numerator of the fraction to which i is raised.
			 * To account for the possibility of a -1 appearing in
			 * the square root of the prime p in the Gauss sum formula, however,
			 * we must adjust to numerator of the fraction to which i
			 * is raised accordingly
			 */
			let pow_numerator: i32 = if total_coef == -1 { 4 * k - p } else { 4 * k };

			// Set the denominator of the fraction to which i
			// is raised
			let pow_denominator: i32 = p;

			// Format the string corresponding to the current term in the sum
			root_sum_string.push_str(&format!(" {op} i^({pow_numerator}/{pow_denominator})"));

			// Add the current term string to the sum
			op_string.push_str(op);
		}

		// Strip the complete string of the very first operation.
		// Otherwise, the result will begin with a + or - sign
		let root_sum_string = &root_sum_string[3..];

		// Print the result
		println!("sqrt({p}) = {root_sum_string}");
	}
}

fn main() {
	// quad_gauss_sums();
	brute_force();
}
