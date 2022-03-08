from pm4py.algo.discovery.inductive import algorithm as inductive_miner

class DecisionModelMiner:
    def apply(self, log):
        net, _, _ = inductive_miner.apply(log)
        return net