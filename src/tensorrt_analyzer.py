import torch
from tensorrt_llm.runtime import ModelConfig, SamplingConfig
from tensorrt_llm.runtime import GenerationSession, Model
from datetime import datetime, timedelta

class SensorAnalyzer:
    def __init__(self, model_path):
        # Initialize TensorRT-LLM model
        self.config = ModelConfig(
            max_batch_size=1,
            max_input_len=512,
            max_output_len=128
        )
        self.model = Model(model_path, self.config)
        self.session = GenerationSession(self.model)

    def analyze_current_readings(self, readings):
        prompt = f"""
        Analyze these environmental sensor readings:
        Temperature: {readings['temperature']}°C
        Humidity: {readings['humidity']}%
        Pressure: {readings['pressure']}hPa
        Gas Resistance: {readings['gas']}Ω

        Provide:
        1. Current conditions assessment
        2. Health impact analysis
        3. Recommended actions
        """

        return self._generate_analysis(prompt)

    def analyze_trends(self, readings_history):
        # Process historical data
        temp_trend = self._calculate_trend([r['temperature'] for r in readings_history])
        humid_trend = self._calculate_trend([r['humidity'] for r in readings_history])

        prompt = f"""
        Analyze these environmental trends over the past {len(readings_history)} readings:
        Temperature trend: {temp_trend}
        Humidity trend: {humid_trend}

        Provide:
        1. Pattern analysis
        2. Potential issues
        3. Long-term recommendations
        """

        return self._generate_analysis(prompt)

    def _generate_analysis(self, prompt):
        sampling_config = SamplingConfig(
            max_new_tokens=128,
            temperature=0.7
        )

        outputs = self.session.generate(
            [prompt],
            sampling_config
        )

        return outputs[0]

    def _calculate_trend(self, values):
        if len(values) < 2:
            return "Insufficient data"
        
        trend = (values[-1] - values[0]) / len(values)
        if abs(trend) < 0.1:
            return "Stable"
        return "Increasing" if trend > 0 else "Decreasing"
