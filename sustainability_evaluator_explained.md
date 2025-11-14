# Sustainability Evaluator: How It Works

This document explains the workflow of the `sustainability_evaluator.py` script and its role in the sustainability analysis process.

## Overview

The `sustainability_evaluator.py` script analyzes project data to generate sustainability reports. It processes input data, applies evaluation logic, and outputs results in various formats (HTML, JSON, etc.).

## Workflow Diagram

```mermaid
graph TD
    A[Start] --> B[Load Input Data]
    B --> C[Preprocess Data]
    C --> D[Run Evaluation Logic]
    D --> E[Generate Report]
    E --> F[Save Output (HTML/JSON)]
    F --> G[End]
```

## Step-by-Step Explanation

1. **Load Input Data**: Reads project data from files (e.g., JSON, CSV).
2. **Preprocess Data**: Cleans and structures the data for analysis.
3. **Run Evaluation Logic**: Applies sustainability metrics and algorithms to assess project performance.
4. **Generate Report**: Formats the results into human-readable reports (HTML, JSON).
5. **Save Output**: Writes the generated reports to disk for review and sharing.

## Example Output Files
- `latest-report.html`: Human-readable sustainability dashboard.
- `latest-report.json`: Machine-readable summary of results.

## Integration
- Can be run standalone or integrated into larger workflows.
- Output files are used for dashboards, summaries, and further analysis.

---
*For more details, see the script: `sustainability_evaluator.py`*
