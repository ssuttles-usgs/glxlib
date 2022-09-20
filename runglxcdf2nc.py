#!/usr/bin/env python
import argparse
import core.cmd
import geolux

args = core.cmd.eofecdf2nc_parser().parse_args()

ds = geolux.cdf_to_nc(args.cdfname)
