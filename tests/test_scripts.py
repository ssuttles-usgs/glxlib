import subprocess
import pytest


def glx_raw(glob_att, config_yaml):
    result = subprocess.run(
        ["python", "../../runglxcsv2cdf.py", glob_att, config_yaml],
        capture_output=True,
        cwd="tests/data",
    )
    assert "Finished writing data" in result.stdout.decode("utf8")


def glx_nc(nc_file):
    result = subprocess.run(
        ["python", "../../runglxcdf2nc.py", nc_file],
        capture_output=True,
        cwd="tests/data",
    )
    assert "Done writing netCDF file" in result.stdout.decode("utf8")

def test_glx():
    glx_raw("glob_att_Geolux_2022_NC_FieldTest.txt", "config_Geolux_2022_NC_FieldTest.yaml")
    glx_nc("Geolux_example-raw.cdf")
    
