#!/usr/bin/env python3

## Copyright(c) 2022 Yoann Robin
## 
## This file is part of pygadm.
## 
## pygadm is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## pygadm is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with pygadm.  If not, see <https://www.gnu.org/licenses/>.

###############
## Libraries ##
###############

import sys,os
import urllib

import numpy  as np
import pandas as pd
import xarray as xr

import matplotlib as mpl
import matplotlib.pyplot   as plt
import matplotlib.gridspec as mplg

import cartopy.crs as ccrs

import pygadm

########################
## Set mpl parameters ##
########################

mpl.rcdefaults()
mpl.rcParams['font.size'] = 7
mpl.rcParams['axes.linewidth']  = 0.5
mpl.rcParams['lines.linewidth'] = 0.5
mpl.rcParams['patch.linewidth'] = 0.5
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['ytick.major.width'] = 0.5
mpl.rcParams['font.serif']      = "Liberation Serif"
mpl.rcParams['font.sans-serif'] = "Liberation Sans"
mpl.rcParams['font.monospace']  = "Liberation Mono"

##########
## main ##
##########

def load_data():
	
	ofile = os.path.join( os.path.dirname(os.path.abspath(__file__)) , "elevation_eobs.nc" )
	if not os.path.isfile(ofile):
		url = "https://knmi-ecad-assets-prd.s3.amazonaws.com/ensembles/data/Grid_0.1deg_reg_ensemble/elev_ens_0.1deg_reg_v26.0e.nc"
		urllib.request.urlretrieve( url , ofile )
	
	return ofile


if __name__ == "__main__":
	
	## Load and open data
	ifile = load_data()
	idata = xr.open_dataset(ifile)
	z     = idata.elevation.rename( latitude = "lat" ).rename( longitude = "lon" )
	z     = z[(41 < z.lat) & (z.lat < 53),:]
	z     = z[:,(-7 < z.lon) & (z.lon < 12)]
	lat   = z.lat
	lon   = z.lon
	
	## Build the colormap of topo
	zmin  = -1000
	zmax  = 4500
	ztot  = zmax - zmin
	n_neg = int( 10000 * - zmin / ztot )
	n_pos = int( 10000 *   zmax / ztot )
	
	cut_neg = 0.18
	cut_pos = 0.28
	cmap    = mpl.colors.ListedColormap( np.vstack( (plt.cm.terrain(np.linspace(0,cut_neg,n_neg)),plt.cm.terrain(np.linspace(cut_pos,1,n_pos)))) )
	
	
	## Load the features
	countries0 = ["FRA","CHE","ESP","BEL","GBR","DEU","NLD","ITA"]
	countries1 = ["FRA"]
	feats0 = [ pygadm.feature_gadm( c , 0 , verbose = True ) for c in countries0 ]
	feats1 = [ pygadm.feature_gadm( c , 1 , verbose = True ) for c in countries1 ]
	
	fig  = plt.figure( dpi = 120 )
	grid = mplg.GridSpec( 1 + 1 + 3 , 1 + 2 + 1 )
	
	for i in range(2):
		ax   = fig.add_subplot( grid[1,i+1] , projection = ccrs.epsg(2154) )
		
		im = ax.pcolormesh( lon , lat , z , transform = ccrs.PlateCarree() , shading = "nearest" , zorder = 0 , cmap = cmap , vmin = zmin , vmax = zmax )
		
		for f0 in feats0:
			ax.add_feature( f0 , facecolor = "none" , edgecolor = "black" , linestyle = "-" , zorder = 2 )
		if i == 0:
			ax.set_title( "Level = 0" )
		if i == 1:
			ax.set_title( "Level = 1 (for France)" )
			for f1 in feats1:
				ax.add_feature( f1 , facecolor = "none" , edgecolor = "grey" , linestyle = ":" , zorder = 1 )
		ax.set_extent( [-5,10,41,52] )
	
	cax = fig.add_subplot( grid[3,:].subgridspec( 1 , 3 , width_ratios = [0.1,0.8,0.1] )[0,1] )
	plt.colorbar( mappable = im , cax = cax , orientation = "horizontal" , label = "Elevation from E-OBS" )
	
	## Width / height
	mm       = 1. / 25.4
	pt       = 1. / 72
	width    = 180*mm
	w_lr     = 1*pt
	width_ax = ( width - 2 * w_lr ) / 2
	widths   = [w_lr] + [width_ax for _ in range(2)] + [w_lr]
	
	try:
		ratio = ax.get_aspect() * ax.get_data_ratio()
	except:
		ratio = ax.get_data_ratio()
	
	height_ax    = width_ax * ratio
	height_tit   = 15*pt
	height_top_c = 5*pt
	height_cbar  = 10*pt
	height_bot_c = 30*pt
	heights      = [height_tit] + [height_ax] + [height_top_c,height_cbar,height_bot_c]
	height       = sum(heights)
	
	grid.set_height_ratios(heights)
	grid.set_width_ratios(widths)
	fig.set_figwidth(width)
	fig.set_figheight(height)
	
	plt.subplots_adjust( left = 0 , right = 1 , bottom = 0 , top = 1 , wspace = 0 , hspace = 0 )
	plt.savefig( os.path.join( os.path.dirname(os.path.abspath(__file__)) , "example_FR.png" ) , dpi = 600 )
	
	print("Done")
