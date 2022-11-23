from business_logic.model import *
from business_logic.algorithms.classical_methods import *
from business_logic.algorithms.metaheuristics import *
from business_logic.utils.utils import *
import base64
import os

dict = {
    'SI': SI,
    'SIR': SIR,
    'SIRS': SIRS,
    'SEIR': SEIR
}


class ParameterEstimationService:
    def __init__(self,model_name,vars_initials,params,params_est,t,method,N,
                 params_min,params_max,classical_method,metaheuristic,iter,particle,cognitive,
                 social,inercia,population,crossing,scaled,di) -> None:
        self.model_name = model_name
        self.params_initials = params
        self.params = []
        for i,item in enumerate(params_est):
            if(item):
                self.params.append(params[i])
        self.params_est = params_est
        self.t = t
        self.method = method
        self.N = N
        self.params_min = params_min
        self.params_max = params_max
        self.classical_method = classical_method
        self.metaheuristic = metaheuristic
        self.iter = iter
        self.particle = particle
        self.cognitive = cognitive
        self.social = social
        self.inercia = inercia
        self.population = population
        self.crossing = crossing
        self.scaled = scaled
        self.di = di
        S = N
        for i in vars_initials:
            S -= i
        self.vars_initials = [S] + vars_initials

    def solve_model(self):
        min = []
        max = []
        min_max =[]
        for index,item in enumerate(self.params_est):
            if(item):
                min.append(self.params_min[index])
                max.append(self.params_max[index])
                min_max.append((self.params_min[index],self.params_max[index]))
        print(min)
        print(max)
        print('Soy min max')
        print(min_max)

        data = read('data.xlsx',self.N,self.model_name)

        model = dict[self.model_name](self.vars_initials,self.params_initials,self.di,params_est=self.params_est,
                                      N=self.N)
        opt = []
        print(self.metaheuristic)
        if(self.classical_method!='None'and self.metaheuristic!='None'):
            sol_met = []
            if (self.metaheuristic=='PSO'):
                metaheuristic = PSO(model,data,[min,max],self.iter,self.particle,
                                self.cognitive,self.social,self.inercia)
                sol_met,fun = metaheuristic.solve()
            else:
                metaheuristic = DifferentialEvolution(model,data,min_max,
                                                  self.iter,self.population,self.crossing,self.scaled)
                sol_met,fun = metaheuristic.solve()

            classical = ClassicalMethods(self.classical_method,model,data,sol_met,min_max)
            opt,fun = classical.solve()

        elif(self.classical_method!='None'):
            classical = ClassicalMethods(self.classical_method,model,data,self.params,min_max)
            opt,fun = classical.solve()

        else:
            if (self.metaheuristic=='PSO'):
                metaheuristic = PSO(model,data,[min,max],self.iter,self.particle,
                                self.cognitive,self.social,self.inercia)
                opt,fun = metaheuristic.solve()
            else:
                metaheuristic = DifferentialEvolution(model,data,min_max,
                                                  self.iter,self.population,self.crossing,self.scaled)
                opt,fun = metaheuristic.solve()
                
        sol = model.numeric_solver([0,self.t],opt,self.method)
        model.plot(sol,data,[0,self.t])

        sol_new =[]
        sol_init =[1]
        for i in self.vars_initials:
            sol_init.append(i)
        sol_new.append(sol_init)
    
        for index,item in enumerate(sol[0]):
            temp = [index+2]
            for element in sol:
                temp.append(element[index])
            sol_new.append(temp)

        opt_new = []
        i=0
        for index,item in enumerate(self.params_est):
            if(item):
                opt_new.append(opt[i])
                i+=1
            else:
                opt_new.append(0)

        print(opt_new)
        imgs = []

        with open("model.png", "rb") as img_file:
            b64_model = base64.b64encode(img_file.read())
            imgs.append(str(b64_model)[2:-1])
        
        os.remove("model.png")
        os.remove("data.xlsx")

        self.model_name = self.model_name[:-1] if self.model_name=='SIRS'else self.model_name
        for i in self.model_name:
            with open(str(i)+'.png', "rb") as img_file:
                b64_model = base64.b64encode(img_file.read())
                imgs.append(str(b64_model)[2:-1])
            
            os.remove(str(i)+'.png')

        return opt_new,sol_new,imgs,fun