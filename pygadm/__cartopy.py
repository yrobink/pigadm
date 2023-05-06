
## Copyright(c)  2023 Yoann Robin
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

#############
## Imports ##
#############

import sys
import os

cartopy_on = True
cartopy_error = None
try:
	from cartopy.feature import ShapelyFeature
	from cartopy.io.shapereader import Reader
	from cartopy.crs import PlateCarree
except ModuleNotFoundError as e:
	cartopy_on = False
	cartopy_error = e

from .__core import pygadmParams


###############
## Functions ##
###############

def feature( country , level = 0 , **kwargs ):
	"""
	pygadm.feature
	==============
	
	Arguments
	---------
	country: [string]
		The country defined by the Alpha-3 code (ISO 3166-1 format).
	level: [integer]
		The level of subdivision. 0 is always the frontier of the country.
		Subdivision depends of the country.
	**kwargs:
		Others keywords arguments are given to the feature.
	
	Returns
	-------
	A 'cartopy.feature.ShapelyFeature'
	
	Notes
	-----
	Original data are available at: https://gadm.org/index.html
	
	"""
	
	if not cartopy_on:
		raise cartopy_error
	
	shpfile = pygadmParams.build_path( country , str(level) )
	
	## Build feat kwargs
	fkwargs = { "edgecolor" : "black" , "facecolor" : "none" , "linestyle" : "-" if level == 0 else ":" }
	for key in kwargs:
		fkwargs[key] = kwargs[key]
	
	## Build the feature
	feature = ShapelyFeature( geometries = Reader(shpfile).geometries() , crs = PlateCarree() , **fkwargs )
	
	return feature


