from pathlib import Path
from dataclasses import dataclass 
import json

import numpy as np 

# Class structure for each row
@dataclass 
class Measurement: 
    batch:          int 
    line_number:    int 
    gas_class:      int 
    features:       list[float]

def read_batch(batch_number: int, 
               raw_dir: Path,
               ) -> list[Measurement]: 
    # get the file of the batch
    file_path = raw_dir / f"batch{batch_number}.dat"

    # create array of measurements 
    measurements = []

    # read the batch file 
    with file_path.open("r", encoding="utf-8") as file: 
        for line_number, line in enumerate(file, start=1): 
            # get tokens 
            tokens = line.split()
            # no tokens found 
            if not tokens: 
                continue 

            if len(tokens) != 129: 
                raise ValueError(
                    f"Line {line_number}: expected 129 tokens"
                )
            gas_class = int(tokens[0])
            features = []

            for expected_index, token in enumerate(tokens[1:], start=1): 
                index_text, value_text = token.split(":")

                if int(index_text) != expected_index: 
                    raise ValueError(
                        f"Line {line_number}: "
                        f"expected feature {expected_index}"
                    )
                features.append(float(value_text))

            measurement = Measurement(
                batch = batch_number,
                line_number = line_number,
                gas_class = gas_class,
                features = features
            )

            measurements.append(measurement)

    return measurements

def bin_measurements(batch_x: list[Measurement]): 
    # Each row is an experiment; each column is a feature.
    values = np.array([m.features for m in batch_x], dtype=float)

    # Calculate two thresholds for each feature.
    low_cutoffs, high_cutoffs = np.percentile(
        values, [33, 67], axis=0
    )

    print(f"{'Feature':>8} {'Sensor':>8} {'Local feature':>14} "
        f"{'33rd percentile':>18} {'67th percentile':>18}")

    for index, (low, high) in enumerate(zip(low_cutoffs, high_cutoffs)):
        feature_number = index + 1
        sensor_number = index // 8 + 1
        local_feature = index % 8 + 1

        print(
            f"{feature_number:>8} "
            f"{sensor_number:>8} "
            f"{local_feature:>14} "
            f"{low:>18.6f} "
            f"{high:>18.6f}"
        )
        
    transactions = []

    for row in values:
        transaction = []

        for index, value in enumerate(row):
            if value <= low_cutoffs[index]:
                category = "low"
            elif value <= high_cutoffs[index]:
                category = "medium"
            else:
                category = "high"

            sensor = index // 8 + 1
            local_feature = index % 8 + 1

            transaction.append(
                f"sensor_{sensor}_feature_{local_feature}={category}"
            )

        transactions.append(transaction)

    return transactions, low_cutoffs, high_cutoffs




root = Path(__file__).resolve().parent.parent
raw_dir = root / "data" / "raw"





if __name__ == "__main__": 
    batch_1 = read_batch(1, raw_dir)

    print("Measurements:", len(batch_1))
    print("First gas class:", batch_1[0].gas_class)
    print("Features per measurement:", len(batch_1[0].features))
    print("Measurements:", batch_1)

def write_batch(batch_number: int, batch: list[Measurement]): 
    output_path = root / "data" / "processed" / f"batch{batch_number}.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)

