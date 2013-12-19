fileIn = open('gene.train.txt', 'r')
fileOut = open('test_all.txt', 'w')

for line in fileIn:
	if line != '\n':
		new_line = line[:-3:]
		new_line += '\n'
		fileOut.write(new_line)
	else:
		fileOut.write(line)

fileIn.close()
fileOut.close()