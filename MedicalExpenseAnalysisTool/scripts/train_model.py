import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import mysql.connector

# 连接 MySQL 数据库
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1011YYsr",
    database="MedicalInsurance"
)

# 从数据库中读取数据
query = "SELECT Age, Gender, Medical_Condition, Insurance_Provider, Billing_Amount FROM HOSPITAL_RECORDS"
df = pd.read_sql(query, conn)

# 将分类特征进行One-hot编码
df = pd.get_dummies(df, columns=['Gender', 'Medical_Condition', 'Insurance_Provider'], drop_first=True)

# 分割数据集
X = df.drop('Billing_Amount', axis=1)
y = df['Billing_Amount']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 训练 XGBoost 模型
model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# 预测并评估
y_pred = model.predict(X_test)
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))

# 保存模型
model.save_model("C:/Users/41728/PycharmProjects/MedicalExpenseAnalysisTool/model/medical_cost_model.json")
