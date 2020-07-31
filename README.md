This repository is a collection of miscellaneous packaging recipes for OVIS software, each in its own directory. These recipes provide complete examples of configuring and building the software in diverse environments.
Each directory is self-documenting. Recipes that can be used for complete builds are preferred, but recipes extracted from automated bulk packaging services (e.g. Koji or openSUSE Build Service ) are also accepted.

The directories follow a naming convention to aid new users in identifying which example to examine first. The convention is:

	$release-or-branch.$OS.$subtype.\[feature.\]\*.

for example 
* OVIS-4.rhel7.base.nopython: builds v4 branch tip without python bindings on Redhat installing to LHS/FSB locations as interpretted by redhat packaging guidelines.
* OVIS-4.rhel7.base.optanaconda3: builds v4 branch tip with python assuming /opt/anaconda/3 created outside the RPM packaging system.
* OVIS-4.rhel7.sc: builds v4 branch tip packaged following Redhat 7 Software Collections guide
* OVIS-4.u18.base: builds for standard Ubuntu 18 environment (provides example debian/ directory)
* OVIS-4.CLE7.base: builds v4 branch tip packaged for Cray Linux Environment 7

Notable values of subtype thus far are base, and sc. Use epel as an OS name, since EPEL introduces many packaging incompatibilities via newer versions, or example libssl.

## Making packages

This project assumes you know the generalities of package building for your system. Visit
the packaging info sites below if you need to know more.

Clone this repository to a scratch directory, go to the directory of interest, and review the
specific README.md. For example:

    git clone git@github.com:ovis-hpc/distribution.git
    cd distribution
    cd OVIS-4.rhel7.base.nopython
    more README.md

## Installation
See the README.md in each directory. Package installation varies by platform and use-case.

## Making packages off the grid
Most of the packaging examples collected here include a scripted step to download or clone
sources from github. An example of modifying these scripts to work
on an isolated machine is given in [OffGrid.md](OffGrid.md).

## Making test packages and contributing recipes
Make your own fork of the repository to work on unstable recipes. Contribute new directories (recipes) for this repository by making a pull request.

## Configuring LDMS with systemd and genders support
Scalable configuration management of clusters is easily done using the libgenders
options to control the ldmsd systemd service. The TOSS3 builds demonstrate how to
enable genders support.

## Packaging with python support
The Scalable Object Store, sosdb, and recent/upcoming LDMS use python3/numpy/cython/pandas for easy access to data arrays in python.
The default RHEL 7 Numpy (1.7) and Cython (0.19) are incompatible with this code.
Review the recipes listing python as a feature.

## Platform packaging guides

Debian/Ubuntu
[https://wiki.debian.org/Packaging]
[https://packaging.ubuntu.com/html/]
Software Collections
https://access.redhat.com/documentation/en-us/red_hat_software_collections/1/html/packaging_guide/index
https://www.softwarecollections.org/en/docs/

Redhat 7
https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html-single/rpm_packaging_guide/index

Rehat 8
https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/packaging_and_distributing_software/index

SUSE
https://en.opensuse.org/openSUSE:Packaging_guidelines

FHS
https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard

