def viterbi(obs, states, start_p, trans_p, emit_p):
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

class FileProcess():
	tag_list = []
	tag_set = set()
	word_list = []
	word_tag_dict = {}
	tag_dict = {}
	start_tag = '<start>\n'

	def __init__(self, filename):
		self.filein = open(filename)

	def file_close(self):
		self.filein.close()

	def get_word_tag_dict(self):
		for line in self.filein:
			if line != '':
				line_tuple = tuple(line.split('\t'))
				if len(line_tuple) > 1:
					self.word_list.append(line_tuple[0])
					self.tag_list.append(line_tuple[1])
					if not self.word_tag_dict.has_key(line_tuple):
						self.word_tag_dict[line_tuple] = 1
					else:
						self.word_tag_dict[line_tuple] += 1
		self.tag_set = set(self.tag_list)

	def init_tag_trans_count_dict(self):
		self.tag_set.add(self.start_tag)
		tag_trans_count_dict = {}
		for each in self.tag_set:
			tag_trans_count_dict[each] = {}
			for each1 in self.tag_set:
				tag_trans_count_dict[each][each1] = 1
		return tag_trans_count_dict

	def get_word_likehood_prob_dict(self):
		word_tag_prob_dict = {}
		for each in self.tag_list:
			if not self.tag_dict.has_key(each):
				self.tag_dict[each] = 1
			else:
				self.tag_dict[each] += 1

		word_tag_list = []
		for key in self.word_tag_dict.keys():
			word_tag_item = list(key)
			word_tag_item.append(self.word_tag_dict[key])
			word_tag_list.append(tuple(word_tag_item))

		for word, tag, num in word_tag_list:
			word_tag_prob_dict.setdefault(tag, {})[word] = float(num) / float(self.tag_dict[tag])
		return word_tag_prob_dict

	def get_total_trans_prob_dict(self):
		new_tag_list = []
		new_tag_list.append(self.start_tag)
		for each in self.tag_list:
			new_tag_list.append(each)
			if each == '.\n':
				new_tag_list.append(self.start_tag)
		new_tag_list.pop()
		self.tag_dict[self.start_tag] = new_tag_list.count(self.start_tag)

		total_tag_trans_list = []
		for i in range(0, len(new_tag_list)-1):
			item = [new_tag_list[i], new_tag_list[i+1]]
			total_tag_trans_list.append(item)

		tag_trans_count_dict = self.init_tag_trans_count_dict()
		for each in total_tag_trans_list:
			tag_trans_count_dict[each[0]][each[1]] += 1

		total_tag_trans_prob_dict = {}
		for key in tag_trans_count_dict.keys():
			total_tag_trans_prob_dict[key] = {}
			for each in tag_trans_count_dict[key].keys():
				total_tag_trans_prob_dict[key][each] = float(tag_trans_count_dict[key][each]) / float(self.tag_dict[key] + 37)

		return total_tag_trans_prob_dict

	def get_start_prob_dict(self):
		total_tag_trans_prob_dict = self.get_total_trans_prob_dict()
		return total_tag_trans_prob_dict[self.start_tag]

	def get_tag_trans_prob_dict(self):
		total_tag_trans_prob_dict = self.get_total_trans_prob_dict()
		return total_tag_trans_prob_dict

class FilePreprocess():
	word_dict = {}
	word_list = []

	def __init__(self, filename):
		self.filein = open(filename)

	def get_word_count(self):
		for line in self.filein:
			line_list = line.split('\t')
			self.word_list.append(line_list[0])
		for each in self.word_list:
			if not self.word_dict.has_key(each):
				self.word_dict[each] = 1
			else:
				self.word_dict[each] += 1

	def replace_file(self, filein, fileout):
		filein = open(filein, 'r')
		fileout = open(fileout, 'w')
		for line in filein:
			line_list = line.split('\t')
			if self.word_dict[line_list[0]] == 1:
				line_list[0] = 'UNKOWN '
				line = '\t'.join(line_list)
			fileout.write(line)
		filein.close()
		fileout.close()

	def replace_test_file(self, filein, fileout, word_set):
		filein = open(filein, 'r')
		fileout = open(fileout, 'w')
		for line in filein:
			if line != '\n':
				line = line.rstrip('\n')
				if not line in word_set:
					line = 'UNKOWN '
				fileout.write(line + '\n')
			else:
				fileout.write(line)
		filein.close()
		fileout.close()

	def file_close(self):
		self.filein.close()

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
			if tag_list[i][j] == '.\n':
				fileout.write('\n')
	fileout.close()

def main():
	filename = 'train.txt'
	file_pre_process = FilePreprocess(filename)
	file_pre_process.get_word_count()
	new_filename = 'modified_train.txt'
	file_pre_process.replace_file(filename, new_filename)
	file_pre_process.file_close()

	train_set = FileProcess(new_filename)
	train_set.get_word_tag_dict()
	init_tag_trans_count_dict = train_set.init_tag_trans_count_dict()

	word_tag_prob_dict = train_set.get_word_likehood_prob_dict()
	start_prob_dict = train_set.get_start_prob_dict()
	tag_trans_prob_dict = train_set.get_tag_trans_prob_dict()
	train_set.tag_set.remove(train_set.start_tag)
	tags = tuple(train_set.tag_set)
	word_set = set(train_set.word_list)

	for tag in word_tag_prob_dict.keys():
		for each in list(word_set):
			if not word_tag_prob_dict[tag].has_key(each):
				word_tag_prob_dict[tag][each] = 0

	testname = 'test.txt'
	test_pre_process = FilePreprocess(testname)
	test_pre_process.get_word_count()
	new_testname = 'modified_test.txt'
	test_pre_process.replace_test_file(testname, new_testname, word_set)
	test_pre_process.file_close()

	raw_word_list = read_test_file(testname)
	test_list = read_test_file(new_testname)

	path_list = []
	for words in test_list:
		path = viterbi(words, tags, start_prob_dict, tag_trans_prob_dict, word_tag_prob_dict)
		path_list.append(tuple(path))

	output_result(raw_word_list, path_list, 'output.txt')

	train_set.file_close()

if __name__ == '__main__':
	main()
