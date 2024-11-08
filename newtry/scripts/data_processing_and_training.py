import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sqlalchemy import create_engine
import os

# 使用 SQLAlchemy 连接 MySQL 数据库
engine = create_engine("mysql+mysqlconnector://root:1011YYsr@localhost/MedicalInsurance")

# 从数据库中读取数据
try:
    query = "SELECT Age, Gender, Medical_Condition, Insurance_Provider, Billing_Amount FROM HOSPITAL_RECORDS"
    df = pd.read_sql_query(query, engine)
except Exception as ex:
    print("An error occurred while reading from the database:", ex)
    exit()

# 检查数据是否读取成功
if df.empty:
    print("Dataframe is empty. Please check your database query.")
    exit()

# 将分类特征进行 One-hot 编码
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
output_dir = "C:/Users/41728/PycharmProjects/newtry/models/"
os.makedirs(output_dir, exist_ok=True)
model_path = os.path.join(output_dir, "medical_cost_model.json")

# 如果模型文件已存在，删除旧文件
if os.path.exists(model_path):
    os.remove(model_path)

model.save_model(model_path)
print(f"Model saved to {model_path}")
