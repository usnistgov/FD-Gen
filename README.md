# Fire Data Generator (FD-Gen)  v1.0.0

**Release Name**: FD-Gen v1.0.0

**Release Date**: [Mar 6, 2025]

**Version**: 1.0.0

---


## Getting started
**Fire data generator (FD-Gen)** is a Python-based automated tool designed to streamline the creation of multiple Fire Dynamics Simulator (FDS) case input files. 

The tool is developed using the Python programming language. It generates random values for key fire parameters and integrates them directly into FDS code lines, enabling users to efficiently produce a large volume of FDS case files within specified parameter ranges. The current version of FD-Gen supports the randomization of various fire parameters, including fire source locations, vent locations, door or window opening sequences, obstruction sizes, fire heat release rate (HRR) curves, and other related parameters. The program documentation has been published as a NIST Technical Note and is available at https://doi.org/10.6028/NIST.TN.2332. A comprehensive user guide and examples demonstrating the program’s usage are provided.

The package consists of the following files:

[**executable FD-Gen**](FD-Gen.exe)

[**Python souce code**](main_code) 

[**Test case for namelist main and sample generator**](/test_cases/test_script_MAIN_MRND.txt)
(see documentation Sections 3.1 and 3.2)

[**Test case for fire source location (FSL)**](/test_cases/test_script_FSL.txt)
(see documentation Section 3.3)

[**Test case for vent position (VTP)**](/test_cases/test_script_VTP.txt)
(see documentation Section 3.4)

[**Test case for door or window open time (DWT)**](/test_cases/test_script_DWT.txt)
(see documentation Section 3.5)

[**Test case for random obstruction (RXB)**](/test_cases/test_script_RXB.txt)
(see documentation Section 3.6)

[**Test case for other parameters (OTH)**](/test_cases/test_script_OTH.txt)
(see documentation Section 3.7)

[**Test case for HRR curve (HRC)**](/test_cases/test_script_HRC.txt)
(see documentation Section 3.8)

[**FD-Gen input file for a commercial building fire case**](/example/example_commercial.fds)
(see documentation Section 5.1)

[**FD-Gen input file for a CSTB tunnel fire case**](/example/example_CSTB_Tunnel_Test_2.fds)
(see documentation Section 5.2)

[**FD-Gen input file for a single-story residential room fire case**](/example/example_Single_Story_Gas_1.fds )
(see documentation Section 5.3)

[**FD-Gen input file for a smoke alarm testing fire case**](/example/example_NIST_Smoke_Alarms_SDC02.fds)

[**FD-Gen input file for a wildland fire case**](/example/example_wind_test2.fds)



The workflow of FD-Gen is shown below. It consists of 4 main steps.

![Figure 1. FD-Gen framework.](images/Picture1.png)


## installation instructions
This project provides a GitHub repository for those interested in obtaining and testing FD-Gen. The current location of the repository is https://github.com/usnistgov/FD-Gen. The repository contains both the [**source code**](main_code) and the executable file [**FD-Gen.exe**](FD-Gen.exe). The FD-Gen executable has been tested and confirmed to work effectively on Windows 10 and 11-based personal computers with FDS version 6.9.1. For users utilizing the Python source code, the environment requirements for the dependencies are listed below. Ensure that these dependencies are installed in your Python environment before running FD-Gen:

Python	    3.11 or higher

Numpy	      1.26.4

Pandas	    2.2.3

Scipy	      1.14.1

Matplotlib	3.9.2

Openpyxl	  3.1.5


## Usage approach 
###  Step 1: write the FDS input file.
A FDS input file needs to be prepared. This file should include key components such as the basic building geometry, fire scenario definition, mesh configuration, surface and material properties, as well as device placement and monitoring information. These elements are crucial for accurately simulating fire dynamics and ensuring the proper functionality of the simulation. The setup process for this input file aligns with the standard procedure used in any fire simulation case in FDS. It is advisable to test the file in the FDS program beforehand to ensure correct configurations before proceeding with subsequent FD-Gen steps. Detailed instructions on how to download the executables, manuals, source-code and related utilities of FDS can be found on the official website of NIST FDS project at: https://pages.nist.gov/fds-smv/.


### Step 2: write the FD-Gen input file.
To prepare the FD-Gen input file.

