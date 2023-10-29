# [crypto] Prime Generator

## Solution

It is known that $n$ is efficiently factorized when partial bits of $p$ is exposed usingg coppersmith attack. So our goal is to recover a `UPPER`.

menu1 is quite artificial and it gives a important "hint" of UPPER. For example, when we receive a number 16 through menu1, it refers that `UPPER % 3 != 2`, `UPPER % 5 != 4`, `UPPER % 7 != 5`, ... We can eliminate candidate remainder for specific primes.

By gathering enough informations(about 1200-1600 primes), UPPER can be recovered by Chinise remainder theorem. After that, flag is recovered by Coppersmith attack(RSA Factoring with high bits known attack).