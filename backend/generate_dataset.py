"""
Generate Synthetic Student Performance Dataset
Run this if you don't have the Kaggle dataset.
"""
import pandas as pd
import numpy as np
import os

np.random.seed(42)
n = 1000

data = {
    'Hours_Studied': np.random.uniform(1, 40, n),
    'Attendance': np.random.uniform(50, 100, n),
    'Parental_Involvement': np.random.choice(['Low', 'Medium', 'High'], n),
    'Access_to_Resources': np.random.choice(['Low', 'Medium', 'High'], n),
    'Extracurricular_Activities': np.random.choice(['Yes', 'No'], n),
    'Sleep_Hours': np.random.uniform(4, 10, n),
    'Previous_Scores': np.random.uniform(40, 100, n),
    'Motivation_Level': np.random.choice(['Low', 'Medium', 'High'], n),
    'Internet_Access': np.random.choice(['Yes', 'No'], n),
    'Tutoring_Sessions': np.random.randint(0, 10, n),
    'Family_Income': np.random.choice(['Low', 'Medium', 'High'], n),
    'Teacher_Quality': np.random.choice(['Low', 'Medium', 'High'], n),
    'School_Type': np.random.choice(['Public', 'Private'], n),
    'Peer_Influence': np.random.choice(['Positive', 'Neutral', 'Negative'], n),
    'Physical_Activity': np.random.uniform(0, 6, n),
    'Learning_Disabilities': np.random.choice(['Yes', 'No'], n),
    'Parental_Education_Level': np.random.choice(['High School', 'College', 'Postgraduate'], n),
    'Distance_from_Home': np.random.choice(['Near', 'Moderate', 'Far'], n),
    'Gender': np.random.choice(['Male', 'Female'], n),
}

base = (data['Hours_Studied'] * 1.2 + data['Attendance'] * 0.3 +
        data['Previous_Scores'] * 0.4 + data['Sleep_Hours'] * 2.0 +
        data['Tutoring_Sessions'] * 1.5)
data['Exam_Score'] = np.clip(base + np.random.normal(0, 8, n), 20, 100)

os.makedirs('data', exist_ok=True)
pd.DataFrame(data).to_csv('data/StudentPerformanceFactors.csv', index=False)
print(f"Created dataset: {n} rows, {len(data)} columns")
print(f"Target range: {data['Exam_Score'].min():.1f} - {data['Exam_Score'].max():.1f}")
