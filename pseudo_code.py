#n ---> size of db
#e =  ---> epsilon (perturbation error)
#k>0
import math
import numpy as np
n = 100
k= 0.3
t = n*(math.log(n))^2
a_hats = []   #list containing all the a_hat generated for queries

d = np.random.randint(2, size=n)     #original db
e =  n^(1/2 - k)


# Database algorithm which returns noisy_a (a_hat) depending on the query q
def A(q):
	true_a =  np.sum(np.multiply(d,q))
	noise = np.random.uniform(-e,e)
	noisy_a = true_a + noise

	return noisy_a

#To generate random queries
def gen_q():
	return np.random.randint(2,size=n)


for j in range(1,t+1):
	q_j = gen_q()
	a_hat = A(q_j)
	a_hats.append(a_hat)


# {

# Add a linear program solver with unknowns c1,c2, .......,cn to get a c' in this part
# find the hamming distance between c' and d, Now to prove: dist(c',d)<en

#Repeat the above process 100 times and find the probability: P(dist(c',d)<en)

# }



