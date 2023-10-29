# [reversing] Type confusion

## Solution

Let's refer to the IEEE-754 format. For a 64-bit integer, with the most significant bit set to 0 and the next 11 bits as $x$, and the lower 52 bits as $y$, the integer representation can be expressed as $v1 = x \times (2^{52}) + y$, while the floating-point representation can be expressed as $v2 = ((2^{52} + y) \times 2^{-52}) \times 2^{x - 1023}$.

When comparing these two values, considering that there may be a loss of up to 12 bits in the integer representation, you need to find values for $x$ and $y that differ by $2^{12}$ or less. As $x$ increases, the rate of increase of $v2 becomes very steep. Therefore, the point where $v1 and $v2$ meet is at $x = 1085, and at this point, $y = 268543086285044$.

Here is the code to determine this:

```py
import math

for x in range(1075, 2000):
  a = 2**52 * x - 2**(x-1023)
  b = 2 ** (x-1075) - 1
  if b==0: continue
  y = a/b
  if y < 1 or y > 2**52: continue
  print(x,y,math.log2(y),a%b)
  print((x<<52) + int(y))
```