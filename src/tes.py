from business_logic.model import *
from business_logic.utils.utils import *
from business_logic.algorithms.metaheuristics import *

N=10000
I0 =3
R0 = 0
E0 = 10

a =SIR([N-I0,I0,R0],[0.2,0.01,0,0,0],N,params_est=[True,True,False,False,False])

met = PSO(a,read('C:\\Users\\Airelys\\Desktop\\n.xlsx',N,'SIR'),[[0,0],[1,1]],'RK23',5)

b = met.solve()

print(b)