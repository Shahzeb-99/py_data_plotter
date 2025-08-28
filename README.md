# Spectral Data Analysis Tool

A comprehensive Python tool for analyzing spectral data with features including data validation, intensity normalization, FWHM calculation, peak identification, and professional visualization. This project has been significantly improved with object-oriented design, robust error handling, command-line interface, and extensive documentation.

## Features

- **Robust Data Loading**: Supports various delimiters and decimal formats with comprehensive validation
- **Advanced Analysis**: Calculate FWHM, peak wavelength, and spectral characteristics
- **Professional Visualization**: Generate publication-quality plots with annotations
- **Command-Line Interface**: Easy-to-use CLI with multiple options and help
- **Error Handling**: Comprehensive error checking and user-friendly messages
- **Sample Data Generation**: Built-in capability to create test data
- **Flexible Configuration**: Customizable parameters for different data formats

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Data Format](#data-format)
- [Command-Line Options](#command-line-options)
- [API Documentation](#api-documentation)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Shahzeb-99/py_data_plotter.git
cd py_data_plotter
```

2. **Install required packages:**
   Make sure you have Python 3.6 or later installed. Install the required Python packages using pip:
```bash
pip install pandas matplotlib scikit-learn numpy
```

## Quick Start

The fastest way to get started is to generate sample data and run the analysis:

```bash
# Generate sample data and analyze it
python spectral_analysis.py --create-sample

# Analyze your own data file
python spectral_analysis.py your_data_file.txt

# Get help
python spectral_analysis.py --help
```

## Usage

### Basic Usage

```bash
# Analyze a data file (creates plot automatically)
python spectral_analysis.py data.txt

# Analyze without generating plot
python spectral_analysis.py data.txt --no-plot

# Generate sample data for testing
python spectral_analysis.py --create-sample
```

### Advanced Usage

```bash
# Custom delimiter and decimal separator
python spectral_analysis.py data.csv --delimiter "," --decimal "."

# Display plot on screen instead of just saving
python spectral_analysis.py data.txt --show-plot

# Combine sample generation with analysis
python spectral_analysis.py --create-sample --show-plot
```

## Data Format

The tool expects tab-delimited data files with two columns:
- **First column:** Wavelength values (in nanometers)
- **Second column:** Intensity values

### Default Format
- **Delimiter:** Tab character (`\t`)
- **Decimal separator:** Comma (`,`) - European format
- **Header:** No header row expected

### Example Data File
```
400,0	0,12
410,0	0,23
420,0	0,45
430,0	0,67
440,0	0,78
450,0	0,89
460,0	1,00
470,0	0,95
480,0	0,88
```

### Alternative Formats
You can specify different delimiters and decimal separators:
```bash
# For comma-separated values with period as decimal
python spectral_analysis.py data.csv --delimiter "," --decimal "."

# For space-separated values
python spectral_analysis.py data.txt --delimiter " " --decimal "."
```

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `file_path` | Path to the spectral data file | Required (unless `--create-sample`) |
| `--delimiter` | Column delimiter character | `\t` (tab) |
| `--decimal` | Decimal separator character | `,` (comma) |
| `--no-plot` | Skip plot generation | False |
| `--show-plot` | Display plot on screen | False |
| `--create-sample` | Generate sample data file | False |
| `--help` | Show help message | - |

## API Documentation

### SpectralAnalyzer Class

The main class for spectral data analysis.

#### Constructor
```python
SpectralAnalyzer(delimiter='\t', decimal=',')
```

**Parameters:**
- `delimiter` (str): Column delimiter in data file
- `decimal` (str): Decimal separator in data file

#### Methods

##### `load_data(file_path: str) -> bool`
Load spectral data from a file with validation.

**Parameters:**
- `file_path` (str): Path to the data file

**Returns:**
- `bool`: True if successful, False otherwise

**Raises:**
- `FileNotFoundError`: File doesn't exist
- `ValueError`: Invalid data format

##### `normalize_intensity() -> None`
Normalize intensity values to [0, 1] range using Min-Max scaling.

##### `calculate_fwhm() -> Tuple[float, np.ndarray]`
Calculate Full Width at Half Maximum.

**Returns:**
- `Tuple[float, np.ndarray]`: FWHM value and half-maximum indices

##### `find_peak_wavelength() -> float`
Find wavelength at maximum intensity.

**Returns:**
- `float`: Peak wavelength in nm

##### `plot_spectrum(file_path: str, show_annotations: bool = True, save_plot: bool = True, show_plot: bool = False) -> str`
Generate comprehensive spectral plot.

**Parameters:**
- `file_path` (str): Original data file path
- `show_annotations` (bool): Include FWHM and peak annotations
- `save_plot` (bool): Save plot to file
- `show_plot` (bool): Display plot on screen

**Returns:**
- `str`: Path to saved plot file

##### `analyze(file_path: str) -> dict`
Perform complete spectral analysis.

**Parameters:**
- `file_path` (str): Path to data file

**Returns:**
- `dict`: Analysis results with all calculated parameters

## Examples

### Example 1: Basic Analysis
```python
from spectral_analysis import SpectralAnalyzer

# Initialize analyzer
analyzer = SpectralAnalyzer()

# Perform complete analysis
results = analyzer.analyze('my_spectrum.txt')

# Check if analysis was successful
if results['analysis_successful']:
    print(f"Peak wavelength: {results['peak_wavelength']:.1f} nm")
    print(f"FWHM: {results['fwhm']:.1f} nm")
```

### Example 2: Custom Configuration
```python
# For CSV files with different format
analyzer = SpectralAnalyzer(delimiter=',', decimal='.')
results = analyzer.analyze('spectrum.csv')
```

### Example 3: Plotting Only
```python
analyzer = SpectralAnalyzer()
analyzer.load_data('spectrum.txt')
analyzer.normalize_intensity()

# Create plot without annotations
plot_file = analyzer.plot_spectrum('spectrum.txt', show_annotations=False)
```

### Example 4: Step-by-step Analysis
```python
analyzer = SpectralAnalyzer()

# Load and validate data
if analyzer.load_data('spectrum.txt'):
    # Normalize intensities
    analyzer.normalize_intensity()
    
    # Calculate individual parameters
    peak_wl = analyzer.find_peak_wavelength()
    fwhm, indices = analyzer.calculate_fwhm()
    
    print(f"Peak: {peak_wl:.1f} nm, FWHM: {fwhm:.1f} nm")
    
    # Generate plot
    analyzer.plot_spectrum('spectrum.txt', show_plot=True)
```

## Troubleshooting

### Common Issues

#### 1. File Not Found Error
```
FileNotFoundError: [Errno 2] No such file or directory: 'data.txt'
```
**Solution:** Ensure the file path is correct and the file exists.

#### 2. Invalid Data Format
```
ValueError: Data file must contain at least 2 columns
```
**Solution:** Check that your data file has at least two columns (wavelength and intensity).

#### 3. Decimal Separator Issues
```
ValueError: Intensity data must be numeric
```
**Solution:** Check the decimal separator. Use `--decimal "."` for periods or `--decimal ","` for commas.

#### 4. FWHM Calculation Error
```
ValueError: Cannot calculate FWHM: insufficient data points above half maximum
```
**Solution:** This occurs with very narrow peaks or noisy data. Try:
- Increasing data resolution
- Smoothing the data
- Checking for data quality issues

#### 5. Plot Display Issues
If plots don't display properly:
- Use `--show-plot` flag to display on screen
- Check that matplotlib backend supports display
- Plots are always saved to files regardless of display issues

### Data Quality Guidelines

1. **Minimum Requirements:**
   - At least 10 data points
   - Two numeric columns
   - Monotonic wavelength values (preferred)

2. **Recommended:**
   - 50+ data points for accurate FWHM
   - Sufficient baseline points around the peak
   - Regular wavelength spacing

3. **Data Validation:**
   The tool automatically validates:
   - File existence
   - Column count
   - Numeric data types
   - Non-empty datasets

### Performance Notes

- Processing time scales linearly with data size
- Memory usage is minimal for typical spectral datasets (< 10MB)
- Plot generation may take 1-2 seconds for large datasets

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Style

The code follows Python PEP 8 style guidelines with comprehensive docstrings and type hints.

---

**Author:** Shahzeb-99  
**Repository:** https://github.com/Shahzeb-99/py_data_plotter  
**License:** MIT (if applicable)

