import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score
import matplotlib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / 'output'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_excel(BASE_DIR / 'Vahan_Case_Study.xlsx', sheet_name='Raw Data')

# Feature engineering - avoid leakage (drop FT_after_first_attempt and the % columns
# which are just row-level restatements of the funnel flags / target)

df['upload_date'] = pd.to_datetime(df['upload_date'])
df['upload_dow'] = df['upload_date'].dt.dayofweek

features_num = ['Attempted','Connected','Interested','OB_after_upload','tag_filled',
'Attempt per Lead','upload_to_first_attempt_P50 (hrs)']

df_model = df.copy()
df_model['Attempt per Lead'] = df_model['Attempt per Lead'].fillna(0)
df_model['upload_to_first_attempt_P50 (hrs)'] = df_model['upload_to_first_attempt_P50 (hrs)'].fillna(df_model['upload_to_first_attempt_P50 (hrs)'].median())

# one-hot encode lead_source (top level cohort factor)

X = pd.get_dummies(df_model[features_num + ['lead_source','upload_dow']], columns=['lead_source','upload_dow'], drop_first=True)
y = df_model['FT_after_upload']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

# Random Forest (handles imbalance + non-linearity, gives feature importance)

rf = RandomForestClassifier(n_estimators=300, max_depth=6, class_weight='balanced', random_state=42, min_samples_leaf=5)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
y_proba = rf.predict_proba(X_test)[:,1]

cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix (rows=actual, cols=predicted) [0,1]:")
print(cm)
print(classification_report(y_test, y_pred, digits=3))
print("ROC-AUC:", roc_auc_score(y_test, y_proba))

# Feature importances

imp = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\nTop 15 factors influencing FT:")
print(imp.head(15))

# Save confusion matrix plot

fig, ax = plt.subplots(figsize=(4.5,4))
im = ax.imshow(cm, cmap='Blues')
for i in range(2):
    for j in range(2):
        ax.text(j, i, cm[i,j], ha='center', va='center', fontsize=14,
                color='white' if cm[i,j] > cm.max()/2 else 'black')
ax.set_xticks([0,1]); ax.set_xticklabels(['No FT','FT'])
ax.set_yticks([0,1]); ax.set_yticklabels(['No FT','FT'])
ax.set_xlabel('Predicted'); ax.set_ylabel('Actual')
ax.set_title('Confusion Matrix - Random Forest')
plt.colorbar(im, ax=ax, fraction=0.046)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'confusion_matrix.png', dpi=150)
plt.close()

# Feature importance plot

fig, ax = plt.subplots(figsize=(7,5))
top = imp.head(10).sort_values()
ax.barh(top.index, top.values, color='#2563eb')
ax.set_xlabel('Relative Importance')
ax.set_title('Top 10 Factors Influencing FT Conversion')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'feature_importance.png', dpi=150)
plt.close()

imp.head(15).to_csv(OUTPUT_DIR / 'feature_importance.csv')
np.save(OUTPUT_DIR / 'cm.npy', cm)