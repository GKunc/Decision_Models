from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.util import dataframe_utils

class XesToDataFrameConverter:
    def __init__(self, file_name):
        self.file_name = file_name

    def convert_xes_to_dataframe(self):
        log_xes = xes_importer.apply(self.file_name)
        event_log = log_converter.apply(log_xes, variant=log_converter.Variants.TO_DATA_FRAME)
        event_log = event_log.rename(columns={"timestamp": "time:timestamp"})
        return dataframe_utils.convert_timestamp_columns_in_df(event_log)