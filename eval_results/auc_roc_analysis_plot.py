import pandas as pd
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Folder containing the CSV files
folder_path = '/data/Roufen/IRAK4-eval-plot/'  # Replace with your folder path
output_auc_csv = "auc_results.csv"
output_plot_png = "auc_roc_comparison_lines.png"

# Initialize a dictionary to store results
results = {}

# Possible pdb_id column names
possible_pdb_columns = ['pdb_id', 'id', 'identifier']

# Loop through all CSV files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv') and file_name != output_auc_csv:  # Skip results file
        # Load the data
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path)
        
        # Handle psichic_score.csv with its original logic
        if file_name == "psichic_score.csv":
            print(f"Processing PSICHIC file: {file_name}")
            
            # Use correct column name
            score_column = 'PSICHIC' if 'PSICHIC' in df.columns else 'psichic_score'
            
            # Generate labels: CHEMBL as 1, others starting with "C" as 0
            if 'Name' not in df.columns:
                print(f"Skipping {file_name}, 'Name' column not found")
                continue
            
            df['label'] = df['Name'].apply(lambda x: 1 if str(x).startswith("CHEMBL") else (0 if str(x).startswith("C") else None))
            
            # Remove rows with NaN in label or score
            df = df.dropna(subset=[score_column, 'label'])
            
            # Calculate AUC for PSICHIC/psichic_score
            try:
                auc_psichic = roc_auc_score(df['label'], df[score_column])
                results[file_name] = {score_column: auc_psichic}
            except ValueError as e:
                print(f"Error calculating AUC-ROC for {file_name}: {e}")
                continue
            continue
        
        # Handle other files with docking logic
        pdb_column = next((col for col in possible_pdb_columns if col in df.columns), None)
        if pdb_column is None:
            print(f"Skipping {file_name}, no pdb-like column found")
            continue
        
        # Add labels based on the matched pdb column
        df['label'] = df[pdb_column].apply(lambda x: 1 if str(x).startswith("CHEMBL") else 0)
        
        # Remove rows with NaN in relevant columns
        score_columns = ['KarmaDock', 'ledock', 'planet', 'Vina-gpu', 'Xdock']
        available_columns = [col for col in score_columns if col in df.columns]
        df = df.dropna(subset=available_columns + ['label'])
        
        # Ensure numeric columns are indeed numeric
        for column in available_columns:
            if not pd.api.types.is_numeric_dtype(df[column]):
                raise ValueError(f"Column {column} in {file_name} must contain numeric values")
        
        # Calculate AUC-ROC for each docking software
        try:
            aucs = {col: roc_auc_score(df['label'], df[col]) for col in available_columns}
            results[file_name] = aucs
        except ValueError as e:
            print(f"Error calculating AUC-ROC for {file_name}: {e}")
            continue

# Convert results to a DataFrame and save
results_df = pd.DataFrame(results).T.sort_index()
results_df.to_csv(output_auc_csv, index=True)
print(f"AUC results saved to {output_auc_csv}")

# Set seaborn style
sns.set_theme(style="whitegrid")

# Create the plot
plt.figure(figsize=(14, 8))

# Custom colors and markers
colors = sns.color_palette("viridis", len(results_df.columns))  # High-quality colormap
markers = ['o', 's', 'D', '^', '*', 'x']  # Different marker styles

# Plot each software's AUC values
for idx, column in enumerate(results_df.columns):
    plt.errorbar(
        results_df.index,
        results_df[column],
        yerr=None,  # Add error bars if you have them
        fmt=markers[idx],  # Marker style
        label=column,
        color=colors[idx],
        linewidth=2.5,
        markersize=10,
        capsize=5,
    )

# Add title and axis labels
plt.title('AUC-ROC Comparison for Docking Software Across Datasets', fontsize=20, weight='bold', pad=20)
plt.xlabel('Dataset', fontsize=14, labelpad=10)
plt.ylabel('AUC-ROC', fontsize=14, labelpad=10)

# Customize x and y ticks
plt.xticks(fontsize=12, rotation=45)
plt.yticks(fontsize=12)
plt.ylim(0.0, 1.05)

# Add legend outside the plot
plt.legend(
    title="Docking Software",
    fontsize=12,
    title_fontsize=14,
    loc='upper left',
    bbox_to_anchor=(1.05, 1),  
    frameon=True,
    fancybox=True,
    shadow=True,
    borderpad=1,
)

# Add grid lines
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Adjust layout and save
plt.tight_layout()
plt.savefig(output_plot_png, dpi=300, bbox_inches='tight')
plt.show()

print(f"Plot saved to {output_plot_png}")
