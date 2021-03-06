import os
import io

import json

import math

from struct import *
import glob

def export_JSON( FileName ):
    print( '[ %s ] export JSON...' % FileName )

    with open( FileName, 'rb' ) as F:
        TableList = [ F.read(4) ]
        while True:
            temp = F.read(4)
            TableList.append( temp )
            if unpack('<L',TableList[0])[0] == F.tell():
                break

        jsonData = {}
        FileName = FileName.split("\\")[-1]
        jsonData[ FileName ] = []
        for countx, x in enumerate(TableList[:-1]):
            chapter = []
            
            F.seek( unpack('<L',x)[0] )
            #print( TableList[countx+1].hex(), TableList[countx].hex() )
            Data = F.read( unpack('<L',TableList[countx+1])[0] - unpack('<L',TableList[countx])[0] )

            ioData = io.BytesIO( Data )

            NameTrig = True
            FinPos = len( Data )

            #print( FinPos )
            Text = ''
            chapterPageCount  = 0
            chapterPage = {}
            while True:
                if FinPos == ioData.tell():
                    break
                if NameTrig:
                    index = ioData.read(4)
                    if index.hex()[2:3] == '2' or index.hex()[2:3] == 'a' or index.hex()[2:3] == '6':
                        tempNameAll = b''
                        while True:
                            tempName = ioData.read(2)
                            if tempName.hex() == '0000':
                                chapterPage['NickName'] = tempNameAll.decode( 'utf16' )
                                break
                            else:
                                tempNameAll += tempName
                    else:
                        chapterPage['NickName'] = ""
                    chapterPage['CharCode'] = index[:3].hex()
                    if index[-1:].hex() == '00':
                        chapterPage['Page'] = 'first'
                    else:
                        chapterPage['Page'] = 'more'

                    '''
                    print( index[-2:-1].hex() )
                    print( FileName, index.hex(), sep ='\t' )
                    #input( FileName ) #'''
                        
                    NameTrig = False
                    
                textLen = ioData.read(1)
                #print( textLen.hex() )
                if int.from_bytes( textLen, 'little' )-128 > 0:
                    FinTrig = True
                    NameTrig = True
                    int_textLen = int.from_bytes( textLen, 'little' )-128
                    Text += ioData.read( int_textLen ).decode('utf16')
                    chapterPage['Text'] = Text
                    Text = ''
                    chapter.append( chapterPage )
                    chapterPage = {}
                    chapterPageCount += 1

                else:
                    FinTrig = False
                    int_textLen = int.from_bytes( textLen, 'little' )
                    Text += ioData.read( int_textLen ).decode('utf16')+'\n'

            jsonData[ FileName ].append( chapter )
            #input()
                    
    #'''
    with open( './new/'+FileName.split('.')[0]+'.'+FileName.split('.')[1]+'.json', 'w', encoding='utf16' ) as F:
        json.dump(jsonData, F, ensure_ascii=False, indent=4)
    #'''
        
    pass

def import_JSON(jsonName):
    with open( jsonName, encoding='utf16' ) as JF:   #JsonFile
        json_data = json.load(JF)

        for x in json_data.keys():
            print( x )
            temp_chapter = bytes( len(json_data[x])*4 + 4 )
            offsetTable = [ pack('<L',len(temp_chapter)) ]
            for county, y in enumerate( json_data[x] ):
                for chapter, z in enumerate( json_data[x][county] ):
                    temp_chapter += bytes.fromhex( z['CharCode'] )
                    if z['Page'] == 'first':
                        temp_chapter += bytes.fromhex( '00' )
                    elif z['Page'] == 'more':
                        temp_chapter += bytes.fromhex( '01' )
                    else:
                        print( 'Error %s' % jsonName )
                        return
                    if z['NickName'] != '':
                        temp_chapter += z['NickName'].encode('utf16')[2:]+bytes(2)
                    else:
                        pass
                    for chapterText in z['Text'].split('\n'):
                        cText = chapterText.encode('utf16')[2:]
                        
                        if chapterText == z['Text'].split('\n')[-1]:
                            temp_chapter += int.to_bytes( len(cText)+128, 1, 'little')
                            temp_chapter += cText
                            
                        else:
                            temp_chapter += int.to_bytes( len(cText), 1, 'little')
                            temp_chapter += cText

                offsetTable.append( pack('<L',len(temp_chapter)) )

        bytes_offsetTable = b''
        for x in offsetTable:
            bytes_offsetTable += x

        fData = bytes_offsetTable+temp_chapter[len(bytes_offsetTable):]
        fData += bytes( 128 - len(fData)%128 )
        #'''
        #FileName = FileName.split("\\")[-1]
        newFileName = ''
        for nFN in jsonName.split("\\")[:-1]:
            newFileName+=nFN
        
        newFileName += '\\'+jsonName.split("\\")[-1].split('.')[0]+'.'+jsonName.split("\\")[-1].split('.')[1]+'.bin'
        
        with open( newFileName, 'wb') as F:
            F.write( fData )
        #'''
            
    pass

if __name__=="__main__":
    print( "Program Start" )

    '''
    fRoot = "./test/*.bin"
    for i in glob.glob( fRoot ):
        export_JSON(i) #'''

    #export_JSON('arcTacPrmDat.000178.bin') #

    #'''
    fRoot = "./new.arcTacPrmDat.bin/*.json"
    for i in glob.glob( fRoot ):
        print( i )
        import_JSON(i) #'''
        #input()

    #import_JSON('arcTacPrmDat.000177.json') #
    
    
