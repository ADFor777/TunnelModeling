import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import os
import warnings
warnings.filterwarnings('ignore')

class TunnelFeatureExtractor:
    def __init__(self, n_estimators=200, random_state=42):
        """
        Tunnel Modeling Parameter Feature Extractor (Customized Version)
        
        Parameters:
        -----------
        n_estimators : int, number of trees in random forest
        random_state : int, random seed
        """
        self.rf_model = RandomForestRegressor(
            n_estimators=n_estimators, 
            random_state=random_state,
            max_depth=15,
            min_samples_split=3,
            min_samples_leaf=1,
            max_features='sqrt'
        )
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = None
        self.feature_importance = None
        self.selected_features = None
        self.correlation_matrix = None
        
        # Define tunnel modeling parameters
        self.tunnel_parameters = [
            'hasTunnelLength',           # Tunnel length
            'hasGeologicalCondition',    # Rock mass classification
            'hasHydroCondition',         # Hydrological conditions
            'hasSoilType',              # Soil type
            'TunnelType',               # Tunnel type
            'hasTunnelDiameter',        # Tunnel diameter
            'hasConstructionMethod',     # Construction method
            'hasBoltLength',            # Bolt length
            'hasBoltRowCount',          # Bolt row count
            'hasBoltColumnCount',       # Bolt column count
            'hasLiningThickness',       # Lining thickness
            'hasSteelArchSpacing',      # Steel arch spacing
            'hasSteelArchCount',        # Steel arch count
            'hasSteelArchThickness',    # Steel arch thickness
            'hasWaterproofLayerThickness' # Waterproof layer thickness
        ]
        
        # Target features to be selected
        self.target_features = [
            'hasTunnelLength',           # Tunnel length
            'hasGeologicalCondition',    # Rock mass classification
            'hasHydroCondition',         # Hydrological conditions
            'hasSoilType',              # Soil type
            'TunnelType',               # Tunnel type
            'hasTunnelDiameter'         # Tunnel diameter
        ]
        
        # Categorical features definition
        self.categorical_features = [
            'hasGeologicalCondition',    # Rock mass classification (I, II, III, IV, V)
            'hasHydroCondition',         # Hydrological conditions (Dry, Wet, Flooded)
            'hasSoilType',              # Soil type (Clay: 1, Sand: 2, StrongSoil: 3)
            'TunnelType',               # Tunnel type (Mountain, Underwater, Shallow, Deep)
            'hasConstructionMethod'      # Construction method
        ]
    
    def _clean_feature_name(self, feature_name):
        """
        Clean feature name by removing 'has' prefix and improving readability
        
        Parameters:
        -----------
        feature_name : str, original feature name
        
        Returns:
        --------
        str, cleaned feature name
        """
        # Remove 'has' prefix
        if feature_name.startswith('has'):
            cleaned_name = feature_name[3:]
        else:
            cleaned_name = feature_name
        
        # Add spaces before capital letters for better readability
        import re
        cleaned_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', cleaned_name)
        
        return cleaned_name
    
    def _get_clean_feature_names(self, feature_names):
        """
        Get cleaned versions of feature names for display
        
        Parameters:
        -----------
        feature_names : list, original feature names
        
        Returns:
        --------
        list, cleaned feature names
        """
        return [self._clean_feature_name(name) for name in feature_names]
        
    def prepare_data(self, data_df, target_column='TunnelArea'):
        """
        Data preprocessing
        
        Parameters:
        -----------
        data_df : DataFrame, containing tunnel modeling parameters data
        target_column : str, target variable column name (e.g., tunnel area, volume, etc.)
        """
        print("=== Tunnel Modeling Parameters Data Preprocessing ===")
        print(f"Original data shape: {data_df.shape}")
        
        # Check if all required features are present
        missing_features = [f for f in self.tunnel_parameters if f not in data_df.columns]
        if missing_features:
            print(f"Warning: Missing the following features: {missing_features}")
        
        # Extract features and target variable
        X = data_df[self.tunnel_parameters].copy()
        y = data_df[target_column].copy() if target_column in data_df.columns else None
        
        # Handle categorical features
        X_processed = self._encode_categorical_features(X)
        
        # Handle missing values
        X_processed = self._handle_missing_values(X_processed)
        
        # Handle outliers
        X_processed = self._handle_outliers(X_processed)
        
        # Standardize numerical features
        numerical_features = [f for f in self.tunnel_parameters if f not in self.categorical_features]
        X_processed[numerical_features] = self.scaler.fit_transform(X_processed[numerical_features])
        
        self.feature_names = X_processed.columns.tolist()
        
        print(f"Processed data shape: {X_processed.shape}")
        print(f"Feature list: {self._get_clean_feature_names(self.feature_names)}")
        
        return X_processed.values, y.values if y is not None else None
    
    def _encode_categorical_features(self, X):
        """
        Encode categorical features
        """
        X_encoded = X.copy()
        
        for feature in self.categorical_features:
            if feature in X_encoded.columns:
                if feature == 'hasSoilType':
                    # Soil type is already numerically encoded
                    X_encoded[feature] = X_encoded[feature].astype(int)
                else:
                    # Other categorical features use LabelEncoder
                    le = LabelEncoder()
                    X_encoded[feature] = le.fit_transform(X_encoded[feature].astype(str))
                    self.label_encoders[feature] = le
                    clean_name = self._clean_feature_name(feature)
                    print(f"{clean_name} encoding mapping: {dict(zip(le.classes_, le.transform(le.classes_)))}")
        
        return X_encoded
    
    def _handle_missing_values(self, X):
        """
        Handle missing values
        """
        missing_count = X.isnull().sum().sum()
        if missing_count > 0:
            print(f"Found {missing_count} missing values, filling with mean/mode")
            
            for column in X.columns:
                if X[column].isnull().any():
                    if column in self.categorical_features:
                        # Fill categorical features with mode
                        X[column] = X[column].fillna(X[column].mode()[0])
                    else:
                        # Fill numerical features with mean
                        X[column] = X[column].fillna(X[column].mean())
        
        return X
    
    def _handle_outliers(self, X):
        """
        Handle outliers (only for numerical features)
        """
        numerical_features = [f for f in X.columns if f not in self.categorical_features]
        
        for feature in numerical_features:
            Q1 = X[feature].quantile(0.25)
            Q3 = X[feature].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = ((X[feature] < lower_bound) | (X[feature] > upper_bound)).sum()
            if outliers > 0:
                clean_name = self._clean_feature_name(feature)
                print(f"{clean_name}: Found {outliers} outliers")
                X[feature] = X[feature].clip(lower=lower_bound, upper=upper_bound)
        
        return X
    
    def extract_features_with_target_priority(self, X, y, top_k=6):
        """
        Extract features with priority on target features
        
        Parameters:
        -----------
        X : array-like, preprocessed feature data
        y : array-like, target values
        top_k : int, number of features to select
        """
        print(f"\n=== Feature Extraction (Priority on Target Features) ===")
        clean_target_names = self._get_clean_feature_names(self.target_features)
        print(f"Target features: {clean_target_names}")
        
        # Train random forest model
        self.rf_model.fit(X, y)
        
        # Get feature importance
        self.feature_importance = self.rf_model.feature_importances_
        
        # Create feature importance DataFrame
        clean_feature_names = self._get_clean_feature_names(self.feature_names)
        feature_importance_df = pd.DataFrame({
            'feature': clean_feature_names,
            'importance': self.feature_importance
        }).sort_values('importance', ascending=False)
        
        print("\nAll feature importance ranking:")
        print(feature_importance_df)
        
        # Prioritize target features
        selected_indices = []
        selected_names = []
        selected_importance = []
        
        # First add target features with highest importance
        target_feature_data = []
        for target_feature in self.target_features:
            if target_feature in self.feature_names:
                idx = self.feature_names.index(target_feature)
                importance = self.feature_importance[idx]
                target_feature_data.append((idx, target_feature, importance))
        
        # Sort target features by importance
        target_feature_data.sort(key=lambda x: x[2], reverse=True)
        
        # Add all target features
        for idx, name, importance in target_feature_data:
            selected_indices.append(idx)
            selected_names.append(name)
            selected_importance.append(importance)
        
        # If target features are insufficient, supplement with other features
        if len(selected_indices) < top_k:
            remaining_needed = top_k - len(selected_indices)
            
            # Get importance of non-target features
            other_features = []
            for i, name in enumerate(self.feature_names):
                if name not in selected_names:
                    other_features.append((i, name, self.feature_importance[i]))
            
            # Sort by importance
            other_features.sort(key=lambda x: x[2], reverse=True)
            
            # Add the most important other features
            for i in range(min(remaining_needed, len(other_features))):
                idx, name, importance = other_features[i]
                selected_indices.append(idx)
                selected_names.append(name)
                selected_importance.append(importance)
        
        # Save selected features
        self.selected_features = {
            'indices': selected_indices[:top_k],
            'names': selected_names[:top_k],
            'importance': selected_importance[:top_k]
        }
        
        print(f"\nSelected {len(self.selected_features['names'])} features:")
        for i, (name, importance) in enumerate(zip(self.selected_features['names'], 
                                                  self.selected_features['importance'])):
            clean_name = self._clean_feature_name(name)
            target_mark = "★" if name in self.target_features else "  "
            print(f"{target_mark} {i+1:2d}. {clean_name:25s} | Importance: {importance:.4f}")
        
        return self.selected_features
    
    def check_correlation(self, X, correlation_threshold=0.8):
        """
        Check feature correlation
        """
        print(f"\n=== Feature Correlation Analysis (threshold: {correlation_threshold}) ===")
        
        # Get data for selected features
        selected_X = X[:, self.selected_features['indices']]
        
        # Calculate correlation matrix
        self.correlation_matrix = np.corrcoef(selected_X.T)
        
        # Create correlation DataFrame with clean names
        clean_selected_names = self._get_clean_feature_names(self.selected_features['names'])
        corr_df = pd.DataFrame(
            self.correlation_matrix,
            index=clean_selected_names,
            columns=clean_selected_names
        )
        
        print("\nFeature correlation matrix:")
        print(corr_df.round(3))
        
        # Find high correlation feature pairs
        high_corr_pairs = []
        n_features = len(self.selected_features['names'])
        
        for i in range(n_features):
            for j in range(i+1, n_features):
                corr_value = abs(self.correlation_matrix[i, j])
                if corr_value > correlation_threshold:
                    clean_name1 = self._clean_feature_name(self.selected_features['names'][i])
                    clean_name2 = self._clean_feature_name(self.selected_features['names'][j])
                    high_corr_pairs.append({
                        'feature1': clean_name1,
                        'feature2': clean_name2,
                        'correlation': corr_value
                    })
        
        if high_corr_pairs:
            print(f"\n⚠️  Found {len(high_corr_pairs)} high correlation feature pairs:")
            for pair in high_corr_pairs:
                print(f"   {pair['feature1']} <-> {pair['feature2']}: {pair['correlation']:.3f}")
        else:
            print("\n✅ No high correlation feature pairs found")
        
        return high_corr_pairs
    
    def validate_model(self, X, y, test_size=0.2):
        """
        Validate model performance
        """
        print(f"\n=== Model Validation ===")
        
        # Use selected features
        selected_X = X[:, self.selected_features['indices']]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            selected_X, y, test_size=test_size, random_state=42
        )
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        
        # Calculate evaluation metrics
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Model performance using {len(self.selected_features['names'])} features:")
        print(f"  Mean Squared Error (MSE): {mse:.4f}")
        print(f"  R² Score: {r2:.4f}")
        
        # Evaluate performance
        if r2 > 0.8:
            print("✅ Excellent model performance")
        elif r2 > 0.6:
            print("⚠️  Good model performance")
        else:
            print("❌ Model performance needs improvement")
        
        return mse, r2
    
    def plot_results(self):
        """
        Visualize results (English version with clean feature names)
        """
        if self.selected_features is None:
            print("Please run feature extraction first")
            return
        
        # Get clean feature names for plotting
        clean_selected_names = self._get_clean_feature_names(self.selected_features['names'])
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Feature Importance Bar Chart
        ax1 = axes[0, 0]
        colors = ['red' if name in self.target_features else 'skyblue' 
                 for name in self.selected_features['names']]
        
        bars = ax1.barh(range(len(clean_selected_names)), 
                       self.selected_features['importance'], 
                       color=colors)
        ax1.set_yticks(range(len(clean_selected_names)))
        ax1.set_yticklabels(clean_selected_names)
        ax1.set_xlabel('Feature Importance')
        ax1.set_title('Tunnel Modeling Parameters Importance Ranking\n(Red: Target Features)')
        ax1.invert_yaxis()
        
        # Add value labels
        for i, (bar, importance) in enumerate(zip(bars, self.selected_features['importance'])):
            ax1.text(importance + 0.01, i, f'{importance:.3f}', 
                    va='center', fontsize=9)
        
        # 2. Correlation Heatmap
        ax2 = axes[0, 1]
        if self.correlation_matrix is not None:
            im = ax2.imshow(self.correlation_matrix, cmap='coolwarm', 
                           aspect='auto', vmin=-1, vmax=1)
            ax2.set_xticks(range(len(clean_selected_names)))
            ax2.set_yticks(range(len(clean_selected_names)))
            ax2.set_xticklabels(clean_selected_names, rotation=45, ha='right')
            ax2.set_yticklabels(clean_selected_names)
            ax2.set_title('Feature Correlation Matrix')
            
            # Add value labels
            for i in range(len(clean_selected_names)):
                for j in range(len(clean_selected_names)):
                    text = ax2.text(j, i, f'{self.correlation_matrix[i, j]:.2f}',
                                  ha="center", va="center", color="black", fontsize=8)
            
            plt.colorbar(im, ax=ax2, shrink=0.8)
        
        # 3. Target Feature Coverage
        ax3 = axes[1, 0]
        target_covered = sum(1 for name in self.selected_features['names'] 
                           if name in self.target_features)
        target_total = len(self.target_features)
        
        labels = [f'Selected ({target_covered})', f'Not Selected ({target_total - target_covered})']
        sizes = [target_covered, target_total - target_covered]
        colors = ['lightgreen', 'lightcoral']
        
        wedges, texts, autotexts = ax3.pie(sizes, labels=labels, colors=colors, 
                                          autopct='%1.1f%%', startangle=90)
        ax3.set_title('Target Feature Coverage')
        
        # 4. Feature Type Distribution
        ax4 = axes[1, 1]
        categorical_count = sum(1 for name in self.selected_features['names'] 
                               if name in self.categorical_features)
        numerical_count = len(self.selected_features['names']) - categorical_count
        
        categories = ['Categorical Features', 'Numerical Features']
        counts = [categorical_count, numerical_count]
        colors = ['lightblue', 'lightgreen']
        
        ax4.bar(categories, counts, color=colors)
        ax4.set_ylabel('Number of Features')
        ax4.set_title('Selected Feature Type Distribution')
        
        # Add value labels
        for i, count in enumerate(counts):
            ax4.text(i, count + 0.1, str(count), ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
    
    def export_results_to_csv(self, output_dir="./"):
        """
        Export correlation analysis and feature importance data to CSV files for Origin and CorrelationPlot
        Uses clean feature names (without 'has' prefix)
        
        Parameters:
        -----------
        output_dir : str, output directory path
        """
        if self.selected_features is None:
            print("Please run feature extraction first")
            return
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Get clean feature names
        clean_selected_names = self._get_clean_feature_names(self.selected_features['names'])
        
        # 1. Export Feature Importance Data
        feature_importance_df = pd.DataFrame({
            'Feature': clean_selected_names,
            'Importance': self.selected_features['importance'],
            'IsTargetFeature': [1 if name in self.target_features else 0 
                               for name in self.selected_features['names']],
            'FeatureType': [1 if name in self.categorical_features else 0 
                           for name in self.selected_features['names']]  # 1=Categorical, 0=Numerical
        })
        
        feature_file = os.path.join(output_dir, "feature_importance.csv")
        feature_importance_df.to_csv(feature_file, index=False)
        print(f"✅ Feature importance data exported to: {feature_file}")
        
        # 2. Export Correlation Matrix Data (Standard format)
        if self.correlation_matrix is not None:
            # Create correlation matrix DataFrame with clean names
            corr_df = pd.DataFrame(
                self.correlation_matrix,
                index=clean_selected_names,
                columns=clean_selected_names
            )
            
            corr_file = os.path.join(output_dir, "correlation_matrix.csv")
            corr_df.to_csv(corr_file, index=True)
            print(f"✅ Correlation matrix exported to: {corr_file}")
            
            # 3. Export for CorrelationPlot (Special format)
            # CorrelationPlot matrix file (values only, tab-delimited)
            corr_plot_file = os.path.join(output_dir, "correlationplot_matrix.txt")
            np.savetxt(corr_plot_file, self.correlation_matrix, delimiter='\t', fmt='%.4f')
            print(f"✅ CorrelationPlot matrix file exported to: {corr_plot_file}")
            
            # CorrelationPlot labels file with clean names
            labels_file = os.path.join(output_dir, "correlationplot_labels.txt")
            with open(labels_file, 'w') as f:
                for label in clean_selected_names:
                    f.write(f"{label}\n")
            print(f"✅ CorrelationPlot labels file exported to: {labels_file}")
            
            # CorrelationPlot CSV format (alternative)
            corr_plot_csv = os.path.join(output_dir, "correlationplot_data.csv")
            corr_df_clean = pd.DataFrame(
                self.correlation_matrix,
                columns=[f"Var{i+1}" for i in range(len(clean_selected_names))]
            )
            corr_df_clean.to_csv(corr_plot_csv, index=False)
            print(f"✅ CorrelationPlot CSV format exported to: {corr_plot_csv}")
            
            # CorrelationPlot with clean feature names as headers
            corr_plot_named = os.path.join(output_dir, "correlationplot_named.csv")
            corr_named_df = pd.DataFrame(self.correlation_matrix)
            corr_named_df.columns = clean_selected_names
            corr_named_df.index = clean_selected_names
            corr_named_df.to_csv(corr_plot_named, index=False)
            print(f"✅ CorrelationPlot named format exported to: {corr_plot_named}")
            
            # Create correlation pairs data (for easier plotting in Origin) with clean names
            corr_pairs = []
            for i, feature1 in enumerate(clean_selected_names):
                for j, feature2 in enumerate(clean_selected_names):
                    if i != j:  # Exclude diagonal elements
                        corr_pairs.append({
                            'Feature1': feature1,
                            'Feature2': feature2,
                            'Correlation': self.correlation_matrix[i, j],
                            'AbsCorrelation': abs(self.correlation_matrix[i, j])
                        })
            
            corr_pairs_df = pd.DataFrame(corr_pairs)
            corr_pairs_file = os.path.join(output_dir, "correlation_pairs.csv")
            corr_pairs_df.to_csv(corr_pairs_file, index=False)
            print(f"✅ Correlation pairs data exported to: {corr_pairs_file}")
        
        # 4. Export CorrelationPlot configuration file
        if self.correlation_matrix is not None:
            config_file = os.path.join(output_dir, "correlationplot_config.txt")
            with open(config_file, 'w') as f:
                f.write("# CorrelationPlot Configuration\n")
                f.write(f"# Number of variables: {len(clean_selected_names)}\n")
                f.write(f"# Matrix file: correlationplot_matrix.txt\n")
                f.write(f"# Labels file: correlationplot_labels.txt\n")
                f.write("# Format: Tab-delimited correlation matrix\n")
                f.write("# Range: -1.0 to 1.0\n")
                f.write("# Note: Feature names have been cleaned (removed 'has' prefix)\n")
                f.write("\n# Variable descriptions:\n")
                for i, (original_name, clean_name) in enumerate(zip(self.selected_features['names'], clean_selected_names)):
                    var_type = "Categorical" if original_name in self.categorical_features else "Numerical"
                    is_target = "Target" if original_name in self.target_features else "Non-target"
                    f.write(f"# Var{i+1}: {clean_name} ({var_type}, {is_target})\n")
                    f.write(f"#         Original: {original_name}\n")
            print(f"✅ CorrelationPlot config file exported to: {config_file}")
        
        # 5. Export Summary Statistics
        summary_data = {
            'Metric': [
                'Total Features',
                'Selected Features', 
                'Target Features Covered',
                'Target Coverage Rate (%)',
                'Categorical Features',
                'Numerical Features',
                'Highest Importance',
                'Lowest Importance',
                'Average Importance',
                'Max Correlation',
                'Min Correlation',
                'Avg Abs Correlation'
            ],
            'Value': [
                len(self.tunnel_parameters),
                len(self.selected_features['names']),
                sum(1 for name in self.selected_features['names'] if name in self.target_features),
                round(sum(1 for name in self.selected_features['names'] if name in self.target_features) / len(self.target_features) * 100, 1),
                sum(1 for name in self.selected_features['names'] if name in self.categorical_features),
                sum(1 for name in self.selected_features['names'] if name not in self.categorical_features),
                round(max(self.selected_features['importance']), 4),
                round(min(self.selected_features['importance']), 4),
                round(np.mean(self.selected_features['importance']), 4),
                round(np.max(self.correlation_matrix[np.triu_indices_from(self.correlation_matrix, k=1)]), 4) if self.correlation_matrix is not None else 'N/A',
                round(np.min(self.correlation_matrix[np.triu_indices_from(self.correlation_matrix, k=1)]), 4) if self.correlation_matrix is not None else 'N/A',
                round(np.mean(np.abs(self.correlation_matrix[np.triu_indices_from(self.correlation_matrix, k=1)])), 4) if self.correlation_matrix is not None else 'N/A'
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        summary_file = os.path.join(output_dir, "analysis_summary.csv")
        summary_df.to_csv(summary_file, index=False)
        print(f"✅ Analysis summary exported to: {summary_file}")
        
        # 6. Export Data for Origin Plotting Templates (with clean names)
        origin_data = {
            'FeatureName': clean_selected_names,
            'Importance': self.selected_features['importance'],
            'Rank': list(range(1, len(self.selected_features['names']) + 1)),
            'IsTarget': ['Yes' if name in self.target_features else 'No' 
                        for name in self.selected_features['names']],
            'Type': ['Categorical' if name in self.categorical_features else 'Numerical' 
                    for name in self.selected_features['names']],
            'OriginalName': self.selected_features['names']  # Keep original names for reference
        }
        
        origin_df = pd.DataFrame(origin_data)
        origin_file = os.path.join(output_dir, "origin_plot_data.csv")
        origin_df.to_csv(origin_file, index=False)
        print(f"✅ Origin plotting data exported to: {origin_file}")
        
        # 7. Create CorrelationPlot README
        readme_file = os.path.join(output_dir, "CorrelationPlot_README.txt")
        with open(readme_file, 'w') as f:
            f.write("CorrelationPlot Usage Instructions\n")
            f.write("="*50 + "\n\n")
            f.write("IMPORTANT: Feature names have been cleaned (removed 'has' prefix) for better visualization\n\n")
            f.write("Files for CorrelationPlot:\n")
            f.write("1. correlationplot_matrix.txt - Main correlation matrix (tab-delimited)\n")
            f.write("2. correlationplot_labels.txt - Clean variable names (one per line)\n")
            f.write("3. correlationplot_data.csv - CSV format with Var1, Var2, etc.\n")
            f.write("4. correlationplot_named.csv - CSV with clean feature names\n")
            f.write("5. correlationplot_config.txt - Configuration and variable descriptions\n\n")
            f.write("How to use:\n")
            f.write("- Option 1: Import correlationplot_matrix.txt + correlationplot_labels.txt\n")
            f.write("- Option 2: Import correlationplot_data.csv or correlationplot_named.csv\n")
            f.write("- Check correlationplot_config.txt for variable descriptions\n\n")
            f.write("Matrix Properties:\n")
            f.write(f"- Size: {len(clean_selected_names)}x{len(clean_selected_names)}\n")
            f.write("- Range: -1.0 to 1.0\n")
            f.write("- Format: Symmetric correlation matrix\n")
            f.write("- Precision: 4 decimal places\n\n")
            f.write("Variable Information (Clean Names):\n")
            for i, (original_name, clean_name) in enumerate(zip(self.selected_features['names'], clean_selected_names)):
                var_type = "Categorical" if original_name in self.categorical_features else "Numerical"
                is_target = "★Target" if original_name in self.target_features else "Non-target"
                importance = self.selected_features['importance'][i]
                f.write(f"- {clean_name}: {var_type}, {is_target}, Importance={importance:.4f}\n")
                f.write(f"  (Original: {original_name})\n")
        print(f"✅ CorrelationPlot README exported to: {readme_file}")
        
        print(f"\n📁 All files exported to directory: {output_dir}")
        print("📋 Files for different tools (using clean feature names):")
        print("   📊 CorrelationPlot:")
        print("      - correlationplot_matrix.txt (main matrix file)")
        print("      - correlationplot_labels.txt (clean variable names)")
        print("      - correlationplot_named.csv (CSV with clean names)")
        print("      - CorrelationPlot_README.txt (usage instructions)")
        print("   📈 Origin:")
        print("      - correlation_matrix.csv (standard matrix with clean names)")
        print("      - origin_plot_data.csv (plotting data with clean names)")
        print("   📋 General:")
        print("      - feature_importance.csv (feature analysis with clean names)")
        print("      - correlation_pairs.csv (pairwise data with clean names)")
        print("      - analysis_summary.csv (summary statistics)")
        
        return {
            'feature_importance_file': feature_file,
            'correlation_matrix_file': corr_file if self.correlation_matrix is not None else None,
            'correlationplot_matrix_file': corr_plot_file if self.correlation_matrix is not None else None,
            'correlationplot_labels_file': labels_file if self.correlation_matrix is not None else None,
            'correlationplot_csv_file': corr_plot_csv if self.correlation_matrix is not None else None,
            'origin_plot_file': origin_file,
            'summary_file': summary_file,
            'readme_file': readme_file if self.correlation_matrix is not None else None
        }
    
    def get_final_results(self):
        """
        Get final results with clean feature names
        """
        if self.selected_features is None:
            print("Please run feature extraction first")
            return None
        
        # Check target feature coverage
        covered_targets = [name for name in self.selected_features['names'] 
                          if name in self.target_features]
        missing_targets = [name for name in self.target_features 
                          if name not in self.selected_features['names']]
        
        # Get clean names for display
        clean_covered_targets = self._get_clean_feature_names(covered_targets)
        clean_missing_targets = self._get_clean_feature_names(missing_targets)
        clean_selected_names = self._get_clean_feature_names(self.selected_features['names'])
        
        results = {
            'selected_features': self.selected_features,
            'selected_features_clean_names': clean_selected_names,
            'target_features_covered': covered_targets,
            'target_features_covered_clean': clean_covered_targets,
            'target_features_missing': missing_targets,
            'target_features_missing_clean': clean_missing_targets,
            'coverage_rate': len(covered_targets) / len(self.target_features),
            'correlation_matrix': self.correlation_matrix,
            'feature_importance': self.feature_importance,
            'all_feature_names': self.feature_names,
            'all_feature_names_clean': self._get_clean_feature_names(self.feature_names)
        }
        
        print("\n" + "="*60)
        print("Feature Extraction Final Results")
        print("="*60)
        print(f"Number of selected features: {len(self.selected_features['names'])}")
        print(f"Target feature coverage rate: {results['coverage_rate']:.1%}")
        print(f"\n✅ Selected target features: {clean_covered_targets}")
        if clean_missing_targets:
            print(f"❌ Missing target features: {clean_missing_targets}")
        
        print(f"\n📊 All selected features (clean names): {clean_selected_names}")
        
        return results

# Usage example (unchanged)
def create_sample_data():
    """
    Create realistic tunnel engineering data based on actual engineering logic
    """
    np.random.seed(42)
    n_samples = 150
    
    # Step 1: Generate base tunnel characteristics
    tunnel_types = np.random.choice(['MountainTunnelProject', 'UnderwaterTunnelProject', 
                                   'ShallowTunnelProject', 'DeepTunnelProject'], n_samples)
    
    # Step 2: Generate tunnel geometry based on type
    tunnel_lengths = []
    tunnel_diameters = []
    
    for tunnel_type in tunnel_types:
        if tunnel_type == 'MountainTunnelProject':
            # Mountain tunnels: typically longer, medium diameter
            length = np.random.uniform(800, 8000)
            diameter = np.random.uniform(8, 14)
        elif tunnel_type == 'UnderwaterTunnelProject':
            # Underwater tunnels: medium length, larger diameter
            length = np.random.uniform(500, 3000)
            diameter = np.random.uniform(10, 16)
        elif tunnel_type == 'ShallowTunnelProject':
            # Shallow tunnels: shorter, smaller diameter
            length = np.random.uniform(200, 2000)
            diameter = np.random.uniform(4, 10)
        else:  # DeepTunnelProject
            # Deep tunnels: medium to long, medium diameter
            length = np.random.uniform(1000, 6000)
            diameter = np.random.uniform(6, 12)
        
        tunnel_lengths.append(length)
        tunnel_diameters.append(diameter)
    
    # Step 3: Generate geological conditions with realistic distribution
    # Mountain and deep tunnels more likely to have poor rock conditions
    geological_conditions = []
    for tunnel_type in tunnel_types:
        if tunnel_type in ['MountainTunnelProject', 'DeepTunnelProject']:
            # More challenging conditions
            condition = np.random.choice(['II', 'III', 'IV', 'V'], p=[0.1, 0.3, 0.4, 0.2])
        else:
            # Generally better conditions for shallow and underwater
            condition = np.random.choice(['I', 'II', 'III', 'IV'], p=[0.2, 0.4, 0.3, 0.1])
        geological_conditions.append(condition)
    
    # Step 4: Generate hydrological conditions based on tunnel type
    hydro_conditions = []
    for tunnel_type in tunnel_types:
        if tunnel_type == 'UnderwaterTunnelProject':
            # Underwater tunnels: high water pressure
            condition = np.random.choice(['Wet', 'Flooded'], p=[0.3, 0.7])
        elif tunnel_type == 'ShallowTunnelProject':
            # Shallow tunnels: generally drier
            condition = np.random.choice(['Dry', 'Wet'], p=[0.6, 0.4])
        else:
            # Mountain and deep: variable conditions
            condition = np.random.choice(['Dry', 'Wet', 'Flooded'], p=[0.4, 0.4, 0.2])
        hydro_conditions.append(condition)
    
    # Step 5: Generate soil types based on tunnel type
    soil_types = []
    for tunnel_type in tunnel_types:
        if tunnel_type == 'UnderwaterTunnelProject':
            # Underwater: more likely soft soil
            soil_type = np.random.choice([1, 2], p=[0.6, 0.4])  # Clay, Sand
        elif tunnel_type == 'MountainTunnelProject':
            # Mountain: more likely strong soil/rock
            soil_type = np.random.choice([2, 3], p=[0.3, 0.7])  # Sand, Strong
        else:
            # Balanced distribution
            soil_type = np.random.choice([1, 2, 3], p=[0.4, 0.3, 0.3])
        soil_types.append(soil_type)
    
    # Step 6: Generate construction methods based on conditions
    construction_methods = []
    for i in range(n_samples):
        if tunnel_types[i] == 'UnderwaterTunnelProject':
            # Underwater: mainly Shield method
            method = np.random.choice(['Shield', 'TBM'], p=[0.7, 0.3])
        elif tunnel_types[i] == 'MountainTunnelProject':
            # Mountain: mainly NATM and TBM
            method = np.random.choice(['NATM', 'TBM'], p=[0.6, 0.4])
        else:
            # Others: mixed methods
            method = np.random.choice(['TBM', 'NATM', 'Shield'], p=[0.4, 0.4, 0.2])
        construction_methods.append(method)
    
    # Step 7: Generate support parameters based on geological conditions
    bolt_lengths = []
    bolt_rows = []
    bolt_columns = []
    lining_thickness = []
    steel_arch_spacing = []
    steel_arch_thickness = []
    
    # Geological condition mapping: I=1, II=2, III=3, IV=4, V=5
    geo_mapping = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5}
    
    for i in range(n_samples):
        geo_level = geo_mapping[geological_conditions[i]]
        diameter = tunnel_diameters[i]
        
        # Bolt length: worse geology = longer bolts
        base_bolt_length = 1.5 + (geo_level - 1) * 0.8  # 1.5m to 4.7m
        bolt_length = base_bolt_length + np.random.normal(0, 0.3)
        bolt_length = max(1.2, min(6.0, bolt_length))
        bolt_lengths.append(bolt_length)
        
        # Bolt arrangement: worse geology = denser arrangement
        base_rows = 3 + geo_level  # 4 to 8 rows
        bolt_row = int(base_rows + np.random.normal(0, 1))
        bolt_row = max(3, min(12, bolt_row))
        bolt_rows.append(bolt_row)
        
        # Bolt columns related to tunnel perimeter
        perimeter_factor = diameter / 10  # Normalization
        base_columns = int(8 + perimeter_factor * 6 + geo_level * 2)
        bolt_column = int(base_columns + np.random.normal(0, 2))
        bolt_column = max(6, min(24, bolt_column))
        bolt_columns.append(bolt_column)
        
        # Lining thickness: worse geology = thicker lining
        base_lining = 0.2 + (geo_level - 1) * 0.15  # 0.2m to 0.8m
        lining = base_lining + np.random.normal(0, 0.05)
        lining = max(0.15, min(1.0, lining))
        lining_thickness.append(lining)
        
        # Steel arch spacing: worse geology = smaller spacing
        base_spacing = 2.0 - (geo_level - 1) * 0.3  # 2.0m to 0.8m
        spacing = base_spacing + np.random.normal(0, 0.1)
        spacing = max(0.5, min(2.5, spacing))
        steel_arch_spacing.append(spacing)
        
        # Steel arch thickness: worse geology = thicker steel
        base_thickness = 0.01 + (geo_level - 1) * 0.008  # 0.01m to 0.042m
        thickness = base_thickness + np.random.normal(0, 0.003)
        thickness = max(0.008, min(0.06, thickness))
        steel_arch_thickness.append(thickness)
    
    # Step 8: Calculate steel arch count based on tunnel length and spacing
    steel_arch_counts = []
    for i in range(n_samples):
        count = int(tunnel_lengths[i] / steel_arch_spacing[i]) + np.random.randint(-5, 6)
        count = max(20, count)  # Minimum reasonable count
        steel_arch_counts.append(count)
    
    # Step 9: Generate waterproof layer thickness based on hydrological conditions
    waterproof_thickness = []
    for hydro_condition in hydro_conditions:
        if hydro_condition == 'Dry':
            thickness = np.random.uniform(0.05, 0.15)
        elif hydro_condition == 'Wet':
            thickness = np.random.uniform(0.12, 0.25)
        else:  # Flooded
            thickness = np.random.uniform(0.20, 0.40)
        waterproof_thickness.append(thickness)
    
    # Step 10: Create DataFrame
    data = {
        'hasTunnelLength': tunnel_lengths,
        'hasGeologicalCondition': geological_conditions,
        'hasHydroCondition': hydro_conditions,
        'hasSoilType': soil_types,
        'TunnelType': tunnel_types,
        'hasTunnelDiameter': tunnel_diameters,
        'hasConstructionMethod': construction_methods,
        'hasBoltLength': bolt_lengths,
        'hasBoltRowCount': bolt_rows,
        'hasBoltColumnCount': bolt_columns,
        'hasLiningThickness': lining_thickness,
        'hasSteelArchSpacing': steel_arch_spacing,
        'hasSteelArchCount': steel_arch_counts,
        'hasSteelArchThickness': steel_arch_thickness,
        'hasWaterproofLayerThickness': waterproof_thickness
    }
    
    df = pd.DataFrame(data)
    
    # Step 11: Create realistic target variable (tunnel construction volume)
    # Influenced by: diameter (quadratic), length (linear), geological conditions, support complexity
    tunnel_volumes = []
    for i in range(n_samples):
        # Base volume from geometry
        base_volume = np.pi * (tunnel_diameters[i] / 2) ** 2 * tunnel_lengths[i]
        
        # Geological factor (worse geology = more excavation/support volume)
        geo_factor = 1.0 + (geo_mapping[geological_conditions[i]] - 1) * 0.1
        
        # Support complexity factor
        support_factor = 1.0 + (bolt_lengths[i] / 6.0) * 0.2 + (lining_thickness[i] / 1.0) * 0.3
        
        # Hydrological factor
        hydro_factor = {'Dry': 1.0, 'Wet': 1.1, 'Flooded': 1.2}[hydro_conditions[i]]
        
        # Calculate total construction volume
        total_volume = base_volume * geo_factor * support_factor * hydro_factor
        
        # Add realistic noise
        total_volume *= (1 + np.random.normal(0, 0.05))
        tunnel_volumes.append(total_volume)
    
    df['TunnelArea'] = tunnel_volumes
    
    # Add some engineering insights as comments
    print("\n🏗️  Generated Realistic Tunnel Engineering Data")
    print("="*60)
    print("Engineering Logic Applied:")
    print("• Geological conditions affect support parameters (bolts, lining, steel arch)")
    print("• Tunnel type influences geometry and construction method")
    print("• Hydrological conditions determine waterproofing requirements")
    print("• Steel arch count calculated from tunnel length and spacing")
    print("• Construction volume considers geology, support complexity, and hydrology")
    print("• Correlations reflect real engineering relationships")
    
    return df

def main():
    """
    Main demonstration function with clean feature names
    """
    # Create sample data
    data_df = create_sample_data()
    print("Created sample tunnel data")
    print(data_df.head())
    
    # Create feature extractor
    extractor = TunnelFeatureExtractor()
    
    # Data preprocessing
    X, y = extractor.prepare_data(data_df, target_column='TunnelArea')
    
    # Feature extraction (prioritize target features)
    selected_features = extractor.extract_features_with_target_priority(X, y, top_k=6)
    
    # Correlation check
    extractor.check_correlation(X, correlation_threshold=0.8)
    
    # Model validation
    extractor.validate_model(X, y)
    
    # Visualize results (now with clean feature names)
    extractor.plot_results()
    
    # Export CSV files for Origin (now with clean feature names)
    print("\n" + "="*60)
    print("Exporting Data for Origin Plotting (Clean Feature Names)")
    print("="*60)
    exported_files = extractor.export_results_to_csv(output_dir="./tunnel_analysis_results/")
    
    # Get final results (now includes clean names)
    results = extractor.get_final_results()
    
    print("\n" + "="*60)
    print("Analysis Complete!")
    print("="*60)
    print("✅ Feature extraction completed with English interface and clean feature names")
    print("✅ CSV files exported for Origin plotting (no 'has' prefix)")
    print("✅ All visualizations use clean English labels")
    print("✅ Original feature names preserved in configuration files for reference")
    
    return results, exported_files

if __name__ == "__main__":
    results, files = main()