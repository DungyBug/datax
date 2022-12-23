import eif as iso
from sklearn.ensemble import IsolationForest
import pandas as pd
from anomaly_detector import AnomalyDetector


class IsolationForestBasedAnomalyDetector(AnomalyDetector):
    def __init__(self, threeshold=0.5, sample_size=128, ntrees=256, ext_level=1, contamination=0.005, n_estimators=200, max_samples=0.7):
        super().__init__()

        self.sample_size = sample_size
        self.ntrees = ntrees
        self.ext_level = ext_level
        self.contamination = contamination
        self.n_estimators = n_estimators
        self.max_samples = max_samples
        self.threeshold = threeshold

    def analyze_metric(self, metric: pd.DataFrame, timestamp_unit='s') -> list[int]:
        df = metric.copy()

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit=timestamp_unit)

        df['Weekday'] = df['timestamp'].dt.strftime('%A')
        df['Hour'] = df['timestamp'].dt.hour
        df['Day'] = df['timestamp'].dt.weekday
        df['Month'] = df['timestamp'].dt.month
        df['Year'] = df['timestamp'].dt.year
        df['Month_day'] = df['timestamp'].dt.day

        df['Lag'] = df['value'].shift(1)
        df['Rolling_Mean'] = df['value'].rolling(7).mean()

        model_data = df[['value', 'Hour', 'Day', 'Month_day',
                         'Month', 'Rolling_Mean', 'Lag']].dropna()

        df = df.dropna()

        isoforest = IsolationForest(random_state=0, contamination=self.contamination,
                                    n_estimators=self.n_estimators, max_samples=self.max_samples)
        isoforest.fit(model_data)

        y = isoforest.predict(model_data)

        df['predict'] = y

        np_model_data = model_data.to_numpy()

        forest = iso.iForest(np_model_data, ntrees=self.ntrees,
                             sample_size=self.sample_size, ExtensionLevel=self.ext_level)

        result = forest.compute_paths(X_in=np_model_data)

        df['anomaly_chance'] = result

        return list(df.loc[df['anomaly_chance'] > self.threeshold].index)
