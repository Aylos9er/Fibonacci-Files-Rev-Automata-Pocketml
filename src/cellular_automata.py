import numpy as np
from typing import List, Tuple

class TwoWayCellularAutomata:
    """
    Implements two-way cellular automata with configurable forward/reverse steps.
    Simulates the CA dynamics described in the research paper.
    """
    
    def __init__(self, size: int = 20):
        self.size = size
        self.current_state = np.random.rand(size * size) * 0.5
        self.previous_states = []
        self.step_count = 0
        self.forward_steps = 0
        self.reverse_steps = 0
        
    def update_step(self, input_tensors: np.ndarray, step_type: str = "forward", 
                   stimuli: float = 0.1):
        """Perform one CA update step."""
        # Store current state for history
        self.previous_states.append(self.current_state.copy())
        if len(self.previous_states) > 20:  # Keep limited history
            self.previous_states.pop(0)
            
        if step_type == "forward":
            self._forward_step(input_tensors, stimuli)
            self.forward_steps += 1
        else:
            self._reverse_step(input_tensors, stimuli)
            self.reverse_steps += 1
            
        self.step_count += 1
        
    def _forward_step(self, input_tensors: np.ndarray, stimuli: float):
        """Perform forward CA step with symbiotic weighting."""
        state_2d = self.current_state.reshape(self.size, self.size)
        new_state = np.zeros_like(state_2d)
        
        for i in range(self.size):
            for j in range(self.size):
                # Get neighborhood (Moore neighborhood with toric boundaries)
                neighbors = self._get_neighbors(state_2d, i, j)
                
                # Calculate gradient for symbiotic weight
                if len(self.previous_states) > 0:
                    prev_2d = self.previous_states[-1].reshape(self.size, self.size)
                    gradient = abs(state_2d[i, j] - prev_2d[i, j])
                else:
                    gradient = 0
                
                # Symbiotic weight with stimuli response
                weight = self._calculate_symbiotic_weight(
                    state_2d[i, j], gradient, stimuli, "forward"
                )
                
                # CA rule: weighted average with nonlinear activation
                neighbor_avg = np.mean(neighbors)
                tensor_influence = input_tensors[i * self.size + j] if len(input_tensors) == self.size * self.size else 0
                
                # Forward evolution rule
                new_val = weight * state_2d[i, j] + (1 - weight) * neighbor_avg
                new_val += 0.1 * tensor_influence + 0.05 * stimuli
                
                # Apply activation function (sigmoid-like)
                new_state[i, j] = self._activation_function(new_val)
        
        self.current_state = new_state.flatten()
        
    def _reverse_step(self, input_tensors: np.ndarray, stimuli: float):
        """Perform reverse CA step for temporal symmetry."""
        if len(self.previous_states) < 2:
            return  # Need history for reverse step
            
        state_2d = self.current_state.reshape(self.size, self.size)
        prev_2d = self.previous_states[-2].reshape(self.size, self.size)
        new_state = np.zeros_like(state_2d)
        
        for i in range(self.size):
            for j in range(self.size):
                neighbors = self._get_neighbors(state_2d, i, j)
                gradient = abs(state_2d[i, j] - prev_2d[i, j])
                
                weight = self._calculate_symbiotic_weight(
                    state_2d[i, j], gradient, stimuli, "reverse"
                )
                
                # Reverse evolution: move toward previous configuration
                neighbor_avg = np.mean(neighbors)
                tensor_influence = input_tensors[i * self.size + j] if len(input_tensors) == self.size * self.size else 0
                
                # Reverse rule with dampening
                new_val = weight * prev_2d[i, j] + (1 - weight) * neighbor_avg
                new_val -= 0.05 * tensor_influence + 0.02 * stimuli
                
                new_state[i, j] = self._activation_function(new_val)
        
        self.current_state = new_state.flatten()
        
    def _get_neighbors(self, state_2d: np.ndarray, i: int, j: int) -> List[float]:
        """Get Moore neighborhood with toric (wraparound) boundaries."""
        neighbors = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:  # Skip center cell
                    continue
                ni = (i + di) % self.size
                nj = (j + dj) % self.size
                neighbors.append(state_2d[ni, nj])
        return neighbors
        
    def _calculate_symbiotic_weight(self, tensor_val: float, gradient: float, 
                                  stimuli: float, step_type: str) -> float:
        """Calculate symbiotic weight based on current state and stimuli."""
        base_weight = 0.5
        gradient_contribution = 0.1 * min(gradient, 1.0)  # Cap gradient effect
        
        if step_type == "forward":
            stimuli_contribution = stimuli * 0.05
        else:
            stimuli_contribution = stimuli * 0.02  # Reduced for reverse
            
        weight = base_weight + gradient_contribution + stimuli_contribution
        return np.clip(weight, 0.1, 0.9)  # Keep in reasonable range
        
    def _activation_function(self, x: float) -> float:
        """Smooth activation function for CA states."""
        return 1 / (1 + np.exp(-4 * (x - 0.5)))  # Sigmoid centered at 0.5
        
    def get_current_state(self) -> np.ndarray:
        """Get current CA state."""
        return self.current_state.copy()
        
    def get_statistics(self) -> dict:
        """Get CA statistics."""
        active_cells = np.sum(self.current_state > 0.5)
        avg_activation = np.mean(self.current_state)
        entropy = -np.sum(self.current_state * np.log(self.current_state + 1e-10))
        
        return {
            'active_cells': active_cells,
            'total_cells': len(self.current_state),
            'activation_rate': active_cells / len(self.current_state),
            'average_activation': avg_activation,
            'entropy': entropy,
            'forward_steps': self.forward_steps,
            'reverse_steps': self.reverse_steps,
            'total_steps': self.step_count
        }
