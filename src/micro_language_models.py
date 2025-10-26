import numpy as np
import random
from typing import Dict, List, Tuple
import math

class MicroPM:
    """Ultra-lightweight micro language model for specialized tasks."""
    
    def __init__(self, name: str, specialization: str, vocab_size: int = 300):
        self.name = name
        self.specialization = specialization
        self.vocab_size = vocab_size
        self.hidden_size = 64  # Very small for micro model
        
        # Specialized vocabularies based on domain
        self.vocab = self._create_specialized_vocab()
        self.token_to_id = {token: i for i, token in enumerate(self.vocab)}
        self.id_to_token = {i: token for i, token in enumerate(self.vocab)}
        
        # Micro neural network weights
        self.W_embed = np.random.randn(vocab_size, self.hidden_size) * 0.1
        self.W_hidden = np.random.randn(self.hidden_size, self.hidden_size) * 0.1
        self.W_output = np.random.randn(self.hidden_size, vocab_size) * 0.1
        
        self.temperature = 0.7
        self.generation_count = 0
        
    def _create_specialized_vocab(self) -> List[str]:
        """Create vocabulary specialized for this micro model's domain."""
        base_tokens = ["<pad>", "<start>", "<end>", "<unk>"]
        
        if self.specialization == "mesh_processor":
            domain_tokens = [
                "mesh", "graphene", "node", "energy", "field", "tensor", "matrix",
                "coordinate", "position", "lattice", "hexagonal", "carbon", "bond",
                "stimuli", "light", "response", "excitation", "propagate", "wave",
                "coherence", "stable", "dynamic", "interact", "couple", "resonate",
                "optimize", "enhance", "balance", "efficient", "process", "compute",
                "analyze", "measure", "detect", "sense", "adapt", "adjust", "tune",
                "x", "y", "z", "vector", "scalar", "magnitude", "direction", "angle",
                "frequency", "amplitude", "phase", "sync", "align", "calibrate"
            ]
        elif self.specialization == "automata_processor":
            domain_tokens = [
                "cell", "automata", "state", "rule", "neighbor", "evolution", "step",
                "forward", "reverse", "cycle", "iteration", "generation", "pattern",
                "emerge", "converge", "diverge", "stable", "chaotic", "periodic",
                "birth", "death", "survive", "activate", "deactivate", "toggle",
                "boolean", "binary", "logic", "and", "or", "not", "xor", "gate",
                "memory", "history", "trace", "path", "sequence", "chain", "link",
                "probability", "random", "noise", "signal", "filter", "smooth",
                "threshold", "boundary", "edge", "corner", "center", "local", "global"
            ]
        else:  # swarm_coordinator
            domain_tokens = [
                "swarm", "agent", "pocket", "instance", "cluster", "group", "team",
                "coordinate", "synchronize", "communicate", "broadcast", "message",
                "leader", "follower", "consensus", "vote", "decide", "negotiate",
                "strategy", "plan", "execute", "monitor", "control", "manage",
                "efficient", "optimal", "balance", "load", "distribute", "allocate",
                "resource", "capacity", "bandwidth", "throughput", "latency", "delay",
                "network", "topology", "connection", "link", "route", "path", "flow",
                "priority", "queue", "schedule", "task", "job", "work", "process"
            ]
        
        # Add common programming and math terms
        common_tokens = [
            "function", "class", "method", "variable", "parameter", "return", "value",
            "array", "list", "data", "input", "output", "result", "compute", "calculate",
            "sum", "mean", "max", "min", "norm", "dot", "multiply", "add", "subtract"
        ]
        
        # Combine and limit to vocab_size
        all_tokens = base_tokens + domain_tokens + common_tokens
        return all_tokens[:self.vocab_size]
    
    def tokenize(self, text: str) -> List[int]:
        """Tokenize input text for this micro model."""
        words = text.lower().split()[:16]  # Very short sequences for micro model
        token_ids = []
        
        for word in words:
            if word in self.token_to_id:
                token_ids.append(self.token_to_id[word])
            else:
                token_ids.append(self.token_to_id.get("<unk>", 3))
        
        return token_ids
    
    def generate(self, prompt: str = "", max_length: int = 8) -> str:
        """Generate text using micro neural network."""
        input_ids = self.tokenize(prompt) if prompt else [1]  # <start> token
        
        for _ in range(max_length):
            # Forward pass through micro network
            if not input_ids:
                break
                
            # Simple embedding
            last_token = input_ids[-1] % self.vocab_size
            embed = self.W_embed[last_token]
            
            # Hidden layer
            hidden = np.tanh(np.dot(embed, self.W_hidden))
            
            # Output layer
            logits = np.dot(hidden, self.W_output)
            logits = logits / self.temperature
            
            # Softmax
            exp_logits = np.exp(logits - np.max(logits))
            probs = exp_logits / np.sum(exp_logits)
            
            # Sample next token
            next_token = np.random.choice(len(probs), p=probs)
            
            # Stop conditions
            if next_token == 2:  # <end> token
                break
                
            input_ids.append(next_token)
        
        # Convert back to text
        words = []
        for token_id in input_ids[1:]:  # Skip <start>
            if token_id in self.id_to_token and self.id_to_token[token_id] not in ["<pad>", "<start>", "<end>"]:
                words.append(self.id_to_token[token_id])
        
        self.generation_count += 1
        return " ".join(words)
    
    def analyze_state(self, state_data: Dict) -> str:
        """Analyze state data and generate specialized insights."""
        if self.specialization == "mesh_processor":
            energy_level = state_data.get('energy', 0.5)
            coherence = state_data.get('coherence', 0.5)
            
            if energy_level > 0.7:
                prompt = "high energy mesh optimize"
            elif coherence < 0.4:
                prompt = "low coherence stabilize"
            else:
                prompt = "mesh balance efficient"
                
        elif self.specialization == "automata_processor":
            if 'ca_state' in state_data:
                active_ratio = np.mean(state_data['ca_state']) if len(state_data['ca_state']) > 0 else 0.5
                if active_ratio > 0.6:
                    prompt = "high activation pattern"
                elif active_ratio < 0.3:
                    prompt = "low activation evolve"
                else:
                    prompt = "balanced automata state"
            else:
                prompt = "cellular evolution step"
                
        else:  # swarm_coordinator
            num_agents = state_data.get('swarm_size', 3)
            efficiency = state_data.get('efficiency', 0.5)
            
            if efficiency > 0.7:
                prompt = "swarm efficient coordinate"
            elif num_agents > 5:
                prompt = "large swarm manage"
            else:
                prompt = "optimize coordination strategy"
        
        return self.generate(prompt, max_length=6)
    
    def get_stats(self) -> Dict:
        """Get micro model statistics."""
        return {
            'name': self.name,
            'specialization': self.specialization,
            'vocab_size': self.vocab_size,
            'parameters': self.vocab_size * self.hidden_size * 2 + self.hidden_size * self.hidden_size,
            'generations': self.generation_count,
            'temperature': self.temperature
        }

