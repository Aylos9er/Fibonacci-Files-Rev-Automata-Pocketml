import numpy as np
import random
from typing import List, Dict, Tuple
import math
import re

class TinyLanguageModel:
    """
    Lightweight local language model for text generation and processing.
    No external API keys required.
    """
    
    def __init__(self, model_name: str = "TinyLM-1", vocab_size: int = 1000):
        self.model_name = model_name
        self.vocab_size = vocab_size
        self.hidden_size = 128
        self.sequence_length = 64
        
        # Initialize model parameters
        self.embedding_matrix = np.random.randn(vocab_size, self.hidden_size) * 0.1
        self.weight_matrix = np.random.randn(self.hidden_size, self.hidden_size) * 0.1
        self.output_matrix = np.random.randn(self.hidden_size, vocab_size) * 0.1
        
        # Simple vocabulary and tokenizer
        self.vocab = self._create_vocabulary()
        self.token_to_id = {token: i for i, token in enumerate(self.vocab)}
        self.id_to_token = {i: token for i, token in enumerate(self.vocab)}
        
        # Model state
        self.temperature = 0.8
        self.generation_history = []
        
    def _create_vocabulary(self) -> List[str]:
        """Create a simple vocabulary for the model."""
        # Common words and programming-related terms for PocketLM
        common_words = [
            "the", "and", "or", "in", "to", "of", "a", "an", "is", "are", "was", "were",
            "function", "class", "def", "return", "if", "else", "for", "while", "try",
            "import", "from", "as", "with", "lambda", "print", "str", "int", "float",
            "list", "dict", "set", "tuple", "array", "numpy", "tensor", "matrix",
            "graphene", "mesh", "helix", "symbiotic", "cellular", "automata", "swarm",
            "pocket", "model", "language", "processing", "neural", "network", "AI",
            "data", "code", "algorithm", "optimize", "efficient", "performance",
            "simulation", "visualization", "analysis", "compute", "calculate",
            "coordinate", "transform", "process", "update", "generate", "create",
            "build", "implement", "execute", "run", "test", "debug", "fix", "solve",
            "hello", "world", "example", "sample", "demo", "prototype", "framework",
            "system", "architecture", "design", "pattern", "structure", "component"
        ]
        
        # Add numbers, symbols, and padding tokens
        numbers = [str(i) for i in range(100)]
        symbols = [".", ",", ":", ";", "(", ")", "[", "]", "{", "}", "=", "+", "-", "*", "/"]
        special = ["<PAD>", "<START>", "<END>", "<UNK>"]
        
        # Combine and truncate to vocab_size
        full_vocab = special + common_words + numbers + symbols
        return full_vocab[:self.vocab_size]
    
    def tokenize(self, text: str) -> List[int]:
        """Simple tokenization of input text."""
        # Basic preprocessing
        text = text.lower().strip()
        text = re.sub(r'[^\w\s.,;:()[\]{}=+\-*/]', '', text)
        
        # Split into tokens
        tokens = text.split()
        
        # Convert to IDs
        token_ids = []
        for token in tokens:
            if token in self.token_to_id:
                token_ids.append(self.token_to_id[token])
            else:
                token_ids.append(self.token_to_id.get("<UNK>", 0))
        
        return token_ids[:self.sequence_length]  # Truncate if too long
    
    def detokenize(self, token_ids: List[int]) -> str:
        """Convert token IDs back to text."""
        tokens = []
        for token_id in token_ids:
            if token_id in self.id_to_token:
                token = self.id_to_token[token_id]
                if token not in ["<PAD>", "<START>", "<END>"]:
                    tokens.append(token)
        
        return " ".join(tokens)
    
    def forward_pass(self, input_ids: List[int]) -> np.ndarray:
        """Simple forward pass through the model."""
        if not input_ids:
            input_ids = [self.token_to_id.get("<START>", 0)]
        
        # Pad sequence
        padded_ids = input_ids + [0] * (self.sequence_length - len(input_ids))
        padded_ids = padded_ids[:self.sequence_length]
        
        # Embedding lookup
        embeddings = np.array([self.embedding_matrix[token_id] for token_id in padded_ids])
        
        # Simple RNN-like processing
        hidden_state = np.zeros(self.hidden_size)
        for i, embedding in enumerate(embeddings):
            hidden_state = np.tanh(np.dot(hidden_state, self.weight_matrix) + embedding)
        
        # Output projection
        logits = np.dot(hidden_state, self.output_matrix)
        
        # Apply temperature and softmax
        logits = logits / self.temperature
        exp_logits = np.exp(logits - np.max(logits))  # Numerical stability
        probabilities = exp_logits / np.sum(exp_logits)
        
        return probabilities
    
    def generate_text(self, prompt: str = "", max_length: int = 20) -> str:
        """Generate text based on a prompt."""
        input_ids = self.tokenize(prompt) if prompt else [self.token_to_id.get("<START>", 0)]
        generated_ids = input_ids.copy()
        
        for _ in range(max_length):
            # Get probabilities for next token
            probs = self.forward_pass(generated_ids[-self.sequence_length:])
            
            # Sample next token (with some randomness)
            if random.random() < 0.1:  # 10% chance of random selection
                next_token_id = random.randint(0, len(probs) - 1)
            else:
                next_token_id = np.argmax(probs)
            
            generated_ids.append(int(next_token_id))
            
            # Stop if we hit an end token
            if next_token_id == self.token_to_id.get("<END>", 1):
                break
        
        # Convert back to text
        generated_text = self.detokenize(generated_ids)
        self.generation_history.append({
            'prompt': prompt,
            'generated': generated_text,
            'length': len(generated_ids)
        })
        
        return generated_text
    
    def get_model_stats(self) -> Dict:
        """Get model statistics."""
        return {
            'model_name': self.model_name,
            'vocab_size': self.vocab_size,
            'hidden_size': self.hidden_size,
            'parameters': self.vocab_size * self.hidden_size + self.hidden_size ** 2 + self.hidden_size * self.vocab_size,
            'generations': len(self.generation_history),
            'temperature': self.temperature
        }

