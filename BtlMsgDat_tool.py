import os
import io

import json

import math

from struct import *
import glob

def export_JSON( FileName ):
    print( '[ %s ] export JSON...' % FileName )
    with open( FileName, 'rb' ) as F:
        FileHeader = F.read(6)
        bTable00End = unpack('<h', F.read(2))[0]
        bTable01End = unpack('<h', F.read(2))[0]
        bTable02End = unpack('<h', F.read(2))[0]

        bTable00 = F.read( bTable00End - F.tell() )
        bTable01 = F.read( bTable01End - F.tell() )
        bTable02 = F.read( bTable02End - F.tell() )

        io_bText = io.BytesIO( F.read() )

        io_bTable00 = io.BytesIO( bTable00 )
        fData = []
        for x in range( int(len(bTable00)/34) ):
            temp = io_bTable00.read(34)
            fData.append( [temp[:14].hex(),temp[16:].hex(),unpack('<h', temp[14:16])[0] ] )

        jsonData = {}
        jsonData[ 'FileName' ] = FileName
        jsonData[ 'Header' ] = FileHeader.hex().upper()
        jsonData[ 'bTable01' ] = bTable01.hex().upper()
        jsonData[ 'bTable02' ] = bTable02.hex().upper()
        
        tempData = {}
        tempData[ "BtlMsgDat" ] = []        
        
        for count, x in enumerate( fData ):
            chapter = {}

            if not x == fData[-1]:
                chapter["binaryData00"] = fData[count][0]
                chapter["binaryData01"] = fData[count][1]
                text = io_bText.read(fData[count+1][2]-fData[count][2])
            else:
                chapter["binaryData00"] = fData[-1][0]
                chapter["binaryData01"] = fData[-1][1]
                text = io_bText.read()

            if text.find(b'\xfb\xff') == -1 and text.find(b'\xfc\xff') == -1 and text.find(b'\xfe\xff') == -1:
                chapterText = {}
                chapterText['ⓞ'+text[:6].hex()] = text[6:-2].decode('utf16')
                chapter["Text"] = chapterText
                chapter["Text_Info"] = 1
                
            else:
                io_text = io.BytesIO( text )
                temp_All = ''
                noneTrig  = True
                newLine = False
                while True:
                    temp = io_text.read(2)
                    if temp.hex() == 'ffff':
                        chapterText = {}
                        for countz, z in enumerate( temp_All.split('\n') ):                            
                            chapterText[z.split('\t')[0]] = z.split('\t')[1]
                        chapter["Text"] = chapterText
                        chapter["Text_Info"] = len(temp_All.split('\n'))
                        
                        temp_All = ''
                        noneTrig  = True
                        newLine = False
                        break
                    else:
                        if temp.hex() == 'fbff':
                            if newLine:
                                temp_All+='\n'
                                newLine = False
                            temp_All +='ⓑ'+io_text.read(6).hex()+'\t'
                            noneTrig = False
                            newLine = True
                        elif temp.hex() == 'fcff':
                            if newLine:
                                temp_All+='\n'
                                newLine = False
                            temp_All +='ⓒ'+io_text.read(6).hex()+'\t'
                            noneTrig = False
                            newLine = True
                        elif temp.hex() == 'feff':
                            if newLine:
                                temp_All+='\n'
                                newLine = False
                            temp_All +='ⓔ'+io_text.read(6).hex()+'\t'
                            noneTrig = False
                            newLine = True
                        elif temp.hex() == 'fdff':
                            temp_All +='ⓝ'
                            
                        else:
                            if noneTrig:
                                if newLine:
                                    temp_All+='\n'
                                    newLine = False
                                temp_All +='ⓞ'+temp.hex()+io_text.read(4).hex()+'\t'
                                noneTrig = False
                                newLine = True
                            else:
                                temp_All +=temp.decode('utf16')
    
            tempData[ "BtlMsgDat" ].append( chapter )

        jsonData[ 'BtlMsgDat' ] = tempData[ "BtlMsgDat" ]
            
    with open( FileName.split('.')[1]+'.json', 'w', encoding='utf16' ) as F:
        json.dump(jsonData, F, ensure_ascii=False, indent=4)
    pass

def import_JSON(jsonName):

    with open( jsonName, encoding='utf16' ) as JF:   #JsonFile
        json_data = json.load(JF)

        fData = bytes.fromhex( json_data['Header'] )+bytes(6)

        bTableData = b''
        bTextData = b''
        
        for x in json_data[ 'BtlMsgDat' ]:
            bTableData += bytes.fromhex( x['binaryData00'] )
            bTableData += pack('<h', len(bTextData) )
            bTableData += bytes.fromhex( x['binaryData01'] )
             
            for textData in x['Text']:
                if textData[:1] == 'ⓞ':
                    bTextData += bytes.fromhex( textData[1:] )
                elif textData[:1] == 'ⓑ':
                    bTextData += bytes.fromhex('fbff')+bytes.fromhex( textData[1:] )
                elif textData[:1] == 'ⓒ':
                    bTextData += bytes.fromhex('fcff')+bytes.fromhex( textData[1:] )
                elif textData[:1] == 'ⓔ':
                    bTextData += bytes.fromhex('feff')+bytes.fromhex( textData[1:] )

                bTextData += x['Text'][textData].encode('utf16')[2:].replace(b'\xdd\x24',b'\xfd\xff')

            bTextData += b'\xff\xff'

        fData+=bTableData
        tableOffset00 = pack('<h', len(fData))
        fData += bytes.fromhex( json_data['bTable01'] )
        tableOffset01 = pack('<h', len(fData))
        fData += bytes.fromhex( json_data['bTable02'] )
        tableOffset02 = pack('<h', len(fData))

        fData = fData[:6]+tableOffset00+tableOffset01+tableOffset02+fData[12:]
        fData += bTextData

        with open( jsonName.split(".")[0]+'.new', 'wb') as F:
            F.write( fData )
            
    pass

if __name__=="__main__":
    print( "Program Start" )

    #export_JSON('arcBtlMsgDat.000003.bin.out') #decrypt file. used Kuriimu
    import_JSON('000003.json') #Make new BtlMsgDat file.
    
    