Each data generation project in FD-Gen is controlled by code lines of text-based FD-Gen script embedded within the original FDS case input file. 
This script employs a four-letter-based naming convention for its namelist code lines to define randomized parameters and values within the FD-Gen input file. This structured approach mirrors the conventions used in FDS and Consolidated Fire and Smoke Transport (CFAST), ensuring consistency and enabling an easier transition for existing FDS users. For detailed instructions on how to write FD-Gen input files and view examples, please refer to the NIST technical note at https://doi.org/10.6028/NIST.TN.2332.

The following folder contains several examples of prepared FD-Gen input files.

[**FD-Gen Input File Examples**](example)

### Step 3: execute the program
To open a terminal and use the command to navigate to the location of the FD-Gen main program, and then read an input file using FD-Gen.
1. Open the terminal.
2. Change the current working directory to your local repository.
3. Read the input file with FD-Gen.

    ```bash
    .\FD-Gen <FD-Gen project name>.fds
    ```
      or

        python FDSdata.py <FD-Gen project name>.fds
    

4. sample the parameter value data.

Once the FD-Gen input file is executed, the program reads the FD-Gen code lines and performs basic code checking and parameter sampling. Users can review the sampled parameter values in the **PARAMETER_FILE_FOLDER** located within the project folder. If the sampling aligns with the design, you can proceed with the program in the terminal. Otherwise, you'll need to return to the FD-Gen input file to modify the script guiding the parameter sampling.


5. wrap the FDS input file.

The file wrapping process is responsible for generating the FDS case input files based on the sampled data. As a result, multiple FDS input files, as designed, will be generated and saved in the project folder under **CASE_FOLDER**.


### Step 4: acquire the outputs.
In addition to the spreadsheet containing the sampled parameter value information in the **PARAMETER_FILE_FOLDER** and the FDS input files in the **CASE_FOLDER**, FD-Gen also provides outputs to plot sampled fire source locations, HRR curves, and value distributions. These visual outputs give users a comprehensive view of the data and help ensure the reproducibility of the dataset. The output files are saved in the project folder under **OUTPUT_FOLDER**.


## Example

### Start
[**commercial building fire case**](example/example_commercial.fds)

1. download **FD-Gen.exe** and the example input file **example_commercial.fds**

2. open a terminal

3. change the current working directory to your local repository

4. read the FD-Gen input file with FD-Gen

5. check FD-Gen script and sample the data.
type Y or y to continue the following steps.

6. finish
project folder **example_commercial** will be created under the current working directory.

### Breakdown of the output files

**CASE_FOLDER**
The CASE_FOLDER contains multiple FDS case input files generated based on the sampled values designed in the input FD-Gen file configuration. 

![Figure 2. example of CASE_FOLDER.](images/Picture2.png)

**Figure 2.** example of CASE_FOLDER.

**OUTPUT_FOLDER**
The OUTPUT_FOLDER contains visualizations of the sampled data, including plots of fire source locations, HRR curves, and specific value distributions. 

![Figure 3. example of OUTPUT_FOLDER.](images/Picture3.png)

**Figure 3.** example of OUTPUT_FOLDER.

**PARAMETER_FILE_FOLDER**
The PARAMETER_FILE_FOLDER contains a spreadsheet with the sampled parameter values for each case, along with a text file providing a summary of the parameter values. 

![Figure 4. example of PARAMETER_FILE_FOLDER.](images/Picture4.png)

**Figure 4.** example of PARAMETER_FILE_FOLDER.

**SEEDS_FOLDER**
The SEEDS_FOLDER contains the seeds used for the project, ensuring reproducibility of the sampling process in the future. 

![Figure 5. example of SEEDS_FOLDER.](images/Picture5.png)

**Figure 5.** example of SEEDS_FOLDER.

## Documentation
For detailed instructions and example on using FD-Gen, please refer to the NIST technical note at [https://doi.org/10.6028/NIST.TN.2332].

## Citation
1. Fang, Hongqiang, Tam, Wai Cheong (2025), Fire Data Generator (FD-Gen) , National Institute of Standards and Technology, https://doi.org/10.18434/mds2-3688 (Accessed 2025-03-31)

2. H. Fang, W. C. Tam, (2025) Fire Data Generator (FD-Gen) v1.0.0. (National Institute of Standards and Technology, Gaithersburg, MD), NIST TN 2332. https://doi.org/10.6028/NIST.TN.2332  



---

[usnistgov/FD-Gen] is developed and maintained
by Hongqiang Fang and Andy Tam, principally:

- Hongqiang (Rory) Fang, @hqfang3
- Andy Tam

Please reach out with questions and feedbacks to Hongqiang (Rory) Fang <hongqiang.fang@nist.gov> and Andy Tam <waicheong.tam@nist.gov>.
