file_output = open('output.txt', 'r')
file_verify = open('test.verify.txt', 'r')

output_list = []
verify_list = []

for line in file_output:
	output_list.append(line)

for line in file_verify:
	verify_list.append(line)

print len(output_list), len(verify_list)

count = 0;
total = 0
for i in range(0, len(verify_list)):
	if output_list[i] != verify_list[i]:
		count += 1
		print output_list[i]
		break

# print count
# print float(count) / verify_list.count('B\n')