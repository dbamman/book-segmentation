# -*- coding: utf-8 -*-

import re,sys
import numpy as np
from math import log

class PageSequence:


	def extractFeatures(self, pages, pagenums):
		feats=[]
		maxx=0
		for i in range(len(pages)):
			feats.append({})
			if pagenums[i] > maxx:
				maxx=pagenums[i]
		
		numbers=[None]*(maxx+1)
		numbers[0]={}
		numbers[0][-1]=1
		for i in range(len(pages)):
			
			pagenum=pagenums[i]

			text=""
			lines=pages[i]
			for idx, line in enumerate(lines):
				if idx < 5 or idx >= len(lines)-5:
					text+=line.rstrip()

			tokens=re.split("\s+", text.lower())
			seen={}

			numbers[pagenum]={}
			# null
			numbers[pagenum][-1]=1
			if pagenum == 0:
				continue

			for token in tokens:
				if re.match("^[0-9]+$", token) != None:
					number=int(token)
					if abs(pagenum-number) < 25:
						numbers[pagenum][number]=1


		#print len(numbers)
		for i in range(maxx):
			if numbers[i] == None:
				numbers[i]={}
				numbers[i][-1]=1

		viterbi={}
		backpointer={}
		viterbi[0]={}
		viterbi[0][-1]=log(10)
		numbers[0][-1]=1
		maxpath={}
		maxpath[0]={}
		maxpath[0][-1]=-1
		for i in range(1,maxx):
			# print i
			# print numbers[i]
			viterbi[i]={}
			backpointer[i]={}
			maxpath[i]={}

			# viterbi[i]=[]
			# backpointer[i]=[]
			j=i-1

			for num_i in numbers[i]:
				viterbi[i][num_i]=log(sys.float_info.max)
				backpointer[i][num_i]=-1

				# print "num j", j, numbers[j]
				for num_j in numbers[j]:
					if (num_j > num_i or (num_j == num_i)) and (num_i != -1 and num_j != -1):
						# print num_j, num_i, "too big"
						continue

					#print num_j, maxpath[j]
					# if num_j not in maxpath[j]:
					# 	continue

					# max_on_path=maxpath[j][num_j]
					# if num_i <= max_on_path and num_i != -1 and max_on_path != -1:
					# 	continue

					diff=abs(num_i-num_j)

					if num_i == -1 and num_j == -1:
						diff=10
					elif num_i == -1 or num_j == -1:
						diff=100
					# print diff, num_i, num_j, i, j

					vit=viterbi[j][num_j] + log(diff)
					# print vit
				#	print "vit: %s %.10f %.5f" % (num_j, vit, diff), i, j, num_i
					if vit < viterbi[i][num_i]:
						viterbi[i][num_i]=vit
						backpointer[i][num_i]=num_j
						# maxpath[i][num_i]=num_j
						# if maxpath[j][num_j] > num_j:
						# 	maxpath[i][num_i]=maxpath[j][num_j]
			#	print "back %s" % backpointer[i][num_i]

		final=sys.float_info.max
		finalpointer=-1
		for num_j in numbers[maxx-1]:
			vit=viterbi[maxx-1][num_j]
			if vit < final:
				final=vit
				finalpointer=num_j

		#print "final", final
		pointer=finalpointer
		stack=[]

		for i in reversed(range(1,maxx)):
			#print i
			stack.append(pointer)
			pointer=backpointer[i][pointer]
#			print i, pointer
		
		counts=np.zeros(maxx)

		c=0
		for idx, val in enumerate(reversed(stack)):
			#print val,
			if val != -1:
				offset=(idx-val)+1
				if offset >= 0:
					counts[offset]+=1
				c+=1
			if c >= 20:
				break
		#print
		argmax=np.argmax(counts)

		firstpage=-1
		firstval=-1
		for idx, val in enumerate(reversed(stack)):
			#print val,
			if val != -1:
				offset=(idx-val)+1
				if offset == argmax:
					firstpage=idx
					firstval=val
					break
		
		# print "argmax: %s" % argmax, counts[argmax], firstpage, firstval
		#print counts		

		if counts[argmax] >= 5:
			for p in range(len(pages)):
			
				i=pagenums[p]

				feats[p]["page_sequence:page_count_identified"]=1
				if i < argmax:
					feats[p]["page_sequence:before_first_inferred_page"]=1
				else:
					feats[p]["page_sequence:after_first_inferred_page"]=1

				if firstpage != -1:
					if i < firstpage:
						feats[p]["page_sequence:before_first_marked_page"]=1
					else:
						feats[p]["page_sequence:after_first_marked_page"]=1

		return feats
