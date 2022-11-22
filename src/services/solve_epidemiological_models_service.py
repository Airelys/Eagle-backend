from business_logic.model import *
import base64
import os

dict = {
    'SI': SI,
    'SIR': SIR,
    'SIRS': SIRS,
    'SEIR': SEIR
}


class SolveEpidemiologicalModelsService:
    def __init__(self,name_model,vars_initials,params,params_est,t,method,N,di) -> None:
        self.name_model = name_model
        self.params = params
        self.params_est = params_est
        self.t = t
        self.method = method
        self.N = N
        self.di = di
        S = N
        for i in vars_initials:
            S -= i
        self.vars_initials = [S] + vars_initials

    def solve_model(self):
        model = dict[self.name_model](self.vars_initials,self.params,self.di,params_est=self.params_est,N=self.N)
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

        imgs = []

        with open("model.png", "rb") as img_file:
            b64_model = base64.b64encode(img_file.read())
            imgs.append(str(b64_model)[2:-1])
        
        os.remove("model.png")

        self.name_model = self.name_model[:-1] if self.name_model=='SIRS'else self.name_model
        for i in self.name_model:
            with open(str(i)+'.png', "rb") as img_file:
                b64_model = base64.b64encode(img_file.read())
                imgs.append(str(b64_model)[2:-1])
            os.remove(str(i)+'.png')


        return sol_new,imgs