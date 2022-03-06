from convert_csv_to_xes import CsvToXesConverter
from decision_dependencies import DecisionDependencies
from control_flow_decision import ControlFlowDecisionMiner
from decision_model_miner import DecisionModelMiner
from data_decision import DataDecisionMiner
from xes_to_dataframe import XesToDataFrameConverter


def main():
    # file_name = 'Log_Booleans'
    # file_name = 'Log_Numbers'
    file_name = 'Log_From_Example'
    csvToXesConverter = CsvToXesConverter()
    xesToDataFrameConverter = XesToDataFrameConverter()
    decision_model_miner = DecisionModelMiner()
    cfdMiner = ControlFlowDecisionMiner()
    ddMiner = DataDecisionMiner()
    dDependencies = DecisionDependencies()

    csvToXesConverter.apply(f'./Logs/{file_name}.csv')
    log = xesToDataFrameConverter.apply(f'./Logs/{file_name}.xes')
    net = decision_model_miner.apply(log)
    (relations, attributes) = cfdMiner.apply(log, net)
    (rule_base_data_decisions, functional_data_decisions, data_nodes) = ddMiner.apply(net, log, attributes)
    all_decisions = rule_base_data_decisions + functional_data_decisions + relations
    dependencies = dDependencies.apply(log, net, all_decisions, data_nodes)

    print_result(data_nodes, rule_base_data_decisions, functional_data_decisions, all_decisions, dependencies, relations)


def print_result(data_nodes, rule_base_data_decisions, functional_data_decisions, all_decisions, dependencies, relations):
    print("================================")
    print('ddMiner.attributes')
    print(data_nodes)
   
    print("================================")
    print('all_decisions')
    print(all_decisions)

    print("================================")
    print('rule_base_data_decisions')
    print(rule_base_data_decisions)
    print('functional_data_decisions')
    print(functional_data_decisions)
    print('control flow places')
    print(relations)

    print("================================")
    print('dependencies.find')
    print(dependencies)
if __name__ == "__main__":
    main()  