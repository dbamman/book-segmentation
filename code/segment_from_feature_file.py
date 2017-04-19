"""

For an input feature file and trained model, segment and label

"""

import sys,os,re
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import numpy as np

import seg_model


labelsIds = {"title": 0 , "dedication": 1, "pubinfo": 2, "ad": 3, "toc" : 4, "preface": 5, "content": 6, "index": 7, "appendix": 8, "None": 9}
revLabels=["title", "dedication", "pubinfo", "ad", "toc", "preface", "content", "index", "appendix", "NA"]

cats=len(revLabels)

model=seg_model.Model()

means={}
sds={}


def readmeans(filename):
	file=open(filename)
	for line in file:
		cols=line.rstrip().split("\t")	
		fid=int(cols[0])
		mean=float(cols[1])
		sd=float(cols[2])
		means[fid]=mean
		sds[fid]=sd
	file.close()

def zscore(fid, fval):
	return (fval-means[fid])/sds[fid]


def convertBookToFeats(pages):
	matrix=[]
	page_index=[]
	for page, pagefeatures in sorted(pages.iteritems()):
		rep=np.zeros(model.fsize)
		page_index.append(page)
		for key, val in pagefeatures.items():
			if key in means:
				val=zscore(key, val)
			rep[key]=val
		matrix.append(rep)

	return np.array(matrix), page_index
		

def readbook(filename):

	matrix=[]
	page_index=[]
	file=open(filename)
	for line in file:
		cols=line.rstrip().split("\t")
		if len(cols) < 3:
			continue
		idd=cols[0]
		page=int(cols[1])
		feats=cols[2].split(" ")
		rep=np.zeros(model.fsize)
		for f in feats:
			vals=f.split("=")
			fid=int(vals[0])
			fval=float(vals[1])
			if fid in means:
				fval=zscore(fid, fval)
			rep[fid]=fval
		matrix.append(rep)
		page_index.append(page)

	return np.array(matrix), page_index

def predict(matrix, page_index, modelFile):
	saver = tf.train.Saver()

	config = tf.ConfigProto()

	sess = tf.Session(config=config)

	saver.restore(sess, modelFile)

	[preds] = sess.run([model.prediction], feed_dict={model.x: matrix, model.keep_prob: 1., model.seq_length: len(matrix)})

	predictions=[]
	for p in range(len(preds)):
		predictions.append((page_index[p], revLabels[preds[p]]))
	return predictions

if __name__ == "__main__":
	book=sys.argv[1]
	modelFolder=re.sub("/$", "", sys.argv[2])

	meanFile="%s/means.txt" % (modelFolder)
	modelFile="%s/model.ckpt" % (modelFolder)

	readmeans(meanFile)
	feats, page_index=readbook(book)
	predictions=predict(feats, page_index, modelFile)

	for page, pred in predictions:
		print "%s\t%s" % (page, pred)

