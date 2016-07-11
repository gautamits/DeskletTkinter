import os
paths=[]
spaces=[]
char="|"
def tree(root,string):
	st=' '*(len(string)/2)
	print st+root
	try:
		for i in os.listdir(root):
			p=root+"/"+i
			if os.path.isfile(p):
				print string+i
			elif os.path.isdir(p):
				#print ""
				#print string+root
				#tree(string+"____",p)
				paths.append(p)
				spaces.append("    "+string)
	except:
		print "permission denied for",root

path=raw_input()
paths.append(path)
spaces.append("    ")
while len(paths) > 0:
	#tree("____",path)
	tree(paths.pop(),spaces.pop())

