
## Copyright(c) 2023 Yoann Robin
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

##############
## Packages ##
##############

import sys,os
import datetime as dt
import logging


#############
## Imports ##
#############

from .__core import pygadmParams
from .__curses_doc import print_doc


##################
## Init logging ##
##################

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


###############
## Functions ##
###############

def run_pygadm():
	
	pygadmParams.run()
	

def start_pygadm(argv):
	
	## Time counter
	walltime0 = dt.datetime.utcnow()
	
	## User input
	pygadmParams.init_from_user_input(*argv)
	
	## Init logs
	pygadmParams.init_logging()
	
	## Logging
	logger.info(pygadmParams.LINE)
	logger.info( r"                              _           " )
	logger.info( r"  _ __  _   _  __ _  __ _  __| |_ __ ___  " )
	logger.info( r" | '_ \| | | |/ _` |/ _` |/ _` | '_ ` _ \ " )
	logger.info( r" | |_) | |_| | (_| | (_| | (_| | | | | | |" )
	logger.info( r" | .__/ \__, |\__, |\__,_|\__,_|_| |_| |_|" )
	logger.info( r" |_|    |___/ |___/                       " )
	logger.info(pygadmParams.LINE)
	logger.info( "Start: {}".format( str(walltime0)[:19] + " (UTC)") )
	logger.info(pygadmParams.LINE)
	
	## Serious functions start here
	try:
		## Check inputs
		pygadmParams.check()
		
		## Init temporary
		pygadmParams.init_tmp()
		
		## List of all input
		logger.info("Input parameters:")
		for key in pygadmParams.keys():
			if key in ["LINE"]: continue
			logger.info( " * {:{fill}{align}{n}}".format( key , fill = " ",align = "<" , n = 10 ) + ": {}".format(pygadmParams[key]) )
		logger.info(pygadmParams.LINE)
		
		## If abort, stop execution
		if pygadmParams.abort:
			raise pygadmParams.error
		
		## User asks help
		if pygadmParams.help:
			print_doc()
		
		## Run
		run_pygadm()
		
	except Exception as e:
		logger.error( f"Error: {e}" )
	
	## End
	walltime1 = dt.datetime.utcnow()
	logger.info(pygadmParams.LINE)
	logger.info( "End: {}".format(str(walltime1)[:19] + " (UTC)") )
	logger.info( "Wall time: {}".format(walltime1 - walltime0) )
	logger.info(pygadmParams.LINE)

