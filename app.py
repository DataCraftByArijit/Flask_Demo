from flask import Flask, request
import pickle 

app = Flask(__name__) 

@app.route("/", methods=['GET'])
def hello_world():
    return "<p>Hello, World! from Suraaj</p>"

@app.route("/ping", methods=['GET'])
def hello_ping():
    return {"message": "Hi I am pinging!" }

model_pickle = open("./classifier.pkl", "rb")
clf = pickle.load(model_pickle)

@app.route("/predict", methods=['POST'])
def prediction():
    # Input format: [["Gender", "Married", ApplicantIncome, LoanAmount, Credit_History]]
    data = request.get_json()

    # 1 & 2. Map Categorical Variables 
    gender = 0 if data["Gender"] == 'Male' else 1 
    married = 0 if data["Married"] == 'No' else 1

    # 3. Model Acceptable Format [[ ]]
    encoded_output = [[gender, married, data['ApplicantIncome'], float(data['LoanAmount']), float(data['Credit_History'])]] 

    # 4. Predict (0 = Rejected, 1 = Approved) 
    pred = int(clf.predict(encoded_output)[0]) 
    status = "Approved" if pred == 1 else "Rejected" 



    # 5. Return JSON message 
    return {"prediction": pred, "status": status}

#flask --app Loan_app run