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
    def __init__(self,id:str,vars_initials:list,params_initial:list,di:bool,name:str,name_var:list,
                params_est:list=None,N:float =1) -> None:
        self.id=id
        self.name=name
        self.name_var=name_var
        self.vars_initials=vars_initials
        self.N =N
        self.params_initial = params_initial
        self.params_est = params_est
        self.di = di
        
    @abstractmethod
    def model(self,t:float,z:list,params:list)->list:
        return [1,1]
    
    @abstractmethod
    def numeric_solver(self,t_interval:list,params:list,method:str='RK45')->list:
            
        sol = solve_ivp(self.model, t_interval, self.vars_initials, args=[params], method=method, 
                        dense_output=True)
       
        t = [i for i in range(1,t_interval[1])]
        z = sol.sol(t)
        
        divide_by = self.N if self.di else 1
        fig, ax = plt.subplots()
        color = ['b','r','g','y']
        for i in range(0,len(self.name_var)):
            ax.plot(t, z[i], color[i], alpha=0.5, lw=2, label=self.name_var[i])
        ax.set_xlabel('Tiempo /días')
        ax.set_ylabel(f'Número (dividido por {divide_by:,})')
        legend = ax.legend()
        plt.savefig('model.png')
        plt.close() 

        for i in range(0,len(self.name_var)):
            fig, ax = plt.subplots()
            ax.plot(t, z[i], color[i], alpha=0.5, lw=2, label=self.name_var[i])
            ax.set_xlabel('Tiempo /días')
            ax.set_ylabel(f'Número (dividido por {divide_by:,})')
            legend = ax.legend()
            print(self.name_var[i])
            plt.savefig(self.name_var[i]+'.png')
            plt.close()

        return z
       
class SI(Epidemiological_model):
    def __init__(self,vars_initials:list,params_initial:list,di:bool,name:str='SI',name_var:list=['S','I'],
                params_est:list=None,N:float =1):
        super().__init__('SI',vars_initials,params_initial,di,name,name_var,params_est,N)
        
    def model(self,t:float,z:list,params:list)->list:
        S,I= z

        params_temp = params

        if(any( item for item in self.params_est)):
            params_temp = self.params_initial.copy()
            i=0
            for index,item in enumerate(self.params_est):
                if(item):
                    params_temp[index] = params[i]
                    i+=1

        b,births,deaths,deaths_i = params_temp

        return [births*S-1*b*S*I/self.N-deaths*S,
          b*S*I/self.N-(deaths+deaths_i)*I]
        
    def numeric_solver(self,t_interval:list,params:list,method:str='RK45')->list:
        return super().numeric_solver(t_interval,params,method)
    
class SIR(Epidemiological_model):
    def __init__(self,vars_initials:list,params_initial:list,di:bool,name:str='SIR',name_var:list=['S','I','R'],
                params_est:list=None,N:float =1):
        super().__init__("SIR",vars_initials,params_initial,di,name,name_var,params_est,N)
        
    def model(self,t:float,z:list,params:list)->list:
        S,I,R = z

        params_temp = params

        if(any(item for item in self.params_est)):
            params_temp = self.params_initial.copy()
            i=0
            for index,item in enumerate(self.params_est):
                if(item):
                    params_temp[index] = params[i]
                    i+=1
            
        b,y,births,deaths,deaths_i = params_temp

        return [births*S-1*b*S*I/self.N-deaths*S,
                   b*S*I/self.N-y*I-(deaths+deaths_i)*I,
                   y*I-deaths*R]
        
    def numeric_solver(self, t_interval: list, params: list,method:str='RK45')->list:
        return super().numeric_solver(t_interval, params,method)
           
class SIRS(Epidemiological_model):
    def __init__(self,vars_initials:list,params_initial:list,di:bool,name:str='SIRS',name_var:list=['S','I','R'],
                params_est:list=None,N:float =1):
        super().__init__("SIRS",vars_initials,params_initial,di,name,name_var,params_est,N)
        
    def model(self,t:float,z:list,params:list)->list:
        S,I,R = z

        params_temp = params

        if(any(item for item in self.params_est)):
            params_temp = self.params_initial.copy()
            i=0
            for index,item in enumerate(self.params_est):
                if(item):
                    params_temp[index] = params[i]
                    i+=1


        b,d,y,births,deaths,deaths_i = params_temp
        

        return [births*S-1*b*S*I/self.N+d*R-deaths*S,
                   b*S*I/self.N-y*I-(deaths+deaths_i)*I,
                   y*I-d*R-deaths*R]
        
    def numeric_solver(self,t_interval:list,params:list,method:str='RK45')->list:
        return super().numeric_solver(t_interval,params,method)

        
class SEIR(Epidemiological_model):
    def __init__(self,vars_initials:list,params_initial:list,di:bool,name:str='SEIR',
                name_var:list=['S','I','R','E'],params_est:list=None,N:float =1):
        super().__init__("SEIR",vars_initials,params_initial,di,name,name_var,params_est,N)
            
    def model(self,t:float,z:list,params:list)->list:
        S,I,R,E = z

        params_temp = params

        if(any(item for item in self.params_est)):
            params_temp = self.params_initial.copy()
            i=0
            for index,item in enumerate(self.params_est):
                if(item):
                    params_temp[index] = params[i]
                    i+=1

        b,el,y,births,deaths,deaths_i = params_temp
        print(b,el,y,births,deaths,deaths_i)

        return [births*S-1*b*S*I/self.N-deaths*S,
                el*E-(y+deaths+deaths_i)*I,
                y*I-deaths*R,
                b*S*I/self.N-(deaths+el)*E]
        
    def numeric_solver(self,t_interval:list,params:list,method:str='RK45')->list:
        return super().numeric_solver(t_interval,params,method)
