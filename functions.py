import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
SMALL_SIZE = 8
MEDIUM_SIZE = 12
BIGGER_SIZE = 16
plt.rcParams.update({'font.size': BIGGER_SIZE,'axes.labelsize':BIGGER_SIZE,'axes.titlesize':BIGGER_SIZE,
                     'xtick.labelsize':BIGGER_SIZE,'ytick.labelsize':MEDIUM_SIZE})
# Define your base directory
base_dir = os.getcwd()
# Define different output file path
# Define the thermodynamic output file
thermo_file_exe_1 = os.path.join(base_dir, 'exercise_1_bulk_water/step_1_equilibration/thermo.out')
thermo_file_exe_2 = os.path.join(base_dir, 'exercise_2_sodium_in_water/step_1_equilibration/thermo.out')

# Define the rdf output file
rdf_file_path_exe_1_sess_1 = os.path.join(base_dir, 'exercise_1_bulk_water/step_1_equilibration/rdf.out')
rdf_file_path_exe_1_sess_2 = os.path.join(base_dir, 'exercise_1_bulk_water/step_2_production/rdf.out')
rdf_file_path_exe_2_sess_1 = os.path.join(base_dir, 'exercise_2_sodium_in_water/step_1_equilibration/rdf.out')
rdf_file_path_exe_2_sess_2 = os.path.join(base_dir, 'exercise_2_sodium_in_water/step_2_production/rdf.out')

# Define the msd output file
msd_file_path_exe_1_sess_1 = os.path.join(base_dir, 'exercise_1_bulk_water/step_1_equilibration/water_msd.out')
msd_file_path_exe_1_sess_2 = os.path.join(base_dir, 'exercise_1_bulk_water/step_2_production/water_msd.out')
msd_file_path_exe_2_sess_1 = os.path.join(base_dir, 'exercise_2_sodium_in_water/step_1_equilibration/na_msd.out')
msd_file_path_exe_2_sess_2 = os.path.join(base_dir, 'exercise_2_sodium_in_water/step_2_production/na_msd.out')

expt_rdf_file_path = os.path.join(base_dir,'OwOw_expt_rdf.out')
#water_msd_file = os.path.join(base_dir, 'water_msd.out')  
#ion_msd_file = os.path.join(base_dir, 'na_msd.out')

# Column names based on the required plots
required_columns = ['time', 'temp', 'etotal', 'ke', 'pe','enthalpy', 'density', 'press']

# Function to load the data
def load_data(thermo_file_path):
    # Reading the data and assigning only necessary column names
    df = pd.read_csv(thermo_file_path, delim_whitespace=True, comment='#', header=None, usecols=[1, 2, 3, 4, 5, 6, 7, 15])
    df.columns = required_columns
    return df

# Function to plot time vs. a specified column
def plot_time_vs_column(df, column_name, y_label, y_unit):
    plt.figure()
    plt.plot(df['time']/1e3, df[column_name], label=column_name)
    plt.xlabel('Time (ps)')
    plt.ylabel(f'{y_label} ({y_unit})')
    plt.title(f'Time vs {y_label}')
    #plt.legend()
    plt.show()
    
def plot_water_rdf(file_path, expt_file_path, timestep=2000, nbins=100):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Find the line with the specified timestep and number of bins
    start_line = 0
    for i, line in enumerate(lines):
        if line.startswith('#'):
            continue
        if str(timestep) in line.split() and str(nbins) in line.split():
            start_line = i + 1
            break
    
    # Read the data from the next 'nbins' lines
    rdf_data = []
    for line in lines[start_line:start_line + nbins]:
        if line.strip():  # Ignore empty lines
            rdf_data.append([float(x) for x in line.split()])
    
    # Convert to DataFrame
    df_rdf = pd.DataFrame(rdf_data)
    
    # Read the experimental RDF data
    df_expt_rdf = pd.read_csv(expt_file_path, delim_whitespace=True, header=None, names=['distance', 'g(r_OO)'])
    
    # Plot the RDF data (using only the 2nd and 3rd columns)
    plt.figure()
    plt.plot(df_rdf.iloc[:, 1], df_rdf.iloc[:, 2], label='Obtained TIP4P-Ew',linewidth='0.75')
    plt.xlabel('Distance (Å)')
    plt.xlim(0, 8)
    plt.ylim(0, 3.5)
    plt.ylabel(r'$g(r_{OO})$')

    # Plot experimental RDF with shading under the curve and no line
    plt.fill_between(df_expt_rdf['distance'], df_expt_rdf['g(r_OO)'], alpha=0.5, color='gray', label='Experimental')

    plt.legend()
    plt.show()

