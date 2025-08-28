#!/usr/bin/env python3
"""
Spectral Data Analysis Tool

This module provides functionality for analyzing spectral data including:
- Data loading and validation
- Intensity normalization 
- FWHM (Full Width at Half Maximum) calculation
- Peak wavelength identification
- Data visualization and export

Author: Shahzeb-99
Repository: https://github.com/Shahzeb-99/py_data_plotter
"""

import argparse
import os
import sys
from typing import Tuple, Optional
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np


class SpectralAnalyzer:
    """
    A comprehensive tool for spectral data analysis.
    
    This class provides methods for loading, processing, and analyzing spectral data,
    including calculation of key spectral characteristics like FWHM and peak wavelength.
    """
    
    def __init__(self, delimiter: str = '\t', decimal: str = ','):
        """
        Initialize the SpectralAnalyzer.
        
        Args:
            delimiter (str): Column delimiter in the data file. Default is '\t' (tab).
            decimal (str): Decimal separator in the data file. Default is ',' (comma).
        """
        self.delimiter = delimiter
        self.decimal = decimal
        self.wavelength = None
        self.intensity = None
        self.normalized_intensity = None
        self.scaler = MinMaxScaler(feature_range=(0, 1))
    
    def load_data(self, file_path: str) -> bool:
        """
        Load spectral data from a file.
        
        Args:
            file_path (str): Path to the data file.
            
        Returns:
            bool: True if data loaded successfully, False otherwise.
            
        Raises:
            FileNotFoundError: If the specified file doesn't exist.
            pd.errors.EmptyDataError: If the file is empty.
            ValueError: If the data format is invalid.
        """
        try:
            # Validate file existence
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Data file not found: {file_path}")
            
            # Load data
            data = pd.read_csv(file_path, delimiter=self.delimiter, 
                             header=None, decimal=self.decimal)
            
            # Validate data format
            if data.shape[1] < 2:
                raise ValueError("Data file must contain at least 2 columns (wavelength and intensity)")
            
            if data.empty:
                raise ValueError("Data file is empty")
            
            # Extract wavelength and intensity
            self.wavelength = data.iloc[:, 0]
            self.intensity = data.iloc[:, 1]
            
            # Validate data types and values
            if not pd.api.types.is_numeric_dtype(self.wavelength):
                raise ValueError("Wavelength data must be numeric")
            
            if not pd.api.types.is_numeric_dtype(self.intensity):
                raise ValueError("Intensity data must be numeric")
            
            if len(self.wavelength) != len(self.intensity):
                raise ValueError("Wavelength and intensity arrays must have the same length")
            
            print(f"Successfully loaded {len(self.wavelength)} data points from {file_path}")
            return True
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return False
    
    def normalize_intensity(self) -> None:
        """
        Normalize intensity values to the range [0, 1] using Min-Max scaling.
        
        Raises:
            ValueError: If no data has been loaded.
        """
        if self.intensity is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        # Normalize intensity to [0, 1] range
        self.normalized_intensity = self.scaler.fit_transform(
            self.intensity.values.reshape(-1, 1)
        ).flatten()
        
        print(f"Intensity normalized to range [{self.normalized_intensity.min():.3f}, {self.normalized_intensity.max():.3f}]")
    
    def calculate_fwhm(self) -> Tuple[float, np.ndarray]:
        """
        Calculate the Full Width at Half Maximum (FWHM) of the spectrum.
        
        Returns:
            Tuple[float, np.ndarray]: FWHM value and indices of half-maximum points.
            
        Raises:
            ValueError: If no normalized data is available or FWHM cannot be calculated.
        """
        if self.normalized_intensity is None:
            raise ValueError("No normalized data available. Call normalize_intensity() first.")
        
        # Calculate half maximum value
        max_intensity = np.max(self.normalized_intensity)
        half_max = max_intensity / 2.0
        
        # Find points above half maximum
        above_half_max = self.normalized_intensity > half_max
        
        # Find crossing points (transitions from above to below half-max)
        # This identifies the edges of the peak
        crossing_points = np.where(above_half_max[:-1] & ~above_half_max[1:])[0]
        
        if len(crossing_points) < 2:
            # Try alternative method: find first and last points above half-max
            indices_above_half = np.where(above_half_max)[0]
            if len(indices_above_half) < 2:
                raise ValueError("Cannot calculate FWHM: insufficient data points above half maximum")
            crossing_points = np.array([indices_above_half[0], indices_above_half[-1]])
        
        # Calculate FWHM as the difference between the outermost crossing points
        fwhm = self.wavelength.iloc[crossing_points[-1]] - self.wavelength.iloc[crossing_points[0]]
        
        return fwhm, crossing_points
    
    def find_peak_wavelength(self) -> float:
        """
        Find the wavelength at maximum intensity.
        
        Returns:
            float: Wavelength at maximum intensity.
            
        Raises:
            ValueError: If no intensity data is available.
        """
        if self.intensity is None:
            raise ValueError("No intensity data available. Call load_data() first.")
        
        # Find wavelength at maximum intensity
        max_intensity_index = self.intensity.idxmax()
        peak_wavelength = self.wavelength.iloc[max_intensity_index]
        
        return peak_wavelength
    
    def plot_spectrum(self, file_path: str, show_annotations: bool = True, 
                     save_plot: bool = True, show_plot: bool = False) -> str:
        """
        Create a comprehensive plot of the spectral data.
        
        Args:
            file_path (str): Original data file path (used for output filename).
            show_annotations (bool): Whether to show FWHM and peak annotations.
            save_plot (bool): Whether to save the plot to file.
            show_plot (bool): Whether to display the plot.
            
        Returns:
            str: Path to the saved plot file.
            
        Raises:
            ValueError: If no data is available for plotting.
        """
        if self.wavelength is None or self.normalized_intensity is None:
            raise ValueError("No data available for plotting. Load and normalize data first.")
        
        # Create the plot
        plt.figure(figsize=(15, 8))
        plt.scatter(self.wavelength, self.normalized_intensity, 
                   color='blue', marker='o', s=30, alpha=0.7, label='Spectral Data')
        
        # Add peak and FWHM annotations if requested
        if show_annotations:
            try:
                # Calculate and display key characteristics
                fwhm, half_max_indices = self.calculate_fwhm()
                peak_wavelength = self.find_peak_wavelength()
                
                # Mark peak wavelength
                peak_intensity = self.normalized_intensity[self.intensity.idxmax()]
                plt.axvline(x=peak_wavelength, color='red', linestyle='--', alpha=0.7, 
                           label=f'Peak: {peak_wavelength:.1f} nm')
                plt.plot(peak_wavelength, peak_intensity, 'ro', markersize=8)
                
                # Mark FWHM points
                half_max_value = np.max(self.normalized_intensity) / 2.0
                plt.axhline(y=half_max_value, color='green', linestyle=':', alpha=0.7, 
                           label=f'Half Maximum: {half_max_value:.2f}')
                
                # Add text annotations
                plt.text(0.02, 0.95, f'Peak Wavelength: {peak_wavelength:.1f} nm', 
                        transform=plt.gca().transAxes, fontsize=12, 
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
                plt.text(0.02, 0.88, f'FWHM: {fwhm:.1f} nm', 
                        transform=plt.gca().transAxes, fontsize=12,
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
                
            except Exception as e:
                print(f"Warning: Could not add annotations: {str(e)}")
        
        # Customize plot appearance
        plt.title('Spectral Data Analysis: Normalized Intensity vs Wavelength', fontsize=16, fontweight='bold')
        plt.xlabel('Wavelength (nm)', fontsize=14)
        plt.ylabel('Normalized Intensity', fontsize=14)
        plt.tick_params(axis='both', which='major', labelsize=12)
        plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
        plt.legend(fontsize=12)
        
        # Improve layout
        plt.tight_layout()
        
        # Save the plot
        output_file = None
        if save_plot:
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_file = f'{base_name}_spectral_analysis.png'
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"Plot saved as: {output_file}")
        
        # Show the plot if requested
        if show_plot:
            plt.show()
        else:
            plt.close()
        
        return output_file
    
    def analyze(self, file_path: str) -> dict:
        """
        Perform complete spectral analysis.
        
        Args:
            file_path (str): Path to the data file.
            
        Returns:
            dict: Analysis results including FWHM, peak wavelength, and statistics.
        """
        results = {}
        
        try:
            # Load and process data
            if not self.load_data(file_path):
                return {"error": "Failed to load data"}
            
            self.normalize_intensity()
            
            # Calculate key characteristics
            peak_wavelength = self.find_peak_wavelength()
            fwhm, half_max_indices = self.calculate_fwhm()
            
            # Compile results
            results = {
                "file_path": file_path,
                "data_points": len(self.wavelength),
                "wavelength_range": {
                    "min": float(self.wavelength.min()),
                    "max": float(self.wavelength.max())
                },
                "intensity_range": {
                    "min": float(self.intensity.min()),
                    "max": float(self.intensity.max())
                },
                "peak_wavelength": float(peak_wavelength),
                "peak_intensity": float(self.intensity.max()),
                "fwhm": float(fwhm),
                "half_max_value": float(np.max(self.normalized_intensity) / 2.0),
                "analysis_successful": True
            }
            
            # Print detailed analysis results
            self._print_analysis_results(results)
            
        except Exception as e:
            results["error"] = str(e)
            results["analysis_successful"] = False
            print(f"Analysis failed: {str(e)}")
        
        return results
    
    def _print_analysis_results(self, results: dict) -> None:
        """Print formatted analysis results."""
        print("\n" + "="*60)
        print("           SPECTRAL ANALYSIS RESULTS")
        print("="*60)
        print(f"Data file: {results['file_path']}")
        print(f"Data points: {results['data_points']}")
        print(f"Wavelength range: {results['wavelength_range']['min']:.1f} - {results['wavelength_range']['max']:.1f} nm")
        print(f"Intensity range: {results['intensity_range']['min']:.3f} - {results['intensity_range']['max']:.3f}")
        print("\nKEY CHARACTERISTICS:")
        print(f"• Peak wavelength (λ_max): {results['peak_wavelength']:.2f} nm")
        print(f"• Peak intensity: {results['peak_intensity']:.3f}")
        print(f"• FWHM: {results['fwhm']:.2f} nm")
        print(f"• Half-maximum value: {results['half_max_value']:.3f}")
        print("\nINTERPRETATION:")
        print(f"• The spectrum exhibits its maximum emission at {results['peak_wavelength']:.1f} nm")
        print(f"• The spectral width (FWHM) of {results['fwhm']:.1f} nm indicates the bandwidth of the emission")
        print(f"• This corresponds to {'narrow' if results['fwhm'] < 20 else 'broad'} spectral features")
        print("="*60)


def create_sample_data(filename: str = "sample_spectral_data.txt") -> str:
    """
    Create a sample spectral data file for testing and demonstration.
    
    Args:
        filename (str): Name of the sample data file to create.
        
    Returns:
        str: Path to the created sample file.
    """
    # Generate sample spectral data (Gaussian-like peak)
    wavelengths = np.linspace(400, 700, 61)  # 400-700 nm range
    center = 550  # Peak at 550 nm
    width = 30   # Width parameter
    
    # Generate Gaussian-like intensity profile with some noise
    intensities = np.exp(-0.5 * ((wavelengths - center) / width) ** 2)
    intensities += np.random.normal(0, 0.02, len(wavelengths))  # Add small amount of noise
    intensities = np.maximum(intensities, 0)  # Ensure non-negative
    
    # Format data with comma as decimal separator (European format)
    with open(filename, 'w') as f:
        for w, i in zip(wavelengths, intensities):
            f.write(f"{w:.1f}\t{i:.3f}\n".replace('.', ','))
    
    print(f"Sample data created: {filename}")
    return filename


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(
        description="Spectral Data Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python spectral_analysis.py data.txt
  python spectral_analysis.py data.txt --no-plot
  python spectral_analysis.py data.txt --delimiter "," --decimal "."
  python spectral_analysis.py --create-sample
        """
    )
    
    parser.add_argument('file_path', nargs='?', help='Path to the spectral data file')
    parser.add_argument('--delimiter', default='\t', help='Column delimiter (default: tab)')
    parser.add_argument('--decimal', default=',', help='Decimal separator (default: comma)')
    parser.add_argument('--no-plot', action='store_true', help='Skip plot generation')
    parser.add_argument('--show-plot', action='store_true', help='Display plot on screen')
    parser.add_argument('--create-sample', action='store_true', help='Create sample data file')
    
    args = parser.parse_args()
    
    # Create sample data if requested
    if args.create_sample:
        sample_file = create_sample_data()
        print(f"Sample data created: {sample_file}")
        if not args.file_path:
            args.file_path = sample_file
    
    # Validate input
    if not args.file_path:
        parser.error("No input file specified. Use --create-sample to generate sample data.")
    
    # Initialize analyzer
    analyzer = SpectralAnalyzer(delimiter=args.delimiter, decimal=args.decimal)
    
    # Perform analysis
    results = analyzer.analyze(args.file_path)
    
    # Generate plot if analysis was successful and plotting is enabled
    if results.get("analysis_successful", False) and not args.no_plot:
        try:
            output_file = analyzer.plot_spectrum(
                args.file_path, 
                show_plot=args.show_plot, 
                save_plot=True
            )
        except Exception as e:
            print(f"Warning: Plot generation failed: {str(e)}")
    
    return 0 if results.get("analysis_successful", False) else 1


if __name__ == "__main__":
    sys.exit(main())
