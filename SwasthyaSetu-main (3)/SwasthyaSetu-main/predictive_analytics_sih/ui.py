import streamlit as st
import requests
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Hybrid Treatment Planner",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #4CAF50, #2196F3);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .result-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .diet-card {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
    }
    
    .treatment-card {
        background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
    }
    
    .yoga-card {
        background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-top: 3px solid #4CAF50;
    }
    
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #4CAF50, #45a049);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'assessment_done' not in st.session_state:
    st.session_state.assessment_done = False

# Header
st.markdown("""
<div class="main-header">
    <h1>🌿 Hybrid Treatment Planner</h1>
    <p>AI-Powered Holistic Health with Diet, Yoga, and Modern Medicine</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for API configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    api_url = st.text_input(
        "Backend API URL", 
        value="http://localhost:8000",
        help="Enter your backend API URL"
    )
    
    # Check API status
    try:
        response = requests.get(f"{api_url}/health", timeout=5)
        if response.status_code == 200:
            st.success("✅ API Connected")
            status_data = response.json()
            st.json(status_data)
        else:
            st.error("❌ API Connection Failed")
    except:
        st.warning("⚠️ Cannot reach API")
    
    st.markdown("---")
    st.markdown("### 📊 Features")
    features = [
        "🍎 Therapeutic Diet Planning",
        "💊 Modern Medicine Integration", 
        "🌿 Ayurvedic Treatment",
        "🧘 Yoga Therapy",
        "🔄 Holistic Integration"
    ]
    for feature in features:
        st.markdown(f"**{feature}**")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 👤 Patient Information")
    
    # Patient details form
    with st.form("patient_form"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            patient_name = st.text_input("Patient Name", placeholder="Enter full name")
            age = st.number_input("Age", min_value=1, max_value=120, value=30)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            
        with col_b:
            height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
            weight = st.number_input("Weight (kg)", min_value=30, max_value=300, value=70)
            activity_level = st.selectbox(
                "Activity Level", 
                ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"]
            )
        
        st.markdown("### 🩺 Symptoms & Health Concerns")
        
        # Predefined symptoms with custom option
        symptom_categories = {
            "General": ["Fatigue", "Stress", "Anxiety", "Insomnia", "Headache"],
            "Digestive": ["Stomach Pain", "Bloating", "Constipation", "Diarrhea", "Nausea"],
            "Respiratory": ["Cough", "Cold", "Breathing Issues", "Chest Pain"],
            "Musculoskeletal": ["Joint Pain", "Back Pain", "Muscle Cramps", "Arthritis"],
            "Cardiovascular": ["High BP", "Heart Palpitations", "Chest Tightness"],
            "Metabolic": ["Diabetes", "Weight Gain", "Weight Loss", "High Cholesterol"]
        }
        
        selected_symptoms = []
        for category, symptoms in symptom_categories.items():
            st.markdown(f"**{category}:**")
            cols = st.columns(3)
            for i, symptom in enumerate(symptoms):
                with cols[i % 3]:
                    if st.checkbox(symptom, key=f"{category}_{symptom}"):
                        selected_symptoms.append(symptom)
        
        # Custom symptoms
        custom_symptoms = st.text_area(
            "Additional Symptoms/Concerns", 
            placeholder="Enter any other symptoms or health concerns..."
        )
        if custom_symptoms:
            selected_symptoms.extend([s.strip() for s in custom_symptoms.split(',') if s.strip()])
        
        st.markdown("### 🍽️ Dietary Preferences")
        
        col_diet1, col_diet2 = st.columns(2)
        with col_diet1:
            diet_type = st.selectbox(
                "Diet Type", 
                ["Omnivore", "Vegetarian", "Vegan", "Keto", "Mediterranean", "Other"]
            )
            allergies = st.text_input("Food Allergies", placeholder="e.g., nuts, dairy, gluten")
            
        with col_diet2:
            cuisine_pref = st.multiselect(
                "Cuisine Preferences",
                ["Indian", "Mediterranean", "Asian", "Western", "Mexican", "Middle Eastern"]
            )
            cooking_time = st.selectbox(
                "Preferred Cooking Time",
                ["Quick (15-30 min)", "Moderate (30-60 min)", "Elaborate (60+ min)"]
            )
        
        st.markdown("### 🏃 Lifestyle Factors")
        
        col_life1, col_life2 = st.columns(2)
        with col_life1:
            exercise_freq = st.selectbox(
                "Exercise Frequency",
                ["Never", "1-2 times/week", "3-4 times/week", "5+ times/week"]
            )
            sleep_hours = st.slider("Average Sleep Hours", 4, 12, 8)
            
        with col_life2:
            stress_level = st.slider("Stress Level (1-10)", 1, 10, 5)
            yoga_experience = st.selectbox(
                "Yoga Experience",
                ["Beginner", "Intermediate", "Advanced", "None"]
            )
        
        # Submit button
        submitted = st.form_submit_button(
            "🔍 Get Hybrid Treatment Plan", 
            use_container_width=True
        )

with col2:
    st.markdown("## 📊 Quick Stats")
    
    if patient_name and age and weight and height:
        # Calculate BMI
        bmi = weight / ((height/100) ** 2)
        bmi_category = "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"
        
        # Display metrics
        st.markdown(f"""
        <div class="metric-card">
            <h3>BMI</h3>
            <h2>{bmi:.1f}</h2>
            <p>{bmi_category}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>Age Group</h3>
            <h2>{age} years</h2>
            <p>{"Young Adult" if age < 30 else "Adult" if age < 60 else "Senior"}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>Activity</h3>
            <h2>{activity_level}</h2>
            <p>Lifestyle Assessment</p>
        </div>
        """, unsafe_allow_html=True)

# Process form submission
if submitted and patient_name and selected_symptoms:
    # Prepare data for API
    patient_data = {
        "name": patient_name,
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "activity_level": activity_level
    }
    
    dietary_preferences = {
        "diet_type": diet_type,
        "allergies": allergies.split(',') if allergies else [],
        "cuisine_preferences": cuisine_pref,
        "cooking_time": cooking_time
    }
    
    lifestyle_factors = {
        "exercise_frequency": exercise_freq,
        "sleep_hours": sleep_hours,
        "stress_level": stress_level,
        "yoga_experience": yoga_experience
    }
    
    # API call
    with st.spinner("🔄 Generating your personalized hybrid treatment plan..."):
        try:
            api_data = {
                "patient_data": patient_data,
                "symptoms": selected_symptoms,
                "dietary_preferences": dietary_preferences,
                "lifestyle_factors": lifestyle_factors
            }
            
            response = requests.post(
                f"{api_url}/hybrid-assessment",
                json=api_data,
                timeout=30
            )
            
            if response.status_code == 200:
                st.session_state.recommendations = response.json()
                st.session_state.assessment_done = True
                st.success("✅ Treatment plan generated successfully!")
            else:
                st.error(f"❌ API Error: {response.status_code}")
                st.json(response.json() if response.content else "No response content")
                
        except requests.exceptions.RequestException as e:
            st.error(f"🔌 Connection Error: {str(e)}")
        except Exception as e:
            st.error(f"💥 Unexpected Error: {str(e)}")

elif submitted:
    st.warning("⚠️ Please fill in patient name and select at least one symptom.")

# Display results
if st.session_state.assessment_done and st.session_state.recommendations:
    st.markdown("---")
    st.markdown("# 📋 Your Personalized Hybrid Treatment Plan")
    
    rec = st.session_state.recommendations.get("hybrid_recommendations", {})
    
    # Create tabs for different aspects
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🍎 Diet Plan", "💊 Modern Treatment", "🌿 Ayurvedic", "🧘 Yoga Therapy", "🔄 Integration"
    ])
    
    with tab1:
        st.markdown("## 🍎 Therapeutic Diet Plan")
        
        diet_plan = rec.get("diet_plan", {})
        
        # Therapeutic foods
        if "therapeutic_foods" in diet_plan:
            st.markdown("### 🌟 Therapeutic Foods")
            for food in diet_plan["therapeutic_foods"]:
                if isinstance(food, dict):
                    st.markdown(f"""
                    <div class="diet-card">
                        <h4>🥄 {food.get('food', 'Unknown').title()}</h4>
                        <p><strong>Benefit:</strong> {food.get('benefit', 'Health support')}</p>
                        <p><strong>How to use:</strong> {food.get('preparation', 'As needed')}</p>
                        <p><strong>Frequency:</strong> {food.get('frequency', food.get('dosage', 'Daily'))}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Meal schedule
        if "meal_schedule" in diet_plan:
            st.markdown("### ⏰ Daily Meal Schedule")
            meal_schedule = diet_plan["meal_schedule"]
            
            col1, col2, col3 = st.columns(3)
            meals = [("🌅 Breakfast", "breakfast"), ("☀️ Lunch", "lunch"), ("🌙 Dinner", "dinner")]
            
            for i, (meal_name, meal_key) in enumerate(meals):
                with [col1, col2, col3][i]:
                    if meal_key in meal_schedule:
                        st.markdown(f"""
                        <div class="diet-card">
                            <h4>{meal_name}</h4>
                            <p>{meal_schedule[meal_key]}</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Foods to avoid
        if "foods_to_avoid" in diet_plan and diet_plan["foods_to_avoid"]:
            st.markdown("### 🚫 Foods to Avoid")
            avoid_foods = diet_plan["foods_to_avoid"]
            cols = st.columns(min(len(avoid_foods), 4))
            for i, food in enumerate(avoid_foods):
                with cols[i % len(cols)]:
                    st.markdown(f"❌ **{food}**")
    
    with tab2:
        st.markdown("## 💊 Modern Medical Treatment")
        
        modern_treatment = rec.get("modern_treatment", {})
        
        # Medications
        if "medications" in modern_treatment:
            st.markdown("### 💊 Recommended Medications")
            medications = modern_treatment["medications"]
            
            if medications:
                for med in medications:
                    if isinstance(med, dict):
                        st.markdown(f"""
                        <div class="treatment-card">
                            <h4>💊 {med.get('medicine', 'Medication')}</h4>
                            <p><strong>Dosage:</strong> {med.get('dosage', 'As prescribed')}</p>
                            <p><strong>Duration:</strong> {med.get('duration', 'Consult doctor')}</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("🏥 Please consult with a healthcare provider for appropriate medications.")
        
        # Monitoring
        if "monitoring" in modern_treatment:
            st.markdown("### 📊 Health Monitoring")
            monitoring = modern_treatment["monitoring"]
            for item in monitoring:
                st.markdown(f"📋 {item}")
    
    with tab3:
        st.markdown("## 🌿 Ayurvedic Treatment")
        
        ayurvedic = rec.get("ayurvedic_treatment", {})
        
        # Herbs
        if "herbs" in ayurvedic:
            st.markdown("### 🌱 Herbal Remedies")
            herbs = ayurvedic["herbs"]
            
            for herb in herbs:
                if isinstance(herb, dict):
                    st.markdown(f"""
                    <div class="yoga-card">
                        <h4>🌿 {herb.get('herb', 'Herb').title()}</h4>
                        <p><strong>Purpose:</strong> {herb.get('benefit', 'Health support')}</p>
                        <p><strong>How to use:</strong> {herb.get('preparation', 'As directed')}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Lifestyle recommendations
        if "lifestyle" in ayurvedic:
            st.markdown("### 🏡 Lifestyle Recommendations")
            lifestyle_recs = ayurvedic["lifestyle"]
            for rec_item in lifestyle_recs:
                st.markdown(f"✨ {rec_item}")
    
    with tab4:
        st.markdown("## 🧘 Yoga Therapy")
        
        yoga = rec.get("yoga_therapy", {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Poses
            if "poses" in yoga:
                st.markdown("### 🤸 Recommended Poses")
                poses = yoga["poses"]
                for pose in poses:
                    st.markdown(f"🧘 **{pose}**")
            
            # Breathing
            if "breathing" in yoga:
                st.markdown("### 🫁 Breathing Techniques")
                breathing = yoga["breathing"]
                for technique in breathing:
                    st.markdown(f"💨 **{technique}**")
        
        with col2:
            # Meditation
            if "meditation" in yoga:
                st.markdown("### 🧠 Meditation")
                meditation = yoga["meditation"]
                st.markdown(f"""
                <div class="yoga-card">
                    <h4>🧘‍♀️ Daily Practice</h4>
                    <p>{meditation}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown("## 🔄 Holistic Integration Plan")
        
        integration = rec.get("integration_plan", {})
        
        if integration:
            st.markdown("### 📅 Daily Routine Integration")
            
            routines = [
                ("🌅 Morning Routine", "morning_routine"),
                ("☀️ Throughout the Day", "throughout_day"), 
                ("🌙 Evening Routine", "evening_routine")
            ]
            
            for routine_name, routine_key in routines:
                if routine_key in integration:
                    st.markdown(f"""
                    <div class="result-card">
                        <h4>{routine_name}</h4>
                        <p>{integration[routine_key]}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Summary visualization
        st.markdown("### 📊 Treatment Approach Summary")
        
        # Create a simple pie chart of treatment modalities
        modalities = []
        values = []
        
        if rec.get("diet_plan", {}).get("therapeutic_foods"):
            modalities.append("Nutrition")
            values.append(len(rec["diet_plan"]["therapeutic_foods"]))
        
        if rec.get("modern_treatment", {}).get("medications"):
            modalities.append("Modern Medicine")
            values.append(len(rec["modern_treatment"]["medications"]))
        
        if rec.get("ayurvedic_treatment", {}).get("herbs"):
            modalities.append("Ayurveda")
            values.append(len(rec["ayurvedic_treatment"]["herbs"]))
        
        if rec.get("yoga_therapy", {}).get("poses"):
            modalities.append("Yoga")
            values.append(len(rec["yoga_therapy"]["poses"]))
        
        if modalities and values:
            fig = px.pie(
                values=values, 
                names=modalities,
                title="Treatment Modalities Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                showlegend=True,
                height=400,
                font=dict(size=14)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Download button for the report
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("📄 Download Treatment Plan", use_container_width=True):
            # Create a downloadable report
            report_data = {
                "patient": patient_name,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "recommendations": rec
            }
            
            st.download_button(
                label="💾 Download as JSON",
                data=json.dumps(report_data, indent=2),
                file_name=f"treatment_plan_{patient_name}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <p>🌿 <strong>Hybrid Treatment Planner</strong> - Integrating Modern Medicine with Traditional Wisdom</p>
    <p><em>⚠️ This tool provides educational information only. Always consult with healthcare professionals for medical advice.</em></p>
</div>
""", unsafe_allow_html=True)