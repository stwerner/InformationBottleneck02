#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compute tsne for information bottleneck on modes
(for python 3)

needs: bhtsne-master

does:
- USER: specify folder path, perplexity and outputfile
- loads time-shifted modes
- performs tsne with specified complexity value (cannot be run in ipython)
- h5file as output with space = time points in tsne space


Created on Tue Jul 18 23:25:39 2017

@author: stwerner
"""

import os
import numpy as np
import h5py
import sys
path2mainfolder='/Users/admin/Documents/AmsterdamResearch/InformationBottleneck/'
sys.path.append(path2mainfolder+'bhtsne-master')
import bhtsne


# -- USER INPUT: data folder, perplexity of tsne, output file
inputfile=path2mainfolder+'Results02/ModesMat.h5'
perplexity=60
out_file=path2mainfolder+'Results02/Perp'+str(perplexity)+'.h5'
# -- END


#check whether output file already exists
user_input='n'
if os.path.isfile(out_file):
    print('Output file already exists.')
    user_input = input('Do you want to replace file (y/n): ')
else:
    user_input='y'
    
    
if user_input=='y':
    #load input data
    f=h5py.File(inputfile,'r') #r - read only
    modedata=np.array(f['stackedmodes'])
    f.close()
    print('Size of data: '+str(modedata.shape))
    
    #perform tsne algorithm
    #modedata=modedata.astype('float64')
    space=bhtsne.run_bh_tsne(modedata,verbose=True,perplexity=perplexity,
                             initial_dims=5*10,max_iter=5000)

    #Save the result
    f=h5py.File(out_file,'w')
    tsne_s=f.create_dataset('space',(space.shape))
    tsne_s[...]=space
    f.close()

    







