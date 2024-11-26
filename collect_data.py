#! /usr/bin/env /usr/bin/python3

'''
@file collect_data.py
@author Scott L. Williams.
@package ETO_WEATHER
@brief POLI batch implementation to construct a data set for ETo training
@LICENSE
# 
#  Copyright (C) 2020-2024 Scott L. Williams.
# 
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
'''

# constructs a data set for ETo vars training
# using 24 averaged time-slices on actual variables
# can use memory mapping for large datasets

# an embarrasing top-down, global variable prototype...

collect_data_copyright = 'collect_data.py Copyright (c) 2020-2024 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
import glob
import tempfile
import numpy as np

from prep_eto_pack import prep_eto
from wrf_source_pack import wrf_source

datapath = './dates/202404_7days.txt'
outpath = './202404_7days.npy'

mmap = False # use memory map?

# instantiate the operators
src = wrf_source.wrf_source( 'wrf_source' )

prep = prep_eto.prep_eto( 'prep_eto' )
prep.params.albedo = 0.23

nvars = 8    # number of ETo input actual variables

sizex = 171  # fixed geo sizes; TODO make dynamic
sizey = 171
sizez = 192  # 8*24=192   8 vars x 24 hours

# ----------------------------------------------------------------------------

# main

# declare numpy version
print( 'collect_data: using numpy version', np.version.version )

# collect and assemble data to present to minisom for training

# open file with a list of dates (days) to use
datafiles = open( datapath )
ndays = 0

# check if data files exist and have same dimensions and data types
# also get day count
print( 'collect_data: checking if data files exists...',
       file=sys.stderr, flush=True )
for f in datafiles:
    if not os.path.isfile( f.strip() ):
        print( 'collect_data:', f, ' does not exist...exiting',
               file=sys.stderr )
        sys.exit( 1 )
        
    # day counter
    ndays += 1
    print( '.', file=sys.stderr, flush=True, end='' )
    
datafiles.seek( 0, 0 )  # rewind file pointer position for day dates

# construct array (geo shape is fixed at 171x171 see above TODO)
try:
    if mmap:
        collect_mmap = tempfile.NamedTemporaryFile()
        eto_vars = np.memmap( collect_mmap, dtype=np.float32, mode='w+',
                             shape=(sizey*ndays,sizex,sizez) ) 
        print( '\ncollect_data: using memory mapping', file=sys.stderr )
    else:
        eto_vars = np.empty( shape=(sizey*ndays,sizex,sizez), dtype=np.float32 )
        print( '\ncollect_data: using ram memory', file=sys.stderr )

except Exception as e:
    print( e )
    print( 'collect_data: cannot allocate file...exiting ',
           file=sys.stderr )
    sys.exit( 1 )

print( 'collect_data: creating file', outpath, file=sys.stderr )
# NOTE: time slice 11 corresponds to 12:00pm Ecuador time
#       time slice  0 corresponds to 01:00am Ecuador time

# template band string; 0-indexed.
# string 'ts' gets replaced with actual hour below.
# band string indicates which bands get extracted from WRF source file
bandstr = 'TSK:ts,EMISS:ts,SWDOWN:ts,GLW:ts,GRDFLX:ts,T2:ts,PSFC:ts,Q2:ts,U10:ts,V10:ts'

day = 0  # day counter
for f in datafiles:
    
    print( 'processing', f, file=sys.stderr )
    f = f.strip()  # remove white spaces

    # run through hourly slices to augment feature space

    # read two slices and average actual values over the day
    for i in range(0,24):

        # construct wrf_source band string,
        # replace 'ts' with first time slice value
        bstr = bandstr.replace('ts','%02d'%i )
        
        # second time slice is added to string          
        # if operator "prep_eto" sees 10 bands it will implement directly
        # if operator "prep_eto" sees 20 bands it will implement two sets
        # and return an average
        
        # tell the source operator to get both time slices        
        src.params.bandstr = bstr + ',' + bandstr.replace('ts','%02d'%(i+1) )

        # read the WRF file with specifird bands (above) to extract
        src.params.filepath = f
        src.run()

        # process raw variables to get actual input values
        # for Penman-Montieth equation
        prep.source = src.sink
        prep.run()
                                              
        # time slice variable augmentation to feature space
        # implicitly introduces diurnal weather influences over time
        if i == 0: # value needs to be same as start i
            aug = prep.sink
        else:
            aug = np.append( aug, prep.sink, axis=2 )
                         
        ''' same thing done manually                
        for j in range( nvars ):
            aug[:,:,((i-1)*nvars + j)] = prep.sink[:,:,j]
        '''
        print( '.', end='', file=sys.stderr, flush=True )

    print( '\n', file=sys.stderr, flush=True )

    # fill in out buffer on daily basis
    yoff = sizey*day
    eto_vars[ yoff:yoff+sizey, :, : ] = aug
    day += 1

# end day loop

datafiles.close()

if mmap:
    eto_vars.flush()                 # flush values to file; needed?

# save eto vars data as numpy file
print( 'writing to file... ' + outpath, file=sys.stderr, flush=True, end='' )
#eto_vars.dump( outpath, protocol=4 )
np.save( outpath, eto_vars, allow_pickle=False )

print( ' done', file=sys.stderr, flush=True )
