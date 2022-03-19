import json
import os
from flask import Flask, make_response, request
from decision_model_service import DecisionModelService
from convert_csv_to_xes import CsvToXesConverter
from xes_to_dataframe import XesToDataFrameConverter

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/decision_model', methods = ['GET', 'POST'])
def decision_model():
    csvToXesConverter = CsvToXesConverter()
    xesToDataFrameConverter = XesToDataFrameConverter()
    decision_model_service = DecisionModelService()
    print(request)
    f = request.files['file']
    file_path = f.filename
    f.save(file_path)    
    file_ext = f.filename.split('.')[1]
    if file_ext != 'csv' and file_ext != 'xes':
        raise Exception("Not supported file extension")

    if f.filename.split('.')[1] == 'csv':
        csvToXesConverter.apply(file_path)
    
    log = xesToDataFrameConverter.apply(file_path)
    data = decision_model_service.get_decision_model(log)
    data = json.dumps(data)
    content_type = "application/json"

    return create_http_request(data, content_type)

def create_http_request(data, content_type):
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    response.headers.add("Content-type", content_type)
    response.set_data(data)

    return response

if __name__ == '__main__':
    app.run()