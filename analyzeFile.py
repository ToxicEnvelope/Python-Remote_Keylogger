import re
import collections
import sys

def sorting(cleaned_file):
	words = re.findall(r'\w+', open(cleaned_file).read())
	list_words = collections.Counter(words).most_common()
	of = open(cleaned_file, "w+")
	for x,y in list_words:
		print x,y
		of.write("\n".join(["%s %s" % (x, y)]) + "\n")

def clean(file_to_clean, cleaned_file):
	delete_list = ["[ENTER]", "[TAB]"]
	fin = open(file_to_clean, "r")
	fout = open(cleaned_file, "w+")
	for line in fin:
	    for word in delete_list:
	        line = line.replace(word, "")
	    fout.write(line)
	fin.close()
	fout.close()

def main(args):
	clean(args[0], args[1])
	sorting(args[1])

if __name__ == "__main__": 
	total = len(sys.argv)
	if total is 1:
		print "\n[*] Usage: sudo python analizeFile.py <inputfile> <outputfile>\n"
	else:
		main(sys.argv[1:])
