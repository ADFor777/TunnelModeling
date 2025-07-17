CorrelationPlot Usage Instructions
==================================================

IMPORTANT: Feature names have been cleaned (removed 'has' prefix) for better visualization

Files for CorrelationPlot:
1. correlationplot_matrix.txt - Main correlation matrix (tab-delimited)
2. correlationplot_labels.txt - Clean variable names (one per line)
3. correlationplot_data.csv - CSV format with Var1, Var2, etc.
4. correlationplot_named.csv - CSV with clean feature names
5. correlationplot_config.txt - Configuration and variable descriptions

How to use:
- Option 1: Import correlationplot_matrix.txt + correlationplot_labels.txt
- Option 2: Import correlationplot_data.csv or correlationplot_named.csv
- Check correlationplot_config.txt for variable descriptions

Matrix Properties:
- Size: 6x6
- Range: -1.0 to 1.0
- Format: Symmetric correlation matrix
- Precision: 4 decimal places

Variable Information (Clean Names):
- Tunnel Length: Numerical, °ÔTarget, Importance=0.2525
  (Original: hasTunnelLength)
- Tunnel Diameter: Numerical, °ÔTarget, Importance=0.1357
  (Original: hasTunnelDiameter)
- Tunnel Type: Categorical, °ÔTarget, Importance=0.0397
  (Original: TunnelType)
- Geological Condition: Categorical, °ÔTarget, Importance=0.0125
  (Original: hasGeologicalCondition)
- Soil Type: Categorical, °ÔTarget, Importance=0.0077
  (Original: hasSoilType)
- Hydro Condition: Categorical, °ÔTarget, Importance=0.0076
  (Original: hasHydroCondition)