# Equilibriated rdf file: final step = 200000

def plot_msd_water(file_path):
    # Load the data, ignoring lines starting with #
    df = pd.read_csv(file_path, delim_whitespace=True, comment='#', header=None)
    
    # Extracting the required columns
    time = df[0]/1e3 # fs to ps
    msd = df[4]
    
    # Plotting the data
    plt.figure()
    plt.plot(time, msd, label='Mean Square Displacement')
    plt.xlabel('Time (ps)')
    plt.ylabel('Mean Square Displacement (Å²)')
    plt.title('MSD of Water molecule')
    plt.legend()
    plt.show()
    
def plot_msd_ion(file_path):
    # Load the data, ignoring lines starting with #
    df = pd.read_csv(file_path, delim_whitespace=True, comment='#', header=None)
    
    # Extracting the required columns
    time = df[0]/1e3 # fs to ps
    msd = np.round(df[4],2)
    
    # Plotting the data
    plt.figure()
    plt.plot(time, msd, label='Mean Square Displacement')
    plt.xlabel('Time (ps)')
    plt.xlim(time.min(), time.max())
    plt.ylabel('Mean Square Displacement (Å²)')
    plt.title('MSD of Ion molecule')
    plt.legend()
    plt.show()
    
def plot_all_energy(df, y_label, y_unit):
    plt.figure()
    plt.plot(df['time']/1e3, df['ke'], label='Kinetic Energy')  # Uncommented this line
    plt.plot(df['time']/1e3, df['pe'], label='Potential Energy')
    plt.plot(df['time']/1e3, df['etotal'], label='Total Energy')
    plt.xlabel('Time (ps)')
    plt.ylabel(f'{y_label} ({y_unit})')
    plt.title(f'Time vs {y_label}')
    plt.legend()  # Uncommented this line
    plt.show()
    
def plot_ion_rdf(file_path, timestep=2000, nbins=100,title='Na-Ow RDF'):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Find the line with the specified timestep and number of bins
    start_line = 0
    for i, line in enumerate(lines):
        if line.startswith('#'):
            continue
        if str(timestep) in line.split() and str(nbins) in line.split():
            start_line = i + 1
            break
    
    # Read the data from the next 'nbins' lines
    rdf_data = []
    for line in lines[start_line:start_line + nbins]:
        if line.strip():  # Ignore empty lines
            rdf_data.append([float(x) for x in line.split()])
    
    # Convert to DataFrame
    df_rdf = pd.DataFrame(rdf_data)
    
    # Plot the RDF data (using only the 2nd and 3rd columns)
    plt.figure()
    plt.plot(df_rdf.iloc[:, 1], df_rdf.iloc[:, 4], label='g(r)')
    #plt.plot(df_rdf.iloc[:, 1], df_rdf.iloc[:, 5], label='Coordination number',linewidth='0.75')

    plt.xlabel('Distance (Å)')
    plt.xlim(0, 8)
    plt.ylim(0, 10)
    plt.ylabel(r'$g(r_{OO})$')
    plt.title(title)

    # Plot experimental RDF with shading under the curve and no line
    #plt.fill_between(df_expt_rdf['distance'], df_expt_rdf['g(r_OO)'], alpha=0.5, color='gray', label='TIP4P-Ew')

    plt.legend()
    plt.show()