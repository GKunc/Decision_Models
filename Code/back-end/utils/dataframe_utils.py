import pandas
from math import nan
import pandas as pd
from pandas.api.types import is_numeric_dtype


class DataframeUtils:
    def get_labels_column(df):
        return df["label"]

    def get_data_columns(df):
        return df.drop(['label'], axis=1)

    def convert_to_dataframe(self, data, labels):
        table = pd.DataFrame(data, columns=labels)
        table = table.replace({'True': '1', 'False': '0'})
        return table

    # make sure that I can just take 2 values next to each other (SORT BY CASE ID)
    # get event log where all data are in one column (easier to parse)
    def create_decision_table(self, log):
        data = []
        index = 0
        while index < log.shape[0]:
            row = []
            labels = []
            if log.iloc[index]['data'] != nan:
                row_data = log.iloc[index]['data'].split(';')
                for single_var in row_data:
                    labels.append(single_var.split('=')[0].strip())
                    row.append(single_var.split('=')[1].strip())
            label = log.iloc[index + 1]['concept:name']
            row.append(label)
            data.append(row)
            index += 2

        labels.append('label')
        return self.get_traning_data(self.convert_to_dataframe(data, labels))

    def create_decision_table_for_attribute(self, log, attribute, possible_attributes):
        filtered_log = log.loc[log['activity'].isin(
            possible_attributes)]
        data = []
        labels = self.get_column_names(filtered_log, attribute)
        traces_id = list(set(filtered_log['case']))
        for trace_id in traces_id:
            single_trace_log = filtered_log.loc[filtered_log['case'] == trace_id]
            index = 0
            label = None
            row = []
            while index < single_trace_log.shape[0]:
                if single_trace_log.iloc[index]['data'] != nan and single_trace_log.iloc[index]['data'] != '':
                    row_data = single_trace_log.iloc[index]['data'].split(';')
                    for single_var in row_data:
                        name = single_var.split('=')[0].strip()
                        value = single_var.split('=')[1].strip()
                        if(name != attribute):
                            row.append(value)
                        else:
                            label = value
                index += 1
            row.append(label)
            data.append(row)

        return self.get_traning_data(self.convert_to_dataframe(data, labels))

    def get_column_names(self, log, attribute):
        columns = []
        first_index = log['case'].iloc[0]
        single_trace_log = log.loc[log['case'] == first_index]
        index = 0
        while index < single_trace_log.shape[0]:
            if single_trace_log.iloc[index]['data'] != nan and single_trace_log.iloc[index]['data'] != '':
                row_data = single_trace_log.iloc[index]['data'].split(';')
                for single_var in row_data:
                    name = single_var.split('=')[0].strip()
                    if(name != attribute):
                        columns.append(name)
            index += 1
        columns.append('label')
        return columns

    def get_only_numeric_columns(self, decision_table):
        decision_table = decision_table.apply(pd.to_numeric, errors='ignore')
        columns = decision_table.columns
        numeric_columns = []
        for column in columns:
            if is_numeric_dtype(decision_table[column]):
                numeric_columns.append(column)
        return decision_table[numeric_columns]

    def get_traning_data(self, decision_table):
        y = decision_table["label"]
        X = decision_table.drop(['label'], axis=1)
        return (X, y)
