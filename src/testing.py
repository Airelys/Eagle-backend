from business_logic.model import *
from math import *
from business_logic.utils.utils import *
from business_logic.algorithms.classical_methods import *
from business_logic.algorithms.metaheuristics import *



temp = {'SIR':SIR}

si=temp['SIR']([1000,1,0],[0.5,0.3,0,0,0],params_est=[1])

sol = ClassicalMethods('CG',si,read('backend/src/business_logic/Cuba_Datos_CoVid19_2022.xlsx','Hoja1',[2,3,8]),1000,[1])
a = sol.solve()
si.print_numeric_solve([0,50],a,1000)
print(a)

sol2 = PSO(si,read('backend/src/business_logic/Cuba_Datos_CoVid19_2022.xlsx','Hoja1',[2,3,8]),1000)
a2 = sol2.solve()
si.print_numeric_solve([0,50],a2,1000)
print(a2)

'''
sol3 = DifferentialEvolution(si,read2('backend/src/business_logic/Cuba_Datos_CoVid19_2022.xlsx','Hoja1',[2,3,8]),1000,[[-1,5]])
a3 = sol3.solve()
si.print_numeric_solve([0,50],a3,1000)
print(a3)'''



