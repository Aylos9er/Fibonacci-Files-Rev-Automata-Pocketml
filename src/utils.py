import numpy as np
from typing import Dict, List, Any
import time

def calculate_performance_metrics(mesh_state: Dict, processed_tensors: np.ndarray, 
                                 current_step: int, target_pass_at_1: float, 
                                 target_latency: float) -> Dict[str, float]:
    """
    Calculate comprehensive performance metrics for the HelixGrapheneLM system.
    """
    # Simulated Pass@1 score based on mesh coherence and tensor processing
    coherence = mesh_state.get('coherence', 0.5)
    tensor_quality = min(1.0, float(np.linalg.norm(processed_tensors)) / max(len(processed_tensors), 1))
    energy_stability = 1.0 - min(1.0, float(np.std(mesh_state.get('energy', [0.5]))))
    
    # Pass@1 calculation (weighted combination of factors)
    pass_at_1 = (0.4 * coherence + 0.4 * tensor_quality + 0.2 * energy_stability)
    pass_at_1 = np.clip(pass_at_1 + np.random.normal(0, 0.02), 0, 1)  # Small noise
    
    # Simulated latency based on processing complexity and step count
    base_latency = 30  # Base latency in ms/token
    complexity_factor = len(processed_tensors) / 400  # Normalize by typical size
    step_overhead = current_step * 0.5  # Each step adds overhead
    
    latency = base_latency * (1 + complexity_factor) + step_overhead
    latency += np.random.normal(0, 2)  # Realistic variation
    latency = max(15, latency)  # Minimum realistic latency
    
    # Energy efficiency calculation
    mesh_energy = np.sum(mesh_state.get('energy', [1.0]))
    tensor_processing_cost = np.sum(np.abs(processed_tensors)) * 0.01
    base_power = 1.2  # Base power consumption in watts
    
    energy_efficiency = base_power + 0.1 * mesh_energy + tensor_processing_cost
    energy_efficiency = max(0.8, min(5.0, energy_efficiency))  # Reasonable bounds
    
    # Mesh coherence (from mesh_state)
    mesh_coherence = coherence
    
    # Additional derived metrics
    efficiency_ratio = target_pass_at_1 / max(pass_at_1, 0.01)
    latency_ratio = latency / target_latency
    performance_index = pass_at_1 / (latency / 1000)  # Pass@1 per second
    
    return {
        'pass_at_1': pass_at_1,
        'latency': latency,
        'energy_efficiency': energy_efficiency,
        'coherence': mesh_coherence,
        'efficiency_ratio': efficiency_ratio,
        'latency_ratio': latency_ratio,
        'performance_index': performance_index,
        'tensor_quality': tensor_quality,
        'energy_stability': energy_stability,
        'step': current_step
    }

def format_metrics_display(metrics: Dict[str, float]) -> str:
    """
    Format metrics for display in the Streamlit interface.
    """
    formatted = f"""
    **Performance Metrics (Step {metrics.get('step', 0)})**
    
    🎯 **Core Metrics:**
    • Pass@1 Score: {metrics['pass_at_1']:.4f}
    • Latency: {metrics['latency']:.2f} ms/token
    • Energy: {metrics['energy_efficiency']:.2f}W
    • Coherence: {metrics['coherence']:.4f}
    
    📊 **Derived Metrics:**
    • Performance Index: {metrics['performance_index']:.2f}
    • Efficiency Ratio: {metrics['efficiency_ratio']:.3f}
    • Latency Ratio: {metrics['latency_ratio']:.3f}
    • Tensor Quality: {metrics['tensor_quality']:.3f}
    """
    return formatted

def validate_simulation_parameters(mesh_size: int, ca_steps: int, stimuli: float, 
                                 num_pockets: int) -> List[str]:
    """
    Validate simulation parameters and return list of warnings/errors.
    """
    warnings = []
    
    if mesh_size < 5:
        warnings.append("⚠️ Very small mesh size may not show interesting dynamics")
    elif mesh_size > 100:
        warnings.append("⚠️ Large mesh size may cause performance issues")
    
    if ca_steps < 1:
        warnings.append("❌ At least 1 CA step is required")
    elif ca_steps > 50:
        warnings.append("⚠️ Many CA steps will slow down simulation")
    
    if stimuli < 0 or stimuli > 1:
        warnings.append("❌ Stimuli intensity must be between 0 and 1")
    
    if num_pockets < 1:
        warnings.append("❌ At least 1 pocket instance is required")
    elif num_pockets > 10:
        warnings.append("⚠️ Many pockets may impact visualization clarity")
    
    return warnings

