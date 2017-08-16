
import math
import numpy as np
from pulp import *
from itertools import compress

n = int(raw_input("Enter the size of the db n: ")) #Size of the db
d = np.random.randint(2,size=n) #The actual db, generating a random array of size n with 0s and 1s
k= 0.3

t = n*(math.log(n))**2.  #No of queries 
a_hats = []   #list containing all the a_hat generated for queries
q_js = []     #list containing all the queries generated

e =  n**(1/2 - k)  #Perturbation


var_names = []   #List of the unknown LpVariables


#Generating var_names
for i in range(1,n+1):
	var_name = 'c'+str(i)
	var_names.append(LpVariable(var_name, 0, 1))

print var_names


# Database algorithm which returns noisy_a (a_hat) depending on the query q
def A(q):
	true_a =  np.sum(np.multiply(d,q))
	noise = np.random.uniform(0,e)
	noisy_a = true_a + noise

	return noisy_a

#To generate random queries
def gen_q():
	return np.random.randint(2,size=n)



#Generate a_hats and q_js
for j in range(1,int(np.ceil(t))):
	q_j = gen_q()
	q_js.append(q_j)

	
	a_hat = A(q_j)
	a_hats.append(a_hat)


prob = LpProblem("problem", LpMaximize)


#Generate the inequalities from the queries and add them to prob to be optimized
#lhs <= rhs <= rhs_2
for i in range(0,len(q_js)):
	selected = list(compress(var_names,q_js[i]))
	rhs = 0
	for j in selected:
		rhs = rhs+j

	lhs = a_hats[i] - e
	rhs_2 = a_hats[i] + e

	lhs = np.float64(lhs).item()
	rhs_2 = np.float64(rhs_2).item()


	prob += lhs <= rhs
	prob+= rhs <= rhs_2

#all_vars: To maximize the sum of all the unknown LpVariables or C's
all_vars = 0
for j in var_names:
	all_vars += j


prob += all_vars


status = prob.solve(GLPK(msg=0))
LpStatus[status]


d_values = []   #This contains the predicted values
for j in all_vars:
	if(value(j)>0.5):
		d_values.append(1)
	else:
		d_values.append(0)
	print value(j)

print "--------------------------------------"
print "ORIGINAL d "
print d
print "--------------------------------------"
print "Calculated d "
print d_values
print "--------------------------------------"





