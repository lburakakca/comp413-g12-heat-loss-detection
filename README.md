# COMP413-G12-Heat-Loss-Detection

## Project Overview
"Analyzing and Reducing Heat-Loss in Smart Cities" aims to analyze and reduce heat loss in buildings to optimize energy consumption and maintain environmental sustainability. By leveraging IoT technology and TinyML integration, the project provides real-time data collection and analysis, helping users monitor and improve the energy efficiency of their structures.

## Table of Contents
- [Installation](#installation)
- [Hardware List](#hardware-list)
- [Demo](#demo)
- [Live Dashboard](#live-dashboard)
- [Source Code](#source-code)
- [Documentation](#documentation)
- [Contributors](#contributors)
- [References](#references)

## Installation

### Requirements
- Python 3.7+
- Dash Framework
- ESP32 Modules
- Heat Sensors (e.g., DHT22)
- Other Dependencies

### Steps
1. **Clone the Repository:**
    ```bash
    git clone git@github.com:lburakakca/comp413-g12-heat-loss-detection.git
    cd comp413-g12-heat-loss-detection
    ```

2. **Install Required Python Packages:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Upload Microcontroller Code:**
    - Upload the microcontroller code located in `src/microcontrollers/` to your ESP32 modules.

4. **Start the Dashboard:**
    ```bash
    python src/dashboard/app.py
    ```

5. **Configure ESP32 Modules and Mount Sensors:**
    - Set up your ESP32 modules and install heat sensors in the designated locations.

## Hardware List
- **ESP32 Modules:** For data collection and processing.
- **Heat Sensors (DHT22):** To measure temperature and humidity.
- **Connecting Wires:** To connect sensors to the ESP32.
- **Power Supply:** To ensure continuous operation of the system.

## Demo
[3-Minute Video Demo](https://drive.google.com/drive/folders/1L6Y_Qgot_S2nDdHf97BqLQznnGrkJX5-?usp=sharing)

## Source Code
- **Microcontroller Code:** `src/microcontrollers/`
- **Cloud Functions:** `src/cloud_functions/`
- **Dashboard:** `src/dashboard/`

## Documentation
For a detailed project report, please refer to [docs/project_report.pdf](docs/project_report.pdf).

## Contributors
- **Berfin Candemir** - 2011011064
- **Muhammet Emin Tufan** - 2011051003
- **Burak Akça** - 2011051021

## References
- M. R. Johnson and T. R. Lee, "Energy efficiency and the role of IoT in a smart city connected community," in IEEE Conference Publication
- J. A. Smith, "Energy Efficiency in Smart Buildings: IoT Approaches," in IEEE Journals & Magazine

## Dashboard Image
![Dashboard](images/Ekran%20Resmi%202025-01-12%2023.52.32.png)