# [crypto] The Game of DES2

## Solution

(Although I strongly agree that it is brain-teasing,) It is enough to follow the basic linear cryptanalysis attack. Linear trail is obtained from the function `get_linear_info` in `linear_trail_check.py`. 

Last round can be reverted with partial key guess. Then the linear trail is:

1R : 4th sbox, input mask 52, output mask 2 (10/64)
2R : 6th sbox, input mask 4, output mask 10 (12/64)
3R : pass
4R : 6th sbox, input mask 4, output mask 10 (12/64)

