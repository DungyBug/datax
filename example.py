import matplotlib.pyplot as plt
import pandas as pd
from anomaly_detectors.isolation_forest_detector import IsolationForestBasedAnomalyDetector

df = pd.read_csv("dataset.tsv", delimiter="\t")

df["timestamp"] = df["hour"]
df = df.groupby("timestamp")["value"].sum().reset_index()

detector = IsolationForestBasedAnomalyDetector(threeshold=0.54)

analyze = detector.analyze_dataset(df)

df.plot(x="timestamp", y="value")

for timestamp in analyze["timestamp"].array:
    plt.axvline(timestamp, color="#f00", linewidth=0.2)

plt.show()
