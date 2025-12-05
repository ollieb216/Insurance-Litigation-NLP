# Insurance Litigation Natural Language Processing Framework

An extensible text analysis framework for comparative analysis of legal documents, specifically designed for insurance coverage litigation cases from appellate courts.

## Overview

This project implements advanced NLP techniques to analyze linguistic patterns across insurance litigation cases, enabling identification of key legal terminology and comparative analysis between different insurers and case outcomes.

## Core Files

### `textacular.py` **[Main Framework]**
The primary NLP analysis engine containing the `Textacular` class with methods for:
- Text preprocessing and parsing with stopword filtering
- TF-IDF scoring calculations
- Interactive Sankey diagram generation using Plotly
- Histogram subplots for word frequency analysis
- Extensible parser system for different document types

### `sankey.py`
Utility functions for generating Sankey diagram data from word-frequency dictionaries:
- Data preparation for source-target-value relationships
- Word filtering and frequency mapping
- DataFrame construction for visualization

### `textacular_app.py`
Demonstration application analyzing 8 real insurance coverage litigation cases:
- Progressive, Travelers, State Farm, Geico, American Family, Liberty Mutual, Maryland Insurance, Farmers Insurance
- Generates comparative visualizations across all cases
- Shows practical implementation of the framework

### `Extensible_NLP_Oliver_Baccay DS3500.pdf`
Research poster presentation showcasing methodology, findings, and visual analysis results.

*Project for DS3500 (Advanced Programming with Data) - Northeastern University*
