from business_logic.model import *

dict = {
    'SI': SI,
    'SIR': SIR,
    'SIRS': SIRS,
    'SEIR': SEIR
}


class SolveEpidemiologicalModelsService:
    def __init__(self,name_model,vars_initials,params,params_est,t,method,N) -> None:
        self.name_model = name_model
        self.vars_initials = vars_initials
        self.params = params
        self.params_est = params_est
        self.t = t
        self.method = method
        self.N = N

    def solve_model(self):
        model = dict[self.name_model](self.vars_initials,self.params,params_est=self.params_est,N=self.N)
        sol = model.numeric_solver([0,self.t],self.params,self.method)

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

        return sol_new