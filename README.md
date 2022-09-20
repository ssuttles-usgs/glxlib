# Geolux Wave Radar processing tools
Python code, tests, examples, notebooks cd to process Geolux wave radar data for the NOPP 3B project

- Code takes raw geolux continous water level data and produces a CF compliant netcdf file(s)

- Raw .dat files are processed in a 2 steps process while a [IOOS python environment](https://ioos.github.io/ioos_code_lab/content/ioos_installation_conda.html) 
    + Step 1 - process .dat to generate raw netcdf file of data using script runglxcsv2cdf.py from from diectory containg the data file. There are 2 arguments required to the script. A global attribute ext file and an instrument configuration yaml file. Example:
    
    (IOOS) C:\my\datadir> python git\geolux\runglxcsv2cdf.py <glob_att.txt> <config.yaml>

    + Step 2 - process raw.cdf to generate .nc CF compliant netcdf file of water_level data ref to NAVD88 data using script runglxcdf2nc.py from from diectory containg the -raw,cdf file. Example:
    
    (IOOS) C:\my\datadir> python git\geolux\runglxcdf2nc.py <raw.cdf>
