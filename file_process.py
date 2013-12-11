filein = open('modified_train.txt', 'r')

B_list = []
I_list = []
O_list = []
word_list = []
tag_list = []

for line in filein:
	if line != '\n':
		line_list = line.split('\t')
		word_list.append(line_list[0])
		tag_list.append(line_list[1])
		if line_list[1] == 'B\n':
			B_list.append(line_list[0])
		elif line_list[1] == 'I\n':
			I_list.append(line_list[0])
		else:
			O_list.append(line_list[0])

B_set = set(B_list)
I_set = set(I_list)
O_set = set(O_list)
word_set = set(word_list)
unique_word_list = list(word_set)

# 15514, 6069 / 2810 with UNKOWN
print len(B_list), len(B_set)
# 22656, 3128 / 2273 with UNKOWN
print len(I_list), len(I_set)
# 309526, 23372 / 11331 with UNKOWN
print len(O_list), len(O_set)
# 347696 with UNKOWN
print len(word_list)

print B_set
print I_set
# 1167, 1119, 1487 / 1168, 1120, 1488 with UNKOWN
print len(B_set & I_set)
print len(B_set & O_set)
print len(I_set & O_set)
# 13204 with UNKOWN
print len(unique_word_list)

B_tup = tuple(B_list)
I_tup = tuple(I_list)
O_tup = tuple(O_list)

B_dict = {}
I_dict = {}
O_dict = {}
for word in unique_word_list:
	B_dict[word] = 1
	I_dict[word] = 1
	O_dict[word] = 0

for word in B_tup:
	B_dict[word] += 1

for word in I_tup:
	I_dict[word] += 1

for word in O_tup:
	O_dict[word] += 1

for word in unique_word_list:
	B_dict[word] = B_dict[word] / (347696.0 + 3916.0)
	I_dict[word] = I_dict[word] / (347696.0 + 3916.0)
	O_dict[word] = O_dict[word] / (347696.0 + 3916.0)

tag_word_prob_dict = {}
tag_word_prob_dict['B\n'] = B_dict
tag_word_prob_dict['I\n'] = I_dict
tag_word_prob_dict['O\n'] = O_dict

print tag_word_prob_dict['B\n']['phosphatases ']
print tag_word_prob_dict['I\n']['phosphatases ']
print tag_word_prob_dict['O\n']['phosphatases ']

trans_item_list = []
for i in range(0, len(tag_list) - 1):
	item = [tag_list[i], tag_list[i + 1]]
	trans_item_list.append(item)

B_trans_prob_dict = {}
B_trans_prob_dict['B\n'] = (trans_item_list.count(['B\n', 'B\n'])) / 15514.0
B_trans_prob_dict['I\n'] = (trans_item_list.count(['B\n', 'I\n'])) / 15514.0
B_trans_prob_dict['O\n'] = (trans_item_list.count(['B\n', 'O\n'])) / 15514.0

I_trans_prob_dict = {}
I_trans_prob_dict['B\n'] = (trans_item_list.count(['I\n', 'B\n'])) / 22656.0
I_trans_prob_dict['I\n'] = (trans_item_list.count(['I\n', 'I\n'])) / 22656.0
I_trans_prob_dict['O\n'] = (trans_item_list.count(['I\n', 'O\n'])) / 22656.0

O_trans_prob_dict = {}
O_trans_prob_dict['B\n'] = (trans_item_list.count(['O\n', 'B\n'])) / 309526.0
O_trans_prob_dict['I\n'] = (trans_item_list.count(['O\n', 'I\n'])) / 309526.0
O_trans_prob_dict['O\n'] = (trans_item_list.count(['O\n', 'O\n'])) / 309526.0

tag_trans_prob_dict = {}
tag_trans_prob_dict['B\n'] = B_trans_prob_dict
tag_trans_prob_dict['I\n'] = I_trans_prob_dict
tag_trans_prob_dict['O\n'] = O_trans_prob_dict

print tag_trans_prob_dict

num_sentence = word_list.count('. ')
start_prob_dict = {}
start_prob_dict['B\n'] = 1.0 / (num_sentence + 2)
start_prob_dict['I\n'] = 1.0 / (num_sentence + 2)
start_prob_dict['O\n'] = 1 - start_prob_dict['B\n'] - start_prob_dict['I\n']

print start_prob_dict

filein.close()

# def viterbi(obs, states, start_p, trans_p, emit_p):
# 	if len(obs) < 2:
# 		return ['O\n']

# 	V = [{y:(start_p[y] * emit_p[y][obs[0]]) for y in states}]
# 	path = {y:[y] for y in states}
# 	for y in states:
# 		V[0][y] = start_p[y] * emit_p[y][obs[0]]
# 		path[y] = [y]

# 	for t in range(1, len(obs)):
# 		V.append({})
# 		newpath = {}

# 		for y in states:
# 			(prob, state) = max((V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states)
# 			V[t][y] = prob
# 			newpath[y] = path[state] + [y]
# 		path = newpath

# 	(prob, state) = max((V[t][y], y) for y in states)
# 	return path[state]

# def read_test_file(filename):
# 	filein = open(filename, 'r')
# 	total_line = ''
# 	for line in filein:
# 		total_line += line

# 	sentence_list = total_line.split('\n\n')
# 	test_list = []
# 	for each in sentence_list:
# 		words = each.split('\n')
# 		if '' in words:
# 			words.remove('')
# 		test_list.append(tuple(words))
# 	return test_list

# tags_tuple = ('B\n', 'I\n', 'O\n')

# test_word_list = read_test_file('modified_test.txt')
# # print len(test_word_list)
# # print test_word_list[-1]

# res_list = []
# for words_tuple in test_word_list:
# 	path = viterbi(words_tuple, tags_tuple, start_prob_dict, tag_trans_prob_dict, tag_word_prob_dict)
# 	res_list.append(tuple(path))
# print len(res_list)

# count = 0
# for path in res_list:
# 	if 'B\n' in path:
# 		count += 1
# print count

# raw_word_list = read_test_file('test.txt')

# def output_result(word_list, tag_list, output_filename):
# 	fileout = open(output_filename, 'w')
# 	for i in range(0, len(word_list)):
# 		for j in range(0, len(word_list[i])):
# 			line = word_list[i][j] + '\t' + tag_list[i][j]
# 			fileout.write(line)
# 			# if word_list[i][j] == '. ':
# 		fileout.write('\n')
# 	fileout.close()

# output_result(raw_word_list, res_list, 'output.txt')