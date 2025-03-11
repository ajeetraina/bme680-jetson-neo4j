# BME680 Sensor Analytics with TensorRT LLM

This extension to the original BME680-Jetson-Neo4j project adds an intelligent filtering and anomaly detection layer using TensorRT LLM before sensor data is stored in Neo4j.

## Overview

The original project collects environmental data from a BME680 sensor connected to a Jetson Nano and stores it directly in Neo4j. This extension adds:

1. **Intelligent data filtering** using a TensorRT LLM model
2. **Anomaly detection** to identify outliers in sensor readings
3. **Data enrichment** with additional context and derived metrics
4. **Batch processing** for more efficient Neo4j database operations

## Architecture

```
+-------------+     +----------------+     +--------------------+     +---------+
| BME680      |     | TensorRT LLM   |     | Data Enrichment &  |     | Neo4j   |
| Sensor      | --> | Filtering &    | --> | Batch Processing   | --> | Database|
| (Jetson)    |     | Anomaly Det.   |     |                    |     |         |
+-------------+     +----------------+     +--------------------+     +---------+
```

## Components

### 1. Sensor Filter (sensor_filter.py)

A Python module that:
- Filters outliers in sensor data using TensorRT or statistical methods
- Detects anomalies in temperature, humidity, pressure, and gas readings
- Adds contextual information to enrich the data

### 2. Enhanced Sensor Loader (sensorloader_trt.py)

An improved version of the original sensorloader.py that:
- Integrates with the TensorRT filtering layer
- Supports batch processing for more efficient database operations
- Includes detailed logging for debugging and model training

### 3. Model Builder (build_sensor_model.py)

A tool to build and train the TensorRT LLM model:
- Can use actual sensor logs or generate synthetic training data
- Exports to ONNX and then builds a TensorRT engine
- Optimized for the Jetson Nano's GPU capabilities

## Setup Instructions

### Prerequisites

In addition to the original project prerequisites, you'll need:

- NVIDIA TensorRT (installed via JetPack on the Jetson Nano)
- PyTorch
- ONNX Runtime

### Installation Steps

1. Clone the repository:
   ```
   git clone https://github.com/ajeetraina/bme680-jetson-neo4j.git
   cd bme680-jetson-neo4j
   ```

2. Install additional dependencies:
   ```
   pip install torch onnx onnxruntime-gpu tensorrt
   ```

3. Update the configuration file:
   ```
   nano config.json
   ```
   Replace the Neo4j password and adjust other settings as needed.

4. Build the TensorRT model:
   ```
   python build_sensor_model.py
   ```
   This will create a model in the `models/` directory.

5. Run the enhanced sensor loader:
   ```
   python sensorloader_trt.py
   ```

## Configuration Options

The `config.json` file allows you to customize the behavior:

- **neo4j**: Connection settings for your Neo4j database
- **tensorrt**: Model path and filtering threshold settings
- **sampling**: Data collection interval and batch size
- **logging**: Log file location and verbosity settings
- **features**: Enable/disable specific features like anomaly detection

## How TensorRT LLM Filtering Works

The TensorRT model processes each sensor reading to:

1. Determine if the reading is valid (outputs a validity score)
2. If invalid, provide corrected values based on historical patterns
3. Add confidence scores to each reading

The model is designed to detect:
- Sudden spikes or drops in any sensor value
- Physically impossible or highly unlikely readings
- Sensor drift or calibration issues

## Neo4j Integration

The enhanced data model in Neo4j includes:

- Original sensor properties (temperature, humidity, pressure, gas)
- Data quality indicators (validity scores, filtering status)
- Temporal context (hour of day, day of week, month)
- Derived metrics (heat index, etc.)

## Example Queries

### Find Anomalous Readings

```cypher
MATCH (s:SensorReading)
WHERE s.data_quality = 'filtered'
RETURN s.timestamp, s.temperature, s.humidity, s.pressure, s.gas
ORDER BY s.timestamp DESC
LIMIT 10
```

### Temporal Patterns with Heat Index

```cypher
MATCH (s:SensorReading)
WHERE s.heat_index IS NOT NULL
RETURN s.hour_of_day, AVG(s.heat_index) as avg_heat_index
ORDER BY avg_heat_index DESC
```

## Training the Model with Your Own Data

After running the system for some time, you can retrain the model with your actual sensor data:

```
python build_sensor_model.py
```

This will use the logs in `sensor_logs.json` to create a more accurate model for your specific environment.

## Extending the System

You can extend this system in several ways:

1. Add more derived metrics specific to your use case
2. Implement notifications for severe anomalies
3. Create additional filtering modules for other sensor types
4. Integrate with cloud services for remote monitoring

## Troubleshooting

- **TensorRT initialization fails**: The system will automatically fall back to statistical filtering.
- **Neo4j connection issues**: Data will be logged locally and can be imported later.
- **Sensor reading errors**: These are logged and reported in the console.

## License

This project is released under the MIT License.
