import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, Optional

# Page configuration
st.set_page_config(
    page_title="AYUSH ↔ WHO Health Search Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #4CAF50 0%, #2196F3 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .search-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin-bottom: 1rem;
    }
    
    .result-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 3px solid #2196F3;
    }
    
    .health-passport-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: #f1f3f4;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

# Configuration
API_BASE_URL = "http://localhost:8000"  # Change this to your API URL

class APIClient:
    """Simple API client for interacting with the AYUSH-WHO API"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    
    def search_mappings(self, term: str, threshold: int = 80) -> Dict[str, Any]:
        """Search for AYUSH-WHO mappings"""
        try:
            response = requests.get(
                f"{self.base_url}/search/{term}",
                params={"threshold": threshold},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_demo_health_passport(self) -> Dict[str, Any]:
        """Get demo health passport"""
        try:
            response = requests.get(f"{self.base_url}/demo/health-passport", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_health_passport(self, token: str) -> Dict[str, Any]:
        """Get authenticated health passport"""
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{self.base_url}/health-passport", headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_api_status(self) -> Dict[str, Any]:
        """Get API health status"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

# Initialize API client
api_client = APIClient(API_BASE_URL)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 AYUSH ↔ WHO Health Search Portal</h1>
        <p>Bridging Traditional Medicine with Global Health Standards</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Settings & Navigation")
        
        # API Configuration
        st.subheader("API Configuration")
        api_url = st.text_input("API Base URL", value=API_BASE_URL, help="URL of your AYUSH-WHO API")
        if api_url != API_BASE_URL:
            global api_client
            api_client = APIClient(api_url)
        
        # Check API Status
        if st.button("🔍 Check API Status"):
            with st.spinner("Checking API status..."):
                status = api_client.get_api_status()
                if "error" not in status:
                    st.success("✅ API is running")
                    st.json(status)
                else:
                    st.error(f"❌ API Error: {status['error']}")
        
        st.divider()
        
        # Navigation
        st.subheader("📋 Navigation")
        page = st.radio(
            "Select a feature:",
            ["🔍 Search Mappings", "📋 Health Passport", "📊 Analytics"],
            help="Choose what you'd like to do"
        )
    
    # Main content area
    if page == "🔍 Search Mappings":
        show_search_page()
    elif page == "📋 Health Passport":
        show_health_passport_page()
    elif page == "📊 Analytics":
        show_analytics_page()

