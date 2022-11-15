from business_logic.model import *
from business_logic.algorithms.classical_methods import *
from business_logic.algorithms.metaheuristics import *
from business_logic.utils.utils import *

dict = {
    'SI': SI,
    'SIR': SIR,
    'SIRS': SIRS,
    'SEIR': SEIR
}


class ParameterEstimationService:
    def __init__(self,model_name,vars_initials,params,params_est,t,total_points,method,N,
                 params_min,params_max,classical_method,metaheuristic,path,iter,particle,cognitive,
                 social,inercia,population,crossing,scaled) -> None:
        self.model_name = model_name
        self.vars_initials = vars_initials
        self.params_initials = params
        self.params = []
        for i,item in enumerate(params_est):
            if(item):
                self.params.append(params[i])
        print(self.params)
        self.params_est = params_est
        self.t = t
        self.total_points = total_points
        self.method = method
        self.N = N
        self.params_min = params_min
        self.params_max = params_max
        self.classical_method = classical_method
        self.metaheuristic = metaheuristic
        self.path = path
        self.iter = iter
        self.particle = particle
        self.cognitive = cognitive
        self.social = social
        self.inercia = inercia
        self.population = population
        self.crossing = crossing
        self.scaled = scaled

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

        model = dict[self.model_name](self.vars_initials,self.params_initials,params_est=self.params_est,N=self.N)
        opt = []
        print(self.metaheuristic)
        if(self.classical_method!='None'and self.metaheuristic!='None'):
            sol_met = []
            if (self.metaheuristic=='PSO'):
                metaheuristic = PSO(model,read(self.path),self.total_points,[min,max],self.iter,self.particle,
                                self.cognitive,self.social,self.inercia)
                sol_met = metaheuristic.solve()
            else:
                metaheuristic = DifferentialEvolution(model,read(self.path),self.total_points,min_max,
                                                  self.iter,self.population,self.crossing,self.scaled)
                sol_met = metaheuristic.solve()

            classical = ClassicalMethods(self.classical_method,model,read(self.path),self.total_points,sol_met)
            opt = classical.solve()

        elif(self.classical_method!='None'):
            classical = ClassicalMethods(self.classical_method,model,read(self.path),self.total_points,self.params)
            opt = classical.solve()

        else:
            if (self.metaheuristic=='PSO'):
                metaheuristic = PSO(model,read(self.path),self.total_points,[min,max],self.iter,self.particle,
                                self.cognitive,self.social,self.inercia)
                opt = metaheuristic.solve()
            else:
                metaheuristic = DifferentialEvolution(model,read(self.path),self.total_points,min_max,
                                                  self.iter,self.population,self.crossing,self.scaled)
                opt = metaheuristic.solve()
                
        sol = model.numeric_solver([0,self.t],opt,self.total_points,self.method)

        sol_new =[]

        for index,item in enumerate(sol[0]):
            temp = []
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

        return opt_new,sol_new