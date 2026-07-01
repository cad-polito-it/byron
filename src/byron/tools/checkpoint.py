###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################

# Copyright 2023 Giovanni Squillero and Alberto Tonda
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.

# =[ HISTORY ]===============================================================
# v1 / November 2025 / Checkpoint utilities for population persistence

__all__ = ['save_population', 'load_population', 'save_individuals', 'load_individuals']

import pickle
from pathlib import Path
from typing import Optional

from byron.classes.population import Population
from byron.classes.individual import Individual
from byron.user_messages import logger as byron_logger

# Try to use dill for better serialization of complex objects (like closures)
# If not available, fall back to standard pickle
try:
    import dill
    _pickle_module = dill
    byron_logger.debug("Checkpoint: Using dill for enhanced serialization")
except ImportError:
    _pickle_module = pickle
    byron_logger.debug("Checkpoint: Using standard pickle (install dill for better support)")


def save_population(population: Population, filepath: str | Path) -> None:
    """Save an entire population to disk using pickle.
    
    This function serializes the complete Population object including:
    - All individuals with their genomes (NetworkX graphs)
    - Fitness values for each individual
    - Generation counter
    - Population metadata and extra parameters
    - Operator configurations
    
    Parameters
    ----------
    population : Population
        The population to save
    filepath : str | Path
        Path where the population will be saved (typically with .pkl extension)
        
    Examples
    --------
    >>> population = byron.ea.simple_ea(top_frame, evaluator, max_generation=100)
    >>> byron.tools.save_population(population, 'checkpoint_gen100.pkl')
    
    Notes
    -----
    The saved file can be loaded with `load_population()` to resume evolution.
    Pickle files are Python-version dependent; use the same Python version to load.
    """
    filepath = Path(filepath)
    
    try:
        # Create parent directories if they don't exist
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            _pickle_module.dump(population, f, protocol=pickle.HIGHEST_PROTOCOL)
            
        byron_logger.info(
            f"Checkpoint: Saved population (gen {population.generation}, "
            f"{len(population)} individuals) to {filepath}"
        )
    except Exception as e:
        byron_logger.error(f"Checkpoint: Failed to save population to {filepath}: {e}")
        raise


def load_population(filepath: str | Path) -> tuple[Population, int]:
    """Load a population from a pickle file.
    
    This function deserializes a Population object that was previously saved
    with `save_population()`. The loaded population can be used to:
    - Resume evolution from a checkpoint
    - Analyze evolved populations
    - Extract best individuals
    - Continue experiments
    
    Parameters
    ----------
    filepath : str | Path
        Path to the pickle file containing the saved population
        
    Returns
    -------
    tuple[Population, int]
        A tuple containing:
        - population: The reconstructed population object with all individuals and metadata
        - generation: The generation number at which the checkpoint was saved
        
    Examples
    --------
    >>> # Resume evolution from checkpoint
    >>> population, generation = byron.tools.load_population('checkpoint_gen100.pkl')
    >>> print(f"Loaded generation {generation}")
    >>> print(f"Best fitness: {population[0].fitness}")
    >>> 
    >>> # Continue evolution with simple_ea
    >>> population = byron.ea.simple_ea(
    ...     top_frame, evaluator,
    ...     population=population,
    ...     max_generation=200
    ... )
    
    Notes
    -----
    The loaded population retains all state, but you'll need to:
    1. Re-create the evaluator (functions can't always be pickled)
    2. Re-create the top_frame definition
    3. Pass the population to simple_ea() or topk_tournament_ea() to resume evolution
    
    Warnings
    --------
    Only load pickle files from trusted sources - pickle can execute arbitrary code.
    """
    filepath = Path(filepath)
    
    try:
        with open(filepath, 'rb') as f:
            population = _pickle_module.load(f)
            
        if not isinstance(population, Population):
            raise TypeError(f"Loaded object is not a Population, got {type(population)}")
        
        generation = population.generation
            
        byron_logger.info(
            f"Checkpoint: Loaded population (gen {generation}, "
            f"{len(population)} individuals) from {filepath}"
        )
        return population, generation
    except Exception as e:
        byron_logger.error(f"Checkpoint: Failed to load population from {filepath}: {e}")
        raise


