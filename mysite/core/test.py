import os
import pandas as pd

for file in os.listdir('media/'):
    if file.endswith(".xlsx"):
        cols = pd.read_excel('media/'+file).columns
        avro_str = '''
{
  "type": "record",
  "name": "avro_schemma",
  "fields":
  [ 
'''
        i = 0
        length = len(cols)
        for s in cols:
            for ch in ['\\','/','*','-','.',',','(',')']:
                s = s.replace(ch,'')
            s = s.replace(r' ','_')
            i+=1
            if i < length:
                avro_str = avro_str + '    { "name": "' + s + '", "type": ["null","string"]},' + '\n'
            else:
                avro_str = avro_str + '    { "name": "' + s + '", "type": ["null","string"]}' + '\n'
        avro_str = avro_str + ''' ]
}'''
        print(avro_str)