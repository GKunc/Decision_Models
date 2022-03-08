import json
import os
from flask import Flask, make_response, request
from decision_model_service import DecisionModelService
from convert_csv_to_xes import CsvToXesConverter
from xes_to_dataframe import XesToDataFrameConverter

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/test')
def test():  # put application's code here
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    response.headers.add("Content-type", "text/plain")
    response.set_data("Working test!")
    return response


@app.route('/decision_model', methods = ['GET', 'POST'])
def pm4py():
    csvToXesConverter = CsvToXesConverter()
    xesToDataFrameConverter = XesToDataFrameConverter()
    decision_model_service = DecisionModelService()
    print(request)
    f = request.files['file']
    file_path = f.filename
    f.save(file_path)    
    print(f"FILEPATH:: {file_path}")
    if f.filename.split('.')[1] == 'csv':
        csvToXesConverter.apply(file_path)
    
    log = xesToDataFrameConverter.apply(file_path)
    data = decision_model_service.get_decision_model(log)
    data = json.dumps(data)

    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    response.headers.add("Content-type", "application/json")
    response.set_data(data)
    return response


if __name__ == '__main__':
    app.run()