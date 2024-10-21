from flask import Flask, render_template, request
import mysql.connector
import xgboost as xgb
import numpy as np
import hashlib

app = Flask(__name__)

# 加载 XGBoost 模型
model = xgb.XGBRegressor()
model.load_model("model/medical_cost_model.json")


# 辅助函数：将字符串转为数值
def hash_string_to_numeric(value):
    if value:
        return int(hashlib.md5(value.encode('utf-8')).hexdigest(), 16) % (10 ** 8)
    return 0


# 预测函数
def predict_cost(age, gender, medical_condition, insurance_provider, blood_type, room_number, admission_type, doctor,
                 hospital, medication, test_results):
    # 对输入数据进行编码
    gender_map = {"Male": 0, "Female": 1, "Other": 2}
    medical_condition_map = {
        "Heart Disease": 0, "Diabetes": 1, "Cancer": 2,
        "Hypertension": 3, "Asthma": 4, "COVID-19": 5,
        "Kidney Disease": 6, "Liver Disease": 7, "Stroke": 8
    }
    insurance_provider_map = {"Provider A": 0, "Provider B": 1, "Provider C": 2, "Provider D": 3}
    blood_type_map = {"A": 0, "B": 1, "AB": 2, "O": 3}

    # 将所有特征整理成一个数组，字符串通过hash转换成数值
    input_data = [
        int(age),  # 确保是整数
        gender_map.get(gender, 0),
        medical_condition_map.get(medical_condition, 0),
        insurance_provider_map.get(insurance_provider, 0),
        blood_type_map.get(blood_type, 0),
        int(room_number) if room_number else 0,  # 如果 room_number 为空，默认值为0
        int(admission_type) if isinstance(admission_type, (int, float)) else hash_string_to_numeric(admission_type),
        # admission_type 应该是数值类型，如果不是，进行哈希转换
        hash_string_to_numeric(doctor),  # 将 doctor 字符串转换为数值
        hash_string_to_numeric(hospital),  # 将 hospital 字符串转换为数值
        hash_string_to_numeric(medication),  # 将 medication 字符串转换为数值
        hash_string_to_numeric(test_results)  # 将 test_results 字符串转换为数值
    ]

    # 确保 input_data 是数值数组
    input_data = np.array([input_data], dtype=np.float32)

    # 将 input_data 转换为模型能够接受的格式
    return model.predict(input_data)


# 存储预测结果到数据库
def store_prediction(data, predicted_cost):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # 替换为你的数据库用户名
        password="1011YYsr",  # 替换为你的数据库密码
        database="MedicalInsurance"
    )
    cursor = conn.cursor()
    sql = """
    INSERT INTO HOSPITAL_RECORDS 
    (Name, Age, Gender, Blood_Type, Medical_Condition, Date_of_Admission, Doctor, Hospital, Insurance_Provider, Billing_Amount, Room_Number, Admission_Type, Discharge_Date, Medication, Test_Results)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data['name'], data['age'], data['gender'], data['blood_type'], data['medical_condition'],
        data['discharge_date'],
        data['doctor'], data['hospital'], data['insurance_provider'], predicted_cost, data['room_number'],
        data['admission_type'], data['discharge_date'], data['medication'], data['test_results']
    )
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()


# 获取历史记录
def get_history():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1011YYsr",
        database="MedicalInsurance"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM HOSPITAL_RECORDS")
    return cursor.fetchall()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    # 获取表单数据
    data = {
        'name': request.form['name'],
        'age': request.form['age'],
        'gender': request.form['gender'],
        'blood_type': request.form['blood_type'],
        'medical_condition': request.form['medical_condition'],
        'doctor': request.form['doctor'],
        'hospital': request.form['hospital'],
        'insurance_provider': request.form['insurance_provider'],
        'room_number': request.form.get('room_number', None),
        'admission_type': request.form['admission_type'],
        'discharge_date': request.form['discharge_date'],
        'medication': request.form.get('medication', None),
        'test_results': request.form.get('test_results', None)
    }

    # 调用修改后的 predict_cost 函数，传递所有特征
    predicted_cost = predict_cost(
        data['age'], data['gender'], data['medical_condition'],
        data['insurance_provider'], data['blood_type'],
        data['room_number'], data['admission_type'],
        data['doctor'], data['hospital'], data['medication'], data['test_results']
    )

    # 存储预测结果
    store_prediction(data, predicted_cost)

    return f"The predicted medical cost is: {predicted_cost}"


@app.route('/history')
def history():
    records = get_history()
    return render_template('history.html', records=records)


if __name__ == "__main__":
    app.run(debug=True)
