# [crypto] anti Kerckhoffs

## Tag

SAS construction, Hidden S-box, DOI 10.1007/3-540-44987-6_24(Structural Cryptanalysis of SASAS)

## Difficulty

Hard

## Scenario

Field is `GF(17)` and plaintext size is $20$. Calculation has three layers:

1. SboxLayer1 - $S_1(x) = a_1x^2 + b_1x + c_1$ for some hidden $a_1,b_1,c_1$.
2. LinearLayer - Multiplying with hidden matrix $M$.
3. SboxLayer2 - $S_1(x) = a_2x^2 + b_2x + c_2$ for some hidden $a_2,b_2,c_2$.

`TARGET` is given and the goal is finding input `I` such that `calc(I) = TARGET`. A user can query at most `77777` times. When the user provides the input `x`, server does not replies the actual value of the output. It only replies whether each element in the output matches each element in the `TARGET`.