class LocalAISwarm:
    """
    Manages multiple tiny language models for distributed AI processing.
    """
    
    def __init__(self, num_models: int = 3):
        self.models = []
        self.model_names = ["TinyLM-Alpha", "TinyLM-Beta", "TinyLM-Gamma", "TinyLM-Delta", "TinyLM-Epsilon"]
        
        # Create diverse models
        for i in range(min(num_models, len(self.model_names))):
            model = TinyLanguageModel(
                model_name=self.model_names[i],
                vocab_size=800 + i * 50  # Slightly different vocab sizes
            )
            model.temperature = 0.6 + i * 0.1  # Different temperatures
            self.models.append(model)
    
    def generate_consensus(self, prompt: str, max_length: int = 15) -> Dict:
        """Generate text using multiple models and create consensus."""
        generations = []
        
        for model in self.models:
            generated_text = model.generate_text(prompt, max_length)
            generations.append({
                'model': model.model_name,
                'text': generated_text,
                'stats': model.get_model_stats()
            })
        
        # Simple consensus: pick the most common words
        all_words = []
        for gen in generations:
            all_words.extend(gen['text'].split())
        
        # Find most common words for consensus
        word_counts = {}
        for word in all_words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        # Create consensus text from most frequent words
        frequent_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        consensus_words = [word for word, count in frequent_words[:max_length] if count > 1]
        consensus_text = " ".join(consensus_words)
        
        return {
            'prompt': prompt,
            'consensus': consensus_text,
            'individual_generations': generations,
            'swarm_size': len(self.models),
            'total_parameters': sum(model.get_model_stats()['parameters'] for model in self.models)
        }
    
    def process_mesh_data(self, mesh_state: Dict) -> Dict:
        """Process mesh data through AI swarm for intelligent insights."""
        # Create prompts based on mesh state
        coherence = mesh_state.get('coherence', 0.5)
        energy = np.mean(mesh_state.get('energy', [0.5]))
        
        if coherence > 0.7:
            prompt = "high coherence optimal mesh"
        elif coherence > 0.4:
            prompt = "moderate coherence stable system"
        else:
            prompt = "low coherence optimization needed"
        
        if energy > 0.6:
            prompt += " high energy active processing"
        else:
            prompt += " low energy efficient mode"
        
        # Generate AI insights
        ai_result = self.generate_consensus(prompt, max_length=10)
        
        # Create recommendations
        recommendations = []
        if coherence < 0.5:
            recommendations.append("Increase mesh coordination")
        if energy < 0.3:
            recommendations.append("Boost stimuli intensity")
        if len(ai_result['consensus'].split()) < 3:
            recommendations.append("Diversify swarm parameters")
        
        return {
            'ai_analysis': ai_result,
            'recommendations': recommendations,
            'confidence': min(1.0, coherence + energy) / 2,
            'processing_mode': 'local_ai_swarm'
        }
    
    def get_swarm_stats(self) -> Dict:
        """Get comprehensive swarm statistics."""
        model_stats = [model.get_model_stats() for model in self.models]
        
        return {
            'swarm_size': len(self.models),
            'model_stats': model_stats,
            'total_parameters': sum(stats['parameters'] for stats in model_stats),
            'total_generations': sum(stats['generations'] for stats in model_stats),
            'average_temperature': np.mean([stats['temperature'] for stats in model_stats]),
            'model_diversity': len(set(stats['vocab_size'] for stats in model_stats))
        }

def create_pocket_ai_models(num_models: int = 3) -> LocalAISwarm:
    """Factory function to create local AI models for PocketLM."""
    return LocalAISwarm(num_models)