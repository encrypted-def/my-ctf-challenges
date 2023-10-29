# [crypto] discrete_log

## Solution

First, given $x = at + b$, consider $(g^x)^{2q}$: $(g^x)^{2q} = g^{x \times 2q} = g^{(at + b) \times 2q} = g^{2tq \times a} \times g^{2qb} = (g^{p-1})^{qa} \times g^{2qb}$, and by Fermat's theorem, $g^{p-1} \equiv 1 ( \text{mod } p)$, so we conclude that $(g^x)^{2q} \equiv g^{2qb} = (g^{2q})^b (\text{mod } p)$.


Next, let's define $g' = g^{2q}$, then since $(g') ^ t \equiv 1 (\text{mod } p)$, the order of $g'$ is a weak number in $t$, and in particular, if $t$ is prime, the order of $g'$ is $1$ or $t$. So if $g' \not\equiv 1(\text{mod } p)$ when $t$ is prime, then the order of $g'$ is necessarily $t$, which means that $(g')^0, (g')^1, (g')^2, \dots, (g')^{t-1}$ are all different values. Finally, if we compute $(g^x)^{2q}$ and $(g')^0, (g')^1, (g')^2, \dots, (g')^{t-1}$ and find a $(g')^b$ among them that matches $(g^x)^{2q}$, we know that $x$ divided by $t$ is the remainder $b$.

This means that for every query, an attacker can find the remainder of $x$ divided by $t$ by setting $p$ to $p = 2 \times t \times q + 1$ for small primes $t$ of 24 bits or less and large primes $q$ of 1000 bits or more. The way to find this $p$ is to simply grab an arbitrary $t$ and $q$ and see if $2 \times t \times q + 1$ is prime. The prime number theorem tells us that the probability of a 1024-bit number being prime is $1/1024$, so roughly 1024 iterations will give us $p$. However, this is a relatively time-consuming process, and you may want to consider preprocessing the list of such $p$ beforehand. In my actual exploit code, I preprocessed the $(p, q, t)$ pairs by picking a prime $q$ at random and holding it fixed, keeping the primes below $10^6$ as candidates for $t$, and then going through them one by one to find $p$ for which $2tq+1$ is prime.

This can be repeated a total of 77 times for the 24-bit or smaller primes chosen by the attacker, and since the product of these primes is roughly 1848 bits, which is much larger than $x$, which is 1020 bits, we can finally recover $x$ using the Chinese Remainder Theorem.

[+] I made a dumb mistakes that $q$'s primality is not checked in original problem(`prob.py`)😥😥. Please check `prob_revenge.py`.