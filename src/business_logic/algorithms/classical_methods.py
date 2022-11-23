from scipy.optimize import minimize
from business_logic.model import Epidemiological_model
from business_logic.objective_function import ObjectiveFunction


class ClassicalMethods:
    def __init__(self, method:str, model: Epidemiological_model, data: list, params: list, bounds:list) -> None:
        self.method = method
        self.objective_function = ObjectiveFunction(model, data)
        self.params = params
        self.bounds =bounds

    def solve(self):
        model = minimize(self.objective_function.objective_function, self.params, method=self.method, 
                        bounds=self.bounds,options={'disp': True})
        
        return model.x,model.fun
        
