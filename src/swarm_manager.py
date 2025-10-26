import numpy as np
from typing import Dict, List, Tuple
import random

class SwarmManager:
    """
    Manages the modular swarm of pocket instances for distributed processing.
    Implements coordination strategies for 3-5 pocket instances.
    """
    
    def __init__(self, num_pockets: int = 3):
        self.num_pockets = min(max(num_pockets, 1), 10)  # Limit between 1-10
        self.coordination_history = []
        self.communication_matrix = np.eye(self.num_pockets)
        self.global_state = {}
        self.pockets = self._initialize_pockets()
        self._establish_connections()
        
    def _initialize_pockets(self) -> List[Dict]:
        """Initialize pocket instances with unique properties."""
        pockets = []
        
        for i in range(self.num_pockets):
            pocket = {
                'id': i,
                'position': {
                    'x': random.uniform(-5, 5),
                    'y': random.uniform(-5, 5),
                    'z': random.uniform(-1, 1)
                },
                'specialization': self._assign_specialization(i),
                'activity_level': random.uniform(0.3, 1.0),
                'processing_capacity': random.uniform(0.5, 1.0),
                'local_state': np.random.rand(10) * 0.5,  # Local tensor state
                'connections': [],
                'energy': random.uniform(0.7, 1.0),
                'coordination_weight': 1.0 / self.num_pockets
            }
            pockets.append(pocket)
            
        return pockets
    
    def _assign_specialization(self, pocket_id: int) -> str:
        """Assign specialization to each pocket based on ID."""
        specializations = [
            'tensor_processing',    # Primary tensor operations
            'mesh_coordination',    # Mesh state management
            'stimuli_response',     # Environmental response
            'ca_evolution',         # Cellular automata processing
            'energy_management'     # Power and resource optimization
        ]
        return specializations[pocket_id % len(specializations)]
    
    def _establish_connections(self):
        """Establish communication connections between pockets."""
        for i, pocket in enumerate(self.pockets):
            # Connect to adjacent pockets and one random distant pocket
            connections = []
            
            # Adjacent connections
            if i > 0:
                connections.append(i - 1)
            if i < len(self.pockets) - 1:
                connections.append(i + 1)
                
            # Random distant connection for diversity
            if len(self.pockets) > 3:
                distant_candidates = [j for j in range(len(self.pockets)) 
                                    if j not in connections and j != i]
                if distant_candidates:
                    connections.append(random.choice(distant_candidates))
            
            pocket['connections'] = connections
            
            # Update communication matrix
            for j in connections:
                self.communication_matrix[i, j] = 1
                self.communication_matrix[j, i] = 1
    
    def coordinate_pockets(self, mesh_state: Dict, strategy: str = "Synchronous") -> Dict:
        """Coordinate pocket instances based on chosen strategy."""
        if strategy == "Synchronous":
            return self._synchronous_coordination(mesh_state)
        elif strategy == "Asynchronous":
            return self._asynchronous_coordination(mesh_state)
        elif strategy == "Adaptive":
            return self._adaptive_coordination(mesh_state)
        else:
            return self._synchronous_coordination(mesh_state)  # Default
    
    def _synchronous_coordination(self, mesh_state: Dict) -> Dict:
        """Synchronous coordination where all pockets update simultaneously."""
        global_tensor_state = mesh_state.get('tensor_magnitude', 0)
        global_energy = mesh_state.get('energy', np.zeros((10, 10)))
        
        # Update all pockets based on global state
        for pocket in self.pockets:
            self._update_pocket_state(pocket, mesh_state, "synchronous")
        
        # Calculate consensus and efficiency
        consensus = self._calculate_consensus()
        efficiency = self._calculate_swarm_efficiency()
        
        return {
            'strategy': 'Synchronous',
            'consensus': consensus,
            'efficiency': efficiency,
            'pocket_states': [self._get_pocket_summary(p) for p in self.pockets],
            'communication_load': np.sum(self.communication_matrix) / (self.num_pockets ** 2)
        }
    
    def _asynchronous_coordination(self, mesh_state: Dict) -> Dict:
        """Asynchronous coordination with staggered updates."""
        # Only update a subset of pockets each cycle
        active_pockets = random.sample(range(self.num_pockets), 
                                     max(1, self.num_pockets // 2))
        
        for pocket_id in active_pockets:
            pocket = self.pockets[pocket_id]
            self._update_pocket_state(pocket, mesh_state, "asynchronous")
            
            # Propagate information to connected pockets
            self._propagate_information(pocket)
        
        consensus = self._calculate_consensus()
        efficiency = self._calculate_swarm_efficiency() * 1.1  # Async bonus
        
        return {
            'strategy': 'Asynchronous',
            'consensus': consensus,
            'efficiency': efficiency,
            'pocket_states': [self._get_pocket_summary(p) for p in self.pockets],
            'active_pockets': len(active_pockets),
            'communication_load': len(active_pockets) / self.num_pockets
        }
    
    def _adaptive_coordination(self, mesh_state: Dict) -> Dict:
        """Adaptive coordination that switches strategy based on conditions."""
        # Decide strategy based on mesh state
        energy_level = np.mean(mesh_state.get('energy', [0.5]))
        coherence = mesh_state.get('coherence', 0.5)
        
        if energy_level > 0.7 and coherence > 0.6:
            # High energy and coherence: use synchronous for stability
            return self._synchronous_coordination(mesh_state)
        elif energy_level < 0.3:
            # Low energy: use asynchronous to save resources
            result = self._asynchronous_coordination(mesh_state)
            result['strategy'] = 'Adaptive (Async)'
            return result
        else:
            # Mixed conditions: hybrid approach
            return self._hybrid_coordination(mesh_state)
    
    def _hybrid_coordination(self, mesh_state: Dict) -> Dict:
        """Hybrid coordination combining sync and async elements."""
        # Critical pockets update synchronously
        critical_specializations = ['tensor_processing', 'mesh_coordination']
        critical_pockets = [p for p in self.pockets 
                          if p['specialization'] in critical_specializations]
        
        # Update critical pockets synchronously
        for pocket in critical_pockets:
            self._update_pocket_state(pocket, mesh_state, "synchronous")
        
        # Update remaining pockets asynchronously
        remaining_pockets = [p for p in self.pockets if p not in critical_pockets]
        active_remaining = random.sample(remaining_pockets, 
                                       max(1, len(remaining_pockets) // 2))
        
        for pocket in active_remaining:
            self._update_pocket_state(pocket, mesh_state, "asynchronous")
            self._propagate_information(pocket)
        
        consensus = self._calculate_consensus()
        efficiency = self._calculate_swarm_efficiency() * 1.05  # Small hybrid bonus
        
        return {
            'strategy': 'Adaptive (Hybrid)',
            'consensus': consensus,
            'efficiency': efficiency,
            'pocket_states': [self._get_pocket_summary(p) for p in self.pockets],
            'critical_pockets': len(critical_pockets),
            'communication_load': 0.7  # Medium load
        }
    
    def _update_pocket_state(self, pocket: Dict, mesh_state: Dict, update_type: str):
        """Update individual pocket state based on mesh and coordination."""
        # Specialization-based processing
        if pocket['specialization'] == 'tensor_processing':
            influence = mesh_state.get('tensor_magnitude', 0) * 0.1
        elif pocket['specialization'] == 'mesh_coordination':
            influence = mesh_state.get('coherence', 0) * 0.1
        elif pocket['specialization'] == 'stimuli_response':
            influence = np.mean(mesh_state.get('stimuli', [0])) * 0.2
        else:
            influence = mesh_state.get('energy', np.array([0.5])).mean() * 0.1
        
        # Update local state
        learning_rate = 0.1 if update_type == "synchronous" else 0.05
        pocket['local_state'] += learning_rate * (influence - pocket['local_state'])
        
        # Update activity based on local state
        pocket['activity_level'] = np.clip(
            np.mean(pocket['local_state']) + random.uniform(-0.1, 0.1),
            0.1, 1.0
        )
        
        # Energy consumption based on activity
        consumption = 0.01 * pocket['activity_level']
        pocket['energy'] = np.clip(pocket['energy'] - consumption + 0.02, 0.1, 1.0)
        
        # Update position based on local gradients (simple movement)
        gradient = np.mean(pocket['local_state']) - 0.5
        movement_scale = 0.1
        pocket['position']['x'] += movement_scale * gradient * random.uniform(-1, 1)
        pocket['position']['y'] += movement_scale * gradient * random.uniform(-1, 1)
        
        # Keep positions bounded
        for coord in ['x', 'y']:
            pocket['position'][coord] = np.clip(pocket['position'][coord], -10, 10)
    
    def _propagate_information(self, source_pocket: Dict):
        """Propagate information from source pocket to connected pockets."""
        source_id = source_pocket['id']
        
        for target_id in source_pocket['connections']:
            if target_id < len(self.pockets):
                target_pocket = self.pockets[target_id]
                
                # Information exchange
                exchange_rate = 0.05
                avg_state = (source_pocket['local_state'] + target_pocket['local_state']) / 2
                
                source_pocket['local_state'] += exchange_rate * (avg_state - source_pocket['local_state'])
                target_pocket['local_state'] += exchange_rate * (avg_state - target_pocket['local_state'])
    
    def _calculate_consensus(self) -> float:
        """Calculate consensus level among pockets."""
        if len(self.pockets) < 2:
            return 1.0
        
        # Calculate pairwise similarities
        similarities = []
        for i in range(len(self.pockets)):
            for j in range(i + 1, len(self.pockets)):
                state_i = self.pockets[i]['local_state']
                state_j = self.pockets[j]['local_state']
                
                # Cosine similarity
                similarity = np.dot(state_i, state_j) / (np.linalg.norm(state_i) * np.linalg.norm(state_j))
                similarities.append(max(0, similarity))  # Only positive similarities
        
        return float(np.mean(similarities)) if similarities else 0.0
    
    def _calculate_swarm_efficiency(self) -> float:
        """Calculate overall swarm efficiency."""
        # Factors: energy levels, activity balance, communication effectiveness
        avg_energy = np.mean([p['energy'] for p in self.pockets])
        
        # Activity balance (penalize extreme imbalances)
        activities = [p['activity_level'] for p in self.pockets]
        activity_balance = 1.0 - np.std(activities)  # Lower std = better balance
        
        # Communication effectiveness
        comm_effectiveness = np.sum(self.communication_matrix) / (self.num_pockets ** 2)
        
        # Combined efficiency
        efficiency = 0.4 * avg_energy + 0.3 * activity_balance + 0.3 * comm_effectiveness
        return float(np.clip(efficiency, 0.0, 1.0))
    
    def _get_pocket_summary(self, pocket: Dict) -> Dict:
        """Get summary information for a pocket."""
        return {
            'pocket_id': pocket['id'],
            'x': pocket['position']['x'],
            'y': pocket['position']['y'],
            'specialization': pocket['specialization'],
            'activity': pocket['activity_level'],
            'energy': pocket['energy'],
            'local_norm': np.linalg.norm(pocket['local_state'])
        }
    
    def get_swarm_statistics(self) -> Dict:
        """Get comprehensive swarm statistics."""
        specializations = {}
        for pocket in self.pockets:
            spec = pocket['specialization']
            if spec not in specializations:
                specializations[spec] = 0
            specializations[spec] += 1
        
        return {
            'total_pockets': self.num_pockets,
            'specialization_distribution': specializations,
            'average_energy': np.mean([p['energy'] for p in self.pockets]),
            'average_activity': np.mean([p['activity_level'] for p in self.pockets]),
            'total_connections': np.sum(self.communication_matrix) / 2,  # Divide by 2 for undirected
            'communication_density': np.sum(self.communication_matrix) / (self.num_pockets ** 2)
        }
