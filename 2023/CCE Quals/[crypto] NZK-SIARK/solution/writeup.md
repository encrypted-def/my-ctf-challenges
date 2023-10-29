# 개요

AES 중 S-box의 계산을 prover에게 위임한 환경에서 결과를 조작하는 문제

# 풀이

x의 Inverse xinv에 대한 검증을 `x * (x * xinv - GF(1)) == GF(0)` 으로 하는데, 이 경우 `x = 0, xinv = arbitrary`가 검증을 통과한다는 문제가 있다.

그렇기 때문에 공격자는 일단 `KEY = PLAINTEXT`으로 두고 keygen을 정상적으로 한 후, 매번 Sbox layer의 input이 all zero가 되게끔 S-box의 출력을 적절하게 맞추면 된다. 제일 마지막 S-box의 출력은 output이 `CIPHERTEXT`가 되게끔 잘 끼워맞추면 된다.

# 문제 세팅 방법

플래그 모듈 빌드 && 도커 업 : `make`

도커 업 : `make start`

# 출제지문

Not Zero-Knowledge Succint Interactive Argument of Knowledge

Not Zero-Knowledge : This system is "not" zero-knowledge.
Succint : The verifier does not directly compute the inverse; it only verifies it.
Interactive : The prover and verifier should interact.
Argument of Knowledge : A malicious prover cannot cheat.