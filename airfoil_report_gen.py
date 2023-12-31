import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def extract_airfoil_name(file_path):
    with open(file_path, "r") as file:
        for i in range(5):
            line = file.readline()
            if "Calculated polar for" in line:
                return line.split(":")[-1].strip()
    return "Unknown Airfoil"


def extract_reynolds_number(file_path):
    with open(file_path, "r") as file:
        for line in file:
            if "Re =" in line:
                parts = line.split("Re =")[1].split()
                re_number = (
                    parts[0] + "E" + parts[2]
                )  # Combine the number and exponent parts
                return float(re_number)
    return "Unknown Reynolds Number"


def plot_airfoil_data(file_path, pdf, page_number):
    airfoil_name = extract_airfoil_name(file_path)
    reynolds_number = extract_reynolds_number(file_path)

    # Read the data from the file
    column_names = ["alpha", "CL", "CD", "CDp", "CM", "Top_Xtr", "Bot_Xtr"]
    data = pd.read_csv(file_path, sep="\s+", skiprows=13, names=column_names)

    # Find the alpha value for maximum CL/CD ratio
    max_cl_cd_index = (data["CL"] / data["CD"]).idxmax()
    max_cl_cd_alpha = data.at[max_cl_cd_index, "alpha"]
    max_cl_cd = data["CL"][max_cl_cd_index] / data["CD"][max_cl_cd_index]
    max_cl = data["CL"][max_cl_cd_index]
    max_cd = data["CD"][max_cl_cd_index]

    # Create plots
    fig, axes = plt.subplots(3, 1, figsize=(8, 11))
    plt.suptitle(
        f"{airfoil_name}, Re = {reynolds_number:.3e}",
        fontsize=16,
        fontweight="bold",
    )

    # Plot CL vs alpha
    axes[0].plot(data["alpha"], data["CL"], label="CL", color="blue")
    axes[0].axvline(max_cl_cd_alpha, color="grey", linestyle="--")
    axes[0].axhline(max_cl, color="grey", linestyle="--")
    axes[0].text(
        max_cl_cd_alpha,
        0,
        f"alpha = {max_cl_cd_alpha:.2f}",
        verticalalignment="bottom",
        horizontalalignment="right",
    )
    axes[0].text(0, max_cl, f"CL = {max_cl:.4f}", verticalalignment="bottom")
    axes[0].set_xlabel("Angle of Attack (alpha)")
    axes[0].set_ylabel("Lift Coefficient (CL)")
    axes[0].set_title(
        f"Lift Coefficient (CL) vs Angle of Attack ({os.path.basename(file_path)})"
    )
    axes[0].grid(True)

    # Plot CD vs alpha
    axes[1].plot(data["alpha"], data["CD"], label="CD", color="green")
    axes[1].axvline(max_cl_cd_alpha, color="grey", linestyle="--")
    axes[1].axhline(max_cd, color="grey", linestyle="--")
    axes[1].text(
        max_cl_cd_alpha,
        0,
        f"alpha = {max_cl_cd_alpha:.2f}",
        verticalalignment="bottom",
        horizontalalignment="right",
    )
    axes[1].text(0, max_cd, f"CD = {max_cd:.4f}", verticalalignment="bottom")
    axes[1].set_xlabel("Angle of Attack (alpha)")
    axes[1].set_ylabel("Drag Coefficient (CD)")
    axes[1].set_title(
        f"Drag Coefficient (CD) vs Angle of Attack ({os.path.basename(file_path)})"
    )
    axes[1].grid(True)

    # Plot CL/CD vs alpha
    axes[2].plot(
        data["alpha"], data["CL"] / data["CD"], label="CL/CD", color="red"
    )
    axes[2].axvline(max_cl_cd_alpha, color="grey", linestyle="--")
    axes[2].axhline(max_cl_cd, color="grey", linestyle="--")
    axes[2].text(
        max_cl_cd_alpha,
        0,
        f"alpha = {max_cl_cd_alpha:.2f}",
        verticalalignment="bottom",
        horizontalalignment="right",
    )
    axes[2].text(
        0,
        max_cl_cd,
        f"Max CL/CD = {max_cl_cd:.4f}",
        verticalalignment="bottom",
    )
    axes[2].set_xlabel("Angle of Attack (alpha)")
    axes[2].set_ylabel("Lift-to-Drag Ratio (CL/CD)")
    axes[2].set_title(
        f"Lift-to-Drag Ratio (CL/CD) vs Angle of Attack ({os.path.basename(file_path)})"
    )
    axes[2].grid(True)

    # Add annotations for CL, CD, CL/CD at the bottom of the page
    plt.figtext(
        0.5,
        0.02,
        f"At alpha = {max_cl_cd_alpha:.2f}: CL = {max_cl:.4f}, CD = {max_cd:.4f}, Max CL/CD = {max_cl_cd:.4f}",
        ha="center",
        fontsize=10,
        bbox={"facecolor": "orange", "alpha": 0.5, "pad": 5},
    )

    # Add page number at the bottom right of the page
    plt.figtext(
        0.95,
        0.02,
        f"Page {page_number}",
        ha="right",
        fontsize=10,
    )

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    pdf.savefig(fig)  # Save the current figure to PDF
    plt.close()


def process_directory_to_pdf(directory_path, pdf_path):
    # Collect file paths, airfoil names, and corresponding max CL values
    airfoils_info = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            airfoil_name = extract_airfoil_name(file_path)
            column_names = [
                "alpha",
                "CL",
                "CD",
                "CDp",
                "CM",
                "Top_Xtr",
                "Bot_Xtr",
            ]
            data = pd.read_csv(
                file_path, sep="\s+", skiprows=13, names=column_names
            )
            max_cl_cd_index = (data["CL"] / data["CD"]).idxmax()
            max_cl = data["CL"][max_cl_cd_index]
            airfoils_info.append((file_path, airfoil_name, max_cl))

    # Sort airfoils by increasing CL value
    airfoils_info.sort(key=lambda x: x[2])

    with PdfPages(pdf_path) as pdf:
        # Create a title page
        title_page = plt.figure(figsize=(8, 11))
        title_page.clf()
        title_page.text(
            0.5,
            0.5,
            "Airfoil Analysis Report",
            ha="center",
            va="center",
            fontsize=20,
            fontweight="bold",
        )
        pdf.savefig(title_page)
        plt.close()

        # Create a table of contents page
        toc_page = plt.figure(figsize=(8, 11))
        toc_page.clf()
        toc_page.text(
            0.5,
            0.9,
            "Table of Contents",
            ha="center",
            va="center",
            fontsize=16,
            fontweight="bold",
        )
        for i, (_, airfoil_name, max_cl) in enumerate(airfoils_info, start=1):
            toc_page.text(
                0.1,
                0.8 - 0.05 * i,
                f"{i}. {airfoil_name}, CL at Max CL/CD: {max_cl:.4f}",
                ha="left",
                va="top",
                fontsize=12,
            )
            toc_page.text(
                0.9,
                0.8 - 0.05 * i,
                f"Page {i}",
                ha="right",
                va="top",
                fontsize=12,
            )
        pdf.savefig(toc_page)
        plt.close()

        # Process each file and add plots to the PDF
        for i, (file_path, _, _) in enumerate(airfoils_info):
            plot_airfoil_data(
                file_path, pdf, i + 1
            )  # Start page numbering from 3 because of title and TOC pages


# Replace with the path to your directory and desired PDF output path
directory_path = "airfoil-data"
pdf_path = "airfoil_analysis_report.pdf"
process_directory_to_pdf(directory_path, pdf_path)
