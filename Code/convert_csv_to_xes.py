# CSV to XES

import pandas
import pm4py
from pathlib import Path

class CsvToXesConverter:
    def __init__(self, file_name):
        self.file_name = file_name
    
    def convert(self):
        log = pandas.read_csv(self.file_name, sep=',')
        log = pm4py.format_dataframe(log, case_id='case', activity_key='activity', timestamp_key='timestamp')
        log.drop(columns=['@@index'], inplace=True)
        log.rename(columns = {
            'time:timestamp': 'timestamp'
            }, inplace = True)
        
        new_file_name = './Logs/' + Path(self.file_name).stem + '.xes'
        pm4py.write_xes(log, new_file_name)