import torch
import numpy as np
from tqdm import tqdm

def generate_calibration_data(sample_size=1000):
    """Generate calibration data for INT8 quantization"""
    
    # Example environmental patterns
    patterns = [
        {'temp': (15, 30), 'humidity': (30, 70)},
        {'temp': (20, 25), 'humidity': (40, 60)},
        {'temp': (25, 35), 'humidity': (50, 80)}
    ]
    
    calibration_data = []
    
    for _ in tqdm(range(sample_size)):
        pattern = np.random.choice(patterns)
        
        # Generate sample data
        temp = np.random.uniform(pattern['temp'][0], pattern['temp'][1])
        humidity = np.random.uniform(pattern['humidity'][0], 
                                   pattern['humidity'][1])
        
        # Create input tensor
        sample = torch.tensor([temp, humidity], dtype=torch.float32)
        calibration_data.append(sample)
    
    return torch.stack(calibration_data)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--samples', type=int, default=1000)
    
    args = parser.parse_args()
    
    data = generate_calibration_data(args.samples)
    torch.save(data, args.output)
    print(f'Calibration data saved to {args.output}')
