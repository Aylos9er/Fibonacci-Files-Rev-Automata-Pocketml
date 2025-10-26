"""
Replit Auth utilities for Streamlit applications
Uses Replit's integrated authentication system
"""
import os
import streamlit as st


class ReplitAuth:
    """Replit Authentication handler for Streamlit apps using integrated auth"""
    
    def __init__(self):
        # Get user info from Replit environment variables
        self.replit_user = os.getenv('REPLIT_USER')
        self.repl_owner = os.getenv('REPL_OWNER')
        self.repl_owner_id = os.getenv('REPL_OWNER_ID')
        self.replit_userid = os.getenv('REPLIT_USERID')
        
        # Check if we're in a Replit environment with authenticated user
        self.in_replit = bool(self.replit_user and self.repl_owner)
    
    def is_authenticated(self):
        """Check if user is currently authenticated in Replit environment"""
        return self.in_replit and self.replit_user is not None
    
    def get_current_user(self):
        """Get current authenticated user info from Replit environment"""
        if not self.is_authenticated():
            return None
            
        return {
            'id': self.replit_userid or self.repl_owner_id,
            'name': self.replit_user,
            'username': self.replit_user,
            'email': f"{self.replit_user}@replit.user",  # Placeholder email
            'picture': f"https://replit.com/@{self.replit_user}.png"  # Replit avatar URL format
        }
    
    def logout(self):
        """Clear session data (note: cannot actually log out of Replit environment)"""
        user = self.get_current_user()
        user_id = user.get('id', 'anonymous') if user else 'anonymous'
        user_prefix = f"user_{user_id}_"
        
        # Clear user-specific session state data
        keys_to_remove = [key for key in st.session_state.keys() if isinstance(key, str) and key.startswith(user_prefix)]
        for key in keys_to_remove:
            del st.session_state[key]
            
        # Clear any generic aliases that might exist
        generic_keys = ['mesh', 'ca', 'tensor_processor', 'visualizer', 'swarm', 
                       'ai_swarm', 'micro_system', 'tiny_cluster', 'simulation_running',
                       'metrics_history', 'ai_insights', 'micro_insights', 'cluster_insights']
        for key in generic_keys:
            if key in st.session_state:
                del st.session_state[key]
                
        st.success("Session cleared! Note: You remain authenticated in your Replit environment.")
        st.rerun()


def require_auth(func):
    """Decorator to require authentication for a function"""
    def wrapper(*args, **kwargs):
        auth = ReplitAuth()
        if not auth.is_authenticated():
            show_login_page()
            return None
        return func(*args, **kwargs)
    return wrapper


def show_login_page():
    """Display information about authentication requirements"""
    st.title("🔐 Authentication Required")
    st.markdown("""This application requires authentication to access PocketLM - Symbiotic Graphene Mesh Simulation.
    
    **If you're seeing this page, it means:**
    - You may not be in an authenticated Replit environment
    - The application cannot detect your Replit user information
    
    **To resolve this:**
    - Ensure you're running this app in a Replit environment
    - Make sure you're logged into your Replit account
    - Try refreshing the page
    """)
    
    auth = ReplitAuth()
    
    st.info(f"Debug Info: Detected user: {auth.replit_user or 'None'}")
    
    if st.button("🔄 Retry Authentication", type="primary", use_container_width=True):
        st.rerun()


def show_user_info():
    """Display current user information in sidebar"""
    auth = ReplitAuth()
    user = auth.get_current_user()
    
    if user:
        st.sidebar.markdown("---")
        st.sidebar.subheader("👤 User Profile")
        
        # User avatar and info
        if user.get('picture'):
            st.sidebar.image(user['picture'], width=60)
        
        st.sidebar.write(f"**{user.get('name', 'User')}**")
        st.sidebar.write(f"📧 {user.get('email', 'No email')}")
        
        # Logout button
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            auth.logout()


def init_auth():
    """Initialize Replit integrated authentication system"""
    # No session state initialization needed for integrated auth
    pass