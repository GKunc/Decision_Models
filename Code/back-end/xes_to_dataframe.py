from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.conversion.log import converter as log_converter


class XesToDataFrameConverter:
    def apply(self, file):
        log_xes = xes_importer.apply(file)
        log = log_converter.apply(
            log_xes, variant=log_converter.Variants.TO_DATA_FRAME)
        log = log.rename(columns={"timestamp": "time:timestamp"})
        # log = log.drop(['time:timestamp'])  # this is added

        log = self.__fill_empty_values(log)
        print('XesToDataFrameConverterXesToDataFrameConverterXesToDataFrameConverter')
        print(log)
        return log

    def __fill_empty_values(self, log):
        return log.fillna('')
