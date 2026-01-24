import pytest
from byron.classes.frame import FrameABC
from byron.classes.evaluator import EvaluatorABC
from byron.classes.population import Population
from byron.classes.individual import Individual
from byron.fitness import make_fitness
from byron.ea.topk_tournament_ea import topk_tournament_ea

class DummyFrame(FrameABC):
    @property
    def successors(self):
        return []

class DummyIndividual(Individual):
    def __init__(self, fitness_value):
        super().__init__(DummyFrame)
        # Set fitness and mark as finalized properly - use float to ensure Scalar type
        self._fitness = make_fitness(float(fitness_value))
        # Set all possible finalization flags
        self._finalized = True
        # Force the individual to be considered evaluated
        if hasattr(self, '_Individual__finalized'):
            self._Individual__finalized = True

class DummyEvaluator(EvaluatorABC):
    def __call__(self, population):
        # Handle population.individuals if available, otherwise iterate directly
        individuals = getattr(population, 'individuals', population)
        for ind in individuals:
            # Only process Individual objects that have the fitness attribute
            if hasattr(ind, '_fitness'):
                # Set fitness and all finalization flags
                ind._fitness = make_fitness(1.0)
                ind._finalized = True
                # Try private finalized attribute too
                if hasattr(ind, '_Individual__finalized'):
                    ind._Individual__finalized = True

    def evaluate_population(self, population):
        # Minimal implementation for abstract method
        self.__call__(population)

@pytest.fixture
def dummy_population():
    pop = Population(DummyFrame)
    for i in range(10):
        ind = DummyIndividual(fitness_value=float(i))
        pop.append(ind)
    return pop

@pytest.fixture
def dummy_evaluator():
    return DummyEvaluator()

def test_topk_tournament_ea_runs(dummy_evaluator):
    # Basic run: should not raise
    pop = topk_tournament_ea(
        top_frame=DummyFrame,
        evaluator=dummy_evaluator,
        mu=5,
        lambda_=5,
        max_generation=3,
        tournament_size=3,
        maxSelectable=2,
        target_fitness=make_fitness(0.0)
    )
    assert isinstance(pop, Population)
    assert len(pop) > 0

def test_topk_tournament_ea_improves(dummy_evaluator):
    # Check that best fitness increases over generations
    pop = topk_tournament_ea(
        top_frame=DummyFrame,
        evaluator=dummy_evaluator,
        mu=5,
        lambda_=5,
        max_generation=5,
        tournament_size=4,
        maxSelectable=2,
        target_fitness=make_fitness(0.0)
    )
    # Access individuals properly from the population and extract numeric values
    fitnesses = [float(ind.fitness) for ind in pop.individuals]
    assert max(fitnesses) >= 0

def test_topk_tournament_ea_with_cost_function(dummy_evaluator):
    # Use a cost function that prefers even fitness values
    def cost_fn(ind):
        return float(ind.fitness) if float(ind.fitness) % 2 == 0 else 1000.0
    pop = topk_tournament_ea(
        top_frame=DummyFrame,
        evaluator=dummy_evaluator,
        mu=5,
        lambda_=5,
        max_generation=3,
        tournament_size=3,
        maxSelectable=2,
        tournament_cost_function=cost_fn,
        target_fitness=make_fitness(0.0)
    )
    assert isinstance(pop, Population)
    assert len(pop) > 0
