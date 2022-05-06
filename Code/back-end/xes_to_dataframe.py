from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.util import dataframe_utils


class XesToDataFrameConverter:
    def apply(self, file):
        log_xes = xes_importer.apply(file)
        log = log_converter.apply(
            log_xes, variant=log_converter.Variants.TO_DATA_FRAME)
        log = log.rename(columns={"timestamp": "time:timestamp"})
        log = self.__fill_empty_values(log)
        return log
        # return dataframe_utils.convert_timestamp_columns_in_df(log)

    def __fill_empty_values(self, log):
        return log.fillna('')
