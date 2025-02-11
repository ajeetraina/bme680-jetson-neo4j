import os
import torch
from tensorrt_llm.builder import Builder
from tensorrt_llm.logger import logger

def optimize_model(model_path, output_path, precision='fp16'):
    """Optimize a model for TensorRT-LLM"""
    
    logger.info(f'Optimizing model from {model_path}')
    
    # Builder configuration
    builder = Builder()
    builder.max_batch_size = 1
    builder.max_workspace_size = 8 * 1024 * 1024 * 1024  # 8GB
    
    # Set precision
    if precision == 'fp16':
        builder.fp16_mode = True
    elif precision == 'int8':
        builder.int8_mode = True
        
    # Build optimized engine
    engine = builder.build_engine(model_path, output_path)
    
    logger.info(f'Optimized model saved to {output_path}')
    return engine

def quantize_model(model_path, calibration_data):
    """Quantize model to INT8 using calibration data"""
    
    logger.info('Starting INT8 quantization')
    
    # Load calibration data
    calib_data = torch.load(calibration_data)
    
    # Configure quantization
    config = {
        'calibration_algorithm': 'minmax',
        'calibration_batches': 100,
        'calibration_cache': 'calibration.cache'
    }
    
    # Perform quantization
    quantized_model = optimize_model(model_path, 
                                   output_path='quantized_model',
                                   precision='int8')
    
    return quantized_model

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', required=True)
    parser.add_argument('--output_path', required=True)
    parser.add_argument('--precision', choices=['fp32', 'fp16', 'int8'],
                        default='fp16')
    parser.add_argument('--calibration_data', help='Required for INT8')
    
    args = parser.parse_args()
    
    if args.precision == 'int8' and not args.calibration_data:
        raise ValueError('Calibration data required for INT8 quantization')
    
    if args.precision == 'int8':
        quantize_model(args.model_path, args.calibration_data)
    else:
        optimize_model(args.model_path, args.output_path, args.precision)
