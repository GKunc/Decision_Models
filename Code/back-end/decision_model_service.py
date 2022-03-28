from decision_dependencies import DecisionDependencies
from control_flow_decision_miner import ControlFlowDecisionMiner
from process_model_miner import ProcessModelMiner
from data_decision import DataDecisionMiner


class DecisionModelService:
    def get_decision_rules(self, log):
        return ["To be implemented"]

    def get_attributes(self, log):
        process_model_miner = ProcessModelMiner()
        ddMiner = DataDecisionMiner()

        net = process_model_miner.apply(log)
        (_, _, atttibutes) = ddMiner.apply(net, log)
        return atttibutes

    def get_nodes(self, log):
        process_model_miner = ProcessModelMiner()
        ddMiner = DataDecisionMiner()
        cfdMiner = ControlFlowDecisionMiner()

        net = process_model_miner.apply(log)
        cfd = cfdMiner.apply(log, net)

        (rule_base_data_decisions, functional_data_decisions,
         _) = ddMiner.apply(net, log)

        decisions = rule_base_data_decisions + functional_data_decisions
        nodes = []

        row = []
        for (decision, _) in decisions:
            row.append(decision)
        nodes.append(list(set(row)))

        row = []
        for (relation, _) in cfd:
            row.append(relation)
        nodes.append(list(set(row)))

        return nodes

    def get_process_model(self, log):
        process_model_miner = ProcessModelMiner()
        net = process_model_miner.apply(log)

        data = []
        for arc in net.arcs:
            element = []
            if hasattr(arc.source, 'label'):
                element.append(arc.source.label)
            else:
                element.append(arc.source.name)

            if hasattr(arc.target, 'label'):
                element.append(arc.target.label)
            else:
                element.append(arc.target.name)

            data.append(element)

        data = [list(x) for x in set(tuple(x) for x in data)]
        return data

    def get_decision_model(self, log):
        process_model_miner = ProcessModelMiner()
        cfdMiner = ControlFlowDecisionMiner()
        ddMiner = DataDecisionMiner()
        dDependencies = DecisionDependencies()

        net = process_model_miner.apply(log)
        cfd = cfdMiner.apply(log, net)
        (rule_base_data_decisions, functional_data_decisions,
         data_nodes) = ddMiner.apply(net, log)
        all_decisions = rule_base_data_decisions + functional_data_decisions + cfd
        dependencies = dDependencies.apply(log, net, all_decisions, data_nodes)

        self.print_result(data_nodes, rule_base_data_decisions,
                          functional_data_decisions, all_decisions, dependencies, cfd)

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
