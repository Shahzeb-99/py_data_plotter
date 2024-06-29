import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Specify the path to your data file
file_path = '3_6_3'

# Read the data into a DataFrame
data = pd.read_csv(file_path, delimiter='\t', header=None, decimal=',')

# Extract wavelength and intensity
wavelength = data.iloc[:, 0]
intensity = data.iloc[:, 1]

# Normalize intensity to the range [0, 1]
scaler = MinMaxScaler(feature_range=(0, 1))
normalized_intensity = scaler.fit_transform(intensity.values.reshape(-1, 1)).flatten()

# Create the scatter plot
plt.figure(figsize=(15, 6))
plt.scatter(wavelength, normalized_intensity, color='b', marker='o')

# Find FWHM (Full Width at Half Maximum)
half_max = max(normalized_intensity) / 2.0
greater_than_half_max = normalized_intensity > half_max
half_max_indices = np.where(greater_than_half_max[:-1] & ~greater_than_half_max[1:])[0]
fwhm = wavelength.iloc[half_max_indices[-1]] - wavelength.iloc[half_max_indices[0]]

# Find wavelength at maximum emission
lambda_max = wavelength.iloc[intensity.idxmax()]

# Print values used for FWHM calculation
print("Values used for FWHM calculation:")
print(f"Maximum intensity (I_max): {max(normalized_intensity):.2f}")
print(f"Half-maximum intensity (I_half_max): {half_max:.2f}")
print(f"Wavelengths at half-maximum intensity: {wavelength.iloc[half_max_indices[0]]} nm and {wavelength.iloc[half_max_indices[-1]]} nm")

# Add labels and title with units and scaling factors
plt.title('Normalized Intensity vs Wavelength')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Normalized Intensity')

# Display FWHM and wavelength at maximum emission
# plt.text(0.05, 0.9, f'FWHM: {fwhm:.2f} nm', transform=plt.gca().transAxes, fontsize=12)
# plt.text(0.05, 0.85, f'λ at Max Intensity: {lambda_max:.2f} nm', transform=plt.gca().transAxes, fontsize=12)

# Customize ticks and grid
plt.tick_params(axis='both', which='major', labelsize=12)
plt.grid(True, linestyle='--', linewidth=0.5)

# Save the plot to a file with file_path as the base name
output_file = f'{file_path}_normalized_scatter.png'  # Constructing the output filename
plt.savefig(output_file, dpi=300)  # Save as PNG with 300 DPI (adjust as needed)

# Show the plot
plt.tight_layout()
plt.show()

# Describe the characteristics of the spectrum
print("\nCharacteristics of the Spectrum:")
print("- The spectrum peaks at wavelength λ = {:.2f} nm.".format(lambda_max))
print("- The FWHM of the spectrum is {:.2f} nm, indicating its spectral width.".format(fwhm))
print("- The spectrum shows variations in intensity across different wavelengths.")
