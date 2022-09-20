import pandas as pd
import xarray as xr

import core.utils


def read_glx(filnam, skiprows=0, header=1, encoding="utf-8"):
    """Read data from a Vaisala WXT met .csv file into an xarray
    Dataset.
    Parameters
    ----------
    filnam : string
        The filename
    skiprows : int, optional
        How many header rows to skip. Default 7
    encoding : string, optional
        File encoding. Default 'utf-8'
    Returns
    -------
    xarray.Dataset
        An xarray Dataset of the WXT data
    """

    df = pd.read_csv(
        filnam,
        skiprows=skiprows,
        header=header,
        encoding=encoding,
        index_col=False,
    )

    # drop 2 header rows below column headings
    df.drop([0, 1], axis=0, inplace=True)

    # recast dtypes since set to string by extra header rows below column headings
    df["RECORD"] = df["RECORD"].astype(int)

    for c in df.columns[2:]:
        df[c] = df[c].astype(float)

    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"])
    df.rename(columns={"TIMESTAMP": "time"}, inplace=True)
    df.index.names = ["time"]
    glx = xr.Dataset.from_dataframe(df)
    return glx


# Make raw CDF
def csv_to_cdf(metadata):

    basefile = metadata["basefile"]

    ds = read_glx(basefile + ".dat", skiprows=metadata["skiprows"])
    metadata.pop("skiprows")
    ds = core.utils.write_metadata(ds, metadata)
    # ds['time'] = xr.DataArray(time, dims='time')

    # configure file
    cdf_filename = ds.attrs["filename"] + "-raw.cdf"

    ds.to_netcdf(cdf_filename, unlimited_dims=["time"])

    print("Finished writing data to %s" % cdf_filename)

    return ds


# Process data and write to .nc file
def cdf_to_nc(cdf_filename):
    """
    Load a "raw" .cdf file and generate a processed .nc file
    """

    # Load raw .cdf data
    ds = xr.open_dataset(cdf_filename)
    ds.time.encoding.pop(
        "units"
    )  # remove units in case we change and we can use larger time steps

    # create vert dim z
    ds = create_z_glx(ds)

    # Get rid of unneeded variables
    for k in [
        "Avg_Level_10Hz",
        "Distance_10Hz",
    ]:
        if k in ds:
            ds = ds.drop_vars(k)

    # Rename variables to CF compliant names
    ds = ds_rename_vars(ds)

    # Add attributes
    ds = ds_add_attrs(ds)

    # Run utilities
    ds = core.utils.add_start_stop_time(ds)
    ds = core.utils.ds_add_lat_lon(ds)
    ds = core.utils.add_min_max(ds)
    ds = core.utils.add_delta_t(ds)
    
    ds = core.utils.ds_coord_no_fillvalue(ds)

    # Write to .nc file
    print("Writing cleaned/trimmed data to .nc file")
    nc_filename = ds.attrs["filename"] + "-cont.nc"

    ds.to_netcdf(
        nc_filename, unlimited_dims=["time"], encoding={"time": {"dtype": "i4"}}
    )
    core.utils.check_compliance(nc_filename, conventions=ds.attrs["Conventions"])
    print("Done writing netCDF file", nc_filename)


# Rename variables to be CF compliant
def ds_rename_vars(ds):
    varnames = {
        "RECORD": "record",
        "Level_10Hz": "water_level",
    }

    # Check to make sure they exist before trying to rename
    newvars = {}
    for k in varnames:
        if k in ds:
            newvars[k] = varnames[k]
    return ds.rename(newvars)


# Convert data from float 64 to float32
def ds_convertfloat(ds):
    for var in ds.variables:
        if ds[var].name != "time":
            ds[var] = ds[var].astype("float32")
    return ds


# Add attributes: units, standard name from CF website, epic code
def ds_add_attrs(ds):

    

    ds["time"].attrs.update(
        {"standard_name": "time", "axis": "T", "long_name": "time (UTC)"}
    )

    if "record" in ds:
        ds["record"].attrs.update({"units": "1", "long_name": "record number"})

    if "water_level" in ds:
        ds["water_level"].attrs.update(
            {
                "units": "meters",
                "long_name": "sea surface height ref to %s"
                % ds.attrs["geopotential_datum_name"],
                "standard_name": "sea_surface_height_above_geopotential_datum",
                "geopotential_datum_name": ds.attrs["geopotential_datum_name"],
                "initial_instrument_height": ds.attrs["initial_instrument_height"],
            }
        )

    return ds


def create_z_glx(ds):
    # create z for geolux

    ds["z"] = xr.DataArray(
        [ds.attrs["initial_instrument_height"] - ds["Distance_10Hz"].mean().values],
        dims="z",
    )

    ds["z"].attrs["geopotential_datum_name"] = ds.attrs["geopotential_datum_name"]
    ds["z"].attrs["long_name"] = (
        "height relative to %s" % ds.attrs["geopotential_datum_name"]
    )

    ds["z"].attrs["positive"] = "up"
    ds["z"].attrs["axis"] = "Z"
    ds["z"].attrs["units"] = "m"
    ds["z"].attrs["standard_name"] = "height"

    ds["depth"] = xr.DataArray([0.0], dims="depth")
    ds["depth"].attrs["positive"] = "down"
    ds["depth"].attrs["units"] = "m"
    ds["depth"].attrs["standard_name"] = "depth"
    ds["depth"].attrs["long_name"] = "depth below mean sea level"
    ds["depth"].attrs["note"] = "measurement ref is to the local mean sea surface"

    return ds
