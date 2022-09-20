# Geolux Wave Radar processing tools
Python code, tests, and examples to process Geolux wave radar data for the NOPP 3B project.

- Code takes raw geolux continuous water level data and produces a CF compliant netcdf file(s).

- Raw .dat files are processed in 2 steps from an [IOOS python environment](https://ioos.github.io/ioos_code_lab/content/ioos_installation_conda.html)
    + Step 1 - process .dat to generate raw netcdf file of data using script runglxcsv2cdf.py from directory containg the data file. There are 2 arguments required to this script; 1) global attribute text file, and 2) instrument configuration yaml file. Examples of these files can be found in the examples folder. 
    
    Usage: (IOOS) C:\my\datadir> python git\geolux\runglxcsv2cdf.py <glob_att.txt> <config.yaml>

    + Step 2 - process raw.cdf to generate .nc CF compliant netcdf file of water_level data referenced to NAVD88 datum using script runglxcdf2nc.py from directory containing the raw.cdf file.
    
    Usage: (IOOS) C:\my\datadir> python git\geolux\runglxcdf2nc.py <raw.cdf>
