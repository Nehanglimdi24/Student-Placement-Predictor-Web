#Importing all the necessary libraries first
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

#Loading the first dataset

dataset_dict = load_dataset("Krooz/Campus_Recruitment_CSV")

# Convert each split to pandas DataFrame
df_train = dataset_dict["train"].to_pandas()
df_val = dataset_dict["validation"].to_pandas()
df_test = dataset_dict["test"].to_pandas()

# Concatenate all splits into a single DataFrame
df = pd.concat([df_train, df_val, df_test], ignore_index=True)

print(df.columns)
def create(internships):  
    if internships > 0:  
        return "Yes"  
    else:  
        return "No"  
df['work_experience'] = df['Internships'].apply(create)
df=df[['CGPA','SSC_Marks','HSC_Marks','AptitudeTestScore','work_experience','PlacementStatus']]
df.head(6)

#Applying the z-score normalization on CGPA
mean_gpa=df['CGPA'].mean()
sd1=df['CGPA'].std()
df['CGPA']=(df['CGPA']-mean_gpa)/sd1
df.head()

#Applying the Z-score normalization on ssc_marks,hsc_marks and AptitudeTestScore
mean_ssc=df['SSC_Marks'].mean()
sd_ssc=df['SSC_Marks'].std()
df['SSC_Marks']=(df['SSC_Marks']-mean_ssc)/sd_ssc
mean_hsc=df['HSC_Marks'].mean()
sd_hsc=df['HSC_Marks'].std()
df['HSC_Marks']=(df['HSC_Marks']-mean_hsc)/sd_hsc
mean_apt=df['AptitudeTestScore'].mean()
sd_apt=df['AptitudeTestScore'].std()
df['AptitudeTestScore']=(df['AptitudeTestScore']-mean_apt)/sd_apt
#changing the categorial attribute to numeric
def help(data):
    if(data=="Yes"): 
        return 1
    else:
        return 0
    
df['work_experience']=df['work_experience'].apply(help)
df.head()

df['PlacementStatus'].unique()

#Converting the categorical attribute to numerical.
def to_numeric(data):
    if(data=="Placed"):
        return 1
    else:
        return 0
df['PlacementStatus']=df['PlacementStatus'].apply(to_numeric)
#Ploting the heat map of correlation matrix for data reduction
corr_matrix=df.corr()
sns.heatmap(corr_matrix,annot=True)


#Making a train test split of 80:20 ratio
output=df['PlacementStatus']
df.drop(columns=['PlacementStatus'],inplace=True)
X_train, X_test, y_train, y_test = train_test_split(df, output, test_size=0.2)

#importing all the necessary algorithms

models = [
    
    # Naive Bayes model (good for small datasets, assumes independence between features)
    GaussianNB(),
    
    # Decision Tree model (simple and interpretable, prone to overfitting)
    DecisionTreeClassifier(random_state=42),

    # Random Forest (ensemble of decision trees, reduces overfitting and improves accuracy)
    RandomForestClassifier(n_estimators=100, random_state=42),
    
    # Logistic Regression (linear model, great for binary classification problems)
    LogisticRegression(random_state=50, max_iter=1000),
   
    # AdaBoost (boosting algorithm, combines weak learners to create a strong classifier)
    AdaBoostClassifier(random_state=45),

    # XGBoost (powerful gradient boosting algorithm, handles missing data well and has regularization)
    XGBClassifier(random_state=42),

    # LightGBM (another gradient boosting model optimized for speed and performance)
    LGBMClassifier(boosting_type='gbdt', bagging_fraction=0.9, learning_rate=0.05, feature_fraction=0.9, bagging_freq=50, verbosity=-1, verbose=50),
    
    # K-Nearest Neighbors (instance-based learning, predicts class based on closest neighbors)
    KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2),   

    # Gradient Boosting (boosting technique that builds models sequentially to reduce errors)
    GradientBoostingClassifier(random_state=42)]

predictions = {}
scores = {}

for i, model in enumerate(models):
    
    # Train the model on the training dataset
    model.fit(X_train, y_train)
   
    # Calculate the training accuracy
    train_accuracy = accuracy_score(y_train, model.predict(X_train))
   
    # Calculate the testing accuracy
    test_accuracy = accuracy_score(y_test, model.predict(X_test))   

    # Make predictions
    y_pred = model.predict(X_test)
    predictions[type(model).__name__] = y_pred

    # Calculate the accuracy of the predictions
    score = accuracy_score(y_test, y_pred)
    scores[type(model).__name__] = score

    # Print the model name and the accuracies on the training and testing datasets
    print("-----------------")
    print(f"Model {i+1}: {type(model).__name__}")
    print(f"Training Accuracy: {train_accuracy}")
    print(f"Testing Accuracy: {test_accuracy}")
    print(f"Prediction Accuracy: {score}")
    print("-----------------")
    print()

# Print the model scores
print("Model Scores")
for model_name, score in scores.items():
    print()
    print(f"{model_name}: {score}")

import joblib

# Find the model with the best accuracy
best_model_name = max(scores, key=scores.get)
print(f"\nBest model: {best_model_name} with accuracy {scores[best_model_name]:.4f}")

# Get the best model object
best_model = [model for model in models if type(model).__name__ == best_model_name][0]

# Retrain on the full dataset (optional but recommended for deployment)
best_model.fit(df, output)  # output is PlacementStatus

# Save the model
joblib.dump(best_model, 'placement_model.pkl')
print("✅ Model saved as 'placement_model.pkl'")