def show_search_page():
    """Display the semantic search page"""
    st.header("🔍 Search AYUSH ↔ WHO Mappings")
    
    st.markdown("""
    <div class="search-box">
        <h4>🎯 What would you like to search for?</h4>
        <p>Enter any medical condition, symptom, or treatment name in English, Hindi, or Sanskrit. 
        Our AI will find relevant mappings between traditional AYUSH systems and WHO standards.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search form
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input(
            "Enter medical term:",
            placeholder="e.g., diabetes, hypertension, Madhumeha, Rakta Gata Vata...",
            help="You can search in English, Hindi, or Sanskrit"
        )
    
    with col2:
        threshold = st.slider(
            "Match Sensitivity",
            min_value=50,
            max_value=100,
            value=80,
            step=5,
            help="Higher values = more exact matches, Lower values = more broad matches"
        )
    
    # Search examples
    st.markdown("**💡 Example searches:** *diabetes, hypertension, arthritis, Madhumeha, Amavata, Rakta Gata Vata*")
    
    # Quick search buttons
    st.markdown("**⚡ Quick Search:**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🍯 Diabetes"):
            search_term = "diabetes"
    with col2:
        if st.button("💓 Hypertension"):
            search_term = "hypertension"
    with col3:
        if st.button("🦴 Arthritis"):
            search_term = "arthritis"
    with col4:
        if st.button("🧘 Madhumeha"):
            search_term = "madhumeha"
    
    # Perform search
    if search_term:
        with st.spinner(f"🔍 Searching for '{search_term}'..."):
            results = api_client.search_mappings(search_term, threshold)
            
            if "error" in results:
                st.error(f"❌ Search failed: {results['error']}")
            elif "mappings" not in results or not results["mappings"]:
                st.warning(f"🤷 No matches found for '{search_term}' with {threshold}% sensitivity")
                st.info("💡 Try lowering the match sensitivity or using different search terms")
            else:
                display_search_results(results)

def display_search_results(results: Dict[str, Any]):
    """Display search results in a user-friendly format"""
    mappings = results.get("mappings", [])
    
    # Results summary
    st.success(f"✅ Found {len(mappings)} matches for '{results['query']}'")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 Results List", "📊 Visual Summary", "📁 Export Data"])
    
    with tab1:
        # Display each mapping
        for i, mapping in enumerate(mappings, 1):
            with st.container():
                st.markdown(f"""
                <div class="result-card">
                    <h4>#{i} - {mapping.get('AYUSH_Term', 'N/A')}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🌿 AYUSH Information:**")
                    st.write(f"**Term:** {mapping.get('AYUSH_Term', 'N/A')}")
                    st.write(f"**Code:** {mapping.get('AYUSH_Code', 'N/A')}")
                    st.write(f"**System:** {mapping.get('Target_System', 'N/A')}")
                
                with col2:
                    st.markdown("**🌍 WHO Information:**")
                    st.write(f"**Term:** {mapping.get('WHO_Term_Candidate', 'N/A')}")
                    st.write(f"**Code:** {mapping.get('WHO_Code_Candidate', 'N/A')}")
                
                # Similarity score with progress bar
                similarity = mapping.get('Similarity_Score', 0)
                if similarity:
                    st.markdown("**🎯 Match Quality:**")
                    st.progress(similarity, text=f"{similarity:.1%} similarity")
                
                # Relationship type
                relationship = mapping.get('Suggested_Relationship', 'N/A')
                if relationship != 'N/A':
                    st.info(f"**Relationship Type:** {relationship}")
                
                st.divider()
    
    with tab2:
        display_visual_summary(mappings)
    
    with tab3:
        display_export_options(results)

def display_visual_summary(mappings):
    """Display visual summary of search results"""
    if not mappings:
        st.info("No data to visualize")
        return
    
    df = pd.DataFrame(mappings)
    
    # System distribution
    if 'Target_System' in df.columns:
        st.subheader("📊 Distribution by AYUSH System")
        system_counts = df['Target_System'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pie = px.pie(
                values=system_counts.values,
                names=system_counts.index,
                title="AYUSH Systems Distribution"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("**📈 System Breakdown:**")
            for system, count in system_counts.items():
                st.metric(system, count)
    
    # Similarity score distribution
    if 'Similarity_Score' in df.columns:
        st.subheader("🎯 Match Quality Distribution")
        
        # Filter out null values
        similarity_scores = df['Similarity_Score'].dropna()
        
        if not similarity_scores.empty:
            fig_hist = px.histogram(
                similarity_scores,
                nbins=10,
                title="Distribution of Match Quality Scores",
                labels={'value': 'Similarity Score', 'count': 'Number of Mappings'}
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            
            # Quality metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Quality", f"{similarity_scores.mean():.1%}")
            with col2:
                st.metric("Best Match", f"{similarity_scores.max():.1%}")
            with col3:
                st.metric("Total Matches", len(similarity_scores))

def display_export_options(results):
    """Display data export options"""
    st.subheader("📁 Export Search Results")
    
    # Convert to DataFrame
    if results.get("mappings"):
        df = pd.DataFrame(results["mappings"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CSV Export
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="📄 Download as CSV",
                data=csv_data,
                file_name=f"ayush_who_mappings_{results['query']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # JSON Export
            json_data = json.dumps(results, indent=2)
            st.download_button(
                label="📋 Download as JSON",
                data=json_data,
                file_name=f"ayush_who_mappings_{results['query']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        # Preview the data
        st.subheader("👀 Data Preview")
        st.dataframe(df, use_container_width=True)

def show_health_passport_page():
    """Display the health passport page"""
    st.header("📋 Digital Health Passport")
    
    st.markdown("""
    <div class="health-passport-card">
        <h4>🔐 Your Digital Health Record</h4>
        <p>Access your comprehensive health information with AYUSH-WHO integrated mappings.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Authentication options
    auth_tab1, auth_tab2 = st.tabs(["🆓 Demo Access", "🔐 ABHA Login"])
    
    with auth_tab1:
        st.subheader("🎭 Demo Health Passport")
        st.info("💡 This is a demonstration using sample health data - no login required!")
        
        if st.button("🚀 View Demo Health Passport", type="primary"):
            with st.spinner("📥 Loading demo health passport..."):
                passport_data = api_client.get_demo_health_passport()
                
                if "error" in passport_data:
                    st.error(f"❌ Failed to load passport: {passport_data['error']}")
                else:
                    display_health_passport(passport_data)
    
    with auth_tab2:
        st.subheader("🔐 ABHA Authenticated Access")
        
        # Test token options
        st.markdown("**🧪 For testing, use these tokens:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            token_option = st.selectbox(
                "Choose test user:",
                [
                    "test_patient_001 (Test Patient)",
                    "test_doctor_001 (Dr. Test Physician)",
                    "demo_user (Demo User)",
                    "custom (Enter your own token)"
                ]
            )
        
        with col2:
            if token_option == "custom":
                auth_token = st.text_input("Enter ABHA token:", placeholder="Your ABHA authentication token")
            else:
                auth_token = token_option.split(" ")[0]
                st.text_input("Token:", value=auth_token, disabled=True)
        
        if st.button("🔓 Access Health Passport", type="primary"):
            if auth_token:
                with st.spinner("🔍 Authenticating and loading health passport..."):
                    passport_data = api_client.get_health_passport(auth_token)
                    
                    if "error" in passport_data:
                        st.error(f"❌ Authentication failed: {passport_data['error']}")
                    else:
                        display_health_passport(passport_data)
            else:
                st.warning("⚠️ Please enter an authentication token")

def display_health_passport(passport_data):
    """Display health passport data in a user-friendly format"""
    if "health_passport" not in passport_data:
        st.error("❌ Invalid passport data received")
        return
    
    passport = passport_data["health_passport"]
    user_info = passport_data.get("user", {})
    
    # User header
    st.success("✅ Health Passport Loaded Successfully!")
    
    # Patient demographics
    demographics = passport.get("patient_demographics", {})
    
    with st.container():
        st.markdown("### 👤 Patient Information")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Name", demographics.get("name", "Unknown"))
        with col2:
            st.metric("Age", f"{demographics.get('age', 'Unknown')} years")
        with col3:
            st.metric("Blood Group", demographics.get("blood_group", "Unknown"))
        with col4:
            st.metric("ABHA ID", user_info.get("abha_id", "Unknown"))
    
    # Medical History
    if passport.get("medical_history"):
        st.markdown("### 🏥 Medical History")
        
        for condition in passport["medical_history"]:
            with st.expander(f"📋 {condition['condition']} - {condition['severity']} ({condition['diagnosed_date']})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🌿 AYUSH Information:**")
                    st.write(f"**Term:** {condition.get('ayush_term', 'N/A')}")
                    st.write(f"**Code:** {condition.get('ayush_code', 'N/A')}")
                    st.write(f"**System:** {condition.get('system', 'N/A')}")
                
                with col2:
                    st.markdown("**🌍 WHO Information:**")
                    st.write(f"**Code:** {condition.get('who_code', 'N/A')}")
                    st.write(f"**Severity:** {condition.get('severity', 'N/A')}")
                    st.write(f"**Diagnosed:** {condition.get('diagnosed_date', 'N/A')}")
                
                # Show semantic mappings if available
                if condition.get("semantic_mappings"):
                    st.markdown("**🔗 Related Mappings:**")
                    for mapping in condition["semantic_mappings"][:3]:
                        st.info(f"🔹 {mapping.get('AYUSH_Term', 'N/A')} ↔ {mapping.get('WHO_Term_Candidate', 'N/A')} ({mapping.get('Similarity_Score', 0):.1%} match)")
    
    # Current Medications
    if passport.get("current_medications"):
        st.markdown("### 💊 Current Medications")
        
        for med in passport["current_medications"]:
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**🌿 {med['medicine']}**")
                    st.write(f"Dosage: {med['dosage']}")
                
                with col2:
                    st.write(f"System: {med['system']}")
                
                with col3:
                    st.write(f"Since: {med['prescribed_date']}")
                
                st.divider()
    
    # Vital Signs
    if passport.get("vital_signs"):
        st.markdown("### 📈 Latest Vital Signs")
        vitals = passport["vital_signs"]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Blood Pressure", vitals.get("blood_pressure", "N/A"))
        with col2:
            st.metric("Heart Rate", vitals.get("heart_rate", "N/A"))
        with col3:
            st.metric("Weight", vitals.get("weight", "N/A"))
        with col4:
            st.metric("BMI", vitals.get("bmi", "N/A"))
        
        st.caption(f"Last recorded: {vitals.get('last_recorded', 'Unknown')}")
    
    # Allergies
    if passport.get("allergies"):
        st.markdown("### ⚠️ Allergies")
        for allergy in passport["allergies"]:
            st.warning(f"🚨 {allergy}")

def show_analytics_page():
    """Display analytics and statistics"""
    st.header("📊 System Analytics")
    
    st.info("📈 Analytics features will show mapping statistics, usage patterns, and system health metrics.")
    
    # Mock analytics data
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Mappings", "2,547", delta="23 new")
    
    with col2:
        st.metric("API Calls Today", "156", delta="12%")
    
    with col3:
        st.metric("Average Match Quality", "87.3%", delta="2.1%")
    
    with col4:
        st.metric("Active Users", "42", delta="5")
    
    # Sample charts
    st.subheader("📈 Usage Trends")
    
    # Sample data for demonstration
    dates = pd.date_range(start="2024-09-01", end="2024-09-29", freq="D")
    usage_data = pd.DataFrame({
        "Date": dates,
        "API Calls": [50 + i*2 + (i%7)*10 for i in range(len(dates))],
        "Unique Users": [10 + i//3 + (i%5)*2 for i in range(len(dates))]
    })
    
    fig = px.line(usage_data, x="Date", y=["API Calls", "Unique Users"], 
                  title="Daily API Usage")
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()