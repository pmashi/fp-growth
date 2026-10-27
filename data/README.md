# Steel Industry Energy Consumption data

The raw file is [`raw/Steel_industry_data.csv`](raw/Steel_industry_data.csv).
It contains measurements from DAEWOO Steel Co. Ltd in South Korea, distributed
through the [UCI dataset page](https://archive.ics.uci.edu/dataset/851/steel+industry+energy+consumption).

## CSV layout

The local file has a header followed by **35,040 records and 11 columns**, with
no empty cells. Values are comma-separated, and decimal numbers use a period.
The file includes a UTF-8 byte-order mark; use `encoding="utf-8-sig"` so the
first column is read as `date` without an invisible prefix.

| Column (exact CSV header) | Meaning and representation |
| --- | --- |
| `date` | Timestamp formatted as `DD/MM/YYYY HH:MM`, using a 24-hour clock. |
| `Usage_kWh` | Electrical energy consumption, in kilowatt-hours (kWh). |
| `Lagging_Current_Reactive.Power_kVarh` | Lagging reactive energy, in kilovolt-ampere reactive hours (kVarh). Note the period in this header. |
| `Leading_Current_Reactive_Power_kVarh` | Leading reactive energy, in kVarh. |
| `CO2(tCO2)` | CO2 measurement. The header suggests tonnes of CO2, but UCI lists ppm; the unit is ambiguous in the source documentation. |
| `Lagging_Current_Power_Factor` | Lagging power factor, expressed as a percentage. |
| `Leading_Current_Power_Factor` | Leading power factor, expressed as a percentage. |
| `NSM` | Number of seconds from midnight; local values range from 0 to 85,500. |
| `WeekStatus` | `Weekday` or `Weekend` strings in this CSV. |
| `Day_of_week` | English weekday name, such as `Monday`. |
| `Load_Type` | `Light_Load`, `Medium_Load`, or `Maximum_Load`. |

Variable descriptions and published units are available on the
[UCI dataset page](https://archive.ics.uci.edu/dataset/851/steel+industry+energy+consumption).
Preserve the CO2 values as supplied rather than assuming a unit conversion.
Zeros are valid measurements, not missing-value markers.

The raw row order is not strictly chronological. For 
example, the file has
`01/01/2018 23:45`, then `01/01/2018 00:00`, then `02/01/2018 00:15`.
The preprocessing script preserves these dates and the original row order;
it does not reinterpret midnight as the following day. Account for this
convention before doing time-series analysis.



## Attribution

V E, S., Shin, C., & Cho, Y. (2021). *Steel Industry Energy Consumption*
[Dataset]. UCI Machine Learning Repository.
[DOI: 10.24432/C52G8C](https://doi.org/10.24432/C52G8C).
The dataset is distributed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
