# Imaginary-Irrational-Bridge

Alright, there's definitely more to be said here, and there's actually plenty more documentation in this repo's files, but I wanted to put something down to document this whole process:

It actually started about a year or two ago when I was playing around with [Euler’s formula](https://en.wikipedia.org/wiki/Euler%27s_formula) and wondered if you could express the square roots of numbers using powers of `i`. I realized that for this task, I really only needed to look for the square roots of prime numbers as the square roots of composite numbers were just products of the square roots of their prime factors. Using some trig identities, I was able to pretty quickly find expressions for the square roots of two and three, but I struggled to find an expression for the square root of five. I would come back to this problem periodically, and at some point near the beginning of October 2022, I decided try a programmatic approach instead of a strict mathematical approach. Specifically, I tried brute forcing various combinations of powers of `i` to try and see if they would match the square roots of small prime numbers. This is the first of the two main files: “brute_force.py”. After messing around with some parameters, the brute force approach produced a plethora of results for the square root of five, as well as for the square roots of two and three. After trying for many more hours, however, I could not product results for any primes above five. Then in mid February 2023, I was looking into some group theory terminology for a cryptography research class when I stumbled across a piece of math called the [Kronecker–Weber theorem](https://en.wikipedia.org/wiki/Kronecker%E2%80%93Weber_theorem). The Wikipedia entry had a very interesting concrete example to demonstrate a consequence of the theorem: It was mapping the square roots of prime numbers to sums of roots of unity. I couldn’t believe it! After doing some more frantic searching online, I found a [Stack Overflow post](https://mathoverflow.net/questions/287947/is-every-square-root-of-an-integer-a-linear-combination-of-cosines-of-pi-rati?rq=1) explaining how this exact mapping could be calculated using something called [quadratic Gauss sums](https://en.wikipedia.org/wiki/Quadratic_Gauss_sum). I whipped up a new Python file, coded up a version of the formula, and bam! It worked like magic. I could calculate the “imaginary version" of the square root of any prime number out there. This is the second of the two main files: “quad_gauss_sums.py”.

As of late February 2023, I have also implemented Rust versions of the two aforementioned files. (I constructed the files as a way to learn Rust, so the code is by no means perfect. Apologies for that in advance.)

 Thank you so much for reading this! I really appreciate it. I also gotta send my thanks to Euler, the [Kronecker–Weber theorem](https://en.wikipedia.org/wiki/Kronecker%E2%80%93Weber_theorem), and [Professor David E Speyer](https://dept.math.lsa.umich.edu/~speyer/) who provided the truly enlightening answer on Stack Overflow. :)
