from abc import ABC,abstractmethod
from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('dark_background')

#['Solarize_Light2', 'bmh', 'dark_background', 
#'ggplot', 'seaborn-v0_8', 'seaborn-v0_8-bright',  
#'seaborn-v0_8-darkgrid', 'seaborn-v0_8-muted', 
#'seaborn-v0_8-whitegrid']

models=["SI","SIR","SIRS","SEIR"]

methods = ['RK45','RK23','DOP853','Radau','BDF','LSODA']
    
class Epidemiological_model(ABC):
    @abstractmethod
    def __init__(self,id:str,vars_initials:list,params_initial:list,name:str,name_var:list,params_est:list=None,N:float =1) -> None:
        self.id=id
        self.name=name
        self.name_var=name_var
        self.vars_initials=vars_initials
        self.N =N
        self.params_initial = params_initial
        self.params_est = params_est
        
    @abstractmethod
    def model(self,t:float,z:list,params:list)->list:
        return [1,1]
    
    @abstractmethod
    def numeric_solver(self,t_interval:list,params:list,method:str='RK45')->list:
            
        sol = solve_ivp(self.model, t_interval, self.vars_initials, args=[params], method=method, dense_output=True)
       
        t = [i for i in range(1,t_interval[1])]
        print(t)
        z = sol.sol(t)
        
        plt.plot(t,z.T)
        plt.xlabel('t')
        plt.legend(self.name_var, shadow=True)
        plt.title(self.name)
        plt.savefig('model.png')
        plt.close()

        return z
       
class SI(Epidemiological_model):
    def __init__(self,vars_initials:list,params_initial:list,name:str='SI',name_var:list=['S','I'],params_est:list=None,N:float =1):
        super().__init__('SI',vars_initials,params_initial,name,name_var,params_est,N)
        
    def model(self,t:float,z:list,params:list)->list:
        s,i = z
        s = s/self.N
        i = i/self.N

        params_temp = params

        if(any( item for item in self.params_est)):
            params_temp = self.params_initial.copy()
            i=0
            for index,item in enumerate(self.params_est):
                if(item):
                    params_temp[index] = params[i]
                    i+=1

        b,births,deaths,deaths_i = params_temp

        return [births*s-1*b*s*i-deaths*s,
          b*s*i-(deaths+deaths_i)*i]
        
    def numeric_solver(self,t_interval:list,params:list,method:str='RK45')->list:
        return super().numeric_solver(t_interval,params,method)
    
class SIR(Epidemiological_model):
    def __init__(self,vars_initials:list,params_initial:list,name:str='SIR',name_var:list=['S','I','R'],params_est:list=None,N:float =1):
        super().__init__("SIR",vars_initials,params_initial,name,name_var,params_est,N)
        
    def model(self,t:float,z:list,params:list)->list:
        s,i,r = z
        s = s/self.N
        i = i/self.N

        params_temp = params

        if(any(item for item in self.params_est)):
            params_temp = self.params_initial.copy()
            i=0
            for index,item in enumerate(self.params_est):
                if(item):
                    params_temp[index] = params[i]
                    i+=1
            
        b,y,births,deaths,deaths_i = params_temp

        return [births*s-1*b*s*i-deaths*s,
                   b*s*i-y*i-(deaths+deaths_i)*i,
                   y*i-deaths*r]
        
    def numeric_solver(self, t_interval: list, params: list,method:str='RK45')->list:
        return super().numeric_solver(t_interval, params,method)
           
class SIRS(Epidemiological_model):
    def __init__(self,vars_initials:list,params_initial:list,name:str='SIRS',name_var:list=['S','I','R'],params_est:list=None,N:float =1):
        super().__init__("SIRS",vars_initials,params_initial,name,name_var,params_est,N)
        
    def model(self,t:float,z:list,params:list)->list:
        s,i,r = z
        s = s/self.N
        i = i/self.N

        params_temp = params

        if(any(item for item in self.params_est)):
            params_temp = self.params_initial.copy()
            i=0
            for index,item in enumerate(self.params_est):
                if(item):
                    params_temp[index] = params[i]
                    i+=1


        b,d,y,births,deaths,deaths_i = params_temp
        

        return [births*s-1*b*s*i+d*r-deaths*s,
                   b*s*i-y*i-(deaths+deaths_i)*i,
                   y*i-d*r-deaths*r]
        
    def numeric_solver(self,t_interval:list,params:list,method:str='RK45')->list:
        return super().numeric_solver(t_interval,params,method)

        
class SEIR(Epidemiological_model):
    def __init__(self,vars_initials:list,params_initial:list,name:str='SEIR',name_var:list=['S','E','I','R'],params_est:list=None,N:float =1):
        super().__init__("SEIR",vars_initials,params_initial,name,name_var,params_est,N)
            
    def model(self,t:float,z:list,params:list)->list:
        s,e,i,r = z
        s = s/self.N
        i = i/self.N

        params_temp = params

        if(any(item for item in self.params_est)):
            params_temp = self.params_initial.copy()
            i=0
            for index,item in enumerate(self.params_est):
                if(item):
                    params_temp[index] = params[i]
                    i+=1

        b,el,y,births,deaths,deaths_i = params_temp

        return [births*s-1*b*s*i-deaths*s,
                   b*s*i-(deaths+el)*e,
                   el*e-(y+deaths+deaths_i)*i,
                   y*i-deaths*r]
        
    def numeric_solver(self,t_interval:list,params:list,method:str='RK45')->list:
        return super().numeric_solver(t_interval,params,method)