def save_individuals(
    population: Population,
    filepath: str | Path,
    indices: Optional[list[int]] = None,
    top_n: Optional[int] = None
) -> None:
    """Save specific individuals from a population to disk.
    
    This function allows selective saving of individuals, useful for:
    - Saving only the best individuals
    - Creating a hall of fame
    - Reducing checkpoint size
    - Exporting solutions
    
    Parameters
    ----------
    population : Population
        The population containing the individuals
    filepath : str | Path
        Path where individuals will be saved (typically with .pkl extension)
    indices : list[int], optional
        Specific indices of individuals to save. If None, uses top_n or all
    top_n : int, optional
        Save only the top N fittest individuals. Ignored if indices is provided
        
    Examples
    --------
    >>> # Save top 10 individuals
    >>> byron.tools.save_individuals(population, 'top10.pkl', top_n=10)
    >>> 
    >>> # Save specific individuals
    >>> byron.tools.save_individuals(population, 'selected.pkl', indices=[0, 5, 10])
    >>> 
    >>> # Save all individuals
    >>> byron.tools.save_individuals(population, 'all_individuals.pkl')
    
    Notes
    -----
    Each saved individual includes:
    - Genome (NetworkX MultiDiGraph)
    - Fitness value
    - Age information
    - Lineage data
    - Individual ID
    """
    filepath = Path(filepath)
    
    try:
        # Determine which individuals to save
        if indices is not None:
            individuals_to_save = [population[i] for i in indices]
        elif top_n is not None:
            individuals_to_save = population.individuals[:top_n]
        else:
            individuals_to_save = population.individuals
        
        # Create data structure with metadata
        checkpoint_data = {
            'individuals': individuals_to_save,
            'generation': population.generation,
            'top_frame': population.top_frame,
            'population_extra_parameters': population.population_extra_parameters,
            'num_saved': len(individuals_to_save),
            'total_population_size': len(population)
        }
        
        # Create parent directories if they don't exist
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            _pickle_module.dump(checkpoint_data, f, protocol=pickle.HIGHEST_PROTOCOL)
            
        byron_logger.info(
            f"Checkpoint: Saved {len(individuals_to_save)} individuals "
            f"from generation {population.generation} to {filepath}"
        )
    except Exception as e:
        byron_logger.error(f"Checkpoint: Failed to save individuals to {filepath}: {e}")
        raise


def load_individuals(filepath: str | Path) -> dict:
    """Load individuals from a checkpoint file.
    
    This function loads individuals that were saved with `save_individuals()`.
    Returns a dictionary containing the individuals and metadata.
    
    Parameters
    ----------
    filepath : str | Path
        Path to the pickle file containing saved individuals
        
    Returns
    -------
    dict
        Dictionary containing:
        - 'individuals': list of Individual objects
        - 'generation': generation number when saved
        - 'top_frame': the top frame used
        - 'population_extra_parameters': population parameters
        - 'num_saved': number of saved individuals
        - 'total_population_size': original population size
        
    Examples
    --------
    >>> # Load previously saved individuals
    >>> data = byron.tools.load_individuals('top10.pkl')
    >>> print(f"Loaded {data['num_saved']} individuals from gen {data['generation']}")
    >>> 
    >>> # Access the best individual
    >>> best = data['individuals'][0]
    >>> print(f"Best fitness: {best.fitness}")
    >>> 
    >>> # Create a new population with loaded individuals
    >>> new_pop = Population(data['top_frame'], extra_parameters=data['population_extra_parameters'])
    >>> new_pop += data['individuals']
    
    Notes
    -----
    To use loaded individuals in a new evolution run, you'll need to:
    1. Re-create the appropriate Population object
    2. Add individuals using the += operator
    3. Set the generation counter appropriately
    """
    filepath = Path(filepath)
    
    try:
        with open(filepath, 'rb') as f:
            data = _pickle_module.load(f)
            
        if not isinstance(data, dict) or 'individuals' not in data:
            raise ValueError(f"Invalid checkpoint format in {filepath}")
            
        byron_logger.info(
            f"Checkpoint: Loaded {data['num_saved']} individuals "
            f"(from generation {data['generation']}) from {filepath}"
        )
        return data
    except Exception as e:
        byron_logger.error(f"Checkpoint: Failed to load individuals from {filepath}: {e}")
        raise
