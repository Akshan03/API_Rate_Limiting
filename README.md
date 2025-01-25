```markdown
# AI-Powered Adaptive API Rate Limiting System

An intelligent API rate-limiting system that uses LSTM for traffic prediction and Isolation Forest for anomaly detection to dynamically adjust rate limits.

## Features
- **Adaptive Rate Limiting**: Adjusts limits based on predicted traffic spikes.
- **Anomaly Detection**: Identifies and throttles malicious IPs.
- **Priority Endpoints**: Differentiates between high/low-priority endpoints (e.g., `/payment-gateway` vs. `/browse`).
- **User Tiering**: Applies stricter limits to free-tier (`STD`) users during high traffic.

## Installation

### Prerequisites
- Python 3.8+
- [Poetry](https://python-poetry.org/) (recommended) or `pip`

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/ai-api-rate-limiter.git
   cd ai-api-rate-limiter
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   **`requirements.txt`:**
   ```
   pandas>=1.3.5
   numpy>=1.21.5
   scikit-learn>=1.0.2
   tensorflow>=2.8.0
   keras>=2.8.0
   faker>=13.3.4
   matplotlib>=3.5.1
   seaborn>=0.11.2
   openpyxl>=3.0.10
   jupyter>=1.0.0
   joblib>=1.1.0
   ```

## Folder Structure
```
.
├── data/
│   ├── raw/                   # Raw synthetic data (e.g., synthetic_api_traffic.xlsx)
│   └── processed/             # Preprocessed data (e.g., hourly_pivot.csv)
│
├── models/                    # Saved models and scalers
│   ├── lstm_payment_traffic_predictor.h5
│   ├── payment_anomaly_detector.pkl
│   ├── lstm_scaler.pkl
│   └── anomaly_scaler.pkl
│
├── src/                       # Source code
│   ├── adaptive_limiter.py    # Dynamic rate-limiting logic
│   └── config/
│       └── rate_limits.json   # Baseline limits & adjustment rules
│
├── notebooks/                 # Jupyter notebooks
│   └── api_rate_limiting.ipynb  # Model training/evaluation
│
├── tests/                     # Unit tests
│   └── test_adaptive_limiter.py
│
└── main.py                    # Production entry point
```

## Usage

### 1. Generate Synthetic Data
Run the notebook to generate synthetic API traffic data:
```bash
jupyter notebook notebooks/api_rate_limiting.ipynb
```
Execute all cells in the notebook. Data will be saved to `data/raw/synthetic_api_traffic.xlsx`.

### 2. Train Models
Follow the notebook steps to:
- Preprocess data
- Train the LSTM traffic predictor
- Train the Isolation Forest anomaly detector

### 3. Adjust Rate Limits Dynamically
```python
from src.adaptive_limiter import AdaptiveRateLimiter

# Initialize with config
limiter = AdaptiveRateLimiter(config_path="src/config/rate_limits.json")

# Example: Predict traffic spike (2500 requests/hour) and detect anomalies
adjusted_limits = limiter.adjust_limits(
    predicted_traffic=2500,
    anomaly_ips=["192.168.1.1", "10.0.0.5"]
)

print("Adjusted Limits:", adjusted_limits)
```

### 4. Deploy to API Gateway
Integrate with your API gateway (e.g., Spring Cloud Gateway, Nginx):
```java
// Spring Boot Example
@Bean
public RedisRateLimiter redisRateLimiter() {
    return new RedisRateLimiter(
        adjustedLimits.get("STD").get("/payment-gateway"),
        adjustedLimits.get("PRM").get("/payment-gateway")
    );
}
```

## Configuration
Modify `src/config/rate_limits.json` to set baseline limits and adjustment rules:
```json
{
  "baseline_limits": {
    "STD": {
      "/payment-gateway": 100,
      "/browse": 500
    },
    "PRM": {
      "/payment-gateway": 1000,
      "/browse": 2000
    }
  },
  "adjustment_rules": {
    "high_traffic_multiplier": 0.5,
    "anomaly_multiplier": 0.1
  }
}
```

## Contributing
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/new-algorithm`.
3. Commit changes: `git commit -am 'Add new anomaly detection algorithm'`.
4. Push to the branch: `git push origin feature/new-algorithm`.
5. Submit a pull request.

## License
MIT License. See [LICENSE](LICENSE).
