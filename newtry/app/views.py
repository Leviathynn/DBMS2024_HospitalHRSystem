from flask import Blueprint, render_template, request
import xgboost as xgb
import numpy as np
import os
from .models import historyItem
from . import db

views = Blueprint('views', __name__)

# 加载模型
model = xgb.XGBRegressor()
current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)
temp_dir = str(current_dir)
temp_dir = temp_dir[:-3]
temp_dir = temp_dir + "models\\medical_cost_model.json"
#model_path = os.path.join(current_dir, r'C:\Users\Levy\Documents\CSCI 5560 - Databases pt2\DBMS2024_MedicalSystem-1\newtry\models\medical_cost_model.json')
model_path = os.path.join(current_dir, temp_dir)
model.load_model(model_path)

# 定义辅助函数来处理输入并进行预测
def predict_medical_cost(age, gender, medical_conditions, insurance_provider):
    # 编码性别
    gender_encoded = 1 if gender.lower() == 'male' else 0

    # 编码保险提供商
    insurance_encoded = [
        1 if insurance_provider == "Blue Cross" else 0,
        1 if insurance_provider == "Cigna" else 0,
        1 if insurance_provider == "Medicare" else 0,
        1 if insurance_provider == "UnitedHealthcare" else 0
    ]

    # 编码医疗条件
    conditions_encoded = [
        1 if 'asthma' in medical_conditions else 0,
        1 if 'cancer' in medical_conditions else 0,
        1 if 'diabetes' in medical_conditions else 0,
        1 if 'hypertension' in medical_conditions else 0,
        1 if 'obesity' in medical_conditions else 0
    ]

    # 创建输入数据数组
    input_data = [age, gender_encoded] + conditions_encoded + insurance_encoded
    return model.predict(np.array([input_data]))[0]

@views.route('/')
def info():
    return render_template("info.html")

@views.route("/calculations/", methods=['GET', 'POST'])
def calc():
    predicted_cost = None
    lastFive = None
    if request.method == 'POST':
        age = int(request.form.get('age'))
        gender = request.form.get('gender')
        medical_conditions = request.form.getlist('medical_condition')
        insurance_provider = request.form.get('insurance')

        # 调用预测函数
        predicted_cost = predict_medical_cost(age, gender, medical_conditions, insurance_provider)
        
        
        itemToBeLogged = historyItem(age = str(age), gender = str(gender), medicalCondition = str(medical_conditions[0]),
                                     insuranceProvider = str(insurance_provider), estimatedCost = str(predicted_cost))
        db.session.add(itemToBeLogged)
        db.session.commit()
        #historyItem.query.all()
        #print(historyItem.query.all(), sep = '\n')
        lastFive = historyItem.query.order_by(historyItem.number.desc()).limit(5).all()
        
    return render_template("calc.html", predicted_cost=predicted_cost, historyItem = lastFive)

@views.route("/references/")
def ref():
    return render_template("ref.html")

