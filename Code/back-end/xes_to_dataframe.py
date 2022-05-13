from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.conversion.log import converter as log_converter
from pandas.api.types import is_datetime64_any_dtype as is_datetime


class XesToDataFrameConverter:
    def apply(self, file):
        log_xes = xes_importer.apply(file)
        log = log_converter.apply(
            log_xes, variant=log_converter.Variants.TO_DATA_FRAME)
        log = log.rename(columns={"timestamp": "time:timestamp"})

        to_delete = []
        for column in log.columns:
            if is_datetime(log[column]):
                to_delete.append(column)

        print("COLUMNS TO DELETE")
        log = log.drop(columns=to_delete)
        # log = log.drop(columns=['case:REG_DATE'])
        # log = log.drop(columns=['time:timestamp'])
        log = self.__fill_empty_values(log)
        print('XesToDataFrameConverterXesToDataFrameConverterXesToDataFrameConverter')
        print(log)
        return log

    def __fill_empty_values(self, log):
        return log.fillna('')
