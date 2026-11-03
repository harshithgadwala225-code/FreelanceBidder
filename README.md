# 💼 FreelanceBidder: AI Proposal Pricing Intelligence for India

FreelanceBidder is a full-stack, machine learning-powered web application built to help Indian freelancers optimize their proposal pricing and predict their likelihood of winning projects on platforms like Upwork, Freelancer, and Fiverr.

---

## 🚀 Key Features

* **Win Probability Prediction**: Uses a trained Logistic Regression classification model to estimate the exact percentage chance of winning a bid.
* **Market-Tailored Pricing (₹ INR)**: Calibrated specifically to Indian freelance market budgets and client spending trends.
* **Smart AI Insights**: Evaluates bid-to-budget ratios and market competition levels to provide actionable proposal advice.
* **Decoupled Architecture**: Features a high-performance FastAPI backend communicating seamlessly with a modern Tailwind CSS frontend.

---

## 🛠️ Tech Stack

* **Machine Learning**: Python, Scikit-Learn (Logistic Regression), NumPy, Pandas, Joblib
* **Backend API**: FastAPI, Uvicorn, Pydantic, CORS Middleware
* **Frontend UI**: HTML5, Tailwind CSS, JavaScript (Fetch API)

---

## 📁 Project Directory Structure

```text
FreelanceBidder/
│
├── backend/
│   └── main.py                  # FastAPI server & prediction endpoints
│
├── frontend/
│   ├── index.html               # Tailwind CSS responsive dashboard
│   └── script.js                # Event handlers & API communication
│
├── models/
│   ├── bid_model.pkl            # Trained Logistic Regression model
│   └── scaler.pkl               # Feature scaler for standardized inputs
│
├── data/
│   └── freelance_bids_india.csv # Indian market dataset
│
├── README.md                    # Project documentation
└── requirements.txt             # Python dependencies
```

---

## ⚙️ Local Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/FreelanceBidder.git
cd FreelanceBidder
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Backend API Server
```bash
uvicorn backend.main:app --reload
```
* **Base API URL**: `http://127.0.0.1:8000`
* **Interactive Swagger UI**: `http://127.0.0.1:8000/docs`

### 4. Launch the Frontend Application
Open `frontend/index.html` in your web browser or run it using VS Code's **Live Server** extension.

---

## 📊 Model & Features Overview

The model evaluates predictions using 9 core feature inputs:
1. `client_budget_inr`: Client's stated budget in ₹.
2. `client_avg_spend_inr`: Historical average spend of the client.
3. `client_total_reviews`: Total number of reviews on the client's profile.
4. `freelancer_experience_yrs`: Freelancer's experience level in years.
5. `freelancer_rating`: Star rating (4.0 to 5.0 scale).
6. `proposal_count`: Total active bids submitted on the job post.
7. `skill_match_score`: Similarity match score between freelancer skills and requirements (0.5 to 1.0).
8. `freelancer_bid_inr`: Proposed bid amount in ₹.
9. `bid_to_budget_ratio`: Calculated ratio of `freelancer_bid_inr / client_budget_inr`.

---

## 🌐 Deployment Overview

* **Backend**: Hosted on cloud platforms like **Render** or **Railway** using the dynamic `PORT` environment variable.
* **Frontend**: Static hosting via **Vercel** or **Netlify** pointing to the production FastAPI `/predict` URL.

---

## 📄 License

Distributed under the **MIT License**.