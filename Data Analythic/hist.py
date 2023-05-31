import pandas as pd
import matplotlib.pyplot as plt
import glob

def filter_mapillary(csv_file_path):
    # Read the metadata of images surrounded by locations in the US
    df = pd.read_csv(csv_file_path, low_memory=False)
    return df

# Get a list of all the CSV files in the directory
csv_files = glob.glob('/home/negin/March 2023/USCANADA/Finalsafegraph-clean/Final JSON file Gathered/CSV Folders for true and totals/TrueCSVs/*.csv')

# Create an empty list to store DataFrames
dfs = []

# Loop over the list of CSV files and concatenate them
for csv_file in csv_files:
    print('#############################################')
    print(csv_file)
    print('#############################################\n')
    df = filter_mapillary(csv_file)
    dfs.append(df)

# Concatenate the DataFrames into a single DataFrame
combined_df = pd.concat(dfs, ignore_index=True)

# Grouping by coordinates and counting the number of images
# Grouping by coordinates and counting the number of rows in each group
grouped = df.groupby('Coordinates').size().sort_values(ascending=False)

# Creating the coordinates and count arrays for plotting
coordinates = grouped.index
count = grouped.values
# Set the font for LaTeX
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times", "Palatino", "New Century Schoolbook", "Bookman", "Computer Modern Roman"],
})

# Plotting the histogram
fig, ax = plt.subplots(figsize=(3.5, 2.5))
ax.bar(coordinates, count, color='#7fcdbb')  # Set the color using a hexadecimal value
ax.bar(coordinates, count, color='#7fcdbb')  # Set the color using a hexadecimal value
ax.set_xlabel('Unique POIs')  # Change x-axis label if needed
ax.set_ylabel('Count of Mapillary Images per POI')
ax.set_xticklabels([])  # Remove x-axis tick labels

# Saving the plot as a high-quality EPS file for LaTeX
plt.savefig('distribution_plot.eps', format='eps', dpi=1200)  # Increase dpi for higher quality
# Saving the plot as a PNG file
plt.savefig('distribution_plot.png', dpi=1200)

# Calculating mode and average image counts
mode_count = grouped.mode().values[0]
average_count = grouped.mean()

# Print mode and average image counts
print("Mode Image Count:", mode_count)
print("Average Image Count:", average_count)
