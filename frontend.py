"""
InsureMate Frontend - Streamlit UI for Insurance Premium Prediction
"""
import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="InsureMate - Premium Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .prediction-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .success {
        color: #00cc00;
    }
    .error {
        color: #ff0000;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = st.sidebar.text_input(
    "API Base URL",
    value="http://127.0.0.1:8000",
    help="Enter the backend API server URL"
)

# Header
st.markdown("<h1 class='header'>🏥 InsureMate - Insurance Premium Predictor</h1>", unsafe_allow_html=True)
st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs(["🔮 Predict Premium", "📊 Results", "❤️ Health Check"])

# ============================================
# TAB 1: PREDICT PREMIUM
# ============================================
with tab1:
    st.subheader("Enter Your Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=35, step=1)
        weight = st.number_input("Weight (kg)", min_value=20.0, max_value=250.0, value=70.0, step=0.5)
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=175.0, step=0.5)
        income_lpa = st.number_input("Annual Income (LPA)", min_value=0.5, max_value=500.0, value=5.0, step=0.5)
    
    with col2:
        smoker = st.selectbox("Are you a Smoker?", options=[False, True], format_func=lambda x: "Yes" if x else "No")
        
        city_options = [
            # Tier 1
            "Delhi", "Mumbai", "Bengaluru", "Chennai", "Hyderabad", "Kolkata", "Pune", "Ahmedabad",
            # Tier 2
            "Chandigarh", "Jaipur", "Lucknow", "Indore", "Nagpur", "Kochi", "Coimbatore",
            "Bhubaneswar", "Surat", "Vadodara", "Bhopal", "Ludhiana", "Kanpur", "Patna",
            "Agra", "Amritsar", "Varanasi", "Guwahati", "Raipur", "Ranchi", "Visakhapatnam",
            # Tier 3
            "Other"
        ]
        city = st.selectbox("City", options=city_options, index=1)
        
        occupation_options = [
            'retired', 'freelancer', 'student', 'government_job',
            'business_owner', 'unemployed', 'private_job'
        ]
        occupation = st.selectbox("Occupation", options=occupation_options)
    
    # Predict Button
    if st.button("🔮 Predict Premium Category", use_container_width=True, type="primary"):
        try:
            with st.spinner("Processing your prediction..."):
                payload = {
                    "age": int(age),
                    "weight": float(weight),
                    "height": float(height),
                    "income_lpa": float(income_lpa),
                    "smoker": bool(smoker),
                    "city": city,
                    "occupation": occupation
                }
                
                response = requests.post(
                    f"{API_BASE_URL}/predict",
                    json=payload,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("✅ Prediction Successful!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Premium Category", result["predicted_category"].upper())
                    with col2:
                        st.metric("BMI", f"{payload['weight'] / ((payload['height']/100)**2):.2f}")
                    with col3:
                        st.metric("Result ID", result["result_id"])
                    
                    # Display additional info
                    st.markdown("<div class='prediction-box'>", unsafe_allow_html=True)
                    st.markdown(f"**Status**: {result['message']}")
                    st.markdown(f"**Predicted at**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error(f"❌ Error: {response.status_code}")
                    st.write(response.text)
                    
        except requests.exceptions.ConnectionError:
            st.error(f"❌ Cannot connect to API at {API_BASE_URL}")
            st.info("Make sure the backend is running: `uvicorn insuremate.main:app --host 127.0.0.1 --port 8000`")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ============================================
# TAB 2: RESULTS
# ============================================
with tab2:
    st.subheader("Prediction Results")
    
    result_filter = st.radio("Filter by:", options=["All Results", "By City", "By Premium Category"])
    
    try:
        if result_filter == "All Results":
            if st.button("📊 Fetch All Results", use_container_width=True):
                response = requests.get(f"{API_BASE_URL}/results", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Total Results: {data['total_results']}")
                    
                    if data['results']:
                        # Convert to table format
                        results_data = []
                        for result in data['results']:
                            results_data.append({
                                "ID": result['id'],
                                "Age": result['age'],
                                "BMI": f"{result['bmi']:.2f}",
                                "City": result['city'],
                                "Occupation": result['occupation'],
                                "Category": result['predicted_category'],
                                "Created At": result['created_at'][:10]
                            })
                        st.dataframe(results_data, use_container_width=True)
                    else:
                        st.info("No results found yet. Make a prediction first!")
        
        elif result_filter == "By City":
            city = st.text_input("Enter City Name")
            if st.button("🔍 Search by City", use_container_width=True):
                response = requests.get(f"{API_BASE_URL}/results/city/{city}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Results in {data['city']}: {data['total_results']}")
                    
                    if data['results']:
                        results_data = []
                        for result in data['results']:
                            results_data.append({
                                "ID": result['id'],
                                "Age": result['age'],
                                "BMI": f"{result['bmi']:.2f}",
                                "Occupation": result['occupation'],
                                "Category": result['predicted_category'],
                                "Created At": result['created_at'][:10]
                            })
                        st.dataframe(results_data, use_container_width=True)
                    else:
                        st.info(f"No results found for city: {city}")
        
        elif result_filter == "By Premium Category":
            category = st.selectbox("Select Premium Category", 
                                   options=["basic", "standard", "premium", "elite"])
            if st.button("🏷️ Search by Category", use_container_width=True):
                response = requests.get(f"{API_BASE_URL}/results/category/{category}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"{data['category'].upper()} category: {data['total_results']} results")
                    
                    if data['results']:
                        results_data = []
                        for result in data['results']:
                            results_data.append({
                                "ID": result['id'],
                                "Age": result['age'],
                                "City": result['city'],
                                "BMI": f"{result['bmi']:.2f}",
                                "Occupation": result['occupation'],
                                "Created At": result['created_at'][:10]
                            })
                        st.dataframe(results_data, use_container_width=True)
                    else:
                        st.info(f"No results found for category: {category}")
                        
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to API at {API_BASE_URL}")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# ============================================
# TAB 3: HEALTH CHECK
# ============================================
with tab3:
    st.subheader("API Health Status")
    
    if st.button("🏥 Check API Health", use_container_width=True, type="secondary"):
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                health = response.json()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("API Status", "🟢 Online" if health.get('status') == 'ok' else "🟡 Degraded")
                with col2:
                    db_status = "✅ Connected" if health.get('database') else "❌ Disconnected"
                    st.metric("Database", db_status)
                
                st.success("Backend is running and healthy!")
            else:
                st.error(f"❌ API returned status {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error(f"❌ Cannot connect to API at {API_BASE_URL}")
            st.warning("Please ensure the backend server is running on the configured URL.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ============================================
# SIDEBAR INFO
# ============================================
with st.sidebar:
    st.markdown("---")
    st.subheader("ℹ️ About")
    st.info(
        """
        **InsureMate** predicts health insurance premium categories based on:
        - Age, Weight, Height (calculates BMI)
        - Annual Income
        - Smoking Status
        - City Tier Classification
        - Occupation Type
        
        **Categories**: Basic, Standard, Premium, Elite
        """
    )
    
    st.markdown("---")
    st.subheader("🚀 Quick Start")
    st.write("""
    1. Fill in your details on the **Predict Premium** tab
    2. Click "Predict Premium Category"
    3. View results on the **Results** tab
    4. Check backend health on **Health Check** tab
    """)
    
    st.markdown("---")
    st.subheader("📱 API Endpoints")
    st.code("""
POST /predict
GET /health
GET /results
GET /results/city/{city}
GET /results/category/{category}
    """, language="markdown")
