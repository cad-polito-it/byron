###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-25 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

"""Comprehensive tests for checkpoint functionality"""

import pytest
import tempfile
from pathlib import Path
import byron
from byron.tools.checkpoint import save_population, load_population, save_individuals, load_individuals


@pytest.fixture
def simple_problem():
    """Create a simple OneMax problem for testing"""
    @byron.fitness_function
    def fitness(phenotype: str) -> int:
        return phenotype.count('1')
    
    macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', 20))
    top_frame = byron.f.sequence([macro])
    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)
    
    return top_frame, evaluator, fitness


@pytest.fixture
def sample_population(simple_problem):
    """Create a sample population for testing"""
    top_frame, evaluator, fitness = simple_problem
    
    population = byron.ea.simple_ea(
        top_frame,
        evaluator,
        mu=10,
        lambda_=20,
        max_generation=5,
        target_fitness=byron.fitness.make_fitness(20)
    )
    
    return population


@pytest.fixture
def temp_checkpoint_file():
    """Create a temporary file for checkpoint testing"""
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pkl') as f:
        temp_path = Path(f.name)
    
    yield temp_path
    
    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


class TestSaveLoadPopulation:
    """Tests for save_population and load_population functions"""
    
    def test_save_and_load_population(self, sample_population, temp_checkpoint_file):
        """Test basic save and load of population"""
        # Save
        save_population(sample_population, temp_checkpoint_file)
        
        # Verify file exists
        assert temp_checkpoint_file.exists()
        assert temp_checkpoint_file.stat().st_size > 0
        
        # Load
        loaded_pop = load_population(temp_checkpoint_file)
        
        # Verify attributes
        assert loaded_pop.generation == sample_population.generation
        assert len(loaded_pop) == len(sample_population)
        assert loaded_pop[0].fitness == sample_population[0].fitness
    
    def test_loaded_population_has_correct_individuals(self, sample_population, temp_checkpoint_file):
        """Test that all individuals are preserved correctly"""
        save_population(sample_population, temp_checkpoint_file)
        loaded_pop = load_population(temp_checkpoint_file)
        
        # Check all individuals
        for i in range(len(sample_population)):
            assert loaded_pop[i].fitness == sample_population[i].fitness
            assert loaded_pop[i].id == sample_population[i].id
    
    def test_loaded_population_preserves_metadata(self, sample_population, temp_checkpoint_file):
        """Test that population metadata is preserved"""
        save_population(sample_population, temp_checkpoint_file)
        loaded_pop = load_population(temp_checkpoint_file)
        
        assert loaded_pop.generation == sample_population.generation
        assert abs(loaded_pop.entropy - sample_population.entropy) < 0.001
        assert loaded_pop.population_extra_parameters == sample_population.population_extra_parameters
    
    def test_save_overwrites_existing_file(self, sample_population, temp_checkpoint_file):
        """Test that saving overwrites existing checkpoint"""
        # Save first population
        save_population(sample_population, temp_checkpoint_file)
        first_size = temp_checkpoint_file.stat().st_size
        
        # Save again (should overwrite)
        save_population(sample_population, temp_checkpoint_file)
        second_size = temp_checkpoint_file.stat().st_size
        
        # File should still exist and be roughly same size
        assert temp_checkpoint_file.exists()
        assert abs(first_size - second_size) < 1000  # Allow small variance
    
    def test_load_nonexistent_file_raises_error(self):
        """Test that loading non-existent file raises appropriate error"""
        with pytest.raises(FileNotFoundError):
            load_population(Path('/nonexistent/checkpoint.pkl'))
    
    def test_save_to_nested_directory(self, sample_population):
        """Test saving checkpoint in nested directory structure"""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = Path(tmpdir) / 'subdir1' / 'subdir2' / 'checkpoint.pkl'
            
            # Should create directories automatically
            save_population(sample_population, nested_path)
            
            assert nested_path.exists()
            loaded_pop = load_population(nested_path)
            assert len(loaded_pop) == len(sample_population)


