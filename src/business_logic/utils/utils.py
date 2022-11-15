import pandas as pd

def read (path):
    df = pd.read_excel(path,header=None)
    s,i,r,e = [],[],[],[]
    
    column_s, column_i, column_r, column_e = [0,1,2,3]
    for index, row in df.iterrows():
        s.append(row[column_s])
        i.append(row[column_i])
        r.append(row[column_r])
        e.append(row[column_e])

    return s[1:],i[1:],r[1:],e[1:]


