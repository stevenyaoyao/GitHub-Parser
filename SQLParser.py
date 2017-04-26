# -*- coding: utf-8 -*-
"""
@author: StevenYAO
"""

fhand = open('SQLString.txt')
#fhand = open('Debug.txt')
fout = open('Result.txt', 'w')

startKeyWordString = [' SELECT ', ' Select ', ' select ',
                      ' INSERT INTO ', ' Insert Into ',
                      ' UPDATE ', ' Update ',
                      ' DELETE FROM ', ' Delete From ']

keywordString = [' FROM ', ' From ', ' from ', 'INNER JOIN ', ' LEFT JOIN ', ' RIGHT JOIN ', ' FULL JOIN ', ' LEFT OUTER JOIN ', ' RIGHT OUTER JOIN ',
                 ' INSERT INTO ', ' Insert Into ',
                 ' UPDATE ', ' Update ']

fromKeywordsString =  [' FROM ', ' From ', ' from ']
emptyAfterFromString = ['WHERE', 'Where', 'where']
#nonDuplicationKeyworkString =  [' INSERT INTO ', ' Insert Into ',
#                                ' UPDATE ', ' Update ']

count = 0
totalCount = 0;
firstLine = True;
for line in fhand:
    totalCount = totalCount + 1
    isSQL = False
    
    adjustedLine = line.lstrip()
    adjustedLine = ' ' + adjustedLine
    
    for startKey in startKeyWordString:
        if adjustedLine.startswith(startKey):
            isSQL = True
            break
    if isSQL:
        count = count + 1
        stringToWrite = '';
        for key in keywordString:
            a = adjustedLine.split(key)
            #print ("Start: ", a)
            #print ('Key: ', key)
            #print (len(a))
            for i in range (1, len(a)):
                #print ('a[i]: ', a[i])
                
                b = a[i].lstrip().split(' ')
                #print ('b[0]: ', b[0])
                
                c = b[0];
                
                if (c.startswith('(')): # for select/inner join from a select
                    continue
                if (c.startswith('<')): # for insert into missing table
                    continue
                if ('(' in c):
                    d = c.split('(') # for insert into tableName(column name, )
                    c = d[0]
                    
                    c = c.rstrip('\n')
                    stringToWrite = stringToWrite + c
                    stringToWrite = stringToWrite + ','
                else:
                    j = 0
                    while True: # for multiple tables after from
                        c = b[j]
                        #print ('j =', j, ' c: ', c)
                        if (c.endswith(',')):
                            c = c[:-1]
                        
                            stringToWrite = stringToWrite + c
                            if (stringToWrite.endswith(';')):
                                stringToWrite = stringToWrite[:-1]
                            stringToWrite = stringToWrite + ','
                            
                            j = j + 1
                            
                            if key in fromKeywordsString:
                                continue
                            else:
                                break;
                        else:
                            c = c.rstrip('\n')
                            stringToWrite = stringToWrite + c
                            if (stringToWrite.endswith(';')):
                                stringToWrite = stringToWrite[:-1]
                            stringToWrite = stringToWrite + ','
                            
                            j = j + 1
                            if j >= len(b):
                                break
                            
                            c = b[j]
                            if (c.endswith(',')):
                                 j = j + 1
                            else:
                                break
                            
                            if key in fromKeywordsString:
                                continue
                            else:
                                break
                
                #if key in nonDuplicationKeyworkString:
                #    break
                #if (i == len(a) - 1):
                    #lastString = b[1]
        #if ("\n" not in lastString):
        #Remove last comma
        stringToWrite = stringToWrite[:-1]
        #stringToWrite2= stringToWrite.replace('#', '')
        
        if (stringToWrite.endswith(';')):
            stringToWrite = stringToWrite[:-1]
        
        if (stringToWrite.endswith('.\\')):
            stringToWrite = stringToWrite[:-2]
        
        stringToWrite = stringToWrite.replace(';', ',')
        
        if stringToWrite not in emptyAfterFromString:
            fout.write(stringToWrite)
        fout.write('\n')
    else:
        if (firstLine):
            fout.write('Tables_Contained_In_SQL')
            firstLine = False
        fout.write('\n')
print ('Total Line Count: ', totalCount)
print ('Line Count: ', count)