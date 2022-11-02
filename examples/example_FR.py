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

if __name__ == "__main__":
	
	## Data
	km  = 1000
	dxy = 8*km
	x   = np.arange(  100*km , 1250*km + dxy / 2 , dxy )
	y   = np.arange( 6050*km , 7120*km + dxy / 2 , dxy )
	X   = np.linspace( - np.pi , np.pi , x.size )
	Y   = np.linspace( - np.pi , np.pi , y.size )
	D   = Y.reshape(-1,1)**2 + X.reshape(1,-1)**2
	H   = Y.reshape(-1,1)**2 - X.reshape(1,-1)**2
	Z   = np.exp( - D / ( 2 * np.pi ) ) * np.cos(H)
	
	featFRA0 = pygadm.feature_gadm( "FRA" , 0 , verbose = True )
	featFRA1 = pygadm.feature_gadm( "FRA" , 1 , verbose = True )
	featCHE0 = pygadm.feature_gadm( "CHE" , 0 , verbose = True )
	
	fig  = plt.figure( dpi = 120 )
	grid = mplg.GridSpec( 1 + 3 , 1 )
	ax   = fig.add_subplot( grid[0,0] , projection = ccrs.epsg(2154) )
	
	im = ax.pcolormesh( x , y , Z , transform = ccrs.epsg(2154) , shading = "nearest" , cmap = plt.cm.RdBu_r , vmin = -1 , vmax = 1 )
	
	ax.add_feature( featFRA0 , facecolor = "none" , edgecolor = "black" , linestyle = "-" )
	ax.add_feature( featFRA1 , facecolor = "none" , edgecolor = "black" , linestyle = ":" )
	ax.add_feature( featCHE0 , facecolor = "none" , edgecolor = "black" , linestyle = "-" )
	ax.set_axis_off()
	
	cax = fig.add_subplot( grid[2,:].subgridspec( 1 , 3 , width_ratios = [0.1,0.8,0.1] )[0,1] )
	plt.colorbar( mappable = im , cax = cax , orientation = "horizontal" )
	
	## Width / height
	mm       = 1. / 25.4
	pt       = 1. / 72
	width    = 120*mm
	width_ax = width
	widths   = [width_ax]
	
	try:
		ratio = ax.get_aspect() * ax.get_data_ratio()
	except:
		ratio = ax.get_data_ratio()
	
	height_ax    = width_ax * ratio
	height_top_c = 5*pt
	height_cbar  = 10*pt
	height_bot_c = 15*pt
	heights      = [height_ax] + [height_top_c,height_cbar,height_bot_c]
	height       = sum(heights)
	
	grid.set_height_ratios(heights)
	grid.set_width_ratios(widths)
	fig.set_figwidth(width)
	fig.set_figheight(height)
	
	plt.subplots_adjust( left = 0 , right = 1 , bottom = 0 , top = 1 , wspace = 0 , hspace = 0 )
	
	plt.show()
	
	print("Done")
