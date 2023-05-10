
## Copyright(c) 2022, 2023 Yoann Robin
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

version_major = 2
version_minor = 1
version_patch = 0
version_extra = "r1"
version       = f"{version_major}.{version_minor}.{version_patch}{version_extra}"


name          = "pygadm"
description   = "GADM shapefile data"
authors       = ["Yoann Robin"]
authors_email = ["yoann.robin.k@gmail.com"]
license       = "GNU General Public License v3"
src_url       = "https://github.com/yrobink/pygadm"

long_description = """\
Python package to build cartopy features from GADM data.
"""


authors_doc   = ", ".join( [ f"{ath} ({athm})" for ath,athm in zip(authors,authors_email) ] )

src_url = "https://github.com/yrobink/pygadm"

license_txt = """\
Copyright(c) 2022, 2023 Yoann Robin

This file is part of pygadm.

pygadm is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pygadm is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pygadm.  If not, see <https://www.gnu.org/licenses/>.
"""


