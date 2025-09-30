import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="Ayur Allergy Mapper",
    page_icon="🌿",
    layout="wide"
)

# API endpoint - change this to your actual deployed URL
API_URL = "http://localhost:8000/map"


# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #2e7d32;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .candidate-card {
        background-color: #f5f5f5;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 5px solid #4caf50;
    }
    .confidence-high {
        background-color: #c8e6c9;
        padding: 0.3rem 0.6rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .confidence-medium {
        background-color: #fff9c4;
        padding: 0.3rem 0.6rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .confidence-low {
        background-color: #ffccbc;
        padding: 0.3rem 0.6rem;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🌿 Ayur Allergy Mapper</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Find Ayurvedic herb alternatives for pharmaceutical drugs</p>', unsafe_allow_html=True)

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    This tool helps identify potential Ayurvedic herb alternatives 
    when patients have allergies to conventional medications.
    
    **How to use:**
    1. Enter the drug name (e.g., "Penicillin", "Ibuprofen")
    2. Click "Find Alternatives"
    3. Review the suggested herbs and their safety information
    """)
    
    st.header("⚠️ Important Disclaimer")
    st.warning("""
    This is a research and educational tool only. 
    
    **Always consult with qualified healthcare professionals** 
    before making any treatment decisions.
    """)
    
    st.header("📋 Example Drugs")
    st.info("""
    Try searching for:
    - Penicillin G
    - Amoxicillin
    - Ibuprofen
    - Aspirin
    - Omeprazole
    - Cetirizine
    """)

# Main content area
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Drug input
    drug_name = st.text_input(
        "Enter Drug Name",
        placeholder="e.g., Penicillin, Ibuprofen, Amoxicillin",
        help="Enter the name of the pharmaceutical drug you want to find alternatives for"
    )
    
    search_button = st.button("🔍 Find Alternatives", type="primary", use_container_width=True)

# Search functionality
if search_button and drug_name:
    with st.spinner(f'Searching for alternatives to {drug_name}...'):
        try:
            # Make API request
            response = requests.post(
                API_URL,
                json={"drug": drug_name},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Display normalized drug information
                st.success(f"✅ Found information for: **{drug_name}**")
                
                with st.expander("📊 Drug Information", expanded=True):
                    normalized = data.get("normalized", {})
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write("**Drug Name:**", normalized.get("name", "N/A"))
                        st.write("**RxCUI:**", normalized.get("rxcui", "N/A"))
                    with col_b:
                        st.write("**Type:**", normalized.get("tty", "N/A"))
                        st.write("**Synonym:**", normalized.get("synonym", "N/A") or "None")
                
                # Display therapeutic classes
                if data.get("therapeutic_classes"):
                    with st.expander("💊 Therapeutic Classes"):
                        for cls in data["therapeutic_classes"]:
                            st.write(f"- **{cls.get('className')}** ({cls.get('classType')})")
                
                # Display indication keywords
                if data.get("indication_keywords"):
                    st.write("**🎯 Therapeutic Functions:**")
                    keywords_str = ", ".join(data["indication_keywords"])
                    st.info(keywords_str)
                
                # Display candidates
                st.markdown("---")
                st.header("🌿 Suggested Ayurvedic Alternatives")
                
                candidates = data.get("candidates", [])
                
                if candidates:
                    for idx, candidate in enumerate(candidates, 1):
                        # Confidence badge color
                        confidence = candidate.get("confidence", "Low")
                        conf_class = f"confidence-{confidence.lower()}"
                        
                        with st.container():
                            st.markdown(f"### {idx}. {candidate.get('common', 'Unknown')}")
                            
                            col_x, col_y, col_z = st.columns([2, 1, 1])
                            
                            with col_x:
                                st.write(f"**Sanskrit:** {candidate.get('sanskrit', 'N/A')}")
                                st.write(f"**Botanical:** *{candidate.get('botanical', 'N/A')}*")
                            
                            with col_y:
                                st.markdown(f'<span class="{conf_class}">Confidence: {confidence}</span>', 
                                          unsafe_allow_html=True)
                            
                            with col_z:
                                st.metric("Score", candidate.get("score", 0))
                            
                            # Risk information
                            risk = candidate.get("risk", {})
                            risk_label = risk.get("label", "Unknown")
                            
                            if risk_label == "Low" or "Low" in risk_label:
                                st.success(f"**Risk Level:** {risk_label}")
                            elif risk_label == "Medium" or "Moderate" in risk_label:
                                st.warning(f"**Risk Level:** {risk_label}")
                            else:
                                st.error(f"**Risk Level:** {risk_label}")
                            
                            # Risk notes
                            risk_notes = risk.get("notes", [])
                            if risk_notes:
                                st.write("**⚠️ Safety Notes:**")
                                for note in risk_notes:
                                    st.write(f"- {note}")
                            
                            # Why this herb
                            why = candidate.get("why", [])
                            if why:
                                with st.expander("Why this herb?"):
                                    for reason in why:
                                        st.write(reason)
                            
                            # Evidence links
                            evidence_links = candidate.get("evidence_links", [])
                            if evidence_links:
                                st.write("**📚 Research Evidence:**")
                                for link in evidence_links:
                                    st.markdown(f"- [PubMed Article]({link})")
                            
                            # References
                            refs = candidate.get("refs", [])
                            if refs:
                                with st.expander("📖 Traditional References"):
                                    for ref in refs:
                                        st.write(f"- {ref}")
                            
                            st.markdown("---")
                else:
                    st.warning("No suitable Ayurvedic alternatives found for this drug.")
                
                # Disclaimer
                st.markdown("---")
                st.error(f"⚠️ **{data.get('disclaimer', 'Always consult a clinician.')}**")
                
            elif response.status_code == 404:
                st.error(f"""
                **Drug not found:** Could not normalize '{drug_name}'.
                
                Please try:
                - Using the specific drug name (e.g., 'Penicillin G' instead of just 'Penicillin')
                - Checking the spelling
                - Using the generic name instead of brand name (or vice versa)
                """)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("""
            **Connection Error:** Cannot connect to the API server.
            
            Please ensure:
            1. The FastAPI server is running
            2. The API_URL is correctly configured
            3. There are no firewall issues
            """)
        except requests.exceptions.Timeout:
            st.error("Request timed out. The server might be slow or unavailable.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

elif search_button and not drug_name:
    st.warning("⚠️ Please enter a drug name to search.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>Ayur Allergy Mapper v0.5.0 | For research and educational purposes only</p>
    <p>🌿 Bridging Traditional Ayurveda with Modern Medicine 🌿</p>
</div>
""", unsafe_allow_html=True)