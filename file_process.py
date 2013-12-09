filein = open('train.txt', 'r')

B_list = []
I_list = []

for line in filein:
	if line != '':
		line_list = line.split('\t')
		if len(line_list) >= 2:
			if line_list[1] == 'B\n':
				B_list.append(line_list[0])
			elif line_list[1] == 'I\n':
				I_list.append(line_list[0])

B_set = set(B_list)
I_set = set(I_list)

print len(B_list), len(B_set)
print len(I_list), len(I_set)

print B_set
print I_set
print len(B_set & I_set)

filein.close()