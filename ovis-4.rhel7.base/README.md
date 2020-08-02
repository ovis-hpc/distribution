# Build notes:

The rpms here are NOT relocatable in any way.
They omit the SOS python dependencies, hpc related samplers, and libgenders-based configuration.

Daemons install to /usr
Runtime files appear in /var/run

To Build it all:

Install the dependencies listed at the end, then:

./firesos

./fireldms

./rootmakerepo

# Installation:

To get started, just use (assuming an x86_64 host):

```
rpm -Uvh ovis-local.repo/*.x86_64.rpm
```

# Running hints (configuration of ldmsd and use of systemd is covered elsewhere)
Then to get the daemon running, you will need to (per your site tastes) fix the authentication 
to be a real authentication secret file or a symbolic link, perhaps with a link:
```
cd /etc/sysconfig/ldms.d/ClusterSecrets
```
and note that ldmsauth.conf must start with a valid secretword= line and have permissions 600.


# Package Dependencies:
	gcc
	rpm-build
	bison bison-devel
	flex flex-devel
	boost-devel
	doxygen
	gettext-devel
	openssl openssl-devel
	python2 python2-devel
	swig
	createrepo ( only needed to build a repo from the rpms )