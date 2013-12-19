import re

class FilePreProcess():
	word_dict = {}
	word_list = []

	def __init__(self, filename):
		self.filein = open(filename)

	def file_close(self):
		self.filein.close()
		
	def get_word_count(self):
		for line in self.filein:
			line_list = line.split('\t')
			self.word_list.append(line_list[0])

		for each in self.word_list:
			if not self.word_dict.has_key(each):
				self.word_dict[each] = 1
			else:
				self.word_dict[each] += 1

	def replace_train_file(self, filein, fileout):
		filein = open(filein, 'r')
		fileout = open(fileout, 'w')

		pattern_num = re.compile(r'.*\d+.*')
		pattern_mix = re.compile(r'(?:^[a-z]+[A-Z]+[a-zA-Z]*|^[A-Z]+[a-z]+[a-zA-Z]*)')

		for line in filein:
			line_list = line.split('\t')
			word = line_list[0]
			if self.word_dict[word] == 1:
				if len(word) >= 8:
					line_list[0] = 'UNKOWN_long'
				elif pattern_num.match(word) != None:
					line_list[0] = 'UNKOWN_num'
				elif word.isupper():
					line_list[0] = 'UNKOWN_upper'
				elif pattern_mix.match(word) != None:
					line_list[0] = 'UNKOWN_mix'
				else:
					line_list[0] = 'UNKOWN_other'
				line = '\t'.join(line_list)
			fileout.write(line)

		filein.close()
		fileout.close()

	def replace_test_file(self, filein, fileout, word_set):
		filein = open(filein, 'r')
		fileout = open(fileout, 'w')
		pattern_num = re.compile(r'.*\d+.*')
		pattern_mix = re.compile(r'(?:^[a-z]+[A-Z]+[a-zA-Z]*|^[A-Z]+[a-z]+[a-zA-Z]*)')

		for word in filein:
			if word != '\n':
				word = word.rstrip('\n')
				if not word in word_set:
					if len(word) >= 8:
						word = 'UNKOWN_long'
					elif pattern_num.match(word) != None:
						word = 'UNKOWN_num'
					elif word.isupper():
						word = 'UNKOWN_upper'
					elif pattern_mix.match(word) != None:
						word = 'UNKOWN_mix'
					else:
						word = 'UNKOWN_other'
				fileout.write(word + '\n')	
			else:
				fileout.write(word)

		filein.close()
		fileout.close()


class FileProcess():
	unique_word_list = []

	def __init__(self, filename):
		self.filein = open(filename)

	def file_close(self):
		self.filein.close()

	def get_start_prob_dict(self):
		self.filein.seek(0)
		start_prob_dict = {}
		sentence_num = 0

		for line in self.filein:
			if line == '\n':
				sentence_num += 1

		start_prob_dict['B\n'] = 1.0 / (sentence_num + 2)
		start_prob_dict['I\n'] = 1.0 / (sentence_num + 2)
		start_prob_dict['O\n'] = 1 - start_prob_dict['B\n'] - start_prob_dict['I\n']

		return start_prob_dict

	def get_tag_trans_prob_dict(self):
		self.filein.seek(0)
		tag_list = []
		for line in self.filein:
			if line != '\n':
				line_list = line.split('\t')
				tag_list.append(line_list[1])

		trans_item_list = []
		for i in range(0, len(tag_list)-1):
			item = [tag_list[i], tag_list[i + 1]]
			trans_item_list.append(item)

		B_trans_prob_dict = {}
		B_trans_prob_dict['B\n'] = (trans_item_list.count(['B\n', 'B\n']) + 1) / (16637.0 + 3.0)
		B_trans_prob_dict['I\n'] = (trans_item_list.count(['B\n', 'I\n']) + 1) / (16637.0 + 3.0)
		B_trans_prob_dict['O\n'] = (trans_item_list.count(['B\n', 'O\n']) + 1) / (16637.0 + 3.0)

		I_trans_prob_dict = {}
		I_trans_prob_dict['B\n'] = (trans_item_list.count(['I\n', 'B\n']) + 1) / (24435.0 + 3.0)
		I_trans_prob_dict['I\n'] = (trans_item_list.count(['I\n', 'I\n']) + 1) / (24435.0 + 3.0)
		I_trans_prob_dict['O\n'] = (trans_item_list.count(['I\n', 'O\n']) + 1) / (24435.0 + 3.0)

		O_trans_prob_dict = {}
		O_trans_prob_dict['B\n'] = (trans_item_list.count(['O\n', 'B\n']) + 1) / (345128.0 + 3.0)
		O_trans_prob_dict['I\n'] = (trans_item_list.count(['O\n', 'I\n']) + 1) / (345128.0 + 3.0)
		O_trans_prob_dict['O\n'] = (trans_item_list.count(['O\n', 'O\n']) + 1) / (345128.0 + 3.0)

		tag_trans_prob_dict = {}
		tag_trans_prob_dict['B\n'] = B_trans_prob_dict
		tag_trans_prob_dict['I\n'] = I_trans_prob_dict
		tag_trans_prob_dict['O\n'] = O_trans_prob_dict

		return tag_trans_prob_dict

	def get_tag_word_prob_dict(self):
		self.filein.seek(0)
		B_list = []
		I_list = []
		O_list = []
		word_list = []

		for line in self.filein:
			if line != '\n':
				line_list = line.split('\t')
				word_list.append(line_list[0])
				if line_list[1] == 'B\n':
					B_list.append(line_list[0])
				elif line_list[1] == 'I\n':
					I_list.append(line_list[0])
				else:
					O_list.append(line_list[0])

		self.unique_word_list = list(set(word_list))
		B_dict = {}
		I_dict = {}
		O_dict = {}

		for word in self.unique_word_list:
			B_dict[word] = 0
			I_dict[word] = 0
			O_dict[word] = 0

		for word in B_list:
			B_dict[word] += 1
		for word in I_list:
			I_dict[word] += 1
		for word in O_list:
			O_dict[word] += 1

		for word in self.unique_word_list:
			B_dict[word] = B_dict[word] / 16637.0
			I_dict[word] = I_dict[word] / 24435.0
			O_dict[word] = O_dict[word] / 345128.0

		tag_word_prob_dict = {}
		tag_word_prob_dict['B\n'] = B_dict
		tag_word_prob_dict['I\n'] = I_dict
		tag_word_prob_dict['O\n'] = O_dict

		return tag_word_prob_dict


