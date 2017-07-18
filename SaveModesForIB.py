#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compute matrix for Information Bottleneck on Modes directly

- add all timepoints of all worms and all movies in one matrix (dim 0)
- also add time-shifted values as additional modes
- use 10 time shifts

- at first, only movie 2 and 14 as before
- also only the fragments about a turn
- note decode() is needed for the string of the worm names because of the
difference between unicode and bytes (https://nedbatchelder.com/text/unipain.html)

Created on Tue Jul 18 22:08:53 2017

@author: stwerner
"""

import os
import numpy as np
import h5py
path2mainfolder='/Users/admin/Documents/AmsterdamResearch/InformationBottleneck/'
datapath=path2mainfolder+'NewMathijsModes/TotalFile_Rot4.h5'
out_file=path2mainfolder+'Results02/ModesMat.h5'


# -- Check whether output file already exists
user_input='n'
if os.path.isfile(out_file):
    print('Output file already exists.')
    user_input = input('Do you want to replace file (y/n): ')
else:
    user_input='y'


# -- Load data
if user_input=='y':
    f=h5py.File(datapath,'r')
    wormnames=list(f['WormNames'])
    movnumber=np.array([int(mywormnames.decode().split('_')[0].split('h')[-1]) for mywormnames in wormnames])
    movnumberind=np.append(np.where(movnumber==2)[0],np.where(movnumber==14)[0])
    TurnSequences=np.array((f['TurnSolver'][movnumberind,:]==True).astype(int))
    WormFlipped=np.array(f['WormFlipped'])[movnumberind]
    WormFlipped[WormFlipped==0]=-1
    WormModes=np.array(f['WormModes'])[movnumberind,:,:]
    #Matrix with 1 for start and -1 for end position:
    [numow,numot]=TurnSequences.shape
    TurnSeqSE=np.append(TurnSequences,np.ones([numow,1])*0,axis=1)-np.append(np.ones([numow,1])*0,TurnSequences,axis=1)
    numos=np.sum(TurnSeqSE==1,axis=1)
    for i in range(numow):
        startvals=[j for j in range(numot) if TurnSeqSE[i,j]==1]
        endvals=[j for j in range(numot+1) if TurnSeqSE[i,j]==-1]
        for j in range(numos[i]):
            mywormmodes=WormFlipped[i]*WormModes[i,startvals[j]:endvals[j],:]
            wormmodesstack=np.copy(mywormmodes[9:,:])
            for k in range(1,10):
                wormmodesstack=np.append(wormmodesstack,mywormmodes[(9-k):-k,:]
                                    ,axis=1)
            if i==0 and j==0:
                ModeOutput=np.copy(wormmodesstack)
                entrynumber=np.copy(endvals[j]-startvals[j])
            else:
                ModeOutput=np.vstack((ModeOutput,wormmodesstack))
                entrynumber=np.append(entrynumber,endvals[j]-startvals[j])
    f.close()

# -- Save data
    f=h5py.File(out_file,'w')
    entrynumberf=f.create_dataset('entrynumber',(entrynumber.shape))
    entrynumberf[...]=entrynumber
    ModeOutputf=f.create_dataset('stackedmodes',(ModeOutput.shape))
    ModeOutputf[...]=ModeOutput
    f.close()



