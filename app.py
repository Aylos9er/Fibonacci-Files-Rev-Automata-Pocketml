import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
from datetime import datetime

from src.symbiotic_mesh import SymbioticGrapheneMesh
from src.cellular_automata import TwoWayCellularAutomata
from src.tensor_processor import HelixTensorProcessor
from src.helix_visualizer import HelixVisualizer
from src.swarm_manager import SwarmManager
from src.utils import calculate_performance_metrics, format_metrics_display
from src.local_ai_models import create_pocket_ai_models
from src.micro_language_models import create_three_part_micro_system
from src.tiny_cluster_models import create_tiny_model_cluster
from src.advanced_automata_models import create_advanced_automata_swarm
from src.auth_utils import init_auth, ReplitAuth, show_login_page, show_user_info

# Page configuration
st.set_page_config(
    page_title="PocketLM - Symbiotic Graphene Mesh",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize authentication
init_auth()
auth = ReplitAuth()

# Check authentication - if not authenticated, show login page
if not auth.is_authenticated():
    show_login_page()
    st.stop()

# Main title and description
st.title("🧬 PocketLM: Symbiotic Graphene Mesh Simulation")
st.markdown("""
**Advanced AI Framework with Double Helix Tensor Processing**

This application demonstrates the symbiotic graphene mesh technology for pocket-sized language models,
featuring two-way cellular automata, double helix tensor processing, and modular swarm intelligence.

*Proof of Concept by j Mosij - mosij@icloud.com*
""")

# Sidebar configuration
st.sidebar.header("⚙️ Simulation Parameters")

# Show user info in sidebar
show_user_info()

# Mesh configuration
mesh_size = st.sidebar.slider("Mesh Grid Size", 10, 50, 20)
stimuli_intensity = st.sidebar.slider("Light Stimuli Intensity", 0.0, 1.0, 0.1, 0.01)
ca_steps_forward = st.sidebar.slider("CA Forward Steps", 1, 15, 6)
ca_steps_reverse = st.sidebar.slider("CA Reverse Steps", 1, 20, 13)

# Swarm configuration
st.sidebar.subheader("🔄 Swarm Configuration")
num_pockets = st.sidebar.slider("Number of Pocket Instances", 1, 10, 3)
swarm_coordination = st.sidebar.selectbox(
    "Coordination Strategy", 
    ["Synchronous", "Asynchronous", "Adaptive"]
)

# AI Model Configuration
st.sidebar.subheader("🤖 Local AI Models")
num_ai_models = st.sidebar.slider("Number of AI Models", 1, 5, 3)
ai_temperature = st.sidebar.slider("AI Temperature", 0.1, 1.5, 0.8, 0.1)
ai_prompt_mode = st.sidebar.selectbox(
    "AI Analysis Mode",
    ["Mesh Analysis", "Performance Insights", "Code Generation", "Creative Mode"]
)

# Three-Part Micro PM System
st.sidebar.subheader("🧠 Micro Language Models")
mesh_temp = st.sidebar.slider("Mesh PM Temperature", 0.1, 2.0, 0.7, 0.1)
automata_temp = st.sidebar.slider("Automata PM Temperature", 0.1, 2.0, 0.8, 0.1)
swarm_temp = st.sidebar.slider("Swarm PM Temperature", 0.1, 2.0, 0.6, 0.1)
enable_micro_pms = st.sidebar.checkbox("Enable Micro PMs", value=True)

# Tiny Cluster Models (Real-world tiny models)
st.sidebar.subheader("🕰️ Tiny Model Cluster")
cluster_strategy = st.sidebar.selectbox(
    "Cluster Strategy",
    ["consensus", "load_balanced", "specialized", "failover"]
)
enable_tiny_cluster = st.sidebar.checkbox("Enable Tiny Cluster", value=True)

# Advanced Cellular Automata
st.sidebar.subheader("🌀 Advanced Automata")
num_fibonacci = st.sidebar.slider("Fibonacci Automata", 1, 4, 2)
num_quad_core = st.sidebar.slider("Quad Core Automata", 1, 4, 2)
fibonacci_scales = st.sidebar.slider("Fibonacci Scales", 50, 300, 89)
quad_fault_rate = st.sidebar.slider("Fault Injection Rate %", 0.0, 10.0, 1.0, 0.5)
enable_advanced_automata = st.sidebar.checkbox("Enable Advanced Automata", value=True)

# Performance targets
st.sidebar.subheader("🎯 Performance Targets")
target_pass_at_1 = st.sidebar.number_input("Target Pass@1", 0.0, 1.0, 0.98, 0.01)
target_latency = st.sidebar.number_input("Target Latency (ms/token)", 1, 100, 35)

# Initialize user-specific session state
user = auth.get_current_user()
user_id = user.get('id', 'anonymous') if user else 'anonymous'
user_prefix = f"user_{user_id}_"

# User state management functions with proper initialization
def get_user_state(key, default=None):
    """Get user-specific session state value with fallback"""
    return st.session_state.get(f'{user_prefix}{key}', default)

def set_user_state(key, value):
    """Set user-specific session state value"""
    st.session_state[f'{user_prefix}{key}'] = value

def user_state_exists(key):
    """Check if user-specific session state key exists"""
    return f'{user_prefix}{key}' in st.session_state

def ensure_user_state_initialized():
    """Ensure all user state objects are properly initialized"""
    # Initialize missing objects with fallback
    if not user_state_exists('mesh') or get_user_state('mesh') is None:
        set_user_state('mesh', SymbioticGrapheneMesh(mesh_size))
    
    if not user_state_exists('ca') or get_user_state('ca') is None:
        set_user_state('ca', TwoWayCellularAutomata(mesh_size))
    
    if not user_state_exists('tensor_processor') or get_user_state('tensor_processor') is None:
        set_user_state('tensor_processor', HelixTensorProcessor())
    
    if not user_state_exists('visualizer') or get_user_state('visualizer') is None:
        set_user_state('visualizer', HelixVisualizer())
    
    if not user_state_exists('swarm') or get_user_state('swarm') is None:
        set_user_state('swarm', SwarmManager(num_pockets))
    
    if not user_state_exists('ai_swarm') or get_user_state('ai_swarm') is None:
        set_user_state('ai_swarm', create_pocket_ai_models(num_ai_models))
    
    if not user_state_exists('micro_system') or get_user_state('micro_system') is None:
        set_user_state('micro_system', create_three_part_micro_system())
    
    if not user_state_exists('tiny_cluster') or get_user_state('tiny_cluster') is None:
        set_user_state('tiny_cluster', create_tiny_model_cluster())
    
    if not user_state_exists('advanced_automata') or get_user_state('advanced_automata') is None:
        set_user_state('advanced_automata', create_advanced_automata_swarm(num_fibonacci, num_quad_core))
    
    if not user_state_exists('simulation_running'):
        set_user_state('simulation_running', False)
    
    if not user_state_exists('metrics_history') or get_user_state('metrics_history') is None:
        set_user_state('metrics_history', [])
    
    if not user_state_exists('ai_insights') or get_user_state('ai_insights') is None:
        set_user_state('ai_insights', [])
    
    if not user_state_exists('micro_insights') or get_user_state('micro_insights') is None:
        set_user_state('micro_insights', [])
    
    if not user_state_exists('cluster_insights') or get_user_state('cluster_insights') is None:
        set_user_state('cluster_insights', [])

# Ensure all session state objects are initialized
ensure_user_state_initialized()

# User state accessor class for robust access
class UserState:
    def __init__(self):
        pass
    
    @property
    def mesh(self):
        mesh = get_user_state('mesh')
        if mesh is None:
            mesh = SymbioticGrapheneMesh(mesh_size)
            set_user_state('mesh', mesh)
        return mesh
    
    @property
    def ca(self):
        ca = get_user_state('ca')
        if ca is None:
            ca = TwoWayCellularAutomata(mesh_size)
            set_user_state('ca', ca)
        return ca
    
    @property
    def tensor_processor(self):
        processor = get_user_state('tensor_processor')
        if processor is None:
            processor = HelixTensorProcessor()
            set_user_state('tensor_processor', processor)
        return processor
    
    @property
    def visualizer(self):
        viz = get_user_state('visualizer')
        if viz is None:
            viz = HelixVisualizer()
            set_user_state('visualizer', viz)
        return viz
    
    @property
    def swarm(self):
        swarm = get_user_state('swarm')
        if swarm is None:
            swarm = SwarmManager(num_pockets)
            set_user_state('swarm', swarm)
        return swarm
    
    @property
    def ai_swarm(self):
        ai_swarm = get_user_state('ai_swarm')
        if ai_swarm is None:
            ai_swarm = create_pocket_ai_models(num_ai_models)
            set_user_state('ai_swarm', ai_swarm)
        return ai_swarm
    
    @property
    def micro_system(self):
        micro = get_user_state('micro_system')
        if micro is None:
            micro = create_three_part_micro_system()
            set_user_state('micro_system', micro)
        return micro
    
    @property
    def tiny_cluster(self):
        cluster = get_user_state('tiny_cluster')
        if cluster is None:
            cluster = create_tiny_model_cluster()
            set_user_state('tiny_cluster', cluster)
        return cluster
    
    @property
    def simulation_running(self):
        return get_user_state('simulation_running', False)
    
    @simulation_running.setter
    def simulation_running(self, value):
        set_user_state('simulation_running', value)
    
    @property
    def metrics_history(self):
        history = get_user_state('metrics_history')
        if history is None:
            history = []
            set_user_state('metrics_history', history)
        return history
    
    @property
    def ai_insights(self):
        insights = get_user_state('ai_insights')
        if insights is None:
            insights = []
            set_user_state('ai_insights', insights)
        return insights
    
    @property
    def micro_insights(self):
        insights = get_user_state('micro_insights')
        if insights is None:
            insights = []
            set_user_state('micro_insights', insights)
        return insights
    
    @property
    def cluster_insights(self):
        insights = get_user_state('cluster_insights')
        if insights is None:
            insights = []
            set_user_state('cluster_insights', insights)
        return insights
    
    @property
    def advanced_automata(self):
        automata = get_user_state('advanced_automata')
        if automata is None:
            automata = create_advanced_automata_swarm(num_fibonacci, num_quad_core)
            set_user_state('advanced_automata', automata)
        return automata
    
    @property
    def automata_insights(self):
        insights = get_user_state('automata_insights')
        if insights is None:
            insights = []
            set_user_state('automata_insights', insights)
        return insights

# Create user state instance for robust access
user_state = UserState()

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🌐 Symbiotic Mesh Visualization")
    
    # Control buttons
    button_col1, button_col2, button_col3, button_col4 = st.columns(4)
    
    with button_col1:
        if st.button("🚀 Start Simulation", type="primary"):
            user_state.simulation_running = True
    
    with button_col2:
        if st.button("⏸️ Pause"):
            user_state.simulation_running = False
    
    with button_col3:
        if st.button("🔄 Reset"):
            set_user_state('mesh', SymbioticGrapheneMesh(mesh_size))
            set_user_state('ca', TwoWayCellularAutomata(mesh_size))
            set_user_state('metrics_history', [])
            st.rerun()
    
    with button_col4:
        if st.button("📊 Update Swarm"):
            set_user_state('swarm', SwarmManager(num_pockets))
            set_user_state('ai_swarm', create_pocket_ai_models(num_ai_models))
            set_user_state('micro_system', create_three_part_micro_system())
            set_user_state('tiny_cluster', create_tiny_model_cluster())
            set_user_state('advanced_automata', create_advanced_automata_swarm(num_fibonacci, num_quad_core))
            # Update AI model temperatures
            for model in user_state.ai_swarm.models:
                model.temperature = ai_temperature
            # Update micro PM temperatures
            user_state.micro_system.update_temperatures(mesh_temp, automata_temp, swarm_temp)
            # Update quad core fault rates
            for quad in user_state.advanced_automata.quad_core_automata:
                quad.set_fault_rate(quad_fault_rate / 100.0)
    
    # Visualization placeholder
    viz_placeholder = st.empty()
    
    # Performance metrics display
    st.subheader("📈 Real-time Performance Metrics")
    metrics_placeholder = st.empty()

with col2:
    st.subheader("🔬 Simulation Status")
    status_placeholder = st.empty()
    
    st.subheader("⚡ Cellular Automata State")
    ca_placeholder = st.empty()
    
    st.subheader("🧠 Tensor Processing")
    tensor_placeholder = st.empty()
    
    st.subheader("🔄 Swarm Status")
    swarm_placeholder = st.empty()
    
    st.subheader("🤖 AI Insights")
    ai_placeholder = st.empty()
    
    st.subheader("🧠 Micro PM Analysis")
    micro_pm_placeholder = st.empty()
    
    st.subheader("🕰️ Tiny Model Cluster")
    tiny_cluster_placeholder = st.empty()
    
    st.subheader("🌀 Advanced Cellular Automata")
    advanced_automata_placeholder = st.empty()

# Main simulation loop
if user_state.simulation_running:
    progress_bar = st.progress(0)
    
    for step in range(ca_steps_forward + ca_steps_reverse):
        # Update mesh with stimuli
        user_state.mesh.update_stimuli(stimuli_intensity)
        
        # Determine if forward or reverse step
        is_forward = step < ca_steps_forward
        step_type = "forward" if is_forward else "reverse"
        
        # Perform CA step
        user_state.ca.update_step(
            user_state.mesh.get_tensor_state(),
            step_type,
            stimuli_intensity
        )
        
        # Process tensors through helix
        processed_tensors = user_state.tensor_processor.process_helix(
            user_state.ca.get_current_state()
        )
        
        # Update mesh state
        user_state.mesh.update_from_tensors(processed_tensors)
        
        # Update swarm coordination
        swarm_state = user_state.swarm.coordinate_pockets(
            user_state.mesh.get_mesh_state(),
            swarm_coordination
        )
        
        # Calculate performance metrics
        current_metrics = calculate_performance_metrics(
            user_state.mesh.get_mesh_state(),
            processed_tensors,
            step,
            target_pass_at_1,
            target_latency
        )
        user_state.metrics_history.append(current_metrics)
        set_user_state('metrics_history', user_state.metrics_history)
        
        # Generate AI insights every few steps
        if step % 3 == 0:  # Every 3rd step
            ai_analysis = user_state.ai_swarm.process_mesh_data(
                user_state.mesh.get_mesh_state()
            )
            user_state.ai_insights.append(ai_analysis)
            set_user_state('ai_insights', user_state.ai_insights)
            
            # Generate micro PM insights
            if enable_micro_pms:
                micro_analysis = user_state.micro_system.process_system_state({
                    'mesh_energy': np.mean(user_state.mesh.get_mesh_state()['energy']),
                    'coherence': user_state.mesh.get_mesh_state()['coherence'],
                    'ca_state': user_state.ca.get_current_state(),
                    'num_pockets': num_pockets,
                    'swarm_efficiency': swarm_state['efficiency']
                })
                user_state.micro_insights.append(micro_analysis)
                set_user_state('micro_insights', user_state.micro_insights)
                
            # Generate tiny cluster insights
            if enable_tiny_cluster:
                cluster_prompt = f"analyze {ai_prompt_mode.lower()} mesh coherence {user_state.mesh.get_mesh_state()['coherence']:.2f}"
                cluster_result = user_state.tiny_cluster.distributed_inference(cluster_prompt, cluster_strategy)
                user_state.cluster_insights.append(cluster_result)
                set_user_state('cluster_insights', user_state.cluster_insights)
            
            # Generate advanced automata insights
            if enable_advanced_automata:
                # Step the advanced automata in sync with main CA (forward or reverse)
                is_reverse_step = not is_forward  # Reverse mode when in reverse phase
                user_state.advanced_automata.step_all(reverse_mode=is_reverse_step)
                
                # Generate ML insight based on mesh and CA data
                automata_insight = user_state.advanced_automata.generate_ml_insight(
                    user_state.mesh.get_mesh_state(),
                    {'forward_steps': ca_steps_forward, 'reverse_steps': ca_steps_reverse}
                )
                user_state.automata_insights.append(automata_insight)
                set_user_state('automata_insights', user_state.automata_insights)
        
        # Update visualizations
        with viz_placeholder.container():
            # Create 3D helix visualization
            helix_fig = user_state.visualizer.create_helix_plot(
                user_state.mesh.get_mesh_state(),
                user_state.ca.get_current_state(),
                step
            )
            st.plotly_chart(helix_fig, use_container_width=True)
        
        # Update status displays
        with status_placeholder.container():
            st.metric("Current Step", f"{step + 1}/{ca_steps_forward + ca_steps_reverse}")
            st.metric("Step Type", step_type.title())
            st.metric("Mesh Energy", f"{user_state.mesh.get_energy():.3f}")
            
            # Light stimuli indicator
            if stimuli_intensity > 0:
                st.success(f"💡 Light Stimuli Active: {stimuli_intensity:.2f}")
            else:
                st.info("🌙 No Light Stimuli")
        
        with ca_placeholder.container():
            ca_state = user_state.ca.get_current_state()
            st.metric("Active Cells", len([c for c in ca_state if c > 0.5]))
            st.metric("Average Activation", f"{np.mean(ca_state):.3f}")
            
            # Mini heatmap of CA state
            ca_matrix = np.array(ca_state).reshape(mesh_size, mesh_size)
            fig_ca = px.imshow(ca_matrix, color_continuous_scale="viridis", aspect="auto")
            fig_ca.update_layout(height=200, title="CA State Heatmap")
            st.plotly_chart(fig_ca, use_container_width=True)
        
        with tensor_placeholder.container():
            st.metric("Tensor Magnitude", f"{np.linalg.norm(processed_tensors):.3f}")
            st.metric("Helix Rotations", user_state.tensor_processor.get_rotation_count())
            st.metric("Processing Rate", f"{len(processed_tensors) / (step + 1):.1f} tensors/step")
        
        with swarm_placeholder.container():
            st.metric("Active Pockets", num_pockets)
            st.metric("Coordination", swarm_coordination)
            st.metric("Swarm Efficiency", f"{swarm_state['efficiency']:.2f}")
            
            # Swarm coordination visualization
            if len(swarm_state['pocket_states']) > 1:
                swarm_df = pd.DataFrame(swarm_state['pocket_states'])
                fig_swarm = px.scatter(
                    swarm_df, x='x', y='y', size='activity', color='pocket_id',
                    title="Swarm Coordination Map"
                )
                fig_swarm.update_layout(height=200)
                st.plotly_chart(fig_swarm, use_container_width=True)
        
        # Update AI insights display
        with ai_placeholder.container():
            ai_stats = user_state.ai_swarm.get_swarm_stats()
            st.metric("AI Models Active", ai_stats['swarm_size'])
            st.metric("Total Parameters", f"{ai_stats['total_parameters']:,}")
            st.metric("AI Generations", ai_stats['total_generations'])
            
            # Show latest AI insights
            if user_state.ai_insights:
                latest_insight = user_state.ai_insights[-1]
                st.write("**Latest AI Analysis:**")
                st.write(f"💭 {latest_insight['ai_analysis']['consensus']}")
                st.write(f"🎯 Confidence: {latest_insight['confidence']:.2f}")
                
                if latest_insight['recommendations']:
                    st.write("**Recommendations:**")
                    for rec in latest_insight['recommendations']:
                        st.write(f"• {rec}")
            
            # AI text generation demo
            if st.button("🎲 Generate AI Text"):
                prompts = {
                    "Mesh Analysis": "analyze symbiotic graphene mesh performance",
                    "Performance Insights": "optimize tensor processing efficiency",
                    "Code Generation": "implement cellular automata function",
                    "Creative Mode": "innovative AI architecture design"
                }
                
                prompt = prompts.get(ai_prompt_mode, "analyze system")
                ai_result = user_state.ai_swarm.generate_consensus(prompt, max_length=12)
                
                st.write("**AI Generated Text:**")
                st.write(f"🤖 {ai_result['consensus']}")
                
                with st.expander("Individual Model Outputs"):
                    for gen in ai_result['individual_generations']:
                        st.write(f"**{gen['model']}:** {gen['text']}")
        
        # Update Micro PM display
        with micro_pm_placeholder.container():
            if enable_micro_pms:
                micro_stats = user_state.micro_system.get_system_stats()
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("MeshPM", f"{micro_stats['model_details'][0]['parameters']:,}")
                    st.caption(f"Generations: {micro_stats['model_details'][0]['generations']}")
                
                with col2:
                    st.metric("AutomataPM", f"{micro_stats['model_details'][1]['parameters']:,}")
                    st.caption(f"Generations: {micro_stats['model_details'][1]['generations']}")
                
                with col3:
                    st.metric("SwarmPM", f"{micro_stats['model_details'][2]['parameters']:,}")
                    st.caption(f"Generations: {micro_stats['model_details'][2]['generations']}")
                
                # Show latest micro insights
                if user_state.micro_insights:
                    latest_micro = user_state.micro_insights[-1]
                    st.write("**Three-Part Analysis:**")
                    st.write(f"🧬 Mesh: {latest_micro['mesh_insights']}")
                    st.write(f"🔄 Automata: {latest_micro['automata_insights']}")
                    st.write(f"🐝 Swarm: {latest_micro['swarm_insights']}")
                    st.write(f"⚡ Combined: {latest_micro['combined_analysis']}")
                
                # Micro PM collaborative generation
                if st.button("🎯 Generate Micro PM Analysis"):
                    prompts = {
                        "Mesh Analysis": "optimize graphene mesh",
                        "Performance Insights": "improve system performance",
                        "Code Generation": "implement algorithm",
                        "Creative Mode": "innovative solution"
                    }
                    
                    prompt = prompts.get(ai_prompt_mode, "analyze system")
                    micro_result = user_state.micro_system.generate_collaborative_text(prompt)
                    
                    st.write("**Micro PM Collaborative Generation:**")
                    st.write(f"🧬 **MeshPM:** {micro_result['mesh_response']}")
                    st.write(f"🔄 **AutomataPM:** {micro_result['automata_response']}")
                    st.write(f"🐝 **SwarmPM:** {micro_result['swarm_response']}")
                    st.write(f"⭐ **Summary:** {micro_result['collaborative_summary']}")
            else:
                st.info("Enable Micro PMs in sidebar to see three-part analysis")
        
        # Update Tiny Cluster display
        with tiny_cluster_placeholder.container():
            if enable_tiny_cluster:
                cluster_overview = user_state.tiny_cluster.get_cluster_overview()
                
                # Display cluster health and stats
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    health_color = {
                        "healthy": "green",
                        "degraded": "orange", 
                        "critical": "red",
                        "offline": "gray"
                    }
                    health = cluster_overview['cluster_info']['cluster_health']
                    st.markdown(f"**Cluster Health:** :{health_color.get(health, 'gray')}[{health.upper()}]")
                
                with col2:
                    st.metric("Active Models", 
                            f"{cluster_overview['cluster_info']['active_models']}/{cluster_overview['cluster_info']['total_models']}")
                
                with col3:
                    st.metric("Total Parameters", cluster_overview['cluster_info']['total_parameters'])
                
                with col4:
                    st.metric("Efficiency", f"{cluster_overview['performance_metrics']['cluster_efficiency']:.1%}")
                
                # Show individual model status
                st.write("**Model Status:**")
                for model_stat in cluster_overview['model_stats']:
                    status_icon = "🟢" if model_stat['is_active'] else "🔴"
                    role_icon = {
                        "coordinator": "📋",
                        "worker": "⚙️",
                        "backup": "🛡️"
                    }.get(model_stat['cluster_role'], "🤖")
                    
                    st.write(f"{status_icon} {role_icon} **{model_stat['model_name']}** ({model_stat['params_count']}) - {model_stat['inference_count']} inferences, {model_stat['avg_latency_ms']:.1f}ms avg")
                
                # Show latest cluster insight
                if user_state.cluster_insights:
                    latest_cluster = user_state.cluster_insights[-1]
                    st.write(f"**Latest Cluster Analysis ({cluster_strategy}):**")
                    
                    if cluster_strategy == "consensus":
                        st.write(f"🤝 {latest_cluster['combined_response']}")
                        st.caption(f"Nodes: {latest_cluster['participating_nodes']}, Latency: {latest_cluster['cluster_latency_ms']:.1f}ms")
                    elif cluster_strategy == "specialized":
                        st.write(f"🎯 {latest_cluster['response']}")
                        st.caption(f"Specialist: {latest_cluster['selected_specialist']} ({latest_cluster['specialization_reason']})")
                    elif cluster_strategy == "load_balanced":
                        st.write(f"⚖️ {latest_cluster['response']}")
                        st.caption(f"Model: {latest_cluster['selected_model']}, Node: {latest_cluster['node_id']}")
                    elif cluster_strategy == "failover":
                        st.write(f"🔄 {latest_cluster.get('primary_response', latest_cluster.get('response', 'N/A'))}")
                        if latest_cluster.get('redundancy'):
                            st.caption(f"🔄 Backup: {latest_cluster.get('backup_response', 'N/A')}")
                
                # Cluster management buttons
                cluster_col1, cluster_col2, cluster_col3 = st.columns(3)
                
                with cluster_col1:
                    if st.button("🗨 Generate Cluster Response"):
                        test_prompts = {
                            "Mesh Analysis": "optimize graphene mesh tensor processing",
                            "Performance Insights": "improve distributed system performance", 
                            "Code Generation": "implement efficient clustering algorithm",
                            "Creative Mode": "design innovative AI cluster architecture"
                        }
                        test_prompt = test_prompts.get(ai_prompt_mode, "analyze system performance")
                        result = user_state.tiny_cluster.distributed_inference(test_prompt, cluster_strategy)
                        
                        st.write("**Cluster Response:**")
                        if cluster_strategy == "consensus":
                            st.success(f"🤝 **Consensus:** {result['combined_response']}")
                            with st.expander("Individual Responses"):
                                for resp in result['individual_responses']:
                                    st.write(f"**{resp['model']}:** {resp['text']}")
                        else:
                            response_text = result.get('response', result.get('primary_response', 'No response'))
                            st.success(f"🎯 **Response:** {response_text}")
                
                with cluster_col2:
                    if st.button("🔄 Restart Cluster"):
                        set_user_state('tiny_cluster', create_tiny_model_cluster())
                        st.rerun()
                
                with cluster_col3:
                    cluster_health = cluster_overview['cluster_info']['cluster_health']
                    if cluster_health != "healthy":
                        if st.button(f"🔧 Repair ({cluster_health.title()})"):
                            # Simulate cluster repair
                            for model in user_state.tiny_cluster.models:
                                model.is_active = True
                            st.success("Cluster repaired!")
                            st.rerun()
            else:
                st.info("Enable Tiny Cluster in sidebar to see distributed inference")
        
        # Update Advanced Automata display
        with advanced_automata_placeholder.container():
            if enable_advanced_automata:
                automata_analysis = user_state.advanced_automata.get_combined_analysis()
                swarm_metrics = automata_analysis['swarm_metrics']
                
                # Overall metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Fibonacci Energy", f"{swarm_metrics['avg_fibonacci_energy']:.2%}")
                
                with col2:
                    st.metric("Fault Tolerance", f"{swarm_metrics['avg_fault_tolerance']:.2%}")
                
                with col3:
                    st.metric("Total Faults", swarm_metrics['total_faults_detected'])
                
                with col4:
                    st.metric("Active Automata", f"{swarm_metrics['num_fibonacci'] + swarm_metrics['num_quad_core']}")
                
                # Fibonacci Automata Stats
                st.write("**🌀 Turing-Complete Fibonacci Pine Cone Automata:**")
                for fib_stat in automata_analysis['fibonacci_automata']:
                    mode_icon = "↩️" if fib_stat['reverse_mode'] else "➡️"
                    turing_badge = "✅ TURING COMPLETE" if fib_stat.get('turing_complete', False) else ""
                    reversible_badge = "🔄 REVERSIBLE" if fib_stat.get('reversible', False) else ""
                    
                    st.write(f"{mode_icon} **{fib_stat['automaton_id']}**: {turing_badge} {reversible_badge}")
                    st.write(f"   └─ Spirals ({fib_stat['spiral_count_a']}, {fib_stat['spiral_count_b']}), Energy: {fib_stat['pattern_energy']:.2%}, Golden Angle: {fib_stat['golden_angle_deg']:.1f}°")
                    
                    if 'computation_depth' in fib_stat:
                        st.write(f"   └─ Computation Depth: {fib_stat['computation_depth']}, Entropy: {fib_stat.get('entropy', 0):.3f}, Active Gates: {fib_stat.get('active_gates', 0)}")
                
                # Quad Core Automata Stats
                st.write("**🛡️ Quad Core Error Detection:**")
                for quad_stat in automata_analysis['quad_core_automata']:
                    st.write(f"⚙️ **{quad_stat['automaton_id']}**: Agreement: {quad_stat['core_agreement_pct']:.1f}%, Faults: {quad_stat['total_faults_detected']} (corrected: {quad_stat['total_faults_corrected']}), Tolerance: {quad_stat['fault_tolerance_score']:.2%}")
                
                # Show latest automata insight
                if user_state.automata_insights:
                    latest_automata = user_state.automata_insights[-1]
                    st.write("**Latest Advanced Automata Analysis:**")
                    st.write(f"🧬 {latest_automata}")
                
                # Automata control buttons
                auto_col1, auto_col2 = st.columns(2)
                
                with auto_col1:
                    if st.button("🌀 Step Automata"):
                        user_state.advanced_automata.step_all()
                        st.success("Advanced automata stepped forward one generation")
                        st.rerun()
                
                with auto_col2:
                    if st.button("🔄 Reset Automata"):
                        set_user_state('advanced_automata', create_advanced_automata_swarm(num_fibonacci, num_quad_core))
                        st.success("Advanced automata reset!")
                        st.rerun()
            else:
                st.info("Enable Advanced Automata in sidebar to see Fibonacci and Quad Core analysis")
        
        # Update metrics display
        with metrics_placeholder.container():
            if len(user_state.metrics_history) > 0:
                latest_metrics = user_state.metrics_history[-1]
                
                # Create metrics dashboard
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                
                with metric_col1:
                    st.metric(
                        "Pass@1 Score", 
                        f"{latest_metrics['pass_at_1']:.3f}",
                        delta=f"{latest_metrics['pass_at_1'] - target_pass_at_1:.3f}"
                    )
                
                with metric_col2:
                    st.metric(
                        "Latency (ms/token)", 
                        f"{latest_metrics['latency']:.1f}",
                        delta=f"{target_latency - latest_metrics['latency']:.1f}"
                    )
                
                with metric_col3:
                    st.metric(
                        "Energy Efficiency", 
                        f"{latest_metrics['energy_efficiency']:.2f}W"
                    )
                
                with metric_col4:
                    st.metric(
                        "Mesh Coherence", 
                        f"{latest_metrics['coherence']:.3f}"
                    )
                
                # Performance trend chart
                if len(user_state.metrics_history) > 5:
                    metrics_df = pd.DataFrame(user_state.metrics_history)
                    
                    fig_trends = make_subplots(
                        rows=2, cols=2,
                        subplot_titles=('Pass@1 Score', 'Latency', 'Energy', 'Coherence'),
                        vertical_spacing=0.1
                    )
                    
                    fig_trends.add_trace(
                        go.Scatter(y=metrics_df['pass_at_1'], mode='lines', name='Pass@1'),
                        row=1, col=1
                    )
                    fig_trends.add_trace(
                        go.Scatter(y=metrics_df['latency'], mode='lines', name='Latency'),
                        row=1, col=2
                    )
                    fig_trends.add_trace(
                        go.Scatter(y=metrics_df['energy_efficiency'], mode='lines', name='Energy'),
                        row=2, col=1
                    )
                    fig_trends.add_trace(
                        go.Scatter(y=metrics_df['coherence'], mode='lines', name='Coherence'),
                        row=2, col=2
                    )
                    
                    fig_trends.update_layout(height=400, showlegend=False, title_text="Performance Trends")
                    st.plotly_chart(fig_trends, use_container_width=True)
        
        # Update progress
        progress_bar.progress((step + 1) / (ca_steps_forward + ca_steps_reverse))
        
        # Brief pause for visualization
        time.sleep(0.1)
    
    # Simulation complete
    user_state.simulation_running = False
    progress_bar.empty()
    st.success("🎉 Simulation completed successfully!")
    
    # Final results summary
    if user_state.metrics_history:
        final_metrics = user_state.metrics_history[-1]
        st.subheader("📋 Final Results Summary")
        
        results_col1, results_col2 = st.columns(2)
        
        with results_col1:
            st.write("**Performance Achieved:**")
            st.write(f"• Pass@1 Score: {final_metrics['pass_at_1']:.4f}")
            st.write(f"• Latency: {final_metrics['latency']:.2f} ms/token")
            st.write(f"• Energy Efficiency: {final_metrics['energy_efficiency']:.2f}W")
            st.write(f"• Mesh Coherence: {final_metrics['coherence']:.4f}")
        
        with results_col2:
            st.write("**Target Comparison:**")
            pass_diff = final_metrics['pass_at_1'] - target_pass_at_1
            latency_diff = target_latency - final_metrics['latency']
            
            st.write(f"• Pass@1 Δ: {pass_diff:+.4f} {'✅' if pass_diff >= 0 else '❌'}")
            st.write(f"• Latency Δ: {latency_diff:+.2f}ms {'✅' if latency_diff >= 0 else '❌'}")
            st.write(f"• Swarm Pockets: {num_pockets} active")
            st.write(f"• AI Models: {num_ai_models} local models")
            if enable_micro_pms:
                st.write(f"• Micro PMs: 3 specialized models")
            if enable_tiny_cluster:
                st.write(f"• Tiny Cluster: 3 real-world models (882M params)")
            if enable_advanced_automata:
                st.write(f"• Advanced Automata: {num_fibonacci} Fibonacci + {num_quad_core} Quad Core")
            st.write(f"• Total Steps: {ca_steps_forward + ca_steps_reverse}")
            
            # Final AI summary
            if user_state.ai_insights:
                final_ai_stats = user_state.ai_swarm.get_swarm_stats()
                st.write("\n**AI Processing Summary:**")
                st.write(f"• AI Analyses: {len(user_state.ai_insights)}")
                st.write(f"• Total Parameters: {final_ai_stats['total_parameters']:,}")
                st.write(f"• Model Diversity: {final_ai_stats['model_diversity']} variants")
            
            # Final Micro PM summary
            if enable_micro_pms and user_state.micro_insights:
                final_micro_stats = user_state.micro_system.get_system_stats()
                st.write("\n**Micro PM Summary:**")
                st.write(f"• Micro Analyses: {len(user_state.micro_insights)}")
                st.write(f"• Micro Parameters: {final_micro_stats['total_parameters']:,}")
                st.write(f"• Specializations: {', '.join(final_micro_stats['specializations'])}")
            
            # Final Tiny Cluster summary
            if enable_tiny_cluster and user_state.cluster_insights:
                final_cluster_overview = user_state.tiny_cluster.get_cluster_overview()
                st.write("\n**Tiny Cluster Summary:**")
                st.write(f"• Cluster Inferences: {len(user_state.cluster_insights)}")
                st.write(f"• Strategy Used: {cluster_strategy}")
                st.write(f"• Models: Qwen2.5-0.5B, SmolLM2-360M, MiniLM-L6-v2")
                st.write(f"• Cluster Health: {final_cluster_overview['cluster_info']['cluster_health']}")

# Footer with research information
st.markdown("---")
st.markdown("""
**HelixGrapheneLM Research Project** | *Symbiotic Graphene Mesh for Pocket-Sized Language Models*

This simulation demonstrates the theoretical framework for double helix tensor processing 
with two-way cellular automata in a symbiotic graphene mesh architecture. Now featuring 
**local AI models** that run entirely offline without requiring external API keys!

🤖 **Local AI Features:**
• Multiple tiny language models (TinyLM-Alpha, Beta, Gamma)
• **Three specialized Micro PMs (MeshPM, AutomataPM, SwarmPM)**
• **Real-world Tiny Model Cluster (Qwen2.5-0.5B, SmolLM2-360M, MiniLM-L6-v2)**
• Distributed inference with consensus/load-balancing/specialization/failover
• Domain-specific analysis for each system component
• Ultra-lightweight micro models (<20K parameters each)
• Industry-proven tiny models (882M total parameters)
• Zero external dependencies - runs completely offline

*Contact: mosijbuilder@gmail.com | September 2025*
""")
