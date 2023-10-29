# [crypto] anti Kerckhoffs

## Solution

Note that the quadratic of the first Sbox layer does not need to be exact. For example, if an S-box is `ax^2 + bx + c`, we can find `t * (ax^2 + bx + c)` and multiply each element in the middle Affine layer by `t^(-1)`, which will give us the same output.

So for the first S-box layer, we just need to find something that satisfies `(x-t[i])^2`, which we can do by finding collision pairs in each S-box.

For the next affine layer, we can use a similar idea and consider `A[i][0] = 1`. For `A[i][j]`, we can use a fact that if the $i$-th elements of the output is differ, then the inputs of the $i$-th Sbox in `SboxLayer2`. This removes 1 impossible candidates of `A[i][j]`.

In the end, the last Sbox layer doesn't need to be recovered and we get a candidate input for the last Sbox layer that matches the target, which we can handle appropriately.