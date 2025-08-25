import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"  # Fixed typo: URl -> URL

st.title("Health Insurance Premium Prediction")
st.markdown("Enter the details below to predict your health insurance premium category:")

age = st.number_input("Age", min_value=1, max_value=120, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0)
height = st.number_input("Height (m)", min_value=0.5, max_value=3.0, value=1.7)
income_lpa = st.number_input("Annual Income (LPA)", min_value=0.0, max_value=1000.0, value=5.0)
smoker = st.selectbox("Are you a Smoker?", options=[True, False])
city = st.selectbox("City", options = [
    # Tier 1
    "Delhi", "Mumbai", "Bengaluru", "Chennai", "Hyderabad", "Kolkata", "Pune", "Ahmedabad",

    # Tier 2
    "Chandigarh", "Jaipur", "Lucknow", "Indore", "Nagpur", "Kochi", "Coimbatore",
    "Bhubaneswar", "Surat", "Vadodara", "Bhopal", "Ludhiana", "Kanpur", "Patna",
    "Agra", "Amritsar", "Varanasi", "Guwahati", "Raipur", "Ranchi", "Visakhapatnam",

    # Tier 3
    "Mangalore", "Patiala", "Dehradun", "Udaipur", "Jodhpur", "Guntur", "Mysore",
    "Rajkot", "Madurai", "Allahabad", "Aurangabad", "Jalandhar", "Kolhapur", 
    "Trivandrum", "Gwalior", "Jamshedpur", "Bareilly", "Dhanbad", "Siliguri"
]
)
occupation = st.selectbox("Occupation", options=[
    'retired', 'freelancer', 'student', 'government_job',
    'business_owner', 'unemployed', 'private_job'
])

if st.button("Predict Premium Category"):
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=input_data)
        
        if response.status_code == 200:
            result = response.json()
            
            # Debug: Show what we received
            st.write("Debug - API Response:", result)
            
            # Handle different possible response formats
            if isinstance(result, dict):
                # Try different possible key names
                prediction_keys = ['premium_category', 'prediction', 'result', 'category', 'predicted_category']
                prediction_value = None
                
                for key in prediction_keys:
                    if key in result:
                        prediction_value = result[key]
                        break
                
                if prediction_value is not None:
                    st.success(f"Predicted Premium Category: {prediction_value}")
                else:
                    st.warning(f"Prediction successful but unexpected response format.")
                    st.json(result)  # Show the full response
            else:
                # If result is not a dict, it might be a direct value
                st.success(f"Predicted Premium Category: {result}")
        
        elif response.status_code == 422:
            # Validation error
            error_detail = response.json()
            st.error("Validation Error:")
            st.json(error_detail)
        
        else:
            st.error(f"Error in prediction. Status code: {response.status_code}")
            try:
                error_detail = response.json()
                st.json(error_detail)
            except:
                st.text(response.text)
    
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the prediction service. Please ensure the backend is running on http://localhost:8000")
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

# Add some helpful information
st.markdown("---")
st.markdown("### Troubleshooting Tips:")
st.markdown("""
1. Make sure your FastAPI backend is running on `http://localhost:8000`
2. Check that your API endpoint is `/predict`
3. Verify your backend returns JSON with the expected structure
4. Check the debug output above to see the actual API response
""")