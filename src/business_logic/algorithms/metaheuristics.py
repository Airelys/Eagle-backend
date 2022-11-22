from abc import ABC,abstractmethod
import pyswarms as ps
from business_logic.model import Epidemiological_model
from business_logic.objective_function import ObjectiveFunction
from scipy.optimize import differential_evolution

class Metaheuristics(ABC):
    @abstractmethod
    def __init__(self, model: Epidemiological_model, data: list,bounds:list,
                 iter_max:float=5):
        self.objective_function = ObjectiveFunction(model, data)
        self.iter_max = iter_max
        self.bounds = bounds

    @abstractmethod
    def solve(self):
        return []

class PSO(Metaheuristics):
    def __init__(self, model: Epidemiological_model, data: list,
                 bounds:list=None, iter_max:float=10, particle:float=5, cognitive_param:float=0.5, 
                 social_param:float=0.3, inercia_param:float=0.9) -> None:
        super().__init__(model,data,bounds,iter_max)

        self.particle = particle
        self.dimension = len(bounds[0])
        self.dict_params = {'c1':cognitive_param, 'c2':social_param, 'w': inercia_param}


    def solve(self):
        optimizer = ps.single.GlobalBestPSO(n_particles=self.particle,dimensions=self.dimension,options=self.dict_params, bounds=self.bounds)
        best_cost, best_pos = optimizer.optimize(self.objective_function.objective_function_pso,iters=self.iter_max)
        return best_pos


class DifferentialEvolution(Metaheuristics):
    def __init__(self, model: Epidemiological_model, data: list,
                 bounds:list, iter_max:float=10, population:float=5, crossing_factor:float=0.8, 
                 scaled_factor:float=0.6) -> None:
        super().__init__(model,data,bounds,iter_max)

        self.population = population
        self.crossing_factor = crossing_factor
        self.scaled_factor = scaled_factor

    def solve(self):
        sol = differential_evolution(self.objective_function.objective_function,bounds=self.bounds,
                                    mutation=self.scaled_factor,recombination=self.crossing_factor, 
                                    popsize=self.population)
        return sol.x

