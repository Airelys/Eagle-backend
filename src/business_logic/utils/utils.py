import pandas as pd

def read (path,N,name):
    df = pd.read_excel(path,header=None)
    s,i,r,e = [],[],[],[]
    
    column_i, column_r, column_e = [0,1,2]
    for index, row in df.iterrows():
        i.append(row[column_i])
        r.append(row[column_r])
        e.append(row[column_e])

    if(name=='SI'):
        s.append(N-i[1])
        z= i[1]
        for j in range(2,len(i)):
            s.append(N-z-i[j])
            z += i[j]

    elif(name=='SIR'or name=='SIRS'):
        s.append(N-i[1]-r[1])
        z= i[1]+r[1]
        for j in range(2,len(i)):
            s.append(N-z-i[j]-r[j])
            z += i[j]+r[j]

    elif(name=='SEIR'):
        s.append(N-i[1]-r[1]-e[1])
        z= i[1]+r[1]+e[1]
        for j in range(2,len(i)):
            s.append(N-z-i[j]-r[j]-e[j])
            z += i[j]+r[j]+e[j]

    return s,i[1:],r[1:],e[1:]


