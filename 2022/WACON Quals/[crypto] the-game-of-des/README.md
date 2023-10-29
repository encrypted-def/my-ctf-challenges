# [crypto] The Game of DES

## Tag

DES, DES weak key

## Difficulty

Easy

## Scenario

After performing DES 42 times with a user-selected key, if every byte of the ciphertext is printable ASCII, provide the ciphertext `(print("enc:", data.decode()))`. Each byte of the key must be different each time (`if len(key) != 8 or len(set(key)) != 8`).