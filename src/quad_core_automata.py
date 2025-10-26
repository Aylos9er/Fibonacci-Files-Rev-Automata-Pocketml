"""
Quad Core Error Detecting Cellular Automata
Implements fault-tolerant computing with 4-way redundancy and majority voting
"""
import numpy as np
from typing import List, Tuple, Dict, Optional


class QuadCoreErrorDetectingAutomata:
    """
    Fault-tolerant cellular automata using quadded logic (4-way redundancy).
    Each cell has 4 redundant states with majority voting for error detection/correction.
    """
    
    def __init__(self, grid_size: int = 30):
        self.grid_size = grid_size
        # Four redundant grids (quad redundancy)
        self.core_states = [
            np.random.randint(0, 2, (grid_size, grid_size)) for _ in range(4)
        ]
        self.fault_map = np.zeros((grid_size, grid_size))  # Tracks detected faults
        self.corrected_state = np.zeros((grid_size, grid_size))
        self.generation = 0
        self.total_faults_detected = 0
        self.total_faults_corrected = 0
        self.fault_injection_rate = 0.0
        
    def majority_vote(self, core_values: List[int]) -> Tuple[int | None, bool]:
        """
        Perform majority voting on 4 core values.
        Returns (consensus_value, fault_detected).
        If tie (2-vs-2), returns (None, True) to indicate unresolvable fault.
        """
        counts = np.bincount(core_values, minlength=2)
        
        # Handle ties (2-vs-2) - cannot determine consensus
        if counts[0] == counts[1]:
            # Tie detected - preserve current core states, don't force consensus
            return None, True  # None signals "no correction possible"
        else:
            majority_value = np.argmax(counts)
            # Fault detected if not all cores agree
            fault_detected = not all(v == majority_value for v in core_values)
            return int(majority_value), fault_detected
    
    def detect_and_correct_errors(self):
        """Apply majority voting across all four cores to detect and correct errors."""
        self.fault_map.fill(0)
        faults_this_gen = 0
        corrections_this_gen = 0
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                # Get values from all 4 cores
                core_values = [
                    int(self.core_states[k][i, j]) for k in range(4)
                ]
                
                # Majority voting
                consensus, fault = self.majority_vote(core_values)
                
                if fault:
                    self.fault_map[i, j] = 1
                    faults_this_gen += 1
                    
                    # Only correct if consensus exists (not a tie)
                    if consensus is not None:
                        self.corrected_state[i, j] = consensus
                        
                        # Correct faulty cores to match consensus
                        for k in range(4):
                            if self.core_states[k][i, j] != consensus:
                                self.core_states[k][i, j] = consensus
                                corrections_this_gen += 1
                    else:
                        # Tie: preserve existing cores, use first core for corrected output
                        self.corrected_state[i, j] = self.core_states[0][i, j]
                else:
                    # No fault - all cores agree
                    self.corrected_state[i, j] = consensus
        
        self.total_faults_detected += faults_this_gen
        self.total_faults_corrected += corrections_this_gen
        
        return faults_this_gen, corrections_this_gen
    
    def inject_faults(self):
        """Inject random faults into cores based on fault_injection_rate."""
        if self.fault_injection_rate > 0:
            for core_idx in range(4):
                # Randomly flip bits
                fault_mask = np.random.random((self.grid_size, self.grid_size)) < self.fault_injection_rate
                self.core_states[core_idx] = np.where(
                    fault_mask,
                    1 - self.core_states[core_idx],
                    self.core_states[core_idx]
                ).astype(int)
    
    def apply_ca_rule(self, state: np.ndarray) -> np.ndarray:
        """
        Apply Conway's Game of Life rules as the base CA.
        Can be swapped for other CA rules.
        """
        new_state = state.copy()
        
        for i in range(1, self.grid_size - 1):
            for j in range(1, self.grid_size - 1):
                # Count living neighbors
                neighbors = state[i-1:i+2, j-1:j+2]
                neighbor_sum = np.sum(neighbors) - state[i, j]
                
                # Conway's rules
                if state[i, j] == 1:
                    # Cell dies unless it has 2 or 3 neighbors
                    new_state[i, j] = 1 if neighbor_sum in [2, 3] else 0
                else:
                    # Cell becomes alive with exactly 3 neighbors
                    new_state[i, j] = 1 if neighbor_sum == 3 else 0
        
        return new_state
    
    def step(self):
        """Execute one generation: inject faults, evolve cores, detect/correct errors."""
        # 1. Inject random faults (simulates transient errors)
        self.inject_faults()
        
        # 2. Evolve each core independently using CA rules
        for k in range(4):
            self.core_states[k] = self.apply_ca_rule(self.core_states[k])
        
        # 3. Detect and correct errors via majority voting
        faults, corrections = self.detect_and_correct_errors()
        
        self.generation += 1
        
        return faults, corrections
    
    def set_fault_rate(self, rate: float):
        """Set the fault injection rate (0.0 to 1.0)."""
        self.fault_injection_rate = max(0.0, min(1.0, rate))
    
    def get_core_agreement(self) -> float:
        """Calculate percentage of cells where all 4 cores agree."""
        agreements = 0
        total_cells = self.grid_size * self.grid_size
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                values = [self.core_states[k][i, j] for k in range(4)]
                if len(set(values)) == 1:  # All cores agree
                    agreements += 1
        
        return 100.0 * agreements / total_cells if total_cells > 0 else 0.0
    
    def get_fault_tolerance_score(self) -> float:
        """
        Calculate fault tolerance score based on successful corrections.
        Score is high when system detects and corrects many faults.
        """
        if self.total_faults_detected == 0:
            return 1.0  # Perfect if no faults
        
        correction_rate = self.total_faults_corrected / (self.total_faults_detected * 3)  # Max 3 corrections per fault
        return min(1.0, correction_rate)
    
    def get_hamming_distance(self) -> float:
        """Calculate average Hamming distance between cores."""
        distances = []
        
        for k1 in range(4):
            for k2 in range(k1 + 1, 4):
                diff = np.sum(self.core_states[k1] != self.core_states[k2])
                total = self.grid_size * self.grid_size
                distances.append(diff / total if total > 0 else 0.0)
        
        return float(np.mean(distances)) if distances else 0.0
    
    def reset_cores(self, pattern: Optional[str] = None):
        """Reset all cores to a specific pattern or random state."""
        if pattern == "glider":
            # Classic glider pattern
            base = np.zeros((self.grid_size, self.grid_size), dtype=int)
            if self.grid_size >= 5:
                base[1, 2] = 1
                base[2, 3] = 1
                base[3, 1:4] = 1
        elif pattern == "random":
            base = np.random.randint(0, 2, (self.grid_size, self.grid_size))
        else:
            base = np.zeros((self.grid_size, self.grid_size), dtype=int)
        
        # Copy to all 4 cores
        for k in range(4):
            self.core_states[k] = base.copy()
        
        self.generation = 0
        self.total_faults_detected = 0
        self.total_faults_corrected = 0
        self.fault_map.fill(0)
    
    def get_state_stats(self) -> Dict:
        """Get comprehensive statistics about the automata state."""
        return {
            "generation": self.generation,
            "active_cells": int(np.sum(self.corrected_state)),
            "fault_injection_rate": self.fault_injection_rate * 100,
            "total_faults_detected": self.total_faults_detected,
            "total_faults_corrected": self.total_faults_corrected,
            "core_agreement_pct": self.get_core_agreement(),
            "fault_tolerance_score": self.get_fault_tolerance_score(),
            "avg_hamming_distance": self.get_hamming_distance(),
            "current_faults": int(np.sum(self.fault_map)),
            "grid_size": self.grid_size
        }
    
    def get_core_states_for_viz(self) -> List[np.ndarray]:
        """Return all 4 core states for visualization."""
        return self.core_states.copy()
