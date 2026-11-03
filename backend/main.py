from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import joblib
import os

# Initialize FastAPI app
app = FastAPI(
    title="FreelanceBidder API",
    description="API for predicting freelance bid win probability and providing pricing insights.",
    version="1.0"
)

# Enable CORS so your frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins like frontend,backend,etc to access the backend for local development
    allow_credentials=True, # Include credentials, such as cookies and authentication information, subject to browser and CORS rules.
    allow_methods=["*"], # Allows all HTTP methods ex:GET,POST,PUT,DELETE
    allow_headers=["*"], # Allows all the header requests like content-type,Authorization
)

# Load model and scaler dynamically based on paths
base_dir = os.path.dirname(os.path.abspath(__file__)) # The exact pyfile and its absolute path and in which folder does it is stored that is extracted by the os.path.dirname() function
model_path = os.path.join(base_dir, '../models/bid_model.pkl')
scaler_path = os.path.join(base_dir, '../models/scaler.pkl')

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# Define request body structure using Pydantic
class BidRequest(BaseModel):
    client_budget_inr: float
    client_avg_spend_inr: float
    client_total_reviews: int
    freelancer_experience_yrs: int
    freelancer_rating: float
    proposal_count: int
    skill_match_score: float
    freelancer_bid_inr: float

@app.get("/") # @app.get() tells FastAPI to create a GET endpoint. '/' is the home URL path.
def home():
    return {"message": "Welcome to FreelanceBidder API! Use /docs to test predictions."}

@app.post("/predict")
def predict_win_probability(data: BidRequest): # (data: BidRequest): means the incoming request data is validated against your BidRequest structure.
    
    # Calculate bid-to-budget ratio
    bid_to_budget_ratio = round(data.freelancer_bid_inr / data.client_budget_inr, 2) # This calculates how large the freelancer's bid is compared with the client's budget.
    
    # Prepare feature(input) in array in the exact order used during training
    input_features = np.array([[
        data.client_budget_inr,
        data.client_avg_spend_inr,
        data.client_total_reviews,
        data.freelancer_experience_yrs,
        data.freelancer_rating,
        data.proposal_count,
        data.skill_match_score,
        data.freelancer_bid_inr,
        bid_to_budget_ratio
    ]])
    # Here we have used [[]] because: 
    # - The inner brackets contain the features for one prediction Ex: one budget 10000, one Avg.spend 8000, Reviews 25 etc.
    # - The outer brackets represent a collection of input rows.
    
    # Scale features
    input_scaled = scaler.transform(input_features) # applies the same scaling rules learned during training to the new input.
    
    # Predict win probability (class 1 probability)
    win_prob = float(model.predict_proba(input_scaled)[0][1] * 100)
    # predict_proba(input_scaled) uses that input to calculate probabilities form those calculated probalities we select the wining probability 0 means selects the first prediction, 1 means bid win.
    # Generate insights/explainability
    insights = []
    if bid_to_budget_ratio > 1.2: # 120%
        insights.append("Your bid is significantly higher than the client's budget, reducing your win probability.")
    elif bid_to_budget_ratio < 0.7: # 70%
        insights.append("Your bid is quite low; while competitive, you might be undercutting your value.")
    else:
        insights.append("Your pricing falls right into the optimal sweet spot relative to the client's budget.")

    # Notice that this below if statement is separate if, not an elif. Therefore, a bid can receive both a pricing insight and a competition insight.
    if data.proposal_count > 40:
        insights.append("High market competition detected. A strong skill match and portfolio will be vital.")
        
    return {
        "win_probability_percent": round(win_prob, 2),
        "bid_to_budget_ratio": bid_to_budget_ratio,
        "insights": insights
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port)


# Run the Backend in the terminal with uvicorn "backend.main:app --reload", or you can open the API in your browser at "http://127.0.0.1:8000/docs"