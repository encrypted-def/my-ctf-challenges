# [crypto] Zero time signature

## Tag

Bitcoin Proof-of-Work

## Difficulty

Medium

## Scenario

Create a `seed` with a random string, and then change the `seed` into the hash value of a string chosen by the user, which itself contains the `seed`. Repeat this process until a user has 12 leading zeros, then flag is obtained. If you have fewer than 12 leading zeros, we use a "partial scoring" approach. Check the code for more details.