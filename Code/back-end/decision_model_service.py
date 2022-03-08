from decision_dependencies import DecisionDependencies
from control_flow_decision_miner import ControlFlowDecisionMiner
from decision_model_miner import DecisionModelMiner
from data_decision import DataDecisionMiner

class DecisionModelService:
    def get_decision_model(self, log):
        decision_model_miner = DecisionModelMiner()
        cfdMiner = ControlFlowDecisionMiner()
        ddMiner = DataDecisionMiner()
        dDependencies = DecisionDependencies()


        net = decision_model_miner.apply(log)
        relations = cfdMiner.apply(log, net)
        (rule_base_data_decisions, functional_data_decisions, data_nodes) = ddMiner.apply(net, log)
        all_decisions = rule_base_data_decisions + functional_data_decisions + relations
        dependencies = dDependencies.apply(log, net, all_decisions, data_nodes)

        self.print_result(data_nodes, rule_base_data_decisions, functional_data_decisions, all_decisions, dependencies, relations)

        return dependencies

    def print_result(self, data_nodes, rule_base_data_decisions, functional_data_decisions, all_decisions, dependencies, relations):
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