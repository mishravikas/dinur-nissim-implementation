import logging

logging.basicConfig(filename='output_logs',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.info("-------------------------------------------------------------\n")

import sqlite3
from collections import Counter
import numpy as np
from pulp import *
import math
from itertools import compress
n = 8
k = 0.3
# e =  n**(1/2 - k)  #Perturbation
# e = 4

n_cols = 4
t = n*(math.log(n))**2
# sigma = n**(0.5)/5
sigma = 1 
# e_dynamic = 2*sigma
sqlite_file = 'db_2000.sqlite'    # name of the sqlite database file
table_name = 'binary_data' 
conn = sqlite3.connect(sqlite_file)
cursor = conn.cursor()

n_runs = 20
l_d_values = []

# a_hats = []
# q_js = []
# queries = map(list,itertools.product([0,1],repeat=n_cols-1))
# true_counts = []
# var_names = []
# var_lens = []

# print t

# #Generating var_names
# for i in range(1,n+1):
# 	var_name = 'r'+str(i)
# 	var_names.append(LpVariable(var_name, 0, 1))

# print var_names



#To add noise to the count queries
def execute_query(sql):
	# print sql
	cursor.execute(sql)
	# print sql
	# noise = np.random.normal(0,sigma)
	noise = np.random.normal(0,sigma)
	# print "noise:",noise
	result = cursor.fetchone()
	# print result
	true_count = result[0]
	# print "true_count:",true_count
	noisy_count = true_count + noise
	# print "noisy_count:",noisy_count
	result = noisy_count

	return [noisy_count,true_count]
avg = 0
sum_values = []
for cm in range(0,n_runs):
	succesfull = False
	while not succesfull:
		print "---=====------RUN NO.: ", cm
		e_dynamic = 2*sigma
		a_hats = []
		q_js = []
		queries = map(list,itertools.product([0,1],repeat=n_cols-1))
		true_counts = []
		var_names = []
		var_lens = []
		total_count = execute_query("Select sum(c1) from `binary_data`")[0]
		# print "------TOTAL COUNT------"
		# print total_count
		# Database algorithm which returns noisy_a (a_hat) depending on the query q
		def A(q):
			sql = "SELECT sum(c1) FROM `binary_data` WHERE "
			first_clause = 1
			# print q
			flag = 1
			for v in q:
				if v!=1:
					flag = 0

			if(flag):
				print "=================FOUND======================"
			for idx, val in enumerate(q):
				if(val):
					if(first_clause):
						sql += "(`c2`=%d and `c3`=%d and `c4`=%d)" %(queries[idx][0],queries[idx][1],queries[idx][2])
						first_clause = 0
					else:
						sql += " or (`c2`=%d and `c3`=%d and `c4`=%d)" %(queries[idx][0],queries[idx][1],queries[idx][2])

			# print sql
			# sql = "SELECT sum(c1) FROM `binary_data` WHERE `c2`=%d and `c3`=%d and `c4`=%d" %(queries[j][0],queries[j][1],queries[j][2])
			result = execute_query(sql)
			true_counts.append(result[1])
			return result[0]

		#To generate random queries
		def gen_q():
			while(True):
				q = np.random.randint(2, size=8)
				if sum(q)!=0:
					return q




		#Generate variable ranges
		for m in range(0,len(queries)):
			sql = "SELECT sum(c1) FROM `binary_data` WHERE (`c2`=%d and `c3`=%d and `c4`=%d)" %(queries[m][0],queries[m][1],queries[m][2])
			len_noisy = execute_query(sql)
			var_lens.append(len_noisy[0])

		# print "==========="
		# print var_lens
		message = "Variable_lengths: %s \n" %(','.join(map(str, var_lens)))
		logging.info(message)

		#Generating var_names
		for i in range(1,n+1):
			var_name = 'r'+str(i)
			left_range = var_lens[i-1] - 2*sigma
			right_range = var_lens[i-1] + 2*sigma
			if(left_range<0):
				left_range = 0
			var_names.append(LpVariable(var_name, left_range, right_range))

		# print var_names


		#Generate a_hats and q_js
		for j in range(1,int(np.ceil(t))):
			q_j = gen_q()
			q_js.append(q_j)

			
			a_hat = A(q_j)
			a_hats.append(a_hat)

		# print (2**(n_cols-1)-1)
		# for j in range(0,2**(n_cols-1)-1):
		# 	# q_j = gen_q()
		# 	# q_js.append(q_j)
		# 	print j

		# 	sql = "SELECT sum(c1) FROM `binary_data` WHERE `c2`=%d and `c3`=%d and `c4`=%d" %(queries[j][0],queries[j][1],queries[j][2])
		# 	result = execute_query(sql)
		# 	a_hat = result[0]
		# 	true_counts.append(result[1])
		# 	a_hats.append(a_hat)


		# print a_hats
		message = "a_hats: %s  \n" %(','.join(map(str, a_hats)))
		logging.info(message)
		#print true_counts

		# {{{
		# prob = LpProblem("problem", LpMaximize)


		# #Generate the inequalities from the queries and add them to prob to be optimized
		# #lhs <= rhs <= rhs_2
		# for i in range(0,len(q_js)):
		# 	selected = list(compress(var_names,q_js[i]))
		# 	rhs = 0
		# 	for j in selected:
		# 		rhs = rhs+j

		# 	lhs = a_hats[i] - e
		# 	rhs_2 = a_hats[i] + e

		# 	lhs = np.float64(lhs).item()
		# 	rhs_2 = np.float64(rhs_2).item()


		# 	prob += lhs <= rhs
		# 	prob+= rhs <= rhs_2

		# #all_vars: To maximize the sum of all the unknown LpVariables or C's
		# all_vars = 0
		# for j in var_names:
		# 	all_vars += j


		# prob += all_vars

		# print prob
		# status = prob.solve(GLPK(msg=0))
		# LpStatus[status]


		# d_values = []   #This contains the predicted values
		# for j in all_vars:
		# 	if(value(j)>0.6):
		# 		d_values.append(1)
		# 	else:
		# 		d_values.append(0)
		# 	print value(j)

		# print "--------------------------------------"
		# print "ORIGINAL SUMS "
		# print true_counts
		# print "--------------------------------------"
		# print "Calculated SUMS "
		# print d_values
		# print "--------------------------------------"

		# }}}

		# Uncomment the below for e_dynamic logic
		statuses = {}
		bounds = []
		print "Starting a run with e_dynamic: ", e_dynamic
		while(e_dynamic>0):
			prob = LpProblem("problem", LpMaximize)
			for i in range(0,len(q_js)):
				selected = list(compress(var_names,q_js[i]))
				rhs = 0
				for j in selected:
					rhs = rhs+j

				lhs = a_hats[i] - e_dynamic
				rhs_2 = a_hats[i] + e_dynamic

				lhs = np.float64(lhs).item()
				rhs_2 = np.float64(rhs_2).item()


				prob += lhs <= rhs
				prob+= rhs <= rhs_2

			#all_vars: To maximize the sum of all the unknown LpVariables or C's
			all_vars = 0
			for j in var_names:
				all_vars += j

			prob += (total_count - 2*sigma) <= all_vars
			prob += all_vars <= (total_count + 2*sigma) 
			prob += 1

			status = prob.solve(GLPK(msg=0))
			# print status
			if(status==1):
				bounds.append(e_dynamic)
			# print e_dynamic
			LpStatus[status]
			statuses[e_dynamic] = status

			# print statuses
			e_dynamic -= 0.1
			prob = None

		print bounds
		print statuses
		min_bound = 100
		# print e_dynamic
		# print statuses
		# print var_names
		for k,v in statuses.iteritems():
			if(v==1 and k<min_bound):
				# print "Setting Min_bound"
				min_bound = k

		# print "Min bound", min_bound
		if(min_bound!=100):
			succesfull = True
		else:
			print "///////////////////////////////////////////////"
	# 	continue
	print "Min bound", min_bound
	prob = LpProblem("problem", LpMaximize)


	#Generate the inequalities from the queries and add them to prob to be optimized
	#lhs <= rhs <= rhs_2
	for i in range(0,len(q_js)):
		selected = list(compress(var_names,q_js[i]))
		rhs = 0
		for j in selected:
			rhs = rhs+j

		lhs = a_hats[i] - min_bound
		rhs_2 = a_hats[i] + min_bound

		lhs = np.float64(lhs).item()
		rhs_2 = np.float64(rhs_2).item()


		prob += lhs <= rhs
		prob+= rhs <= rhs_2

	#all_vars: To maximize the sum of all the unknown LpVariables or C's
	all_vars = 0
	for j in var_names:
		all_vars += j


	prob += (total_count - 2*sigma) <= all_vars
	prob += all_vars <= (total_count + 2*sigma)
	prob += 1

	# print prob
	status = prob.solve(GLPK(msg=0))
	LpStatus[status]


	d_values = []   #This contains the predicted values
	# for j in all_vars:
	# 	if(value(j)>0.6):
	# 		d_values.append(1)
	# 	else:
	# 		d_values.append(0)
	# 	print value(j)

	for j in all_vars:
		# print value(j)
		d_values.append(int(round(value(j))))



	# print queries
	# print "--------------------------------------"
	# print "Calculated Values "
	print d_values
	l_d_values.append(d_values)
	# print sum(d_values)
	avg += sum(d_values)
	sum_values.append(sum(d_values))
	# print true_counts
	# print "--------------------------------------"
	message = "d_values: %s" %(','.join(map(str, d_values)))
	logging.info(message)

	logging.info("-------------------------------------------------------------\n")

avg = avg/n_runs
# print avg
# print sum_values
print "HEREHEHREHRHERHERH"
print l_d_values
final_positions = []
for p in range(0,8):
	l_pos = []
	for i in range(0,n_runs):
		l_pos.append(l_d_values[i][p])
	final_positions.append(l_pos)

print "HAHAHAHAH"
print final_positions
latest = []
for fp in final_positions:
	most_common,num_most_common = Counter(fp).most_common(1)[0]

	one = Counter(fp).most_common(2)
	print(one)
	# print len(top_two)
	# for one in top_two:
	if(len(one)==2):
		if(one[0][1]==one[1][1]):
			print "CHECK HERE"
			latest.append(max(one[0][0],one[1][0]))
		else:
			latest.append(most_common)
	else:
		latest.append(most_common)

print "============================="
print latest
print sum(latest)
print "============================="
fsum = 0
na = 0
for s in sum_values:
	if(s>avg):
		fsum += s
		na += 1

print "N: ", sqlite_file
sql = "Select sum(c1) from `binary_data`"
cursor.execute(sql)

result = cursor.fetchone()
true_count = result[0]
print "True count(1): ", true_count
print "Calculated count(1): ", sum(latest)
print "Distribution: ", latest
# print "Average count(1): ", avg
# print "Calculated count: ", fsum/na
# ii = min(sum_values, key=lambda x:abs(x-fsum/na))
# i = sum_values.index(ii)
# print "Distribution: ", l_d_values[i]
print "Count in 5 runs: ", sum_values