class TestSaveLoadIndividuals:
    """Tests for save_individuals and load_individuals functions"""
    
    def test_save_top_n_individuals(self, sample_population, temp_checkpoint_file):
        """Test saving top N individuals"""
        n = 5
        save_individuals(sample_population, temp_checkpoint_file, top_n=n)
        
        data = load_individuals(temp_checkpoint_file)
        
        assert data['num_saved'] == n
        assert len(data['individuals']) == n
        assert data['generation'] == sample_population.generation
    
    def test_save_specific_indices(self, sample_population, temp_checkpoint_file):
        """Test saving individuals by specific indices"""
        indices = [0, 2, 5]
        save_individuals(sample_population, temp_checkpoint_file, indices=indices)
        
        data = load_individuals(temp_checkpoint_file)
        
        assert data['num_saved'] == len(indices)
        assert len(data['individuals']) == len(indices)
        
        # Verify we got the right individuals
        for i, idx in enumerate(indices):
            assert data['individuals'][i].fitness == sample_population[idx].fitness
    
    def test_save_individuals_preserves_metadata(self, sample_population, temp_checkpoint_file):
        """Test that individual metadata is preserved"""
        save_individuals(sample_population, temp_checkpoint_file, top_n=3)
        data = load_individuals(temp_checkpoint_file)
        
        assert 'generation' in data
        assert 'total_population_size' in data
        assert 'top_frame' in data
        assert 'population_extra_parameters' in data
        
        assert data['generation'] == sample_population.generation
        assert data['total_population_size'] == len(sample_population)
    
    def test_top_n_larger_than_population(self, sample_population, temp_checkpoint_file):
        """Test requesting more individuals than exist in population"""
        pop_size = len(sample_population)
        save_individuals(sample_population, temp_checkpoint_file, top_n=pop_size + 10)
        
        data = load_individuals(temp_checkpoint_file)
        
        # Should save all available individuals
        assert data['num_saved'] == pop_size
        assert len(data['individuals']) == pop_size
    
    def test_invalid_indices_raises_error(self, sample_population, temp_checkpoint_file):
        """Test that invalid indices raise appropriate error"""
        with pytest.raises(IndexError):
            save_individuals(sample_population, temp_checkpoint_file, indices=[999])
    
    def test_both_top_n_and_indices_uses_indices(self, sample_population, temp_checkpoint_file):
        """Test that specifying both top_n and indices uses indices (indices takes precedence)"""
        # When both are provided, indices takes precedence
        save_individuals(sample_population, temp_checkpoint_file, top_n=5, indices=[0, 1, 2])
        data = load_individuals(temp_checkpoint_file)
        assert data['num_saved'] == 3  # Uses indices, not top_n
    
    def test_neither_top_n_nor_indices_saves_all(self, sample_population, temp_checkpoint_file):
        """Test that specifying neither parameter saves all individuals"""
        # When neither is provided, saves all individuals
        save_individuals(sample_population, temp_checkpoint_file)
        data = load_individuals(temp_checkpoint_file)
        assert data['num_saved'] == len(sample_population)


