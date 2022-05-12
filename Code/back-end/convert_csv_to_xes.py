import pandas
import pm4py
from pathlib import Path


class CsvToXesConverter:
    def apply(self, folder_name, file_name):
        log = pandas.read_csv(file_name, sep=',')
        log = pm4py.format_dataframe(
            log, case_id='case', activity_key='activity', timestamp_key='timestamp')
        log = log.drop(columns=['@@index', 'case',
                                'activity', 'timestamp'])
        log = log.rename(columns={
            'time:timestamp': 'timestamp'
        })

        print(log.info())
        new_file_name = folder_name + Path(file_name).stem + '.xes'
        pm4py.write_xes(log, new_file_name)
