# [crypto] GIGA Cloud Storage

## Tag

RSA, Man in the Middle attack, eprint 2022/959(MEGA: Malleable Encryption Goes Awry)

## Difficulty

Hard

## Scenario

(Only a very brief summary of the situation is given. For detailed information, please refer to the code.)

Both the server and the client are running as services in different port(9001 / 9002). You can confirm that communication is functioning correctly by passing the client's output to the server and the server's output to the client.

The client can save files on the server or retrieve files from it. Each user has an RSA private key, and the files are encrypted with AES. The AES encryption key is derived from the RSA private key.

The goal is to recover the flag from a file named `flag.enc`, which is saved by a user named `codegate` who is already registered.