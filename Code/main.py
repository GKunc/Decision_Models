from convert_csv_to_xes import CsvToXesConverter
from decision_dependencies import DecisionDependencies
from control_flow_decision import ControlFlowDecisionMiner
from data_decision import DataDecisionMiner
from xes_to_dataframe import XesToDataFrameConverter


def main():
    # file_name = 'Log_Booleans'
    # file_name = 'Log_Numbers'
    file_name = 'Log_From_Example'
    csvToXesConverter = CsvToXesConverter(f'./Logs/{file_name}.csv')
    csvToXesConverter.convert()
    xestToDataFrameConverter = XesToDataFrameConverter(f'./Logs/{file_name}.xes')
    event_log = xestToDataFrameConverter.convert_xes_to_dataframe()
    cfdMiner = ControlFlowDecisionMiner(event_log)
    ddMiner = DataDecisionMiner(cfdMiner.net, event_log, cfdMiner.attributes)
    print("================================")
    print('ddMiner.attributes')
    print(ddMiner.attributes)
    all_decisions = ddMiner.rule_base_data_decisions + ddMiner.functional_data_decisions + cfdMiner.relations
   
    print("================================")
    print('all_decisions')
    print(all_decisions)

    print("================================")
    print('rule_base_data_decisions')
    print(ddMiner.rule_base_data_decisions)
    print('functional_data_decisions')
    print(ddMiner.functional_data_decisions)
    print('control flow places')
    print(cfdMiner.relations)

    dDependencies = DecisionDependencies(event_log, cfdMiner.net, all_decisions)

    dependencies = dDependencies.find_dependencies()
    print("================================")
    print('dependencies.find')
    print(dependencies)
if __name__ == "__main__":
    main()  