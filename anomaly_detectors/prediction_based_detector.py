import pandas as pd
from anomaly_detector import AnomalyDetector
import blackbox


class PredictionBasedAnomalyDetector(AnomalyDetector):
    def __init__(self, window_size: int = 1000, percentile: int = 90):
        super(PredictionBasedAnomalyDetector, self).__init__()

        self.window_size = window_size
        self.percentile = percentile

    def analyze_metric(self, metric: pd.DataFrame):
        time_range = range(metric["timestamp"].min(),
                           metric["timestamp"].max())

        # Fill in gaps
        df = metric.set_index("timestamp") \
            .reindex(time_range, fill_value=0) \
            .reset_index()

        anomalies = blackbox.linear_difference(
            list(df["value"].array), self.window_size, self.percentile)[0]

        return anomalies
