# SuperRobotWar_UX
3DS SuperRobotWarUX translate tools for "ja" to "ko"

# bin_tool
split romFS files. arcBtlGrpDat.bin, arcBtlPrmDat.bin... etc

When separated into a "~.bin" file with a header called ECD, these files can be decrypted with kuriimu.

Encrypt is also possible, and you can use it(kuriimu) to decrypted this file.

# BtlMsgDat_tool.py

".out" to ".json" Or ".json" to ".new"

With this tool, you can modify the value of an item in the text. after encrypting using Kuriimu, combine the files again to create "arcBtlMsgDat.new" file. 

# TacPrmDat_tool.py

Scenario Scrpit ".bin" to ".json" or ".json" to ".bin"

If you change the value of "Text", the dialogue of the scenario will change.

Text value can be entered up to 3 lines per line. Also, if you add an additional {} value in one object, the dialogue can be expanded. In this case, you must carefully enter the values of first and more.

"first" is the first page of the line, and "more" is the page of the continuation line. Pages 3 and 4 are also "more".
