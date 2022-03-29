import json
import os
import glob
from flask import Flask, make_response, request
from decision_model_service import DecisionModelService
from convert_csv_to_xes import CsvToXesConverter
from xes_to_dataframe import XesToDataFrameConverter

UPLOAD_FOLDER = './uploads/'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/decision_model', methods=['GET', 'POST'])
def decision_model():
    csvToXesConverter = CsvToXesConverter()
    xesToDataFrameConverter = XesToDataFrameConverter()
    decision_model_service = DecisionModelService()

    f = request.files['file']
    file_path = UPLOAD_FOLDER + f.filename.split('.')[0]
    f.save(file_path)
    file_ext = f.filename.split('.')[1]
    if file_ext != 'csv' and file_ext != 'xes':
        raise Exception("Not supported file extension")

    if file_ext == 'csv':
        csvToXesConverter.apply(file_path + '.csv')

    log = xesToDataFrameConverter.apply(file_path + '.xes')
    processModel = decision_model_service.get_process_model(log)
    cfd, rule_base_data_decisions, functional_data_decisions, attributes, decisionModel, decisionRules = decision_model_service.get_decision_model(
        log)

    decisions = rule_base_data_decisions + functional_data_decisions
    decisionNodes = []

    row = []
    for (decision, _) in decisions:
        row.append(decision)
    decisionNodes.append(list(set(row)))

    row = []
    for (relation, _) in cfd:
        row.append(relation)
    decisionNodes.append(list(set(row)))

    data = json.dumps({
        "attributes": attributes,
        "decisionRules": decisionRules,
        "decisionNodes": decisionNodes,
        "processModel": processModel,
        "decisionModel": decisionModel
    })
    content_type = "application/json"
    remove_files()

    return create_http_request(data, content_type)


def create_http_request(data, content_type):
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    response.headers.add("Content-type", content_type)
    response.set_data(data)

    return response


def remove_files():
    files = glob.glob('./uploads/*')
    for f in files:
        os.remove(f)


if __name__ == '__main__':
    app.run()
