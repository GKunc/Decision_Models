import pandas
from math import nan

class DataframeUtils:
    def get_labels_column(df):
        return df["label"]

    def get_data_columns(df):
        return df.drop(['label'], axis=1)

    def get_column_names_list(self, params):
        columns = []
        for param in params:
            columns.append(param.split('=')[0].strip())
        columns.append('label')
        return columns   

    # make sure that I can just take 2 values next to each other (SORT BY CASE ID)
    # get event log where all data are in one column (easier to parse)
    def create_decision_table(self, log):
        data = []
        labels = []
        index = 0
        while index < log.shape[0]:
            row = []
            if log.iloc[index]['data'] != nan:
                row_data = log.iloc[index]['data'].split(';')
                for single_var in row_data:
                    row.append(single_var.split('=')[1].strip())
                labels = self.get_column_names_list(row_data)
            label = log.iloc[index + 1]['concept:name']
            row.append(label)
            data.append(row)
            index += 2
            decision_table = pandas.DataFrame(data, columns = labels)
            decision_table = decision_table.replace({'True': 1, 'False': 0})

        return self.__get_traning_data(decision_table)     

    def __get_traning_data(self, decision_table):
        y = decision_table["label"]
        X = decision_table.drop(['label'], axis=1)
        return (X, y)