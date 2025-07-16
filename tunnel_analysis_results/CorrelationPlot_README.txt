CorrelationPlot Usage Instructions
==================================================

Files for CorrelationPlot:
1. correlationplot_matrix.txt - Main correlation matrix (tab-delimited)
2. correlationplot_labels.txt - Variable names (one per line)
3. correlationplot_data.csv - CSV format with Var1, Var2, etc.
4. correlationplot_named.csv - CSV with actual feature names
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

Variable Information:
- hasTunnelLength: Numerical, °ÔTarget, Importance=0.2525
- hasTunnelDiameter: Numerical, °ÔTarget, Importance=0.1357
- TunnelType: Categorical, °ÔTarget, Importance=0.0397
- hasGeologicalCondition: Categorical, °ÔTarget, Importance=0.0125
- hasSoilType: Categorical, °ÔTarget, Importance=0.0077
- hasHydroCondition: Categorical, °ÔTarget, Importance=0.0076
