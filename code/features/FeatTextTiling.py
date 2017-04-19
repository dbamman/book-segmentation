import re
from math import sqrt
import math

class TextTiling:

	def feats(self, features):
		featvals={}
		self.means={}
		self.sds={}
		self.binary={}
		n=0
		for index in features:
			feats=features[index]
			n+=1

			for fid in feats:

				fval=feats[fid]
				if fval == 0:
					continue
				if fid not in featvals:
					featvals[fid]={}
				if fval not in featvals[fid]:
					featvals[fid][fval]=0
				
				featvals[fid][fval]+=1

		for feat in featvals:
			if len(featvals[feat]) == 1:
				self.binary[feat]=1
			else:
				mean=0.
				localn=0
				for fval in featvals[feat]:
					mean+=fval * featvals[feat][fval]
					localn+=featvals[feat][fval]
				self.means[feat]=mean/n
				# print localn, n
			
				sd=0.
				for fval in featvals[feat]:
					sd+=featvals[feat][fval] * (fval - self.means[feat]) * (fval - self.means[feat])
				self.sds[feat]=math.sqrt(sd/n)

	def convert(self, fval, val):
		if fval in self.binary:
			return 1
		else:
			if fval in self.means:
				z=(val-self.means[fval])/self.sds[fval]
				return z
		return 0

	def cosine(self, one, two):
		# print one, two
		num=0.
		onesum=0.
		twosum=0.
		for key in one:
			if key in two:
				# print self.convert(key, one[key])
				num+=self.convert(key, one[key])*self.convert(key, two[key])
			onesum+=self.convert(key, one[key])*self.convert(key, one[key])

		for key in two:
			twosum+=self.convert(key, two[key])*self.convert(key, two[key])

		return num/(sqrt(onesum)*sqrt(twosum))

	def extractFeatures(self, features):
		feats={}
		for i in features:
			feats[i]={}
		self.feats(features)
		
		ordered=sorted(features.keys())
		revordered={}
		for i in range(len(ordered)):
			revordered[ordered[i]]=i

		print ordered
		
		for i in range(1,len(ordered)):
			index=ordered[i]

			previous=ordered[i-1]

			cos=self.cosine(features[index], features[previous])
			print cos
			feats[index]["textiling"]=cos

		return feats
