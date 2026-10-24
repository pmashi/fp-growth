"""Run a batch-1 binning demonstration without writing dataset files."""

from pathlib import Path

from preprocess import bin_measurements, read_batch


def main():
    raw_dir = Path(__file__).resolve().parent.parent / "data" / "raw"
    batch_1 = read_batch(1, raw_dir)
    transactions, lows, highs = bin_measurements(batch_1)

    assert len(batch_1) == len(transactions) == 445
    assert len(lows) == len(highs) == 128
    counts = {"low": 0, "medium": 0, "high": 0}

    for measurement, transaction in zip(batch_1, transactions):
        assert len(transaction) == len(set(transaction)) == 128
        for index, item in enumerate(transaction):
            name, category = item.split("=")
            assert name == f"sensor_{index // 8 + 1}_feature_{index % 8 + 1}"
            value = measurement.features[index]
            intervals = {
                "low": value <= lows[index],
                "medium": lows[index] < value <= highs[index],
                "high": value > highs[index],
            }
            assert intervals[category], (measurement.line_number, index + 1)
            counts[category] += 1

    print("\nFirst measurement: first eight binned features")
    for item in transactions[0][:8]:
        print(item)
    print(f"\nCategory counts across all feature values: {counts}")
    print("PASS: 445 transactions, 128 unique items each; all categories match their intervals.")
    print("These cutoffs were fitted only to batch 1, using original feature values.")
    print("For comparisons across batches, fit shared cutoffs once and reuse them.")


if __name__ == "__main__":
    main()
