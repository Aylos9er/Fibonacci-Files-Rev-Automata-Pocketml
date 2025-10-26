import numpy as np
import json
import random
from typing import Dict, List, Tuple, Optional
import time

class TinyClusterModel:
    """
    Lightweight implementation mimicking real tiny LLM behavior for cluster deployment.
    Based on real-world tiny models: Qwen2.5-0.5B, SmolLM2-360M, MiniLM-L6-v2
    """
    
    def __init__(self, model_name: str, params_count: str, specialization: str):
        self.model_name = model_name
        self.params_count = params_count  # "500M", "360M", "22M"
        self.specialization = specialization
        self.node_id = random.randint(1000, 9999)
        
        # Model state
        self.is_active = True
        self.inference_count = 0
        self.avg_latency = 0.0
        self.cluster_role = "worker"  # worker, coordinator, or backup
        
        # Specialized vocabularies based on real tiny model capabilities
        self.capabilities = self._define_capabilities()
        self.context_window = self._get_context_window()
        
    def _define_capabilities(self) -> Dict:
        """Define capabilities based on real tiny model specs."""
        if "Qwen2.5" in self.model_name:
            return {
                "languages": 29,
                "context_length": 128000,
                "generation_length": 8192,
                "strengths": ["multi-turn dialogue", "reasoning", "coding"],
                "inference_speed": "fast",
                "memory_efficient": True
            }
        elif "SmolLM2" in self.model_name:
            return {
                "languages": 15,
                "context_length": 8192,
                "generation_length": 2048,
                "strengths": ["edge deployment", "IoT", "ARM optimization"],
                "inference_speed": "ultra-fast",
                "memory_efficient": True
            }
        elif "MiniLM" in self.model_name:
            return {
                "languages": 50,
                "context_length": 512,
                "generation_length": 128,
                "strengths": ["embeddings", "semantic search", "clustering"],
                "inference_speed": "blazing-fast",
                "memory_efficient": True
            }
        else:
            return {
                "languages": 10,
                "context_length": 2048,
                "generation_length": 512,
                "strengths": ["general purpose"],
                "inference_speed": "moderate",
                "memory_efficient": False
            }
    
    def _get_context_window(self) -> int:
        """Get context window size."""
        return self.capabilities.get("context_length", 2048)
    
    def generate(self, prompt: str, max_tokens: int = 50) -> Dict:
        """Generate text with cluster-aware processing."""
        start_time = time.time()
        
        # Simulate different tiny model behaviors
        if "Qwen2.5" in self.model_name:
            response = self._qwen_style_generation(prompt, max_tokens)
        elif "SmolLM2" in self.model_name:
            response = self._smollm_style_generation(prompt, max_tokens)
        elif "MiniLM" in self.model_name:
            response = self._minilm_style_generation(prompt, max_tokens)
        else:
            response = self._generic_generation(prompt, max_tokens)
        
        # Calculate inference metrics
        latency = (time.time() - start_time) * 1000  # ms
        self._update_metrics(latency)
        
        return {
            "text": response,
            "model": self.model_name,
            "node_id": self.node_id,
            "latency_ms": round(latency, 2),
            "tokens_generated": len(response.split()),
            "cluster_role": self.cluster_role
        }
    
    def _qwen_style_generation(self, prompt: str, max_tokens: int) -> str:
        """Qwen2.5-0.5B style: Multi-turn dialogue and reasoning focused."""
        keywords = prompt.lower().split()
        
        if any(word in keywords for word in ["mesh", "graphene", "tensor"]):
            responses = [
                "optimizing tensor mesh configuration",
                "graphene lattice shows coherent patterns",
                "mesh energy distribution requires balancing",
                "tensor processing achieved stable state"
            ]
        elif any(word in keywords for word in ["automata", "cellular", "evolution"]):
            responses = [
                "cellular evolution shows emergent behavior",
                "automata rules converging to stable patterns",
                "forward-reverse cycles optimize dynamics",
                "cellular states demonstrate coherent evolution"
            ]
        else:
            responses = [
                "analyzing system parameters for optimization",
                "implementing efficient processing algorithms",
                "coordinating distributed computation tasks",
                "enhancing performance through smart allocation"
            ]
        
        return random.choice(responses)
    
    def _smollm_style_generation(self, prompt: str, max_tokens: int) -> str:
        """SmolLM2-360M style: Edge-optimized, ARM efficient."""
        keywords = prompt.lower().split()
        
        # Edge/IoT focused responses
        if any(word in keywords for word in ["swarm", "coordinate", "cluster"]):
            responses = [
                "edge swarm coordination active",
                "distributed nodes synchronized",
                "cluster efficiency optimized locally",
                "ARM processors handling load efficiently"
            ]
        elif any(word in keywords for word in ["energy", "power", "efficient"]):
            responses = [
                "low power mode engaged",
                "energy efficient processing active",
                "ARM optimization reducing consumption",
                "edge inference minimizing overhead"
            ]
        else:
            responses = [
                "edge processing optimized",
                "local inference complete",
                "ARM acceleration active",
                "IoT deployment ready"
            ]
        
        return random.choice(responses)
    
    def _minilm_style_generation(self, prompt: str, max_tokens: int) -> str:
        """MiniLM-L6-v2 style: Embeddings and semantic search focused."""
        keywords = prompt.lower().split()
        
        # Semantic/embedding focused responses
        if any(word in keywords for word in ["analyze", "search", "semantic"]):
            responses = [
                "semantic patterns identified",
                "embedding vectors clustered",
                "similarity search optimized",
                "vector space analysis complete"
            ]
        elif any(word in keywords for word in ["cluster", "group", "similar"]):
            responses = [
                "clustering algorithm converged",
                "similar patterns grouped",
                "vector clustering successful",
                "semantic groups identified"
            ]
        else:
            responses = [
                "embeddings processed",
                "vectors normalized",
                "similarity computed",
                "search indexed"
            ]
        
        return random.choice(responses)
    
    def _generic_generation(self, prompt: str, max_tokens: int) -> str:
        """Generic tiny model generation."""
        return "processing request through tiny model cluster"
    
    def _update_metrics(self, latency: float):
        """Update inference metrics."""
        self.inference_count += 1
        self.avg_latency = (self.avg_latency * (self.inference_count - 1) + latency) / self.inference_count
    
    def get_cluster_stats(self) -> Dict:
        """Get cluster node statistics."""
        return {
            "model_name": self.model_name,
            "node_id": self.node_id,
            "params_count": self.params_count,
            "specialization": self.specialization,
            "cluster_role": self.cluster_role,
            "inference_count": self.inference_count,
            "avg_latency_ms": round(self.avg_latency, 2),
            "is_active": self.is_active,
            "capabilities": self.capabilities,
            "status": "healthy" if self.is_active else "inactive"
        }

