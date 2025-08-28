#!/usr/bin/env python3
"""
Example usage of the SpectralAnalyzer class.

This script demonstrates various ways to use the spectral analysis tool
programmatically rather than through the command line interface.
"""

from spectral_analysis import SpectralAnalyzer, create_sample_data
import os


def example_basic_analysis():
    """Example 1: Basic analysis workflow."""
    print("="*50)
    print("EXAMPLE 1: Basic Analysis Workflow")
    print("="*50)
    
    # Create sample data
    sample_file = create_sample_data("example1_data.txt")
    
    # Initialize analyzer with default settings
    analyzer = SpectralAnalyzer()
    
    # Perform complete analysis
    results = analyzer.analyze(sample_file)
    
    # Generate plot
    if results['analysis_successful']:
        plot_file = analyzer.plot_spectrum(sample_file, save_plot=True)
        print(f"\nPlot saved as: {plot_file}")
    
    # Clean up
    if os.path.exists(sample_file):
        os.remove(sample_file)


def example_custom_format():
    """Example 2: Custom data format handling."""
    print("\n" + "="*50)
    print("EXAMPLE 2: Custom Data Format")
    print("="*50)
    
    # Create CSV-style data with period decimal separator
    import numpy as np
    wavelengths = np.linspace(450, 650, 41)
    intensities = np.exp(-0.5 * ((wavelengths - 550) / 25) ** 2)
    
    csv_file = "example2_data.csv"
    with open(csv_file, 'w') as f:
        f.write("wavelength,intensity\n")  # Add header
        for w, i in zip(wavelengths, intensities):
            f.write(f"{w:.1f},{i:.4f}\n")
    
    # Analyze with custom format
    analyzer = SpectralAnalyzer(delimiter=',', decimal='.')
    
    # Load data and skip header
    import pandas as pd
    data = pd.read_csv(csv_file, delimiter=',', decimal='.', header=0)
    
    # Manually set data (bypassing load_data for this example)
    analyzer.wavelength = data.iloc[:, 0]
    analyzer.intensity = data.iloc[:, 1]
    
    # Continue with analysis
    analyzer.normalize_intensity()
    peak_wl = analyzer.find_peak_wavelength()
    fwhm, indices = analyzer.calculate_fwhm()
    
    print(f"Peak wavelength: {peak_wl:.1f} nm")
    print(f"FWHM: {fwhm:.1f} nm")
    
    # Generate plot
    plot_file = analyzer.plot_spectrum(csv_file, save_plot=True)
    print(f"Plot saved as: {plot_file}")
    
    # Clean up
    if os.path.exists(csv_file):
        os.remove(csv_file)


def example_step_by_step():
    """Example 3: Step-by-step analysis with error handling."""
    print("\n" + "="*50)
    print("EXAMPLE 3: Step-by-Step Analysis")
    print("="*50)
    
    # Create sample data
    sample_file = create_sample_data("example3_data.txt")
    
    # Initialize analyzer
    analyzer = SpectralAnalyzer()
    
    try:
        # Step 1: Load data
        print("Step 1: Loading data...")
        if not analyzer.load_data(sample_file):
            raise Exception("Failed to load data")
        
        # Step 2: Normalize intensity
        print("Step 2: Normalizing intensity...")
        analyzer.normalize_intensity()
        
        # Step 3: Calculate peak wavelength
        print("Step 3: Finding peak wavelength...")
        peak_wl = analyzer.find_peak_wavelength()
        print(f"  Peak wavelength: {peak_wl:.2f} nm")
        
        # Step 4: Calculate FWHM
        print("Step 4: Calculating FWHM...")
        fwhm, half_max_indices = analyzer.calculate_fwhm()
        print(f"  FWHM: {fwhm:.2f} nm")
        print(f"  Half-max indices: {half_max_indices}")
        
        # Step 5: Generate customized plot
        print("Step 5: Generating plot...")
        plot_file = analyzer.plot_spectrum(
            sample_file, 
            show_annotations=True,
            save_plot=True,
            show_plot=False
        )
        print(f"  Plot saved as: {plot_file}")
        
        print("\nAnalysis completed successfully!")
        
    except Exception as e:
        print(f"Analysis failed: {str(e)}")
    
    finally:
        # Clean up
        if os.path.exists(sample_file):
            os.remove(sample_file)


def example_batch_analysis():
    """Example 4: Batch analysis of multiple files."""
    print("\n" + "="*50)
    print("EXAMPLE 4: Batch Analysis")
    print("="*50)
    
    # Create multiple sample files with different characteristics
    import numpy as np
    
    file_configs = [
        {"name": "narrow_peak.txt", "center": 500, "width": 15},
        {"name": "broad_peak.txt", "center": 600, "width": 40},
        {"name": "double_peak.txt", "center": 550, "width": 20}
    ]
    
    results_summary = []
    
    for config in file_configs:
        # Generate data
        wavelengths = np.linspace(400, 700, 61)
        if "double" in config["name"]:
            # Create double peak
            intensities = (np.exp(-0.5 * ((wavelengths - config["center"]) / config["width"]) ** 2) +
                          0.7 * np.exp(-0.5 * ((wavelengths - (config["center"] + 30)) / config["width"]) ** 2))
        else:
            # Single peak
            intensities = np.exp(-0.5 * ((wavelengths - config["center"]) / config["width"]) ** 2)
        
        # Save data
        with open(config["name"], 'w') as f:
            for w, i in zip(wavelengths, intensities):
                f.write(f"{w:.1f}\t{i:.3f}\n".replace('.', ','))
        
        # Analyze
        analyzer = SpectralAnalyzer()
        results = analyzer.analyze(config["name"])
        
        if results['analysis_successful']:
            results_summary.append({
                "file": config["name"],
                "peak_wl": results['peak_wavelength'],
                "fwhm": results['fwhm'],
                "peak_intensity": results['peak_intensity']
            })
            
            # Generate plot
            analyzer.plot_spectrum(config["name"], save_plot=True)
    
    # Print summary
    print("\nBatch Analysis Summary:")
    print("-" * 60)
    for result in results_summary:
        print(f"{result['file']:<20} Peak: {result['peak_wl']:6.1f} nm  "
              f"FWHM: {result['fwhm']:5.1f} nm  "
              f"Intensity: {result['peak_intensity']:5.3f}")
    
    # Clean up
    for config in file_configs:
        if os.path.exists(config["name"]):
            os.remove(config["name"])


if __name__ == "__main__":
    print("Spectral Analysis Tool - Usage Examples")
    print("======================================")
    
    # Run all examples
    example_basic_analysis()
    example_custom_format()
    example_step_by_step()
    example_batch_analysis()
    
    print("\n" + "="*50)
    print("All examples completed!")
    print("Check the generated plot files for visualization results.")
    print("="*50)