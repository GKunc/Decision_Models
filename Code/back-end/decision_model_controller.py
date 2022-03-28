import json
import os
from flask import Flask, make_response, request
from decision_model_service import DecisionModelService
from convert_csv_to_xes import CsvToXesConverter
from xes_to_dataframe import XesToDataFrameConverter

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/nodes', methods=['GET', 'POST'])
def get_nodes():
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
    data = decision_model_service.get_nodes(log)
    data = json.dumps(data)
    content_type = "application/json"

    return create_http_request(data, content_type)


@app.route('/decision_rules', methods=['GET', 'POST'])
def get_decision_rules():
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
    data = decision_model_service.get_decision_rules(log)
    data = json.dumps(data)
    content_type = "application/json"

    return create_http_request(data, content_type)


@app.route('/attributes', methods=['GET', 'POST'])
def get_attributes():
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
    data = decision_model_service.get_attributes(log)
    data = json.dumps(data)
    content_type = "application/json"

    return create_http_request(data, content_type)


@app.route('/process_model', methods=['GET', 'POST'])
def process_model():
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
    data = decision_model_service.get_process_model(log)

    data = json.dumps(data)
    content_type = "application/json"

    return create_http_request(data, content_type)


@app.route('/decision_model', methods=['GET', 'POST'])
def decision_model():
    csvToXesConverter = CsvToXesConverter()
    xesToDataFrameConverter = XesToDataFrameConverter()
    decision_model_service = DecisionModelService()

    f = request.files['file']
    file_path = f.filename
    f.save(file_path)
    file_ext = f.filename.split('.')[1]
    if file_ext != 'csv' and file_ext != 'xes':
        raise Exception("Not supported file extension")

    if f.filename.split('.')[1] == 'csv':
        csvToXesConverter.apply(file_path)

    log = xesToDataFrameConverter.apply(file_path)
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
