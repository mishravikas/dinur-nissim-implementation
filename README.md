# dinur-nissim-implementation
Implementation for Dinur-Nissim's algo 


Theorem: Let D = (d,A) be a database where A is within o(√n) perturbation then D is poly(n)-non-private.

Proof:
Let A be within E perturbation for E = o(√n). We fix ε > 0 arbitrarily, and show how to find some candidate database c for which dist(c, d) < εn with high probability

Dinur-Nissim linear Program
- Let t = n(logn)^2^. For 1 ≤ j ≤ t choose uniformly at random qj ⊆R [n], and get a ̃qj ← A(qj ) from the database algorithm.

- Solve the following linear program with unknowns c~1~,...,c~n~:
a ̃qj −E≤∑ i∈qj c~i~ ≤a q~j~ +E     
for   1 ≤ j ≤ t 0 ≤ c~i~≤ 1  for 1≤ i ≤n


- Let c′i = 1 if ci > 1/2 and c′i = 0 otherwise. Output c′.

How to Use:
- Install the requirements: pip install -r requirements.txt
- Run dinur.py: python dinur.py



