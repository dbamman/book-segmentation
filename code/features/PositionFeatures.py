
class PositionFeatures:


	def firstTen(self, num):
		""" 
		Returns 1 if the page is in the first 10 pages and 0 otherwise.
		"""
		if num <= 10:
			return 1 
		return 0

	def lastTen(self, num, length):
		""" 
		Returns 1 if the page is in the last 10 pages and 0 otherwise.
		"""
		if (length-num <=10):
			return 1
		return 0

			
	def quintile(self, ratio):
		""" 
		Returns which third of the book that contains the given page.
		"""
		if ratio<=float(1)/float(5):
			return 1
		elif ratio <= float(2)/float(5):
			return 2
		elif ratio <= float(3)/float(5):
			return 3
		elif ratio <= float(4)/float(5):
			return 4
		else:
			return 5

	def extractFeatures(self, pages, pagenums):
		feats=[]
		for i in range(len(pages)):
			feats.append({})
			
		for i in range(len(pages)):
			num = pagenums[i]
			if self.firstTen(num) > 0:
				feats[i]["position_features:first10"] = self.firstTen(num)
			if self.lastTen(num, len(pages)) > 0:
				feats[i]["position_features:last10"] = self.lastTen(num, len(pages))

			ratio = round(float(num)/float(len(pages)), 2)

			if ratio > 0:
				feats[i]["position_features:ratio"] = ratio
			quint = self.quintile(ratio)

			if quint == 1:
				feats[i]["position_features:quint_1"] = 1
			elif quint == 2:
				feats[i]["position_features:quint_2"] = 1
			elif quint == 3:
				feats[i]["position_features:quint_3"] = 1
			elif quint == 4:
				feats[i]["position_features:quint_4"] = 1
			else:
				feats[i]["position_features:quint_5"] = 1
		# print feats
		return feats
