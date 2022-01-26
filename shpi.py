import pandas as pd
df = pd.read_csv('https://docs.google.com/spreadsheets/d/1IfGwdFNR59b0lbpRK_2MM8sx3GXdpjhZ8RmdKVVG9Ng/export?format=csv')
df = df[[i for i in df.columns[1:3]]]
dict_result = {'email': [], 'result': []}
dict_result['email'] = [i for i in df[df.columns[0]]]
dict_result['result'] = [int(i.split(' / ')[0]) for i in df[df.columns[1]]]
print(dict_result)
