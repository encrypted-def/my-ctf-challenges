# [crypto] Tiny Encryption

## Solution

The savefile is encrypted in AES-GCM mode, where the nonce is derived from the ID and the key from the PW. ID and PW are user-selected values. The attacker's goal is to decrypt the savefile encrypted with AES GCM mode with different key1 and key2, so that the result of the decryption with key1 is a normal savefile and the result of the decryption with key2 is a manipulated savefile with an intelligence statistic of $2^{32}-1$ and a friendship value of $33$. In this case, it is possible to manipulate the stats by first storing a savefile encrypted with key1 on the server and then decrypting it with key2.

To explain the attack in simple terms, AES-GCM is Authenticated Encryption and should not be able to be decrypted with an incorrect key, but its operation mode does not satisfy the property of message committing, so if the message is manipulated well, such as in the scenario above, the same message can be decrypted with different keys. This attack is described in [the paper](https://eprint.iacr.org/2019/016).

We can choose two random keys, key1 and key2, and then take advantage of the fact that the value of the nickname field can be set relatively freely by manipulating the value of one block of that field so that the tag in AES-GCM is the same when decrypted with key1 and when decrypted with key2.