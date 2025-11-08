
import pandas as pd
import numpy as np

def process_data(data):
    # Complex data processing
    for i in range(100):
        data = data * 2
    return data

def analyze_performance():
    data = [i for i in range(1000)]
    processed = process_data(data)
    return sum(processed)

if __name__ == "__main__":
    result = analyze_performance()
    print(f"Analysis complete: {result}")
