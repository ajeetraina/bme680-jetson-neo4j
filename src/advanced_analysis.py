import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta

class AdvancedAnalyzer:
    def __init__(self):
        self.scaler = StandardScaler()
        self.anomaly_detector = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        
    def detect_anomalies(self, readings_history):
        """Detect anomalies in sensor readings"""
        data = np.array([
            [r['temperature'], r['humidity'], r['pressure'], r['gas']]
            for r in readings_history
        ])
        
        # Scale the data
        scaled_data = self.scaler.fit_transform(data)
        
        # Detect anomalies
        anomalies = self.anomaly_detector.fit_predict(scaled_data)
        
        return [i for i, x in enumerate(anomalies) if x == -1]
    
    def analyze_patterns(self, readings_history):
        """Analyze patterns in sensor readings"""
        # Extract time series
        times = [r['timestamp'] for r in readings_history]
        temps = [r['temperature'] for r in readings_history]
        
        # Find daily patterns
        daily_patterns = self._analyze_daily_patterns(times, temps)
        
        # Find correlations
        correlations = self._analyze_correlations(readings_history)
        
        return {
            'daily_patterns': daily_patterns,
            'correlations': correlations
        }
    
    def _analyze_daily_patterns(self, times, values):
        """Analyze daily patterns in the data"""
        hours = [t.hour for t in times]
        hourly_avg = {}
        
        for hour, value in zip(hours, values):
            if hour not in hourly_avg:
                hourly_avg[hour] = []
            hourly_avg[hour].append(value)
        
        return {
            hour: np.mean(values)
            for hour, values in hourly_avg.items()
        }
    
    def _analyze_correlations(self, readings):
        """Analyze correlations between different measurements"""
        data = np.array([
            [r['temperature'], r['humidity'], r['pressure'], r['gas']]
            for r in readings
        ])
        
        corr_matrix = np.corrcoef(data.T)
        
        metrics = ['temperature', 'humidity', 'pressure', 'gas']
        return {
            f'{metrics[i]}_{metrics[j]}': corr_matrix[i,j]
            for i in range(len(metrics))
            for j in range(i+1, len(metrics))
        }
