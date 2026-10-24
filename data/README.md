# Gas Sensor Array Drift Dataset


## Source and files

- Source: [UCI Gas Sensor Array Drift Dataset, ID 224](https://archive.ics.uci.edu/dataset/224/gas+sensor+array+drift+dataset)
- Citation: Vergara, A. (2012). *Gas Sensor Array Drift Dataset*. UCI Machine Learning Repository. [DOI: 10.24432/C5RP6W](https://doi.org/10.24432/C5RP6W).
- Local files: 
    - `raw/batch1.dat` 
    - `raw/batch2.dat` 
    - `raw/batch3.dat` 
    - `raw/batch4.dat` 
    - `raw/batch5.dat` 
    - `raw/batch6.dat` 
    - `raw/batch7.dat` 
    - `raw/batch8.dat` 
    - `raw/batch9.dat` 
    - `raw/batch10.dat`.
- Total: 13,910 rows across ten batches.

The `.dat` files are plain text in a LIBSVM-style format. They can be opened in a text editor or parsed by a program. A Windows file association such as "Probe Document" does not change their contents or require special software.

Here, `raw/` means the original downloaded files. The numbers inside are already extracted signal features, not the original sampled resistance waveforms. Preserve these files when creating processed transactions.

## What does one row represent? 

Every row will follow the same exact format as one another. 

The first row of `raw/batch1.dat` begins as follows (truncated):

```text
1 1:15596.162100 2:1.868245 3:2.371604 4:2.803678 5:7.512213 6:-2.739388 7:-3.344671 8:-4.847512 9:15326.691400 ...
```

- The initial standalone `1` is the gas **class label**. The value represents the same type of gas even in different batches. 
- Each remaining token has the form `feature_index:value`.
- `1:15596.162100` means feature 1 has value 15596.162100.
- `9:15326.691400` means feature 9 has value 15326.691400; it does not refer to sensor 9. 
- Feature indices are one-based. Every row in the local files has indices 1 through 128 in order.
- The batch is identified by the filename. These rows do not include an explicit timestamp or gas-concentration field.

A parser should split on whitespace, read the first token as an integer label, and split each remaining token at `:` into an integer index and a floating-point value. Preserve both the label and the source batch as metadata.

## Mapping features to sensors

Each consecutive block of eight features belongs to **one sensor**, not to a group of 16 sensors.

| Feature indices | Sensor |
| --- | --- |
| 1–8 | 1 |
| 9–16 | 2 |
| 17–24 | 3 |
| 25–32 | 4 |
| 33–40 | 5 |
| 41–48 | 6 |
| 49–56 | 7 |
| 57–64 | 8 |
| 65–72 | 9 |
| 73–80 | 10 |
| 81–88 | 11 |
| 89–96 | 12 |
| 97–104 | 13 |
| 105–112 | 14 |
| 113–120 | 15 |
| 121–128 | 16 |

For feature index `j`, the sensor number is `((j - 1) // 8) + 1`, where `//` means integer division. Its position within that sensor's block is `((j - 1) % 8) + 1`.

The files identify sensors by this ordering. They do not contain a sensor-model lookup, calibration record, or operating-temperature metadata. Do not assign a hardware model to a sensor index without a verified mapping.

## Meaning of the eight features

The sensors respond to gas exposure through changes in electrical resistance. Each block summarizes the magnitude and dynamics of one sensor's response.

| Position in block | Feature | Interpretation | Sensor 1, first row |
| --- | --- | --- | ---: |
| 1 | ΔR | Resistance-response magnitude relative to baseline | 15596.162100 |
| 2 | Normalized response | Resistance response expressed relative to baseline as a ratio | 1.868245 |
| 3 | EMAi, α = 0.001 | Rising-response summary | 2.371604 |
| 4 | EMAi, α = 0.01 | Rising-response summary | 2.803678 |
| 5 | EMAi, α = 0.1 | Rising-response summary | 7.512213 |
| 6 | EMAd, α = 0.001 | Decaying-response summary | -2.739388 |
| 7 | EMAd, α = 0.01 | Decaying-response summary | -3.344671 |
| 8 | EMAd, α = 0.1 | Decaying-response summary | -4.847512 |

`EMA` refers to an exponential moving average; `i` and `d` identify increasing and decreasing portions of the response. The stored dynamic features summarize extrema of the filtered response, rather than storing the complete filtered time series. Smaller α gives stronger smoothing; larger α responds more quickly to recent changes.

Negative decay-feature values describe a falling response; they do not represent negative electrical resistance. The eight entries are different feature types, not eight successive time samples. The full original waveform cannot be recovered from these summaries.

The UCI text denotes the normalized feature with `|ΔR|`; in this documentation that notation names the normalized feature, rather than instructing the reader to take the absolute value of feature 1. Do not treat all feature values as sharing one unit, or interpret them as gas concentrations. Consult the source methodology before reproducing the feature extraction or making unit-specific physical claims.

If the source page displays `Î”` or `Î±`, these are text-encoding artifacts for the Greek symbols Δ (delta) and α (alpha).

## Batches and collection periods

The batches group measurements from different collection periods. They are not individual sensors or gas classes. Month IDs below are relative collection-month identifiers from the source documentation.

| File | Month IDs | Local row count |
| --- | --- | ---: |
| `batch1.dat` | 1, 2 | 445 |
| `batch2.dat` | 3, 4, 8, 9, 10 | 1,244 |
| `batch3.dat` | 11, 12, 13 | 1,586 |
| `batch4.dat` | 14, 15 | 161 |
| `batch5.dat` | 16 | 197 |
| `batch6.dat` | 17, 18, 19, 20 | 2,300 |
| `batch7.dat` | 21 | 3,613 |
| `batch8.dat` | 22, 23 | 294 |
| `batch9.dat` | 24, 30 | 470 |
| `batch10.dat` | 36 | 3,600 |
| **Total** | | **13,910** |

The batches support studying sensor drift: changes in response characteristics over time. Pattern differences across batches alone do not prove drift, because gas composition and exposure conditions can also differ. Compare like conditions where the available metadata permits.

## Gas labels: unresolved documentation inconsistency

The UCI prose gives this mapping: 1 = ethanol, 2 = ethylene, 3 = ammonia, 4 = acetaldehyde, 5 = acetone, 6 = toluene. However, the local class counts suggest a conflict with published gas-count tables.

For example, local batch 1 has the following counts:

| Numeric label | Local count |
| --- | ---: |
| 1 | 90 |
| 2 | 98 |
| 3 | 83 |
| 4 | 30 |
| 5 | 70 |
| 6 | 74 |

A [published study's dataset table](https://pmc.ncbi.nlm.nih.gov/articles/PMC6210950/) associates these counts, in order, with acetone, acetaldehyde, ethanol, ethylene, ammonia, and toluene. This suggests a different label ordering, but matching counts is not definitive verification of the mapping.

**Until the mapping is independently confirmed, retain numeric labels such as `gas_class=1` in code and results.** Do not silently replace them with gas names. Frequent-itemset mining and support-count validation can proceed using numeric labels.

## Using the data with FP-growth

FP-growth mines sets of discrete items. These continuous feature values therefore need a documented conversion into transactions.

A suggested starting experiment is to select the normalized-response feature from each sensor: indices `2, 10, 18, ..., 122`. Bin each selected feature into categories such as low, medium, and high. Each measurement then becomes a transaction containing 16 sensor-specific items. This is a proposed preprocessing choice, not a description of an implemented pipeline.

For example, a hypothetical processed transaction could contain:

```text
sensor_1_normalized_response=high
sensor_2_normalized_response=high
sensor_3_normalized_response=low
...
```

These example categories have not been assigned to the first row. They require actual threshold selection.

Record the selected features, binning method, thresholds, item-ID dictionary, and batch metadata with processed outputs. Choose thresholds separately for each numerical feature. For comparisons across batches, apply the same thresholds across those batches; independently re-binning every batch can conceal distribution changes. If evaluating on held-out data, fit thresholds using the training/reference data only.

Keep class and batch as metadata by default. Explicitly document any experiment that includes them as transaction items. Support counts the number of transactions containing an itemset, with each item counted at most once per transaction.

The source page's `C`, `Gamma`, folds, and classification-accuracy settings describe an SVM experiment. They are not FP-growth parameters. For this project, document minimum support and preprocessing choices, validate itemsets and counts on small examples, and measure execution time and memory on the larger dataset.