def viterbi(obs, states, start_p, trans_p, emit_p):
	if len(obs) < 2:
		return ['O\n']

	V = [{y:(start_p[y] * emit_p[y][obs[0]]) for y in states}]
	path = {y:[y] for y in states}
	for y in states:
		V[0][y] = start_p[y] * emit_p[y][obs[0]]
		path[y] = [y]

	for t in range(1, len(obs)):
		V.append({})
		newpath = {}

		for y in states:
			(prob, state) = max((V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states)
			V[t][y] = prob
			newpath[y] = path[state] + [y]
		path = newpath

	(prob, state) = max((V[t][y], y) for y in states)
	return path[state]


def read_test_file(filename):
	filein = open(filename, 'r')
	total_line = ''
	for line in filein:
		total_line += line

	sentence_list = total_line.split('\n\n')
	test_list = []
	for each in sentence_list:
		words = each.split('\n')
		if '' in words:
			words.remove('')
		test_list.append(tuple(words))
	return test_list


def output_result(word_list, tag_list, output_filename):
	fileout = open(output_filename, 'w')

	for i in range(0, len(word_list)):
		for j in range(0, len(word_list[i])):
			line = word_list[i][j] + '\t' + tag_list[i][j]
			fileout.write(line)
		fileout.write('\n')

	fileout.close()


def main():
	filename = 'gene.train.txt'
	train_pre_process = FilePreProcess(filename)
	train_pre_process.get_word_count()
	new_filename = 'modified.train.txt'
	train_pre_process.replace_train_file(filename, new_filename)
	train_pre_process.file_close()

	train_process = FileProcess(new_filename)
	start_prob_dict = train_process.get_start_prob_dict()
	tag_trans_prob_dict = train_process.get_tag_trans_prob_dict()
	tag_word_prob_dict = train_process.get_tag_word_prob_dict()
	train_process.file_close()

	testname = 'test_2.txt'
	test_pre_process = FilePreProcess(testname)
	new_testname = 'modified.test_2.txt'
	word_set = set(train_process.unique_word_list)
	test_pre_process.replace_test_file(testname, new_testname, word_set)

	tags_tuple = ('B\n', 'I\n', 'O\n')
	test_word_list = read_test_file(new_testname)
	res_list = []
	for words_tuple in test_word_list:
		path = viterbi(words_tuple, tags_tuple, start_prob_dict, tag_trans_prob_dict, tag_word_prob_dict)
		res_list.append(path)

	raw_word_list = read_test_file(testname)
	output_result(raw_word_list, res_list, 'output.txt')


if __name__ == '__main__':
	main()