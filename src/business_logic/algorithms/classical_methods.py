from scipy.optimize import minimize
from business_logic.model import Epidemiological_model
from business_logic.objective_function import ObjectiveFunction

'Newton-CG' , 'CG' , 'BFGS' , 'L-BFGS-B' 

class ClassicalMethods:
    def __init__(self, method:str, model: Epidemiological_model, data: list, params: list) -> None:
        self.method = method
        self.objective_function = ObjectiveFunction(model, data)
        self.params = params

    def solve(self):
        model = minimize(self.objective_function.objective_function, self.params, method=self.method, options={'disp': True})
        return model.x
        
