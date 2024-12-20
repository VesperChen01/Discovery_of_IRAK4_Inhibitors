import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def find_decomposition_files(root_dir):
    """
    Recursively find all decomposition files matching the naming pattern.
    """
    decomposition_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.startswith("FINAL_RESULTS_MMPBSA_output_") and filename.endswith("_decomposition.csv"):
                decomposition_files.append(os.path.join(dirpath, filename))
    return decomposition_files

def extract_structure_name(file_path):
    """
    Extract the structure name (number part) from the filename.
    """
    base_name = os.path.basename(file_path)
    try:
        # Extract the number from the filename
        structure_name = base_name.split("_")[4]  # The 4th element is the number part
        return structure_name
    except IndexError:
        return "Unknown"

def load_and_clean_decomposition(files, error_log="error_log.txt"):
    """
    Load and clean decomposition files, filtering residues with TOTAL < 1.
    """
    all_data = []
    with open(error_log, "w") as log_file:
        for file in files:
            try:
                # Skip the first two lines and load the data
                df = pd.read_csv(file, skiprows=3)

                # Ensure the required columns exist
                if not {"Residue", "TOTAL"}.issubset(df.columns):
                    raise ValueError("Missing required columns: Residue or TOTAL")

                # Convert necessary columns to numeric
                df["TOTAL"] = pd.to_numeric(df["TOTAL"], errors="coerce")

                # Drop rows with NaN values in the TOTAL column
                df = df.dropna(subset=["TOTAL"])

                # Filter for TOTAL < 1
                df = df[df["TOTAL"] < 1]

                # Group by Residue and calculate mean TOTAL energy
                df_grouped = df.groupby("Residue")["TOTAL"].mean().reset_index()

                # Extract the structure name from the filename
                structure_name = extract_structure_name(file)
                df_grouped["Source"] = structure_name

                all_data.append(df_grouped)
            except Exception as e:
                log_file.write(f"Error processing {file}: {e}\n")
                print(f"Error processing {file}: {e}")

    if not all_data:
        raise ValueError("No valid decomposition data found.")

    # Combine all data
    combined_data = pd.concat(all_data, ignore_index=True)
    return combined_data

def plot_combined_heatmap(data, output_path):
    """
    Generate a combined horizontal heatmap for residues with TOTAL < 1,
    excluding Residues related to LIG (e.g., those containing "L:").
    """
    # Pivot data (structure names as rows, residues as columns)
    heatmap_data = data.pivot_table(index="Source", columns="Residue", values="TOTAL", aggfunc=np.mean)

    # Remove Residues containing "L:"
    heatmap_data = heatmap_data.loc[:, ~heatmap_data.columns.str.contains("L:")]

    print("Heatmap data shape:", heatmap_data.shape)
    print("Heatmap data preview:\n", heatmap_data)

    # Fill missing values
    heatmap_data = heatmap_data.fillna(0)

    # Plot the heatmap
    cmap = sns.diverging_palette(240, 10, n=256, as_cmap=True)
    plt.figure(figsize=(14, 10))
    sns.heatmap(
        heatmap_data,
        cmap=cmap,
        center=0,
        cbar_kws={"label": "Average TOTAL Energy (kcal/mol)"},
        linewidths=0.5
    )
    plt.title("Binding Energy Below 1 kcal/mol (Horizontal Layout)", fontsize=20, pad=20)
    plt.xlabel("Residue", fontsize=14)
    plt.ylabel("Structure", fontsize=14)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()

    # Save the heatmap image
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.show()

if __name__ == "__main__":
    # Root directory containing decomposition files
    root_directory = "/home/vesper/StarCelestial/Vesper/IRAK4/decom/"  # Update to your directory

    # Path to save the heatmap
    output_heatmap_path = "binding_energy_below_1_heatmap_horizontal.png"

    try:
        # Find all decomposition files
        decomposition_files = find_decomposition_files(root_directory)
        print(f"Found {len(decomposition_files)} decomposition files.")

        # Load and clean the data
        combined_data = load_and_clean_decomposition(decomposition_files)

        # Plot and save the heatmap
        plot_combined_heatmap(combined_data, output_heatmap_path)
        print(f"Heatmap saved to {output_heatmap_path}")
    except ValueError as e:
        print(f"Error: {e}")