class TestCheckpointInSimpleEA:
    """Tests for checkpoint parameters in simple_ea"""
    
    def test_checkpoint_every_creates_files(self, simple_problem):
        """Test that checkpoint_every parameter creates checkpoint files"""
        top_frame, evaluator, fitness = simple_problem
        
        with tempfile.TemporaryDirectory() as tmpdir:
            checkpoint_path = Path(tmpdir) / 'checkpoint_gen{generation}.pkl'
            
            population = byron.ea.simple_ea(
                top_frame,
                evaluator,
                mu=5,
                lambda_=10,
                max_generation=10,
                checkpoint_every=5,
                checkpoint_file=checkpoint_path,
                target_fitness=byron.fitness.make_fitness(20)
            )
            
            # Should create checkpoints at gen 0, 5, 10
            assert Path(str(checkpoint_path).format(generation=0)).exists()
            assert Path(str(checkpoint_path).format(generation=5)).exists()
            assert Path(str(checkpoint_path).format(generation=10)).exists()
    
    def test_checkpoint_on_improvement(self, simple_problem):
        """Test that checkpoint_on_improvement creates files when fitness improves"""
        top_frame, evaluator, fitness = simple_problem
        
        with tempfile.TemporaryDirectory() as tmpdir:
            checkpoint_path = Path(tmpdir) / 'improvement_gen{generation}.pkl'
            
            population = byron.ea.simple_ea(
                top_frame,
                evaluator,
                mu=5,
                lambda_=10,
                max_generation=10,
                checkpoint_on_improvement=True,
                checkpoint_file=checkpoint_path,
                target_fitness=byron.fitness.make_fitness(20)
            )
            
            # Should create at least the initial and final checkpoints
            checkpoints = list(Path(tmpdir).glob('improvement_*.pkl'))
            assert len(checkpoints) >= 2  # At least gen 0 and final
    
    def test_checkpoint_callback_is_called(self, simple_problem):
        """Test that checkpoint_callback is invoked during evolution"""
        top_frame, evaluator, fitness = simple_problem
        
        callback_calls = []
        
        def test_callback(pop, gen):
            callback_calls.append((gen, pop[0].fitness))
        
        population = byron.ea.simple_ea(
            top_frame,
            evaluator,
            mu=5,
            lambda_=10,
            max_generation=5,
            checkpoint_callback=test_callback,
            target_fitness=byron.fitness.make_fitness(20)
        )
        
        # Callback should be called for each generation
        assert len(callback_calls) >= 5
        assert callback_calls[0][0] == 0  # First call at gen 0
    
    def test_checkpoint_callback_can_save_custom_checkpoints(self, simple_problem):
        """Test that callback can save custom checkpoints"""
        top_frame, evaluator, fitness = simple_problem
        
        with tempfile.TemporaryDirectory() as tmpdir:
            custom_saves = []
            
            def save_on_even_generations(pop, gen):
                if gen % 2 == 0:
                    path = Path(tmpdir) / f'custom_gen{gen}.pkl'
                    save_population(pop, path)
                    custom_saves.append(gen)
            
            population = byron.ea.simple_ea(
                top_frame,
                evaluator,
                mu=5,
                lambda_=10,
                max_generation=10,
                checkpoint_callback=save_on_even_generations,
                target_fitness=byron.fitness.make_fitness(20)
            )
            
            # Check custom checkpoints were created
            assert len(custom_saves) >= 5  # 0, 2, 4, 6, 8, 10
            for gen in custom_saves:
                assert (Path(tmpdir) / f'custom_gen{gen}.pkl').exists()
    
    def test_combined_checkpoint_strategies(self, simple_problem):
        """Test using multiple checkpoint strategies together"""
        top_frame, evaluator, fitness = simple_problem
        
        with tempfile.TemporaryDirectory() as tmpdir:
            checkpoint_path = Path(tmpdir) / 'combined_gen{generation}.pkl'
            callback_calls = []
            
            def tracking_callback(pop, gen):
                callback_calls.append(gen)
            
            population = byron.ea.simple_ea(
                top_frame,
                evaluator,
                mu=5,
                lambda_=10,
                max_generation=10,
                checkpoint_every=5,
                checkpoint_on_improvement=True,
                checkpoint_file=checkpoint_path,
                checkpoint_callback=tracking_callback,
                target_fitness=byron.fitness.make_fitness(20)
            )
            
            # All strategies should work together
            assert len(callback_calls) >= 10
            checkpoints = list(Path(tmpdir).glob('combined_*.pkl'))
            assert len(checkpoints) >= 2


class TestCheckpointContinuation:
    """Tests for multi-session evolution continuation"""
    
    def test_load_and_track_generation(self, simple_problem, temp_checkpoint_file):
        """Test loading checkpoint and tracking cumulative generations"""
        top_frame, evaluator, fitness = simple_problem
        
        # First session: 0 -> 5
        pop1 = byron.ea.simple_ea(
            top_frame, evaluator,
            mu=5, lambda_=10, max_generation=5,
            checkpoint_file=temp_checkpoint_file,
            target_fitness=byron.fitness.make_fitness(20)
        )
        
        # Load checkpoint
        loaded_pop = load_population(temp_checkpoint_file)
        starting_gen = loaded_pop.generation
        
        assert starting_gen == 5
        assert loaded_pop[0].fitness == pop1[0].fitness
        
        # Second session: 5 -> 10 (logically)
        pop2 = byron.ea.simple_ea(
            top_frame, evaluator,
            mu=5, lambda_=10, max_generation=5,
            checkpoint_file=temp_checkpoint_file,
            target_fitness=byron.fitness.make_fitness(20)
        )
        
        # Calculate cumulative generation
        total_gen = starting_gen + pop2.generation
        assert total_gen == 10
    
    def test_checkpoint_preserves_problem_definition(self, sample_population, temp_checkpoint_file):
        """Test that problem definition can be reconstructed from checkpoint"""
        save_population(sample_population, temp_checkpoint_file)
        loaded_pop = load_population(temp_checkpoint_file)
        
        # Check that top_frame is preserved (check type rather than string representation)
        assert loaded_pop.top_frame is not None
        assert type(loaded_pop.top_frame).__name__ == type(sample_population.top_frame).__name__


