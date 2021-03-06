import os
import io

import math

from struct import *
import glob

def unpacking(FileName):
    print( '[ %s ] unpacking...' % FileName )

    path = "./org.%s/" % FileName
    if not os.path.isdir(path):                                                           
        os.mkdir(path)

    indexTable = [ ]
    with open( FileName, 'rb' ) as F:
        fileSize = len( F.read() )
        F.seek(0)
        
        while True:
            temp = F.read(4)
            if temp.hex() == '00000000':
                break
            else:
                indexTable.append( unpack('<L', temp)[0] )

            '''
            if unpack('<L', temp)[0] == fileSize:
                indexTable.append( unpack('<L', temp)[0] )
                break
            else:
                indexTable.append( unpack('<L', temp)[0] )
                #'''

        for count, x in enumerate( indexTable[:-1] ):
            F.seek( indexTable[ count ] )
            newData = F.read( indexTable[ count+1 ] - indexTable[ count ] )
            with open( path+FileName.split(".")[0]+"."+"{0:0>6}".format(count)+'.bin', 'wb') as NF:
                NF.write( newData )
            
    pass

def packing(FolderName):
    print( '[ %s ] packing...' % FolderName )

    path = "./%s/*.bin" % FolderName
    fData = b''

    tableSize = math.ceil(( (len( glob.glob( path ) )*4)/128 ) )*128

    fData = bytes( tableSize )
    table = pack( '<L', len(fData) )
    for i in glob.glob( path ):
        with open(i , 'rb') as F:
            temp  = F.read()
            
            if not (len(temp)%128) == 0:
                temp += bytes( 128-(len(temp)%128) )
            

        fData += temp
        table += pack('<L', len(fData) )

    table+=bytes( 128-(len(table)%128) )
    fData = table+fData[ len(table):]

    with open( FolderName.split(".")[1]+'.new', 'wb' ) as F:
        F.write( fData )

    pass

if __name__ == '__main__':
    print( 'Program Start' )
    
    #unpacking('arcTacPrmDat.bin') # fileName.
    #packing('org.arcBtlMsgDat.bin') # FolderName.

    #unpacking('arcTacPrmDat.bin') # fileName.
    packing('org.arcTacPrmDat.bin - 복사본') # FolderName.
