# Airfoil Analysis Program

## Overview

This program is designed to process airfoil data from text files and generate a comprehensive analysis report in PDF format. It includes plots for Lift Coefficient (CL), Drag Coefficient (CD), and Lift-to-Drag Ratio (CL/CD) against the angle of attack for each airfoil. The program automatically sorts the airfoils by their lift coefficients and includes a table of contents for easy navigation in the report.

## Features

- Process multiple airfoil data files (.txt) in a specified directory.
- Generate plots for CL, CD, and CL/CD versus angle of attack.
- Sort airfoils by the lift coefficient at the maximum CL/CD ratio.
- Extract airfoil names directly from the file contents.
- Compile a professional PDF report with a title page and table of contents.

## Installation

No installation is necessary for the script itself, but ensure that Python is installed on your system. Additionally, the script requires `pandas` and `matplotlib` libraries. You can install these dependencies using the following command:

```bash
pip install pandas matplotlib
```

## Usage

1. Place all your airfoil data files (.txt format) in a single directory.
2. Open the script in a text editor and modify the `directory_path` variable to point to your directory containing the airfoil data files.
3. Modify the `pdf_path` variable to set the desired output path for your PDF report.
4. Run the script using Python:

   ```bash
   python airfoil_analysis.py
   ```

## Input File Format

Each input file should contain airfoil data in a text format with specific aerodynamic parameters like alpha, CL, CD, etc., as produced by tools like XFOIL.

## Output

The output is a PDF report titled "Airfoil Analysis Report." The report includes:

- Title Page
- Table of Contents
- Individual pages for each airfoil, sorted by increasing CL, with plots and annotations.
