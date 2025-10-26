import numpy as np
from typing import List, Tuple
import math

class HelixTensorProcessor:
    """
    Implements double helix tensor processing for the graphene mesh.
    Simulates the dual-strand tensor evolution described in the research.
    """
    
    def __init__(self):
        self.rotation_count = 0
        self.helix_state_a = []
        self.helix_state_b = []
        self.processing_history = []
        self.crossover_points = []
        
    def process_helix(self, input_tensors: np.ndarray) -> np.ndarray:
        """Process tensors through double helix structure."""
        n = len(input_tensors)
        
        # Split into two helical strands
        strand_a = input_tensors[:n//2] if n > 1 else input_tensors
        strand_b = input_tensors[n//2:] if n > 1 else input_tensors.copy()
        
        # Ensure equal length
        min_len = min(len(strand_a), len(strand_b))
        strand_a = strand_a[:min_len]
        strand_b = strand_b[:min_len]
        
        # Apply helical transformation
        processed_a, processed_b = self._helical_transform(strand_a, strand_b)
        
        # Perform crossover interactions
        crossed_a, crossed_b = self._crossover_interaction(processed_a, processed_b)
        
        # Combine strands with phase coupling
        combined = self._combine_strands(crossed_a, crossed_b)
        
        # Store state for visualization
        self.helix_state_a = crossed_a
        self.helix_state_b = crossed_b
        self.processing_history.append({
            'input_norm': np.linalg.norm(input_tensors),
            'output_norm': np.linalg.norm(combined),
            'rotation': self.rotation_count
        })
        
        if len(self.processing_history) > 100:  # Limit history
            self.processing_history.pop(0)
            
        return combined
    
    def _helical_transform(self, strand_a: np.ndarray, strand_b: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Apply helical rotation transformation to tensor strands."""
        n = len(strand_a)
        
        # Rotation angle increases with position (helix pitch)
        angles_a = np.linspace(0, 4 * np.pi, n) + self.rotation_count * 0.1
        angles_b = angles_a + np.pi  # 180-degree phase offset
        
        # Helical transformation matrix (simplified 2D rotation in complex plane)
        transformed_a = np.zeros_like(strand_a)
        transformed_b = np.zeros_like(strand_b)
        
        for i in range(n):
            # Treat each tensor element as complex number for rotation
            complex_a = strand_a[i] * np.exp(1j * angles_a[i])
            complex_b = strand_b[i] * np.exp(1j * angles_b[i])
            
            # Extract real part after rotation (simulating 3D projection)
            transformed_a[i] = np.real(complex_a)
            transformed_b[i] = np.real(complex_b)
        
        self.rotation_count += 1
        return transformed_a, transformed_b
    
    def _crossover_interaction(self, strand_a: np.ndarray, strand_b: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Simulate crossover interactions between helix strands."""
        n = len(strand_a)
        crossover_a = strand_a.copy()
        crossover_b = strand_b.copy()
        self.crossover_points = []
        
        # Determine crossover points based on strand similarity
        for i in range(n):
            # Crossover probability based on local tensor similarity
            similarity = 1 - abs(strand_a[i] - strand_b[i])
            crossover_prob = 0.1 + 0.2 * similarity  # Base + similarity bonus
            
            if np.random.random() < crossover_prob:
                # Perform crossover exchange
                coupling_strength = 0.3
                original_a = crossover_a[i]
                original_b = crossover_b[i]
                
                crossover_a[i] = original_a * (1 - coupling_strength) + original_b * coupling_strength
                crossover_b[i] = original_b * (1 - coupling_strength) + original_a * coupling_strength
                
                self.crossover_points.append(i)
        
        return crossover_a, crossover_b
    
    def _combine_strands(self, strand_a: np.ndarray, strand_b: np.ndarray) -> np.ndarray:
        """Combine processed strands into final tensor output."""
        # Interleave strands with phase coupling
        n_total = len(strand_a) + len(strand_b)
        combined = np.zeros(n_total)
        
        # Weighted combination based on strand complementarity
        for i in range(len(strand_a)):
            weight_a = 0.5 + 0.2 * np.sin(self.rotation_count * 0.1 + i * 0.3)
            weight_b = 1 - weight_a
            
            # Primary positions
            combined[i * 2] = weight_a * strand_a[i]
            if i * 2 + 1 < n_total:
                combined[i * 2 + 1] = weight_b * strand_b[i]
        
        # Normalize to prevent runaway growth
        norm = np.linalg.norm(combined)
        if norm > 0:
            combined = combined / norm * min(float(norm), 10.0)  # Cap magnitude
            
        return combined
    
    def get_helix_coordinates(self) -> Tuple[np.ndarray, np.ndarray]:
        """Get 3D coordinates for helix visualization."""
        if len(self.helix_state_a) == 0 or len(self.helix_state_b) == 0:
            return np.array([]), np.array([])
        
        n = len(self.helix_state_a)
        t = np.linspace(0, 4 * np.pi, n)
        
        # Double helix coordinates
        helix_a = np.column_stack([
            np.cos(t) * np.abs(self.helix_state_a),
            np.sin(t) * np.abs(self.helix_state_a),
            t
        ])
        
        helix_b = np.column_stack([
            np.cos(t + np.pi) * np.abs(self.helix_state_b),  # Phase offset
            np.sin(t + np.pi) * np.abs(self.helix_state_b),
            t
        ])
        
        return helix_a, helix_b
    
    def get_rotation_count(self) -> int:
        """Get current rotation count."""
        return self.rotation_count
    
    def get_processing_stats(self) -> dict:
        """Get processing statistics."""
        if not self.processing_history:
            return {'avg_amplification': 1.0, 'stability': 1.0, 'crossover_rate': 0.0}
        
        recent_history = self.processing_history[-10:]  # Last 10 steps
        
        amplifications = [h['output_norm'] / max(h['input_norm'], 1e-10) for h in recent_history]
        avg_amplification = np.mean(amplifications)
        stability = 1.0 / (1.0 + np.std(amplifications))  # Higher stability = lower variance
        
        crossover_rate = len(self.crossover_points) / max(len(self.helix_state_a), 1)
        
        return {
            'avg_amplification': avg_amplification,
            'stability': stability,
            'crossover_rate': crossover_rate,
            'total_rotations': self.rotation_count,
            'active_crossovers': len(self.crossover_points)
        }
