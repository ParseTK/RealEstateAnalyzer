# Real Estate Analyzer

A command-line Python program that reads a CSV of property sales with plain file operations and prints summary statistics for the sale prices.

## What it does

A menu lets you choose:

1. Price summary by city
2. Price summary by property type
3. Price summary by zip code
4. Overall summary
5. Exit

The summaries include the median. The program handles a missing file, a file it cannot read and an empty data set with a message instead of a crash.

## Run it

Needs Python 3.10 or newer, with no other packages. Run it from the folder that contains `RealEstateData.csv`.

```
python RealEstateAnalyzer.py
```

## Notes

This was a coursework project (files). The CSV is read directly instead of with a CSV library, to keep full control of the parsing.
