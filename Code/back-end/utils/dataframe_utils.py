import pandas
from math import nan
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np


class DataframeUtils:
    def get_labels_column(df):
        return df["label"]

    def get_data_columns(df):
        return df.drop(['label'], axis=1)

    def convert_to_dataframe(self, data, labels):
        table = pd.DataFrame(data, columns=labels)
        table = table.replace({'True': '1', 'False': '0'})
        return table

    def create_decision_table(self, log):
        log = log.reset_index()
        log = log.drop(['time:timestamp',
                       'case:concept:name', 'index'], axis=1)
        log = log.rename(columns={"concept:name": "label"})

        index = 0
        rows_to_remove = []
        while index < log.shape[0]:
            log.at[index, 'label'] = log.at[index+1, 'label']
            rows_to_remove.append(index+1)
            index += 2

        log = log.drop(log.index[rows_to_remove])
        table = log.replace({'True': '1', 'False': '0'})
        table.replace("", float("NaN"), inplace=True)
        table.dropna(how='all', axis=1, inplace=True)

        return self.get_traning_data(table)

    # make sure that I can just take 2 values next to each other (SORT BY CASE ID)
    # get event log where all data are in one column (easier to parse)
    def create_decision_table_old(self, log):
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

    # should only have one row for each trace id
    def create_decision_table_for_attribute(self, log, attribute, possible_attributes):
        data = []
        filtered_log = log.loc[log['concept:name'].isin(
            possible_attributes)]
        labels = self.get_column_names(filtered_log, attribute)
        filtered_log = filtered_log.rename(columns={attribute: "label"})
        filtered_log.replace("", float("NaN"), inplace=True)
        filtered_log.dropna(how='all', axis=1, inplace=True)

        traces_id = list(set(filtered_log['case:concept:name']))
        for trace_id in traces_id:
            single_trace_log = filtered_log.loc[filtered_log['case:concept:name'] == trace_id]
            single_trace_log = single_trace_log.reset_index()

            index = 0
            row = []
            print(single_trace_log)
            while index < single_trace_log.shape[0]:
                for column_name in labels:
                    value = single_trace_log.at[index, column_name]  # nan
                    isNaN = np.isnan(value)
                    if not isNaN:
                        row.append(value)
                index += 1
            data.append(row)

        table = self.convert_to_dataframe(data, labels)
        table = table.drop(
            table.columns.difference(labels), axis=1)
        return self.get_traning_data(table)

    def create_decision_table_for_attribute_old(self, log, attribute, possible_attributes):
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
        log = log.drop(['concept:name', 'time:timestamp',
                        'case:concept:name'], axis=1)
        log.replace("", float("NaN"), inplace=True)
        log.dropna(how='all', axis=1, inplace=True)
        log.rename(columns={attribute: "label"}, inplace=True)
        return list(log.columns)

    def get_column_names_old(self, log, attribute):
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
        print('get_traning_dataget_traning_dataget_traning_dataget_traning_data')
        print(decision_table)
        y = decision_table["label"].to_frame(name='label')
        X = decision_table.drop(['label'], axis=1)
        return (X, y)
