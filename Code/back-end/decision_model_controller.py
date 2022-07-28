import json
import os
import glob
from flask import Flask, make_response, request, send_file
from decision_model_service import DecisionModelService
from convert_csv_to_xes import CsvToXesConverter
from xes_to_dataframe import XesToDataFrameConverter
from dmn_creator import DMNCreator
import pm4py
from pm4py.objects.conversion.process_tree import converter

UPLOAD_FOLDER = '/Users/grzegorzkunc/Desktop/Decision_Models/uploads/'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/get_bpmn', methods=['GET', 'POST'])
def get_bpmn():
    response = make_response(
        send_file(UPLOAD_FOLDER + 'result.bpmn', attachment_filename='result.bpmn'))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")

    # remove_files()

    return response


@app.route('/get_dmn', methods=['GET', 'POST'])
def get_dmn():
    response = make_response(
        send_file(UPLOAD_FOLDER + 'result.dmn', attachment_filename='result.dmn'))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")

    # remove_files()

    return response


@app.route('/decision_model', methods=['GET', 'POST'])
def decision_model():
    print("Sending file ...")

    csvToXesConverter = CsvToXesConverter()
    xesToDataFrameConverter = XesToDataFrameConverter()
    decision_model_service = DecisionModelService()
    dmnCreator = DMNCreator()

    f = request.files['file']
    file_path = UPLOAD_FOLDER + f.filename
    f.save(file_path)
    file_name = f.filename.split('.')[0]
    file_ext = f.filename.split('.')[1]
    if file_ext != 'csv' and file_ext != 'xes':
        raise Exception("Not supported file extension")

    if file_ext == 'csv':
        csvToXesConverter.apply(UPLOAD_FOLDER, file_path)

    if file_ext == 'json':
        print('Reading model from json file ...')

    log = xesToDataFrameConverter.apply(UPLOAD_FOLDER + file_name + '.xes')
    processModel = decision_model_service.get_process_model(log)
    tree = pm4py.discover_process_tree_inductive(log)
    bpmn_graph = converter.apply(tree, variant=converter.Variants.TO_BPMN)
    pm4py.write_bpmn(bpmn_graph,
                     UPLOAD_FOLDER + "result.bpmn", enable_layout=True)

    cfd, rule_base_data_decisions, functional_data_decisions, attributes, decision_model, decisionRules = decision_model_service.get_decision_model(
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

    dmnCreator.apply(decisions, cfd, attributes, decision_model)

    data = json.dumps({
        "attributes": attributes,
        "decisionRules": decisionRules,
        "decisionNodes": decisionNodes,
        "processModel": processModel,
        "decisionModel": decision_model
    })
    content_type = "application/json"
    # remove_files()

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