class TinyModelCluster:
    """
    Mini swarm of three tiny language models for distributed inference.
    Based on real-world cluster architectures: distributed-llama, llm-swarm, Ray+vLLM
    """
    
    def __init__(self):
        # Create three real-world tiny models
        self.models = [
            TinyClusterModel("Qwen2.5-0.5B-Instruct", "500M", "dialogue_reasoning"),
            TinyClusterModel("SmolLM2-360M", "360M", "edge_optimization"),
            TinyClusterModel("MiniLM-L6-v2", "22M", "semantic_embeddings")
        ]
        
        # Assign cluster roles
        self.models[0].cluster_role = "coordinator"  # Qwen as coordinator
        self.models[1].cluster_role = "worker"       # SmolLM as worker
        self.models[2].cluster_role = "backup"       # MiniLM as backup/specialist
        
        self.cluster_stats = {
            "total_nodes": len(self.models),
            "active_nodes": len([m for m in self.models if m.is_active]),
            "total_inferences": 0,
            "cluster_health": "healthy"
        }
        
        self.load_balancer_strategy = "round_robin"  # round_robin, capability_based, latency_based
        self.current_model_index = 0
        
    def distributed_inference(self, prompt: str, strategy: str = "consensus") -> Dict:
        """Perform distributed inference across the cluster."""
        if strategy == "consensus":
            return self._consensus_inference(prompt)
        elif strategy == "load_balanced":
            return self._load_balanced_inference(prompt)
        elif strategy == "specialized":
            return self._specialized_inference(prompt)
        else:
            return self._failover_inference(prompt)
    
    def _consensus_inference(self, prompt: str) -> Dict:
        """All models process and create consensus."""
        results = []
        for model in self.models:
            if model.is_active:
                result = model.generate(prompt)
                results.append(result)
        
        # Simple consensus: combine responses
        combined_text = " | ".join([r["text"] for r in results])
        avg_latency = np.mean([r["latency_ms"] for r in results])
        
        self.cluster_stats["total_inferences"] += 1
        
        return {
            "strategy": "consensus",
            "combined_response": combined_text,
            "individual_responses": results,
            "cluster_latency_ms": round(avg_latency, 2),
            "participating_nodes": len(results),
            "cluster_efficiency": self._calculate_cluster_efficiency()
        }
    
    def _load_balanced_inference(self, prompt: str) -> Dict:
        """Load balance across active models."""
        active_models = [m for m in self.models if m.is_active]
        if not active_models:
            return {"error": "No active models in cluster"}
        
        # Round robin load balancing
        selected_model = active_models[self.current_model_index % len(active_models)]
        self.current_model_index += 1
        
        result = selected_model.generate(prompt)
        self.cluster_stats["total_inferences"] += 1
        
        return {
            "strategy": "load_balanced",
            "response": result["text"],
            "selected_model": result["model"],
            "node_id": result["node_id"],
            "latency_ms": result["latency_ms"],
            "load_balance_index": self.current_model_index - 1
        }
    
    def _specialized_inference(self, prompt: str) -> Dict:
        """Route to most appropriate specialist model."""
        keywords = prompt.lower().split()
        
        # Route based on prompt content
        if any(word in keywords for word in ["dialogue", "reasoning", "conversation"]):
            selected_model = self.models[0]  # Qwen2.5
        elif any(word in keywords for word in ["edge", "optimize", "efficient", "ARM"]):
            selected_model = self.models[1]  # SmolLM2
        elif any(word in keywords for word in ["search", "semantic", "embedding", "similar"]):
            selected_model = self.models[2]  # MiniLM
        else:
            selected_model = self.models[0]  # Default to coordinator
        
        if not selected_model.is_active:
            selected_model = next((m for m in self.models if m.is_active), self.models[0])
        
        result = selected_model.generate(prompt)
        self.cluster_stats["total_inferences"] += 1
        
        return {
            "strategy": "specialized",
            "response": result["text"],
            "selected_specialist": result["model"],
            "specialization_reason": selected_model.specialization,
            "node_id": result["node_id"],
            "latency_ms": result["latency_ms"]
        }
    
    def _failover_inference(self, prompt: str) -> Dict:
        """Failover strategy with redundancy."""
        # Try coordinator first
        coordinator = next((m for m in self.models if m.cluster_role == "coordinator"), None)
        
        if coordinator and coordinator.is_active:
            result = coordinator.generate(prompt)
            backup_result = None
            
            # Also get backup response for redundancy
            backup = next((m for m in self.models if m.cluster_role == "backup"), None)
            if backup and backup.is_active:
                backup_result = backup.generate(prompt)
            
            self.cluster_stats["total_inferences"] += 1
            
            return {
                "strategy": "failover",
                "primary_response": result["text"],
                "backup_response": backup_result["text"] if backup_result else None,
                "coordinator_node": result["node_id"],
                "backup_node": backup_result["node_id"] if backup_result else None,
                "latency_ms": result["latency_ms"],
                "redundancy": backup_result is not None
            }
        else:
            # Failover to any active worker
            active_worker = next((m for m in self.models if m.is_active), None)
            if active_worker:
                result = active_worker.generate(prompt)
                self.cluster_stats["total_inferences"] += 1
                
                return {
                    "strategy": "failover",
                    "response": result["text"],
                    "failover_model": result["model"],
                    "note": "coordinator_unavailable",
                    "latency_ms": result["latency_ms"]
                }
            else:
                return {"error": "entire_cluster_offline"}
    
    def _calculate_cluster_efficiency(self) -> float:
        """Calculate overall cluster efficiency."""
        active_count = len([m for m in self.models if m.is_active])
        total_count = len(self.models)
        
        if total_count == 0:
            return 0.0
        
        base_efficiency = active_count / total_count
        
        # Factor in average latency (lower is better)
        avg_latencies = [m.avg_latency for m in self.models if m.avg_latency > 0]
        if avg_latencies:
            latency_factor = max(0.1, 1.0 - (float(np.mean(avg_latencies)) / 1000))  # Normalize to seconds
            base_efficiency *= latency_factor
        
        return float(round(base_efficiency, 3))
    
    def get_cluster_overview(self) -> Dict:
        """Get comprehensive cluster status."""
        return {
            "cluster_info": {
                "total_models": len(self.models),
                "active_models": len([m for m in self.models if m.is_active]),
                "total_parameters": "882M",  # 500M + 360M + 22M
                "cluster_health": self._assess_cluster_health(),
                "load_balance_strategy": self.load_balancer_strategy
            },
            "model_stats": [model.get_cluster_stats() for model in self.models],
            "performance_metrics": {
                "total_inferences": self.cluster_stats["total_inferences"],
                "cluster_efficiency": self._calculate_cluster_efficiency(),
                "avg_cluster_latency": self._get_avg_cluster_latency()
            }
        }
    
    def _assess_cluster_health(self) -> str:
        """Assess overall cluster health."""
        active_count = len([m for m in self.models if m.is_active])
        
        if active_count == len(self.models):
            return "healthy"
        elif active_count >= len(self.models) * 0.6:
            return "degraded"
        elif active_count > 0:
            return "critical"
        else:
            return "offline"
    
    def _get_avg_cluster_latency(self) -> float:
        """Get average latency across all active models."""
        active_latencies = [m.avg_latency for m in self.models if m.is_active and m.avg_latency > 0]
        if active_latencies:
            return float(round(np.mean(active_latencies), 2))
        else:
            return 0.0
    
    def scale_cluster(self, action: str, model_index: int | None = None):
        """Scale cluster up/down (simulate adding/removing nodes)."""
        if action == "add_node" and len(self.models) < 5:
            new_model = TinyClusterModel(f"TinyLlama-1.1B-{len(self.models)}", "1.1B", "general_purpose")
            new_model.cluster_role = "worker"
            self.models.append(new_model)
            
        elif action == "remove_node" and model_index is not None and 0 <= model_index < len(self.models):
            if len(self.models) > 1:  # Keep at least one model
                self.models[model_index].is_active = False
                
        elif action == "restart_node" and model_index is not None:
            if 0 <= model_index < len(self.models):
                self.models[model_index].is_active = True
                self.models[model_index].inference_count = 0
                self.models[model_index].avg_latency = 0.0

def create_tiny_model_cluster() -> TinyModelCluster:
    """Factory function to create the three tiny model cluster."""
    return TinyModelCluster()