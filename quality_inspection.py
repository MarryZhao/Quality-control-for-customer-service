# -*- coding: utf-8 -*
#!/usr/bin/env python
# quality_inspection.py
# Author :ZT
# Date: 20-March-2018
# About:  Intelligent Quality Inspection

import pandas as pd 
import numpy as np
 


"""
PYTHON3  默认UTF-8编码（一个汉字暂1位，3个字节）
"""
sents = "您好很高兴为您服务很高兴呢,还没吃饭"
sents_1 = "您好很高兴为您服务很高兴呢,还没吃饭"
a = "您"
b = "高兴"
character = "还没吃饭|我年轻|(我#岁#5)|(我#没下班)&~工资低"
#ifin(sents,"还没吃饭")|ifin(sents,"我年轻")|(ifnear(sents,"我","岁",5))|(ifnear(sents,"我","没下班"))&ifnotin(sents,"工资低")


def location(sents,a):
	"""
	判断字符串sents中字符串a出现的位置，结果起始为1
	"""	
	i = 0
	j = 0
	A = []
	while(i <= len(sents)-len(a)):      
	    j = 0
	    while(sents[i] == a[j]):
	        i = i + 1
	        j = j + 1
	        if(j == len(a)):
	            A.append(i-j+1)
	            j = 0
	            break
	    i = i + 1
	return A

#print(location(sents,b))


def ifin(sents,a):
	"""
	判断字符串a是否在文本sents中出现
	"""

	if(len(location(sents,a)) == 0):
		return False
	else:
		return True


def ifnotin(sents,a):
	"""
	判断字符串sents中是否包含字符串a
	"""
	if(len(location(sents,a)) == 0):
		return True
	else:
		return False

#或者直接用in 和 not in ，例： a in sents 返回False或者True 
	
	
def ifnear(sents,a,b,k=5):
	"""
	判断字符串sents中字符b是否出现在字符a的后k位内
	"""
	loca_a = location(sents,a)
	loca_b = location(sents,b)
	len_a = len(loca_a)
	len_b = len(loca_b)

	if(len_a|len_b == 0):
		return False
	else:
		for i in range(1,len_a):
			for j in range(1,len_b):
				if (loca_b[j-1]-loca_a[i-1] <= k):
					return True
		return False

#print(ifnear(sents,a,b))


def main_out(sents,character):
	"""
	判断是否符合导入的文字规则：
	1、判断特殊字符在character中的位置（起始位是0）；2、替换字符执行

	规定:括号内只能出现#，且括号和#必须作为整体出现
	"""
	def location_character(character,c):
		i = 0
		j = 0
		A = []
		while(i <= len(character)-len(c)):      
			j = 0
			while(character[i] == c[j]):
				i = i + 1
				j = j + 1
				if(j == len(c)):
					A.append(i-j)
					j = 0
					break
			i = i + 1
		return A

	#构造字符串数组
	len_char = len(character)	
	loca_and = location_character(character,"|")
	loca_or = location_character(character,"&")
	loca_character = sorted(loca_and + loca_or,reverse=False)

	if(len(loca_character) == 0):
		char_2 = "ifin(sents, '"+ character +"')" 
	else:
		char_1 = [character[:(loca_character[0]+1)],]
		for i in range(1,len(loca_character)):
			char_1.append(character[(loca_character[i-1]+1):(loca_character[i]+1)])
		char_1.append(character[(loca_character[i]+1):])

		#字符串替换
		for j in range(0,len(char_1)-1):
			if (char_1[j][0]!="(" and char_1[j][0]!="~"):
				char_1[j] = "ifin(sents, '"+ char_1[j][:-1] +"')" + char_1[j][-1]
			elif (char_1[j][0] == "~"):
				char_1[j] = "ifnotin(sents,'" + char_1[j][1:-1] +"')" + char_1[j][-1]
			else:
				if(len(location_character(char_1[j],"#")) == 1):
					char_1[j] = char_1[j].replace("#","','")
					char_1[j] = char_1[j].replace("(","ifnear(sents,'")
					char_1[j] = char_1[j].replace(")","')")	
				else:
					char_1[j] = char_1[j][:(location_character(char_1[j],"#")[0])] + "','" + char_1[j][(location_character(char_1[j],"#")[0]+1):(location_character(char_1[j],"#")[1])]+"'," + char_1[j][(location_character(char_1[j],"#")[1]+1):]                                                      
					char_1[j] = char_1[j].replace("(","ifnear(sents,'")

		j = len(char_1)-1
		if (char_1[j][0]!="(" and char_1[j][0]!="~"):
			char_1[j] = "ifin(sents, '"+ char_1[j]+"')" 
		elif (char_1[j][0] == "~"):
			char_1[j] = "ifnotin(sents,'" + char_1[j][1:] +"')" 
		else:
			if(len(location_character(char_1[j],"#")) == 1):
				char_1[j] = char_1[j].replace("#","','")
				char_1[j] = char_1[j].replace("(","ifnear(sents,'")
				char_1[j] = char_1[j].replace(")","')")	
			else:
				char_1[j] = char_1[j][:(location_character(char_1[j],"#")[0])] + "','" + char_1[j][(location_character(char_1[j],"#")[0]+1):(location_character(char_1[j],"#")[1])]+"'," + char_1[j][(location_character(char_1[j],"#")[1]+1):]                                                      
				char_1[j] = char_1[j].replace("(","ifnear(sents,'")

		#数组链接
		char_2 = "".join(char_1)

	#执行字符串代码
	out = eval(char_2)

	return out

print (main_out(sents_1,character))
print (main_out(sents_1,"高兴"))



#读入文件，连接同一流水号文件，逐条执行，返回流水号、行标记、话音标记、结果、查询词

filePath = "voice_to_text.txt"

def main(filePath):
	fp = pd.read_csv(filePath,sep='\t')
    for line in range(0,len(fp)):
       	fp[line,"OUT"] = main_out(fp[line,"SESSION_CONTENT"],"李洪志")
    return fp

print (main(filePath))


