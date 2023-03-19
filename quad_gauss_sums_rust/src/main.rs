use std::collections::HashMap;
use num_modular::ModularSymbols;

fn main() {
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
        let mut root_sum_string = String::from("");

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
