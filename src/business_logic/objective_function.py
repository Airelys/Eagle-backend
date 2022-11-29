import numpy as np
from business_logic.model import Epidemiological_model

class ObjectiveFunction:
    
    def __init__(self, model: Epidemiological_model, data: list, method:str) -> None:
        self.model = model
        self.data = data
        self.method = method
 
    def objective_function(self, params:list):
        numeric_solve = self.model.numeric_solver( [0,len(self.data[0])], params,self.method)
        vector_numeric_solve = []
        vector_data = []

        for i in range(len(numeric_solve[0])):
            temp = []
            for j in range(len(numeric_solve)):
                temp.append(numeric_solve[j][i])
            vector_numeric_solve.append(temp)
        for i in range(len(self.data[0])):
            temp = []
            for j in range(len(numeric_solve)):
                temp.append(self.data[j][i])
            vector_data.append(temp)

        sum = 0
        for i in range(min(len(vector_data),len(vector_numeric_solve))):
            yi = np.array(vector_numeric_solve[i])
            yie = np.array(vector_data[i])
            transpose = np.transpose(yi - yie)
            no_transpose = yi-yie
            sum += (transpose@no_transpose)

        funct = sum/2
        return funct

    def objective_function_pso(self, params:list):
        sol = []
        for item in params:
            funct = self.objective_function(item)
            sol.append(funct)
        return sol