def generate_research_summary() -> str:
    """
    Generate formatted research summary for display.
    """
    return """
    ## 🧬 HelixGrapheneLM: Symbiotic Graphene Mesh Research
    
    ### Core Innovation
    This simulation demonstrates a novel approach to pocket-sized language models using:
    
    **1. Symbiotic Graphene Mesh**
    - Light-responsive graphene structure
    - Dynamic tensor field interactions
    - Energy-efficient processing substrate
    
    **2. Double Helix Tensor Processing**
    - Dual-strand tensor evolution
    - Crossover interactions for information exchange
    - Phase-coupled processing for enhanced performance
    
    **3. Two-Way Cellular Automata**
    - Forward evolution (7 steps) for exploration
    - Reverse evolution (4 steps) for consolidation
    - Stimuli-responsive adaptive weights
    
    **4. Modular Swarm Architecture**
    - 3-5 specialized pocket instances
    - Distributed coordination strategies
    - Fault-tolerant collaborative processing
    
    ### Target Performance
    - **Pass@1**: 0.98 on BigCodeBench
    - **Latency**: <35 ms/token
    - **Power**: ~1.2W total consumption
    - **Size**: ~50MB per pocket instance
    
    ### Applications
    - Edge AI deployment
    - Mobile device integration
    - IoT and embedded systems
    - Sustainable AI computing
    
    *Research Contact: mosijbuilder@gmail.com*
    """

def export_simulation_data(metrics_history: List[Dict], mesh_states: List[Dict], 
                          ca_states: List[np.ndarray]) -> Dict[str, Any]:
    """
    Export simulation data for further analysis or research.
    """
    export_data = {
        'metadata': {
            'export_timestamp': time.time(),
            'simulation_steps': len(metrics_history),
            'mesh_size': int(np.sqrt(len(ca_states[0]))) if ca_states else 0,
            'version': 'HelixGrapheneLM v1.0'
        },
        'performance_metrics': metrics_history,
        'mesh_evolution': mesh_states,
        'ca_evolution': [state.tolist() for state in ca_states],  # Convert to serializable format
        'summary_statistics': {
            'final_pass_at_1': metrics_history[-1]['pass_at_1'] if metrics_history else 0,
            'avg_latency': np.mean([m['latency'] for m in metrics_history]) if metrics_history else 0,
            'avg_energy': np.mean([m['energy_efficiency'] for m in metrics_history]) if metrics_history else 0,
            'final_coherence': metrics_history[-1]['coherence'] if metrics_history else 0
        }
    }
    
    return export_data

def calculate_theoretical_limits() -> Dict[str, float]:
    """
    Calculate theoretical performance limits based on the architecture.
    """
    return {
        'max_pass_at_1': 0.995,  # Theoretical maximum with perfect conditions
        'min_latency': 25.0,     # Physical limits of processing
        'min_energy': 0.8,       # Minimum power for operation
        'max_coherence': 0.98,   # Maximum achievable mesh coherence
        'optimal_mesh_size': 30, # Optimal balance of complexity and performance
        'optimal_pockets': 5     # Sweet spot for swarm coordination
    }

def simulate_real_world_conditions(base_metrics: Dict[str, float], 
                                 noise_level: float = 0.1) -> Dict[str, float]:
    """
    Add realistic noise and variations to simulate real-world deployment conditions.
    """
    noisy_metrics = base_metrics.copy()
    
    # Add realistic variations
    for key in ['pass_at_1', 'latency', 'energy_efficiency', 'coherence']:
        if key in noisy_metrics:
            if key == 'latency':
                # Latency can spike occasionally
                spike_prob = 0.05
                if np.random.random() < spike_prob:
                    noisy_metrics[key] *= np.random.uniform(1.5, 3.0)
                else:
                    noisy_metrics[key] *= (1 + np.random.normal(0, noise_level * 0.5))
            else:
                noisy_metrics[key] *= (1 + np.random.normal(0, noise_level))
                
    # Ensure realistic bounds
    noisy_metrics['pass_at_1'] = np.clip(noisy_metrics['pass_at_1'], 0, 1)
    noisy_metrics['latency'] = max(15, noisy_metrics['latency'])
    noisy_metrics['energy_efficiency'] = max(0.5, noisy_metrics['energy_efficiency'])
    noisy_metrics['coherence'] = np.clip(noisy_metrics['coherence'], 0, 1)
    
    return noisy_metrics