class ThreePartMicroSystem:
    """System managing three specialized micro language models."""
    
    def __init__(self):
        # Create three specialized micro PMs
        self.mesh_pm = MicroPM("MeshPM", "mesh_processor", vocab_size=250)
        self.automata_pm = MicroPM("AutomataPM", "automata_processor", vocab_size=280)
        self.swarm_pm = MicroPM("SwarmPM", "swarm_coordinator", vocab_size=300)
        
        self.models = [self.mesh_pm, self.automata_pm, self.swarm_pm]
        self.interaction_history = []
        
    def process_system_state(self, system_state: Dict) -> Dict:
        """Process system state through all three micro PMs."""
        results = {}
        
        # Each micro PM analyzes relevant parts of the system state
        mesh_analysis = self.mesh_pm.analyze_state({
            'energy': system_state.get('mesh_energy', 0.5),
            'coherence': system_state.get('coherence', 0.5)
        })
        
        automata_analysis = self.automata_pm.analyze_state({
            'ca_state': system_state.get('ca_state', [0.5])
        })
        
        swarm_analysis = self.swarm_pm.analyze_state({
            'swarm_size': system_state.get('num_pockets', 3),
            'efficiency': system_state.get('swarm_efficiency', 0.5)
        })
        
        results = {
            'mesh_insights': mesh_analysis,
            'automata_insights': automata_analysis,
            'swarm_insights': swarm_analysis,
            'combined_analysis': self._combine_analyses(mesh_analysis, automata_analysis, swarm_analysis)
        }
        
        self.interaction_history.append(results)
        return results
    
    def _combine_analyses(self, mesh: str, automata: str, swarm: str) -> str:
        """Combine insights from all three micro PMs."""
        all_words = (mesh + " " + automata + " " + swarm).split()
        
        # Simple word frequency analysis
        word_counts = {}
        for word in all_words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        # Get most frequent meaningful words
        frequent_words = [word for word, count in word_counts.items() if count >= 2]
        if not frequent_words:
            frequent_words = all_words[:3]  # Fallback to first few words
        
        return " ".join(frequent_words[:5])  # Max 5 words for combined analysis
    
    def generate_collaborative_text(self, prompt: str) -> Dict:
        """Generate text collaboratively using all three micro PMs."""
        mesh_response = self.mesh_pm.generate(prompt + " mesh", max_length=5)
        automata_response = self.automata_pm.generate(prompt + " automata", max_length=5)
        swarm_response = self.swarm_pm.generate(prompt + " swarm", max_length=5)
        
        return {
            'prompt': prompt,
            'mesh_response': mesh_response,
            'automata_response': automata_response,
            'swarm_response': swarm_response,
            'collaborative_summary': self._combine_analyses(mesh_response, automata_response, swarm_response)
        }
    
    def get_system_stats(self) -> Dict:
        """Get comprehensive system statistics."""
        total_params = sum(model.get_stats()['parameters'] for model in self.models)
        total_generations = sum(model.get_stats()['generations'] for model in self.models)
        
        return {
            'total_micro_models': len(self.models),
            'model_details': [model.get_stats() for model in self.models],
            'total_parameters': total_params,
            'total_generations': total_generations,
            'specializations': [model.specialization for model in self.models],
            'interaction_count': len(self.interaction_history),
            'system_efficiency': min(1.0, total_generations / max(total_params / 1000, 1))
        }
    
    def update_temperatures(self, mesh_temp: float, automata_temp: float, swarm_temp: float):
        """Update temperature settings for all micro models."""
        self.mesh_pm.temperature = max(0.1, min(2.0, mesh_temp))
        self.automata_pm.temperature = max(0.1, min(2.0, automata_temp))
        self.swarm_pm.temperature = max(0.1, min(2.0, swarm_temp))

def create_three_part_micro_system() -> ThreePartMicroSystem:
    """Factory function to create the three-part micro PM system."""
    return ThreePartMicroSystem()