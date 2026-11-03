import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# 1. Load dataset
df = pd.read_csv('../data/freelance_bids_india.csv')

# 2. Define features and target
# These are the nine columns the model uses to make its prediction.
feature_cols = [
    'client_budget_inr', 'client_avg_spend_inr', 'client_total_reviews',
    'freelancer_experience_yrs', 'freelancer_rating', 'proposal_count',
    'skill_match_score', 'freelancer_bid_inr', 'bid_to_budget_ratio'
]

# Your goal is to train a model that predicts this last column using the other information.
X = df[feature_cols] # X contains the input features like different columns.
y = df['won_status'] # y contains the correct outcomes the model should learn to predict.
# won_status = 1 means a win; won_status = 0 means a loss.

# 3. Train-test split
# 80% training and 20% testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train) # fit_transform first scaler.fit understand the dataset and calculate the average and variation of each column. then transform(x_train) uses that information (input columns) to scale the values. 

# 5. Train Logistic Regression Model
model = LogisticRegression(random_state=42) # Empty model which is waiting to be trained
model.fit(X_train_scaled, y_train) # Train the model using the inputs and actual answers.
# The word 'fit' means learn from the training data.
# The model examines your input data and known outcomes and learns
# patterns that help it distinguish winning bids from losing bids.

# 6. Save the trained model and scaler into the models folder
joblib.dump(model, 'bid_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("Model and Scaler successfully trained and saved inside models/ directory!")