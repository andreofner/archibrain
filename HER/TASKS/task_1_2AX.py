## TASK FOR HER TESTING
## The 1-2AX task consists in the presentation to the subject of six possible stimuli/cues '1' - '2', 'A' - 'B', 'X' - 'Y'.
## The tester has 2 possible responses which depend on the temporal order of previous and current stimuli: 
## he has to answer 'R' when
##	- the last stored digit is '1' AND the previous stimulus is 'A' AND the current one is 'X', 
##	- the last stored digit is '2' AND the previous stimulus is 'B' AND the current one is 'Y';
## in any other case , reply 'L'.    
## AUTHOR: Marco Martinolli
## DATE: 28.02.2017

from keras.utils import np_utils
import numpy as np

def preprocess_data(S,R):

	S_new=np_utils.to_categorical(S, nb_classes=6)
	
	R_new=np.where(R==0,[1,0,0,1],[0,1,1,0])		
	
	return S_new, R_new

def subset_data(S,O,training_perc=0.8):

	sz = np.shape(O)[0]
	idx = int(np.around(sz*training_perc))	

	# Distintion in training and test sets
	S_train = S[:idx, :]
	O_train = O[:idx, :]
	S_test = S[idx:, :]
	O_test = O[idx:, :]

	return S_train,O_train,S_test,O_test


# construction of the dataset
def data_construction(N=500,p_digit=0.05,p_wrong=0.225,p_correct=0.225,perc_training=0.8):

	cue_type = ['1', '2', 'AX', 'AY','BX','BY']

	SS = np.random.choice(np.arange(6), (N,1), p=[p_digit,p_digit,p_correct,p_wrong,p_wrong,p_correct]) 

	digit = None
	RR = np.ones(np.shape(SS))
	for i,s in enumerate(SS):

		if s==0 or s==1:
			RR[i]=0
			if s==0:		
				digit='1'
			else:
				digit='2'

		elif (digit=='1' and s==2) or (digit=='2' and s==5):
			RR[i]=1

		else:
			RR[i]=0
	
	# preprocess data to have the right format	
	[S, O] = preprocess_data(SS,RR)

	# data division in training and test subsets
	[S_tr, O_tr, S_test, O_test] = subset_data(S,O,0.8)

	dic_stim = {'array([[1, 0, 0, 0, 0, 0]])':'1',
		    'array([[0, 1, 0, 0, 0, 0]])':'2',
		    'array([[0, 0, 1, 0, 0, 0]])':'AX',
		    'array([[0, 0, 0, 1, 0, 0]])':'AY',
		    'array([[0, 0, 0, 0, 1, 0]])':'BX',
		    'array([[0, 0, 0, 0, 0, 1]])':'BY'}
	dic_resp =  {'array([[1, 0, 0, 1]])':'L', 'array([[0, 1, 1, 0]])':'R',}			

	return S_tr,O_tr,S_test,O_test,dic_stim,dic_resp