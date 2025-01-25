import json
import os

class AdaptiveRateLimiter:
    def __init__(self, config_path="config/rate_limits.json"):
        """
        Initialize with rate-limiting rules from a JSON config.
        """
        self.config = self._load_config(config_path)
        self.baseline = self.config["baseline_limits"]
        self.adjustment = self.config["adjustment_rules"]

    def _load_config(self, config_path):
        """Load configuration from JSON file."""
        with open(config_path, "r") as f:
            return json.load(f)

    def adjust_limits(self, predicted_traffic, anomaly_ips=[]):
        """
        Adjust rate limits based on predicted traffic and anomalies.
        
        Args:
            predicted_traffic (float): Predicted request count for the next hour.
            anomaly_ips (list): List of anomalous IPs to throttle.
        
        Returns:
            dict: Adjusted rate limits for users and anomalies.
        """
        adjusted_limits = {"STD": {}, "PRM": {}, "anomalies": {}}

        # Adjust for predicted traffic spikes
        if predicted_traffic > self._get_traffic_threshold():
            for user_tier in ["STD", "PRM"]:
                adjusted_limits[user_tier] = {
                    endpoint: int(limit * self.adjustment["high_traffic_multiplier"])
                    for endpoint, limit in self.baseline[user_tier].items()
                }
        else:
            adjusted_limits.update(self.baseline)

        # Apply stricter limits for anomalies
        adjusted_limits["anomalies"] = {
            ip: {
                endpoint: int(limit * self.adjustment["anomaly_multiplier"])
                for endpoint, limit in self.baseline["STD"].items()
            }
            for ip in anomaly_ips
        }

        return adjusted_limits

    def _get_traffic_threshold(self):
        """Define traffic spike threshold (e.g., 90th percentile of historical data)."""
        return 2000  # Adjust based on your dataset