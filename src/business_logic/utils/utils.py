import pandas as pd

def read (path,N):
    df = pd.read_excel(path,header=None)
    s,i,r,e = [],[],[],[]
    
    column_i, column_r, column_e = [0,1,2]
    for index, row in df.iterrows():
        i.append(row[column_i])
        r.append(row[column_r])
        e.append(row[column_e])

    for j in range(1,len(i)):
        s.append(N-i[j]-r[j]-e[j])

    return s,i[1:],r[1:],e[1:]


