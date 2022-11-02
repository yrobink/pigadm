
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

#############
## Imports ##
#############

import sys
import os
import tempfile
import urllib.request
import progressbar
import zipfile

from cartopy.feature import ShapelyFeature
from cartopy.io.shapereader import Reader
from cartopy.crs import PlateCarree


class DownloadBar:
	
	def __init__( self ):
		self.bar = None
	
	def __enter__( self ):
		return self
	
	def __exit__( self , *args ):
		print("")
	
	def update( self , b = 1 , bsize = 1 , tsize = None ):
		
		if self.bar is None and tsize is not None:
			self.bar = progressbar.DataTransferBar( max_value = tsize )
		
		if self.bar is not None:
			self.bar.update( min( b * bsize , tsize ) , force = True )


def download_gadm( country , version , opath , verbose ):
	
	## Find the version
	gadm_major,gadm_minor = version.split(".")
	
	## Temporary path
	tmp_dir  = tempfile.TemporaryDirectory()
	tmp      = os.path.join( tmp_dir.name , "pygadm_tmp" )
	os.makedirs(tmp)
	
	## Set url
	url   = f"https://geodata.ucdavis.edu/gadm/gadm{version}/shp/gadm{gadm_major}{gadm_minor}_{country}_shp.zip"
	tfile = f"gadm{gadm_major}{gadm_minor}_{country}_shp.zip"
	
	## Download
	if verbose:
		with DownloadBar() as dwb:
			urllib.request.urlretrieve( url , os.path.join( tmp , tfile ) , reporthook = dwb.update )
	else:
		urllib.request.urlretrieve( url , os.path.join( tmp , tfile ) )
	
	## Set output path
	if not os.path.isdir(opath):
		os.makedirs(opath)
	
	## And extract zip
	with zipfile.ZipFile( os.path.join( tmp , tfile ) , "r" ) as zobj:
		zobj.extractall( path = opath )


def feature_gadm( country , level = 0 , version = "4.1" , verbose = False , **kwargs ):
	"""
	pygadm.feature_gadm
	===================
	
	Arguments
	---------
	country: [string]
		The country defined by the Alpha-3 code (ISO 3166-1 format).
	level: [integer]
		The level of subdivision. 0 is always the frontier of the country.
		Subdivision depends of the country.
	version: [string]
		Version of GADM data
	verbose: [bool]
		Print a progress bar when data are download
	**kwargs:
		Others keywords arguments are given to the feature.
	
	Returns
	-------
	A 'cartopy.feature.ShapelyFeature'
	
	Notes
	-----
	Original data are available at: https://gadm.org/index.html
	
	"""
	
	## Find the version
	gadm_major,gadm_minor = version.split(".")
	
	## Set path
	data_dir = os.path.join( os.path.expanduser("~") , ".local" , "share" , "pygadm" )
	iopath   = os.path.join( data_dir , f"gadm{gadm_major}.{gadm_minor}" , country )
	
	## Data already download
	if not os.path.isdir(iopath):
		download_gadm( country , version , iopath , verbose )
	
	## Liste shapefile
	files = [ f for f in os.listdir(iopath) if os.path.splitext(f)[-1] == ".shp" ]
	files.sort()
	
	## Find available levels
	levels = [ f.split(".")[0].split("_")[-1] for f in files ]
	if not f"{level}" in levels:
		raise Exception( f"Level '{level}' is not available for {country} (avail: {', '.join(levels)})" )
	
	## Build feat kwargs
	fkwargs = { "edgecolor" : "black" , "facecolor" : "none" , "linestyle" : "-" if level == 0 else ":" }
	for key in kwargs:
		fkwargs[key] = kwargs[key]
	
	## Build the feature
	ifile   = os.path.join( iopath , f"gadm{gadm_major}{gadm_minor}_{country}_{level}.shp" )
	feature = ShapelyFeature( geometries = Reader(ifile).geometries() , crs = PlateCarree() , **fkwargs )
	
	return feature
