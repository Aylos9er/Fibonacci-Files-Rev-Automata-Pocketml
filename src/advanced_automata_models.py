"""
Advanced Cellular Automata Models for Local ML Integration
Combines Fibonacci and Quad Core automata with language model analysis
"""
import numpy as np
from typing import Dict, List
from src.fibonacci_automata import ReversePineConeFibonacciAutomata
from src.quad_core_automata import QuadCoreErrorDetectingAutomata


class AdvancedAutomataSwarm:
    """
    Swarm of advanced cellular automata for distributed ML processing.
    Combines Fibonacci and Quad Core automata for pattern recognition and fault tolerance.
    """
    
    def __init__(self, num_fibonacci: int = 2, num_quad_core: int = 2):
        self.fibonacci_automata = [
            ReversePineConeFibonacciAutomata(grid_size=50) for _ in range(num_fibonacci)
        ]
        self.quad_core_automata = [
            QuadCoreErrorDetectingAutomata(grid_size=30) for _ in range(num_quad_core)
        ]
        
        # Set different modes for diversity
        for i, fib in enumerate(self.fibonacci_automata):
            fib.set_reverse_mode(i % 2 == 1)  # Alternate normal/reverse
        
        for i, quad in enumerate(self.quad_core_automata):
            quad.set_fault_rate(0.01 * (i + 1))  # Increasing fault rates
            quad.reset_cores("random")
        
        self.analysis_history = []
    
    def step_all(self, reverse_mode: bool = False):
        """Execute one generation step for all automata in forward or reverse mode."""
        # Step Fibonacci automata with reversible computation
        for fib in self.fibonacci_automata:
            fib.set_reverse_mode(reverse_mode)
            fib.step(num_scales=89)  # Use Fibonacci number 89 for scales
        
        # Step Quad Core automata
        for quad in self.quad_core_automata:
            quad.step()
    
    def get_combined_analysis(self) -> Dict:
        """Get combined analysis from all automata."""
        # Collect Fibonacci stats
        fib_stats = []
        for i, fib in enumerate(self.fibonacci_automata):
            stats = fib.get_state_stats()
            stats['automaton_id'] = f"Fibonacci-{i}"
            fib_stats.append(stats)
        
        # Collect Quad Core stats
        quad_stats = []
        for i, quad in enumerate(self.quad_core_automata):
            stats = quad.get_state_stats()
            stats['automaton_id'] = f"QuadCore-{i}"
            quad_stats.append(stats)
        
        # Compute swarm-level metrics
        avg_fib_energy = np.mean([s['pattern_energy'] for s in fib_stats])
        avg_fault_tolerance = np.mean([s['fault_tolerance_score'] for s in quad_stats])
        total_faults = sum([s['total_faults_detected'] for s in quad_stats])
        
        return {
            "fibonacci_automata": fib_stats,
            "quad_core_automata": quad_stats,
            "swarm_metrics": {
                "avg_fibonacci_energy": float(avg_fib_energy),
                "avg_fault_tolerance": float(avg_fault_tolerance),
                "total_faults_detected": total_faults,
                "num_fibonacci": len(self.fibonacci_automata),
                "num_quad_core": len(self.quad_core_automata)
            }
        }
    
    def generate_ml_insight(self, mesh_data: Dict, ca_data: Dict) -> str:
        """
        Generate ML insight by analyzing mesh and CA data using automata patterns.
        """
        analysis = self.get_combined_analysis()
        
        # Use Fibonacci patterns to analyze mesh coherence
        fib_energy = analysis['swarm_metrics']['avg_fibonacci_energy']
        mesh_coherence = mesh_data.get('coherence', 0.5)
        
        # Use Quad Core fault tolerance for system reliability assessment
        fault_tolerance = analysis['swarm_metrics']['avg_fault_tolerance']
        
        # Generate insight based on patterns
        insights = []
        
        # Fibonacci analysis
        if fib_energy > 0.7:
            insights.append(f"Fibonacci automata detected strong golden ratio alignment ({fib_energy:.2f}), suggesting optimal mesh coherence patterns.")
        else:
            insights.append(f"Fibonacci patterns show deviation from golden ratio ({fib_energy:.2f}), indicating potential for mesh optimization.")
        
        # Get spiral counts
        fib_stats = analysis['fibonacci_automata'][0] if analysis['fibonacci_automata'] else {}
        if fib_stats:
            spiral_a = fib_stats.get('spiral_count_a', 5)
            spiral_b = fib_stats.get('spiral_count_b', 8)
            insights.append(f"Detected Fibonacci spiral pair ({spiral_a}, {spiral_b}) - common in natural systems.")
        
        # Quad Core fault analysis
        total_faults = analysis['swarm_metrics']['total_faults_detected']
        if total_faults > 0:
            insights.append(f"Quad-core error detection identified {total_faults} faults with {fault_tolerance:.2%} correction rate.")
        else:
            insights.append(f"System operating fault-free with {fault_tolerance:.2%} tolerance capacity.")
        
        # Combined analysis
        if fib_energy > 0.6 and fault_tolerance > 0.8:
            insights.append("Advanced automata analysis: System exhibits both optimal pattern formation and high fault resilience.")
        elif fib_energy < 0.5:
            insights.append("Advanced automata suggestion: Consider increasing mesh symmetry for better Fibonacci alignment.")
        
        return " ".join(insights)


def create_advanced_automata_swarm(num_fibonacci: int = 2, num_quad_core: int = 2) -> AdvancedAutomataSwarm:
    """Factory function to create advanced automata swarm."""
    return AdvancedAutomataSwarm(num_fibonacci, num_quad_core)
