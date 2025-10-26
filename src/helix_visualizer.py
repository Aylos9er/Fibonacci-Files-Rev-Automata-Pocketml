import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List, Tuple
import math

class HelixVisualizer:
    """
    Creates interactive 3D visualizations of the symbiotic graphene mesh
    and double helix tensor processing.
    """
    
    def __init__(self):
        self.color_scheme = {
            'strand_a': '#1f77b4',  # Blue
            'strand_b': '#ff7f0e',  # Orange
            'crossover': '#d62728',  # Red
            'mesh_active': '#2ca02c',  # Green
            'mesh_inactive': '#aec7e8',  # Light blue
            'energy_high': '#ff1744',  # Bright red
            'energy_low': '#304ffe'   # Deep blue
        }
    
    def create_helix_plot(self, mesh_state: Dict, ca_state: np.ndarray, 
                         current_step: int) -> go.Figure:
        """Create comprehensive 3D helix and mesh visualization."""
        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{'type': 'scatter3d'}, {'type': 'heatmap'}],
                   [{'type': 'scatter3d'}, {'type': 'scatter'}]],
            subplot_titles=(
                'Double Helix Tensor Processing',
                'Mesh Energy Distribution',
                'Symbiotic Mesh Structure',
                'Cellular Automata State'
            ),
            vertical_spacing=0.1,
            horizontal_spacing=0.1
        )
        
        # 1. Double Helix Visualization (top-left)
        self._add_helix_traces(fig, mesh_state, current_step, row=1, col=1)
        
        # 2. Mesh Energy Heatmap (top-right)
        self._add_energy_heatmap(fig, mesh_state, row=1, col=2)
        
        # 3. 3D Mesh Structure (bottom-left)
        self._add_mesh_structure(fig, mesh_state, ca_state, row=2, col=1)
        
        # 4. CA State Evolution (bottom-right)
        self._add_ca_state_plot(fig, ca_state, current_step, row=2, col=2)
        
        # Update layout
        fig.update_layout(
            title=f"HelixGrapheneLM Simulation - Step {current_step}",
            height=800,
            showlegend=True,
            scene=dict(
                xaxis_title="X",
                yaxis_title="Y",
                zaxis_title="Z",
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
            ),
            scene2=dict(
                xaxis_title="X",
                yaxis_title="Y",
                zaxis_title="Z",
                camera=dict(eye=dict(x=-1.5, y=1.5, z=1.5))
            )
        )
        
        return fig
    
    def _add_helix_traces(self, fig: go.Figure, mesh_state: Dict, 
                         current_step: int, row: int, col: int):
        """Add double helix traces to the figure."""
        # Generate helix coordinates
        n_points = 50
        t = np.linspace(0, 4 * np.pi, n_points)
        
        # Create time-varying helix with mesh energy influence
        energy_influence = np.mean(mesh_state['energy']) * 0.5
        radius_a = 1.0 + energy_influence + 0.2 * np.sin(current_step * 0.1)
        radius_b = 1.0 + energy_influence + 0.2 * np.cos(current_step * 0.1)
        
        # Strand A (primary helix)
        x_a = radius_a * np.cos(t)
        y_a = radius_a * np.sin(t)
        z_a = t
        
        # Strand B (complementary helix with phase offset)
        x_b = radius_b * np.cos(t + np.pi)
        y_b = radius_b * np.sin(t + np.pi)
        z_b = t
        
        # Add helix strands
        fig.add_trace(
            go.Scatter3d(
                x=x_a, y=y_a, z=z_a,
                mode='lines+markers',
                line=dict(color=self.color_scheme['strand_a'], width=6),
                marker=dict(size=3, color=self.color_scheme['strand_a']),
                name='Helix Strand A',
                opacity=0.8
            ),
            row=row, col=col
        )
        
        fig.add_trace(
            go.Scatter3d(
                x=x_b, y=y_b, z=z_b,
                mode='lines+markers',
                line=dict(color=self.color_scheme['strand_b'], width=6),
                marker=dict(size=3, color=self.color_scheme['strand_b']),
                name='Helix Strand B',
                opacity=0.8
            ),
            row=row, col=col
        )
        
        # Add crossover connections
        crossover_indices = np.random.choice(n_points, size=5, replace=False)
        for i in crossover_indices:
            fig.add_trace(
                go.Scatter3d(
                    x=[x_a[i], x_b[i]],
                    y=[y_a[i], y_b[i]],
                    z=[z_a[i], z_b[i]],
                    mode='lines',
                    line=dict(color=self.color_scheme['crossover'], width=3, dash='dash'),
                    name='Crossover' if i == crossover_indices[0] else None,
                    showlegend=i == crossover_indices[0],
                    opacity=0.6
                ),
                row=row, col=col
            )
    
    def _add_energy_heatmap(self, fig: go.Figure, mesh_state: Dict, row: int, col: int):
        """Add mesh energy distribution heatmap."""
        energy_matrix = mesh_state['energy']
        
        fig.add_trace(
            go.Heatmap(
                z=energy_matrix,
                colorscale='Viridis',
                name='Energy Distribution',
                colorbar=dict(title="Energy Level", x=0.48, len=0.4, y=0.75),
                showscale=True
            ),
            row=row, col=col
        )
    
    def _add_mesh_structure(self, fig: go.Figure, mesh_state: Dict, 
                          ca_state: np.ndarray, row: int, col: int):
        """Add 3D mesh structure visualization."""
        nodes = mesh_state['nodes']
        size = int(np.sqrt(len(ca_state)))
        
        # Flatten node coordinates
        x_coords = nodes[:, :, 0].flatten()
        y_coords = nodes[:, :, 1].flatten()
        z_coords = nodes[:, :, 2].flatten()
        
        # Color nodes based on CA state
        colors = ca_state
        marker_colors = [self.color_scheme['mesh_active'] if c > 0.5 
                        else self.color_scheme['mesh_inactive'] for c in colors]
        
        # Add mesh nodes
        fig.add_trace(
            go.Scatter3d(
                x=x_coords,
                y=y_coords,
                z=z_coords,
                mode='markers',
                marker=dict(
                    size=5 + 10 * colors,  # Size based on activation
                    color=colors,
                    colorscale='RdYlBu',
                    opacity=0.7,
                    colorbar=dict(title="CA State", x=0.02, len=0.4, y=0.25)
                ),
                name='Mesh Nodes',
                text=[f'Node {i}: {c:.3f}' for i, c in enumerate(colors)],
                hovertemplate='%{text}<extra></extra>'
            ),
            row=row, col=col
        )
        
        # Add connections between nearby nodes
        connection_threshold = 1.5
        for i in range(len(x_coords)):
            for j in range(i + 1, min(i + 4, len(x_coords))):  # Limit connections
                distance = np.sqrt((x_coords[i] - x_coords[j])**2 + 
                                 (y_coords[i] - y_coords[j])**2)
                if distance < connection_threshold:
                    # Connection strength based on CA states
                    strength = (colors[i] + colors[j]) / 2
                    fig.add_trace(
                        go.Scatter3d(
                            x=[x_coords[i], x_coords[j]],
                            y=[y_coords[i], y_coords[j]],
                            z=[z_coords[i], z_coords[j]],
                            mode='lines',
                            line=dict(
                                color=f'rgba(100, 100, 100, {strength})',
                                width=2
                            ),
                            showlegend=False,
                            hoverinfo='skip'
                        ),
                        row=row, col=col
                    )
    
    def _add_ca_state_plot(self, fig: go.Figure, ca_state: np.ndarray, 
                          current_step: int, row: int, col: int):
        """Add cellular automata state visualization."""
        # Create a time series-style plot showing CA evolution
        x_values = np.arange(len(ca_state))
        
        fig.add_trace(
            go.Scatter(
                x=x_values,
                y=ca_state,
                mode='lines+markers',
                name='CA State',
                line=dict(color=self.color_scheme['strand_a'], width=2),
                marker=dict(
                    size=4,
                    color=ca_state,
                    colorscale='Plasma',
                    showscale=False
                ),
                fill='tonexty' if current_step > 0 else None,
                fillcolor=f'rgba(31, 119, 180, 0.2)'
            ),
            row=row, col=col
        )
        
        # Add horizontal line at activation threshold
        # Add horizontal line at activation threshold
        fig.add_trace(
            go.Scatter(
                x=[0, len(ca_state)],
                y=[0.5, 0.5],
                mode='lines',
                line=dict(color='red', dash='dash'),
                name='Activation Threshold',
                showlegend=False
            ),
            row=row, col=col
        )
    
    def create_performance_dashboard(self, metrics_history: List[Dict]) -> go.Figure:
        """Create performance metrics dashboard."""
        if not metrics_history:
            return go.Figure()
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Pass@1 Performance', 'Latency Trends', 
                          'Energy Efficiency', 'Coherence Evolution'),
            vertical_spacing=0.12
        )
        
        steps = list(range(len(metrics_history)))
        
        # Pass@1 Score
        pass_scores = [m['pass_at_1'] for m in metrics_history]
        fig.add_trace(
            go.Scatter(x=steps, y=pass_scores, name='Pass@1', 
                      line=dict(color=self.color_scheme['strand_a'], width=3)),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=[0, len(pass_scores)], y=[0.98, 0.98], mode='lines',
                      line=dict(color='green', dash='dash'), name='Target: 0.98',
                      showlegend=False), row=1, col=1)
        
        # Latency
        latencies = [m['latency'] for m in metrics_history]
        fig.add_trace(
            go.Scatter(x=steps, y=latencies, name='Latency', 
                      line=dict(color=self.color_scheme['strand_b'], width=3)),
            row=1, col=2
        )
        fig.add_trace(
            go.Scatter(x=[0, len(latencies)], y=[35, 35], mode='lines',
                      line=dict(color='red', dash='dash'), name='Target: 35ms',
                      showlegend=False), row=1, col=2)
        
        # Energy Efficiency
        energies = [m['energy_efficiency'] for m in metrics_history]
        fig.add_trace(
            go.Scatter(x=steps, y=energies, name='Energy', 
                      line=dict(color=self.color_scheme['mesh_active'], width=3)),
            row=2, col=1
        )
        
        # Coherence
        coherences = [m['coherence'] for m in metrics_history]
        fig.add_trace(
            go.Scatter(x=steps, y=coherences, name='Coherence', 
                      line=dict(color=self.color_scheme['crossover'], width=3)),
            row=2, col=2
        )
        
        fig.update_layout(
            title="HelixGrapheneLM Performance Dashboard",
            height=600,
            showlegend=False
        )
        
        return fig
