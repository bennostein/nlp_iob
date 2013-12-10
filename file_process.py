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
# 13204 with UNKNOWN
print len(unique_word_list)

B_dict = {}
I_dict = {}
O_dict = {}
for word in unique_word_list:
	B_dict[word] = (1 + B_list.count(word)) / 347696.0
	I_dict[word] = (1 + I_list.count(word)) / 347696.0
	O_dict[word] = (1 + O_list.count(word)) / 347696.0

tag_word_prob_dict = {}
tag_word_prob_dict['B\n'] = B_dict
tag_word_prob_dict['I\n'] = I_dict
tag_word_prob_dict['O\n'] = O_dict

print tag_word_prob_dict['B\n']['UNKOWN ']
print tag_word_prob_dict['I\n']['UNKOWN ']
print tag_word_prob_dict['O\n']['UNKOWN ']

trans_item_list = []
for i in range(0, len(tag_list) - 1):
	item = [tag_list[i], tag_list[i + 1]]
	trans_item_list.append(item)

B_trans_prob_dict = {}
B_trans_prob_dict['B\n'] = (trans_item_list.count(['B\n', 'B\n']) + 1) / 15514.0
B_trans_prob_dict['I\n'] = (trans_item_list.count(['B\n', 'I\n']) + 1) / 15514.0
B_trans_prob_dict['O\n'] = (trans_item_list.count(['B\n', 'O\n']) + 1) / 15514.0

I_trans_prob_dict = {}
I_trans_prob_dict['B\n'] = (trans_item_list.count(['I\n', 'B\n']) + 1) / 22656.0
I_trans_prob_dict['I\n'] = (trans_item_list.count(['I\n', 'I\n']) + 1) / 22656.0
I_trans_prob_dict['O\n'] = (trans_item_list.count(['I\n', 'O\n']) + 1) / 22656.0

O_trans_prob_dict = {}
O_trans_prob_dict['B\n'] = (trans_item_list.count(['O\n', 'B\n']) + 1) / 309526.0
O_trans_prob_dict['I\n'] = (trans_item_list.count(['O\n', 'I\n']) + 1) / 309526.0
O_trans_prob_dict['O\n'] = (trans_item_list.count(['O\n', 'O\n']) + 1) / 309526.0

tag_trans_prob_dict = {}
tag_trans_prob_dict['B\n'] = B_trans_prob_dict
tag_trans_prob_dict['I\n'] = I_trans_prob_dict
tag_trans_prob_dict['O\n'] = O_trans_prob_dict

print tag_trans_prob_dict

filein.close()


# class FileProcess():
# 	tag_list = []
# 	tag_set = set()
# 	word_list = []
# 	word_tag_dict = {}
# 	tag_dict = {}
# 	start_tag = '<start>\n'

# 	def __init__(self, filename):
# 		self.filein = open(filename)

# 	def file_close(self):
# 		self.filein.close()

# 	def get_word_tag_dict(self):
# 		for line in self.filein:
# 			if line != '\n':
# 				line_tuple = tuple(line.split('\t'))
# 				self.word_list.append(line_tuple[0])
# 				self.tag_list.append(line_tuple[1])
# 				if not self.word_tag_dict.has_key(line_tuple):
# 					self.word_tag_dict[line_tuple] = 1
# 				else:
# 					self.word_tag_dict[line_tuple] += 1
# 		self.tag_set = set(self.tag_list)

# 	def init_tag_trans_count_dict(self):
# 		self.tag_set.add(self.start_tag)
# 		tag_trans_count_dict = {}
# 		for each in self.tag_set:
# 			tag_trans_count_dict[each] = {}
# 			for each1 in self.tag_set:
# 				tag_trans_count_dict[each][each1] = 1
# 		return tag_trans_count_dict

# 	def get_word_likehood_prob_dict(self):
# 		word_tag_prob_dict = {}
# 		for each in self.tag_list:
# 			if not self.tag_dict.has_key(each):
# 				self.tag_dict[each] = 1
# 			else:
# 				self.tag_dict[each] += 1

# 		word_tag_list = []
# 		for key in self.word_tag_dict.keys():
# 			word_tag_item = list(key)
# 			word_tag_item.append(self.word_tag_dict[key])
# 			word_tag_list.append(tuple(word_tag_item))

# 		for word, tag, num in word_tag_list:
# 			word_tag_prob_dict.setdefault(tag, {})[word] = float(num) / float(self.tag_dict[tag])
# 		return word_tag_prob_dict

# 	def get_total_trans_prob_dict(self):
# 		new_tag_list = []
# 		new_tag_list.append(self.start_tag)
# 		for each in self.tag_list:
# 			new_tag_list.append(each)
# 			if each == '.\n':
# 				new_tag_list.append(self.start_tag)
# 		new_tag_list.pop()
# 		self.tag_dict[self.start_tag] = new_tag_list.count(self.start_tag)

# 		total_tag_trans_list = []
# 		for i in range(0, len(new_tag_list)-1):
# 			item = [new_tag_list[i], new_tag_list[i+1]]
# 			total_tag_trans_list.append(item)

# 		tag_trans_count_dict = self.init_tag_trans_count_dict()
# 		for each in total_tag_trans_list:
# 			tag_trans_count_dict[each[0]][each[1]] += 1

# 		total_tag_trans_prob_dict = {}
# 		for key in tag_trans_count_dict.keys():
# 			total_tag_trans_prob_dict[key] = {}
# 			for each in tag_trans_count_dict[key].keys():
# 				total_tag_trans_prob_dict[key][each] = float(tag_trans_count_dict[key][each]) / float(self.tag_dict[key] + 37)

# 		return total_tag_trans_prob_dict

# 	def get_start_prob_dict(self):
# 		total_tag_trans_prob_dict = self.get_total_trans_prob_dict()
# 		return total_tag_trans_prob_dict[self.start_tag]

# 	def get_tag_trans_prob_dict(self):
# 		total_tag_trans_prob_dict = self.get_total_trans_prob_dict()
# 		return total_tag_trans_prob_dict

# train_set = FileProcess('train.txt')
# train_set.get_word_tag_dict()
# init_tag_trans_count_dict = train_set.init_tag_trans_count_dict()

# word_tag_prob_dict = train_set.get_word_likehood_prob_dict()
# start_prob_dict = train_set.get_start_prob_dict()
# tag_trans_prob_dict = train_set.get_tag_trans_prob_dict()
# train_set.tag_set.remove(train_set.start_tag)
# tags = tuple(train_set.tag_set)
# word_set = set(train_set.word_list)

# for tag in word_tag_prob_dict.keys():
# 	for each in list(word_set):
# 		if not word_tag_prob_dict[tag].has_key(each):
# 			word_tag_prob_dict[tag][each] = 0

# print len(start_prob_dict), len(tag_trans_prob_dict), len(word_tag_prob_dict)
# # print start_prob_dict
# # print tag_trans_prob_dict
# print word_tag_prob_dict['I\n'], word_tag_prob_dict['O\n'], word_tag_prob_dict['B\n']