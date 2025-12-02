# RPi4-BLE-Client
BLE Client to connect to a ESP32 BLE Server to issue corrections

# To Run
 - Navigate to the directory cd RPi4-BLE-Client
 - First activate the environment
    source env/bin/activate
 - Then select the program to run eg: to run proxy.py
    python proxy.py

# To set up
 - it is recommended to set up inside a virtual environment before hand
    - on the raspbery pi 4 the command is python -m venv name_of_file
        - usually the name of the file in most cases is env
 - afterwards install the necessary files for the program you are using
    - eg: for bleak -> pip install bleak
        - be sure that the virtual environment is activated before as described in TO RUN
