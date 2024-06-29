# Spectral Data Analysis

This project involves analyzing spectral data from a file, normalizing the intensity values, plotting the normalized intensity against the wavelength, and calculating key characteristics of the spectrum such as the Full Width at Half Maximum (FWHM) and the wavelength at maximum emission. The analysis is done using Python, leveraging libraries such as Pandas, NumPy, and Matplotlib.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Data Description](#data-description)
- [Code Explanation](#code-explanation)
- [Results](#results)

## Installation

1. **Clone the repository:**
```bash
   git clone https://github.com/Shahzeb-99/py_data_plotter.git
   cd py_data_plotter
```

2. **Install required packages:**
   Make sure you have Python installed (preferably Python 3.6 or later). Install the required Python packages using pip:
```bash
   pip install pandas matplotlib scikit-learn numpy
```

## Usage

1. **Place your data file:**
   Ensure the data file you want to analyze has the same name as specified in the script's file_path variable.
   
3. **Run the script:**
```bash
   python spectral_analysis.py
```

3. **Output:**
   The script will read the data, perform the analysis, and generate a plot saved as `3_6_3_normalized_scatter.png`. It will also print key characteristics of the spectrum in the console.

## Data Description

The data file is expected to contain two columns:
- **First column:** Wavelength values (in nanometers).
- **Second column:** Intensity values (decimal numbers, using comma as the decimal separator).

The file should be tab-delimited.

## Code Explanation

1. **Reading the Data:**
   The data is read into a Pandas DataFrame using `pd.read_csv`, with the tab character as the delimiter and a comma as the decimal separator.
```python
   data = pd.read_csv(file_path, delimiter='\t', header=None, decimal=',')
```

2. **Extracting and Normalizing Data:**
   The wavelength and intensity values are extracted from the DataFrame. The intensity values are normalized to the range [0, 1] using `MinMaxScaler`.
```python
   wavelength = data.iloc[:, 0]
   intensity = data.iloc[:, 1]
   scaler = MinMaxScaler(feature_range=(0, 1))
   normalized_intensity = scaler.fit_transform(intensity.values.reshape(-1, 1)).flatten()
```

3. **Plotting the Data:**
   A scatter plot of the normalized intensity against the wavelength is created using Matplotlib.
```python
   plt.scatter(wavelength, normalized_intensity, color='b', marker='o')
```

4. **Calculating FWHM:**
   The Full Width at Half Maximum (FWHM) is calculated by finding the wavelength values where the normalized intensity crosses half of its maximum value.
```python
   half_max = max(normalized_intensity) / 2.0
   greater_than_half_max = normalized_intensity > half_max
   half_max_indices = np.where(greater_than_half_max[:-1] & ~greater_than_half_max[1:])[0]
   fwhm = wavelength.iloc[half_max_indices[-1]] - wavelength.iloc[half_max_indices[0]]
```

5. **Finding Maximum Emission Wavelength:**
   The wavelength corresponding to the maximum intensity is identified.
```python
   lambda_max = wavelength.iloc[intensity.idxmax()]
```

## Results

Running the script will produce a plot showing the normalized intensity versus wavelength. Key characteristics of the spectrum, such as the FWHM and the wavelength at maximum emission, will be printed to the console and annotated on the plot.

