import numpy as np
from typing import List, Dict, Tuple
import math

class SymbioticGrapheneMesh:
    """
    Simulates a symbiotic graphene mesh with light-responsive properties
    and dynamic tensor field interactions.
    """
    
    def __init__(self, size: int = 20):
        self.size = size
        self.mesh_nodes = self._initialize_mesh()
        self.energy_field = np.zeros((size, size))
        self.stimuli_response = np.zeros((size, size))
        self.tensor_state = np.random.rand(size * size) * 0.1
        self.coherence_matrix = np.eye(size)
        self.time_step = 0
        
    def _initialize_mesh(self) -> np.ndarray:
        """Initialize the graphene mesh structure with hexagonal lattice approximation."""
        mesh = np.zeros((self.size, self.size, 3))  # x, y, z coordinates
        
        for i in range(self.size):
            for j in range(self.size):
                # Create hexagonal-like structure with slight randomization
                x = j + 0.5 * (i % 2)  # Offset alternate rows
                y = i * math.sqrt(3) / 2
                z = np.random.normal(0, 0.1)  # Small z-variation for 3D effect
                
                mesh[i, j] = [x, y, z]
                
        return mesh
    
    def update_stimuli(self, intensity: float):
        """Update mesh response to light stimuli."""
        self.time_step += 1
        
        # Simulate light interaction with graphene
        # Light creates localized excitations that propagate
        center_x, center_y = self.size // 2, self.size // 2
        
        for i in range(self.size):
            for j in range(self.size):
                distance = math.sqrt((i - center_x)**2 + (j - center_y)**2)
                
                # Light response follows Gaussian distribution with time modulation
                response = intensity * math.exp(-distance**2 / (2 * (self.size/4)**2))
                response *= (1 + 0.3 * math.sin(self.time_step * 0.1))  # Dynamic modulation
                
                self.stimuli_response[i, j] = response
                
        # Update energy field based on stimuli
        self.energy_field = self.stimuli_response + 0.1 * np.random.rand(self.size, self.size)
        
        # Update tensor state with symbiotic coupling
        stimuli_vector = self.stimuli_response.flatten()
        coupling_strength = 0.05
        self.tensor_state += coupling_strength * (stimuli_vector - self.tensor_state)
        
    def get_mesh_state(self) -> Dict:
        """Get current state of the mesh for visualization."""
        return {
            'nodes': self.mesh_nodes,
            'energy': self.energy_field,
            'stimuli': self.stimuli_response,
            'tensor_magnitude': np.linalg.norm(self.tensor_state),
            'coherence': self._calculate_coherence()
        }
    
    def get_tensor_state(self) -> np.ndarray:
        """Get current tensor state."""
        return self.tensor_state.copy()
    
    def update_from_tensors(self, new_tensors: np.ndarray):
        """Update mesh state from processed tensors."""
        if len(new_tensors) == len(self.tensor_state):
            self.tensor_state = new_tensors
            
            # Update mesh node positions based on tensor values
            tensor_2d = new_tensors.reshape(self.size, self.size)
            self.mesh_nodes[:, :, 2] += 0.01 * tensor_2d  # Small z-displacement
            
    def get_energy(self) -> float:
        """Calculate total mesh energy."""
        kinetic_energy = 0.5 * np.sum(self.tensor_state**2)
        potential_energy = 0.5 * np.sum(self.energy_field**2)
        interaction_energy = np.sum(self.stimuli_response * self.energy_field)
        
        return kinetic_energy + potential_energy + interaction_energy
    
    def _calculate_coherence(self) -> float:
        """Calculate mesh coherence as a measure of organization."""
        # Measure local correlations in the tensor field
        correlations = []
        tensor_2d = self.tensor_state.reshape(self.size, self.size)
        
        for i in range(1, self.size-1):
            for j in range(1, self.size-1):
                local_patch = tensor_2d[i-1:i+2, j-1:j+2]
                center_val = tensor_2d[i, j]
                
                # Calculate correlation with neighbors
                correlation = np.corrcoef(local_patch.flatten(), 
                                       np.full(9, center_val))[0, 1]
                if not np.isnan(correlation):
                    correlations.append(correlation)
        
        return float(np.mean(correlations)) if correlations else 0.0
