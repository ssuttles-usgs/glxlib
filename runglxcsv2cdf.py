#!/usr/bin/env python

import yaml
import argparse

import core.utils
import core.cmd
import geolux


args = core.cmd.glxcsv2cdf_parser().parse_args()

# initialize metadata from the globalatts file
metadata = core.utils.read_globalatts(args.gatts)

# Add additional metadata from metadata config file
with open(args.config) as f:
    config = yaml.safe_load(f)

for k in config:
    metadata[k] = config[k]

RAW = geolux.csv_to_cdf(metadata)
