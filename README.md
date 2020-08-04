This repository is a collection of miscellaneous packaging recipes for OVIS software, each in its own directory. These recipes provide complete examples of configuring and building the software in diverse environments.
Each directory is self-documenting. Recipes that can be used for complete builds are preferred, but recipes extracted from automated bulk packaging services (e.g. Koji or openSUSE Build Service ) are also provided for advanced users.

The directories follow a naming convention to aid new users in identifying which example to examine first. The convention is:

	$release-or-branch.$OS.$subtype[.feature]*

for example:
* ovis-4.rhel7.base: builds v4 branch tip on Redhat installing to FHS locations as interpretted by redhat packaging guidelines.
* v3.4.13.toss3.base.mofed.rabbitmq: build v3.4.13 release for toss3 with MOFED and RabbitMQ support. Produces relocatable rpms.
* ovis-4.toss3.atse-125.papi.llnllustre.sos: ATSE spec files (only) from an opensuse build service instance enabling everything feasible in TOSS3.

### Packaging development plan
The following packagings are planned to be created or ported soon from other projects. If you need a recipe you do not see here, please open an issue about it.
* ovis-4.rhel7.sc: builds v4 branch tip packaged following Redhat 7 Software Collections guide for installing in /opt.
* ovis-4.rhel7.base.opt_anaconda_3: builds v4 branch tip with cython/python assuming /opt/anaconda/3 installed outside the RPM packaging system.
* ovis-4.u18.base:  builds for standard Ubuntu 18 environment (provides example debian/ directory)
* ovis-4.cle7.base:  builds v4 branch tip packaged for Cray Linux Environment 7
* ovis-4.cle6.base:  builds v4 branch tip packaged for Cray Linux Environment 7.

If contributing EPEL packaging, Use epel$version as an OS name, since EPEL introduces many packaging incompatibilities via newer versions, for example libssl.

LLNL does things its own way and shares it: https://github.com/LLNL/ovis/releases, see the spec files. https://github.com/LLNL/ovis/tree/OVIS-4.3.3-toss/rpm

### Making packages

This project assumes you know the generalities of package building for your system. Visit
the packaging info sites below if you need to know more.

Clone this repository to a scratch directory, go to the directory of interest, and review the
specific README.md. For example:

    git clone git@github.com:ovis-hpc/distribution.git
    cd distribution
    cd ovis-4.rhel7.base
    more README.md

### Comparing packages
Graphical diff/editing tools can compare spec files and launch scripts (fire*) across recipes, making it easy to transfer common improvements among recipes, such as including configure options controlling new features. An example comparing a RHEL 7 spec file input to ldms the config.status filter and a hard-coded TOSS3 spec file is: https://github.com/ovis-hpc/distribution/blob/master/doc/meld-example.png.

### Installation
See the README.md in each directory. Package installation varies by platform and use-case.

### Making packages off the grid
Most of the packaging examples collected here include a scripted step to download or clone
sources from github. An example of modifying these scripts to work
on an isolated machine is given in [OffGrid.md](OffGrid.md).

Many sites with Internet access will need to set the https_proxy variable to enable external git repository access. If you see a git clone or curl or wget hung during build, interrupt it and verify https_proxy and http_proxy are set per your site guidelines.

### Making test packages and contributing recipes
Make your own fork of the repository to work on unstable recipes. Contribute new directories (recipes) for this repository by making a pull request.

### Packaging pre-checks
Many recipes provide scripts that stage sources and provide precise arguments to package building utilities. Simple checks prior to starting long build processes can help users get the right required packages installed before building OVIS codes. The support/ directory provides shell script function libraries to check common prerequisites. As platforms evolve, some contributions may need to include alternate versions of support/package-functions.rpm.rhel7.

### Configuring LDMS with systemd and genders support
Scalable configuration management of clusters is easily done using the libgenders
options to control the ldmsd systemd service. The TOSS3 builds demonstrate how to
enable genders support.

### Packaging with python support
The Scalable Object Store, sosdb, and recent/upcoming LDMS use python3/numpy/cython/pandas for easy access to data arrays in python.
The default RHEL 7 Numpy (1.7) and Cython (0.19) are incompatible with this code.
Review the recipes listing python as a feature.

### Platform packaging guides

Debian/Ubuntu
https://wiki.debian.org/Packaging
https://packaging.ubuntu.com/html/

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

