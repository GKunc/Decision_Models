from decision_dependencies import DecisionDependencies
from control_flow_decision import ControlFlowDecisionMiner
from data_decision import DataDecisionMiner
from xes_to_dataframe import XesToDataFrameConverter


def main():
    xestToDataFrameConverter = XesToDataFrameConverter('Decision_Model_Log - data column.xes')
    event_log = xestToDataFrameConverter.convert_xes_to_dataframe()
    cfdMiner = ControlFlowDecisionMiner(event_log)
    ddMiner = DataDecisionMiner(cfdMiner.net, event_log, cfdMiner.attributes)

    # merge all decisions
    all_decisions = ddMiner.rule_base_data_decisions + ddMiner.functional_data_decisions + cfdMiner.relations
    print('all_decisions')
    print(all_decisions)

    dDependencies = DecisionDependencies(event_log, cfdMiner.net, all_decisions)

    dependencies = dDependencies.find_dependencies()
    print('dependencies.find')
    print(dependencies)

if __name__ == "__main__":
    main()