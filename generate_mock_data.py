import joblib, json, os, numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from pathlib import Path

BASE = Path("models")
BASE.mkdir(exist_ok=True)

# 1. Generate Mock JSON Data
roles = ["AI Engineer", "Data Scientist", "Python Developer", "Data Analyst"]
skills = ["Python", "Machine Learning", "SQL", "AWS", "Docker", "Data Analysis", "Tableau"]

with open(BASE / "all_roles.json", "w") as f: json.dump(roles, f)
with open(BASE / "all_skills_list.json", "w") as f: json.dump(skills, f)

role_info_map = {
    r: {"domain": "AI & ML", "demand_score": 95, "future_demand": "High", "ai_replacement_risk": "Very Low", "growth_pct": 30, "market_trend": "Surging", "avg_salary_usd": 120000, "is_emerging": True, "is_at_risk": False}
    for r in roles
}
with open(BASE / "role_info_map.json", "w") as f: json.dump(role_info_map, f)

role_skills_map = {
    r: {"core": ["Python", "SQL", "Data Analysis"], "secondary": ["AWS", "Docker", "Machine Learning"]}
    for r in roles
}
with open(BASE / "role_skills_map.json", "w") as f: json.dump(role_skills_map, f)

with open(BASE / "trending_roles.json", "w") as f: 
    json.dump([{"role": r, "domain": "AI & ML", "demand_score": 95, "growth_pct": 30} for r in roles], f)

with open(BASE / "top_skills.json", "w") as f:
    json.dump([{"skill": s, "count": 20000} for s in skills], f)

# 2. Generate Mock ML Models & Encoders
le_role = LabelEncoder().fit(roles)
joblib.dump(le_role, BASE / "le_role.pkl")

le_edu = LabelEncoder().fit(["Bachelor's", "Master's", "PhD"])
joblib.dump(le_edu, BASE / "le_edu.pkl")
joblib.dump(LabelEncoder().fit(["AI", "Web"]), BASE / "le_domain.pkl")

mlb_user = MultiLabelBinarizer().fit([skills])
joblib.dump(mlb_user, BASE / "mlb_skills.pkl")
joblib.dump(mlb_user, BASE / "mlb_role_skills.pkl")

feat_cols = ['years_of_experience', 'num_user_skills', 'skill_gap_count', 'readiness_score', 'edu_enc', 'role_demand_score', 'role_growth_pct'] + skills
joblib.dump(feat_cols, BASE / "rec_feature_columns.pkl")
joblib.dump(skills, BASE / "top_skill_labels.pkl")

# Train tiny dummy models to prevent crashes
X_dummy_demand = pd.DataFrame(np.random.rand(5, 6), columns=['role_growth_pct', 'ai_risk_encoded', 'market_trend_encoded', 'future_demand_encoded', 'is_emerging_role', 'is_at_risk_role'])
model_demand = RandomForestRegressor(n_estimators=2).fit(X_dummy_demand, np.array([80, 85, 90, 95, 99]))
joblib.dump(model_demand, BASE / "demand_prediction_model.pkl")

X_dummy_rec = pd.DataFrame(np.random.rand(4, len(feat_cols)), columns=feat_cols)
model_rec = RandomForestClassifier(n_estimators=2).fit(X_dummy_rec, roles)
joblib.dump(model_rec, BASE / "recommendation_model.pkl")
joblib.dump(model_rec, BASE / "skill_gap_model.pkl")

print("✅ Mock data and models generated successfully in the 'models' folder!")