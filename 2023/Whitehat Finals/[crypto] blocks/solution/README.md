# [crypto] Blocks

## Solution

For simplicity, we will refer to `0000...00` as `BLOCK0`, `0000...01` as `BLOCK1`, and `pt[i]` as the `i`th block of the plaintext `pt` and `ct[i]` as the `i`th block of the ciphertext `ct`.

Now let's look at the characteristics of each mode.

In ECB, regardless of the index of the block and iv, if the plaintexts are identical, the same ciphertext will result.

CBC considers the decryption process of obtaining a plaintext from a ciphertext, given two plaintext-ciphertext pairs `(pt1, ct1), (pt2, ct2)`. Then, if `ct1[i] = ct2[i]`, then `pt1[i] ^ ct1[i-1] = pt2[i] ^ ct2[i-1]`, independent of `iv`. If `i = 0`, then `pt1[i] ^ iv1 = pt2[i] ^ iv2`.

CTR is `pt1[i] ^ ct1[i] = pt2[i-1] ^ ct2[i-1]` if `iv2 = iv1+1`.

CFB is `pt1[i+1] ^ ct1[i+1] == pt2[i+1] ^ ct2[i+1]` if `ct1[i] == ct2[i]`, regardless of `iv`.

OFB has the property that if `iv1 = iv2`, then `pt1[i] ^ ct1[i] = pt2[i] ^ ct2[i]`, although the solution is to just classify it as OFB if all other modes are absent. However, this is a characteristic that CTR also has.

If we had a generous number of queries allowed, the problem would be simple, but since we are limited to only two queries, we need to devise a way to distinguish between all modes. If you think about it, it's hard to distinguish between CTR and OFB when the iv of two queries is the same. Instead, we need to make the ivs different to distinguish between CTR and OFB. And if the ivs are different, and we encrypt both times, we cannot intentionally create `ct1[i] == ct2[i]', so the full nature of CFB is not revealed. Therefore, we can see that one of the queries must be a decryption process.

From these considerations, we can finally categorize the modes in the following way

- Query 1: `iv1 = BLOCK0`, `pt1 = BLOCK0 + BLOCK0 + BLOCK0 + BLOCK0`, `enc_option = y` (=encrypt)
- Query 2: `iv1 = BLOCK1`, `ct2 = ct1[0] + BLOCK0 + BLOCK0`, `enc_option = n` (=decrypt)

1. Judge as ECB if `ct1[0] == ct1[1]`.
2. if `ct1[3] == pt2[2]`, it is a CTR.
3. CBC if `pt2[0] == BLOCK1`.
4. CFB if `pt2[1] == ct1[1]`.
5. If the above 4 conditions are not satisfied, it is OFB.

Of course, there are many other ways to solve this problem.
