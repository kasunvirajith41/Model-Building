from flask import Flask, render_template, request
import pickle
import numpy as np

# setup application
app = Flask(__name__)

def prediction(lst):
    filename = 'model/predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst])
    return pred_value

def traverse_list(lst, values):
    result_list = []
    for item in lst:
        if item in values:
            result_list.append(1)
        else:
            result_list.append(0)
    return result_list

@app.route('/', methods=['POST', 'GET'])
def index():
    pred_value = 0  # Default value set to zero
    feature_list = []  # Initialize feature_list
    if request.method == 'POST':
        # Extracting form data
        Blood_Glucose = request.form['realtimeglucose']
        Blood_Pressure_Systolic = request.form['Blood_Pressure_Systolic']
        Blood_Pressure_Diastolic = request.form['Blood_Pressure_Diastolic']
        Oxygen_Saturation = request.form['Oxygen_Saturation']
        Pulse_Rate = request.form['Pulse_Rate']
        Exercise_Duration = request.form['Exercise_Duration']
        Altitude_Training = int(request.form['Altitude_Training'])  # Mapping to 0 or 1
        Sleep_Duration = request.form['Sleep_Duration']
        Step_Count = request.form['Step_Count']
        Nutritional_Intake = request.form['Nutritional_Intake']
        Medication_Intake = int(request.form['Medication_Intake'])  # Mapping to 0 or 1
        Stress_Level = int(request.form['Stress_Level'])  # Mapping to 1, 2, or 3
        Temperature = request.form['Temperature']
        Hydration_Status = request.form['Hydration_Status']
        BMI = request.form['BMI']
        Age = request.form['Age']
        Weather_Conditions = request.form.getlist('Weather_Conditions')
        Gender = request.form.getlist('Gender')

        # Printing form data
        print(Blood_Glucose, Blood_Pressure_Systolic, Blood_Pressure_Diastolic, Oxygen_Saturation,
              Pulse_Rate, Exercise_Duration, Altitude_Training, Sleep_Duration, Step_Count,
              Nutritional_Intake, Medication_Intake, Stress_Level, Temperature, Hydration_Status,
              BMI, Age, Weather_Conditions, Gender)

        # Creating feature list
        feature_list = [int(Blood_Glucose), int(Blood_Pressure_Systolic), int(Blood_Pressure_Diastolic),
                        int(Oxygen_Saturation), int(Pulse_Rate), int(Exercise_Duration), Altitude_Training,
                        int(Sleep_Duration), int(Step_Count), int(Nutritional_Intake), Medication_Intake,
                        Stress_Level, int(Temperature), int(Hydration_Status), float(BMI), int(Age)]

        Weather_Conditions_list = ['Cloudy', 'Sunny']
        Gender_list = ['Male', 'Female']

        # Using the modified traverse_list function for Weather_Conditions and Gender
        feature_list += traverse_list(Weather_Conditions_list, Weather_Conditions)
        feature_list += traverse_list(Gender_list, Gender)

        # Printing the final feature list
        print(feature_list)

        pred_value = prediction(feature_list)
        print(pred_value)
        pred_value = np.round(pred_value[0], 2) 

    return render_template('index.html', pred_value=pred_value)

if __name__ == '__main__':
    app.run(debug=True)



