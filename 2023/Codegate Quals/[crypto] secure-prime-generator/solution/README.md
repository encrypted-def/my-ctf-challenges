# [crypto] secure Prime Generator

## Solution

Originally, $N$ should be determined as $N = (p1 + p2) \times (q1 + q2)$. However an attacker can influence the selection of $N$ to be what they desire, not necessarily $(p1 + p2) \times (q1 + q2)$.

However, N must pass the `N_validity_check` routine, so the attacker sets $N$ to be a product of $p$'s, where $p-1$ is a divisor of 1801800 then hope that $N-1-p1-q1$ is a multiple of `1801800`. There are conditions for giving the remainder concerning `SMALL_PRIMES`, and by providing the desired remainder and negatives like `(r, -1, -2, -3, ..)`, they can force the remainder to be as required. This increases the probability of $N-1-p1-q1$ being a divisor of `1801800` to `1/60`. As a result, they can recover the flag after roughly 60 attempts.