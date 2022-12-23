import pandas as pd


class AnomalyDetector:
    def analyze_metric(self, metric: pd.DataFrame) -> list[int]:
        """
        Analyzes metric containing absolute values for some time unit ( seconds, hours, days, etc. ).
        Usually used for date-value-like metrics and algorithms that operate 1-dimensional graphics.
        Must contain "timestamp" and "value" columns.
        """
        return []

    def analyze_dataset(self, dataset: pd.DataFrame) -> list[int]:
        """
        Analyzes pandas dataset and returs rows with anomalies.
        Dataset must contain "timestamp" and "value" columns.
        """

        # Copy dataset to avoid mutation
        df = dataset.copy()

        df["detections"] = 0

        # Make overall metric
        overall = df.groupby("timestamp")["value"].sum().reset_index()

        anomalies = self.analyze_metric(overall)

        # A series object, containing bool value that represents whether this row is abnormal or not
        detection_series = df["timestamp"].isin(
            overall.iloc[anomalies]["timestamp"])

        df["detections"] += detection_series.astype(int)

        return df.loc[df["detections"] > 0]