class TestCheckpointErrorHandling:
    """Tests for error handling in checkpoint functions"""
    
    def test_save_to_invalid_path_raises_error(self, sample_population):
        """Test that saving to invalid path raises appropriate error"""
        with pytest.raises((OSError, PermissionError, FileNotFoundError)):
            save_population(sample_population, Path('/invalid/path/checkpoint.pkl'))
    
    def test_load_corrupted_file_raises_error(self, temp_checkpoint_file):
        """Test that loading corrupted file raises appropriate error"""
        # Create corrupted file
        temp_checkpoint_file.write_text('corrupted data')
        
        with pytest.raises(Exception):  # Could be various pickle errors
            load_population(temp_checkpoint_file)
    
    def test_checkpoint_callback_exception_does_not_crash_evolution(self, simple_problem):
        """Test that exceptions in callback don't crash evolution"""
        top_frame, evaluator, fitness = simple_problem
        
        def failing_callback(pop, gen):
            if gen == 3:
                raise RuntimeError("Intentional error")
        
        # Evolution should complete despite callback error
        population = byron.ea.simple_ea(
            top_frame, evaluator,
            mu=5, lambda_=10, max_generation=5,
            checkpoint_callback=failing_callback,
            target_fitness=byron.fitness.make_fitness(20)
        )
        
        assert population.generation == 5


class TestCheckpointFileFormats:
    """Tests for checkpoint file format handling"""
    
    def test_checkpoint_with_path_object(self, sample_population, temp_checkpoint_file):
        """Test that Path objects work for checkpoint files"""
        save_population(sample_population, temp_checkpoint_file)
        loaded_pop = load_population(temp_checkpoint_file)
        
        assert len(loaded_pop) == len(sample_population)
    
    def test_checkpoint_with_string_path(self, sample_population):
        """Test that string paths work for checkpoint files"""
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pkl') as f:
            temp_path = f.name
        
        try:
            save_population(sample_population, temp_path)
            loaded_pop = load_population(temp_path)
            
            assert len(loaded_pop) == len(sample_population)
        finally:
            if Path(temp_path).exists():
                Path(temp_path).unlink()
    
    def test_generation_placeholder_in_filename(self, simple_problem):
        """Test that {generation} placeholder works in filenames"""
        top_frame, evaluator, fitness = simple_problem
        
        with tempfile.TemporaryDirectory() as tmpdir:
            template = Path(tmpdir) / 'checkpoint_gen{generation}.pkl'
            
            population = byron.ea.simple_ea(
                top_frame, evaluator,
                mu=5, lambda_=10, max_generation=5,
                checkpoint_every=5,
                checkpoint_file=template,
                target_fitness=byron.fitness.make_fitness(20)
            )
            
            # Check that files were created with actual generation numbers
            assert (Path(tmpdir) / 'checkpoint_gen0.pkl').exists()
            assert (Path(tmpdir) / 'checkpoint_gen5.pkl').exists()


class TestCheckpointPerformance:
    """Tests for checkpoint performance characteristics"""
    
    @pytest.mark.avoidable
    def test_large_population_checkpoint(self, simple_problem):
        """Test checkpointing with large population"""
        top_frame, evaluator, fitness = simple_problem
        
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pkl') as f:
            temp_path = Path(f.name)
        
        try:
            # Create larger population
            population = byron.ea.simple_ea(
                top_frame, evaluator,
                mu=50, lambda_=100, max_generation=10,
                target_fitness=byron.fitness.make_fitness(20)
            )
            
            # Save and load should work with larger populations
            save_population(population, temp_path)
            loaded_pop = load_population(temp_path)
            
            assert len(loaded_pop) == len(population)
            assert loaded_pop.generation == population.generation
        finally:
            if temp_path.exists():
                temp_path.unlink()
    
    @pytest.mark.avoidable
    def test_checkpoint_file_size_reasonable(self, sample_population, temp_checkpoint_file):
        """Test that checkpoint files are reasonably sized"""
        save_population(sample_population, temp_checkpoint_file)
        
        file_size = temp_checkpoint_file.stat().st_size
        
        # File should be reasonable size (less than 10MB for small population)
        assert file_size < 10 * 1024 * 1024
        assert file_size > 100  # But not empty
