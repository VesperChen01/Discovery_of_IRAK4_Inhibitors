import pandas as pd
import matplotlib.pyplot as plt

def plot_rmsd(data_file, output_dir):
    # Load the data
    data = pd.read_csv(data_file)

    # Filter data for each molecule
    molecule_1 = data[data['ligand_name'] == '1038620-68-6']
    molecule_2 = data[data['ligand_name.1'] == '1356962-34-9']

    # Plot for molecule 1 (1038620-68-6)
    plt.figure(figsize=(10, 6))
    plt.plot(molecule_1['time(ns)'], molecule_1['backbone'], label='Backbone RMSD', color='blue', alpha=0.7)
    plt.plot(molecule_1['time(ns)'], molecule_1['ligand'], label='Ligand RMSD', color='skyblue', alpha=0.7)
    plt.xlabel('Time (ns)', fontsize=12)
    plt.ylabel('RMSD (nm)', fontsize=12)
    plt.title('RMSD Analysis for Molecule: 1038620-68-6', fontsize=14)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(f"{output_dir}/RMSD_1038620-68-6.png", dpi=300)
    plt.close()

    # Plot for molecule 2 (1356962-34-9)
    plt.figure(figsize=(10, 6))
    plt.plot(molecule_2['time(ns)'], molecule_2['backbone.1'], label='Backbone RMSD', color='blue', alpha=0.7)
    plt.plot(molecule_2['time(ns)'], molecule_2['ligand.1'], label='Ligand RMSD', color='skyblue', alpha=0.7)
    plt.xlabel('Time (ns)', fontsize=12)
    plt.ylabel('RMSD (nm)', fontsize=12)
    plt.title('RMSD Analysis for Molecule: 1356962-34-9', fontsize=14)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(f"{output_dir}/RMSD_1356962-34-9.png", dpi=300)
    plt.close()


plot_rmsd('/home/vesper/StarCelestial/Vesper/IRAK4/rmsd-plot/rmsd.csv', '/home/vesper/StarCelestial/Vesper/IRAK4/rmsd-plot/')