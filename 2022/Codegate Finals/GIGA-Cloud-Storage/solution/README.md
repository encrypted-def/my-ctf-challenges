# [crypto] GIGA Cloud Storage

## Solution

This challenge was inspired by [MEGA: MALLEABLE ENCRYPTION GOES AWRY](https://mega-awry.io/), and this attack directly works in this challenge. It is possible to recover RSA key using binary search.

There was a unintended solution using `p = int(aes_dec(bytes.fromhex(packet_recv_plain(sock).decode()), pw_hash))`(`client.py, L118`). When `int()` is called with non integer values, then it outputs a argument in a error message. This feature made the challenge easier.

Fortunately, this vulnerability doesn't make the challenge like `mic check` level, but it's still regretful personally.