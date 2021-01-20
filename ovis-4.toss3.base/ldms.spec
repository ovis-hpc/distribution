# Set topdir to be builddir/rpm
# note this is intentionally ignored by rpmbuild. must use
# commandline syntax in makefile.am to get this effect.
#% define _topdir %(echo $PWD)/toss
# do not set unfascist build
#%-define _unpackaged_files_terminate_build 0
#%-define _missing_doc_files_terminate_build 0

%define ldms_all System Environment/Libraries
%define build_timestamp %(date +"%Y%m%d_%H%M")
# % global __strip /bin/true
%global _enable_debug_package 0
%global _enable_debug_packages 0
%global debug_package %{nil}
%global __debug_install_post /bin/true
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

# Main package
Summary: OVIS Commands and Libraries
Name: ovis-ldms
Version: %{_version}
Release: %{?ldmsrelease}%{?dist}
License: GPLv2 or BSD
Group: %{ldms_all}
BuildRoot: %{_tmppath}/%{name}-%{version}%{release}-root-%(%{__id_u} -n)
Source: ovis-ldms-%{version}%{ldmssuffix}.tar.gz
Obsoletes: ovis < 4
Requires: rpm >= 4.8.0
Requires: papi600
Requires: python3
Requires: python3-devel
Requires: openssl
Requires: genders
Requires: boost
Requires: munge
BuildRequires: boost-devel boost
BuildRequires: gettext-devel gcc glib2-devel
BuildRequires: doxygen
BuildRequires: openssl-devel
BuildRequires: libibverbs-devel
BuildRequires: librdmacm-devel
BuildRequires: python3 python3-devel
BuildRequires: python36-Cython
BuildRequires: genders
# uncomment after papi600-devel installed.
# see toss 3.7-4 or toss/chaos.llnl.gov/yum/ch6-chaotic/x86_64/os
# Fake libpapi/libpfm libs and include/ under /usr/papi600 until then
#BuildRequires: papi600-devel
BuildRequires: bison bison-devel flex flex-devel
BuildRequires: librabbitmq librabbitmq-devel
BuildRequires: munge-devel munge-libs
Url: https://github.com/ovis-hpc/ovis

%description
This package provides the LDMS commands and libraries, LDMS apis and transport libraries for rhel 7.

%prep
%setup -q -n %{name}-%{version}%{ldmssuffix}

%build
echo bTMPPATH %{_tmppath}
rm -rf $RPM_BUILD_ROOT
echo bBUILDROOT $RPM_BUILD_ROOT
export CFLAGS="%{optflags} -O1 -g -I/usr/papi600/include"
# export CPPFLAGS="-I/usr/papi600/include"
export LDFLAGS="-L/usr/papi600/lib64 -Wl,-rpath=/usr/papi600/lib64"
set -x
%configure \
--with-boost=/usr \
--disable-static \
--with-pkglibdir=ovis-ldms \
--enable-ovis_auth \
--enable-ssl \
--enable-ovis_event \
--enable-zap \
--enable-sock \
--enable-rdma \
--disable-mmap \
--enable-doc \
--enable-doc-html \
--enable-doc-man \
--disable-readline \
--enable-ldms-python \
--enable-python \
--enable-libgenders \
--enable-genderssystemd \
--disable-sos \
--enable-flatfile \
--enable-csv \
--enable-store \
--disable-rabbitv3 \
--enable-rabbitkw \
--disable-kokkos \
--disable-cray_power_sampler \
--disable-cray_system_sampler \
--disable-aries-gpcdr \
--disable-gpcdlocal \
--disable-aries-mmr \
--disable-ugni \
--disable-perfevent \
--enable-papi \
--with-libpapi-prefix=/usr/papi600 \
--disable-procdiskstats \
--disable-atasmart \
--enable-generic_sampler \
--disable-switchx \
--enable-dstat \
--enable-llnl-edac \
--enable-sysclassib \
--enable-ibnet \
--enable-opa2 \
--disable-influx \
--enable-jobinfo-slurm \
--enable-spank-plugin \
--enable-slurm-sampler \
--with-slurm=/usr \
--disable-tsampler \
--enable-perf \
--enable-jobid \
--enable-array_example \
--enable-procinterrupts \
--enable-procnetdev \
--enable-procnfs \
--enable-procstat \
--enable-vmstat \
--enable-meminfo \
--enable-lustre \
--enable-slurmtest \
--enable-filesingle \
--enable-munge \
--with-libpapi=/usr/papi600 \
--with-libpfm=/usr/papi600
#--disable-papi-sampler \

make V=1 %{?_smp_mflags}


%install
echo TMPPATH %{_tmppath}
echo BUILDROOT $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} V=1 install

# sbin wrapper rework
for b in $RPM_BUILD_ROOT%{_sbindir}/ldms*; do
	bn=`basename $b`
	echo wrapping $bn
	dn=`dirname $b`
	mv $b $RPM_BUILD_ROOT%{_libdir}/ovis-ldms/$bn
	(cd $dn; ln -s .ldms-wrapper $bn)
done
# grunge for no-devel restriction in some environments
if test -f $RPM_BUILD_ROOT%{_libdir}/ovis-ldms/libstore_rabbitkw.so -o -f $RPM_BUILD_ROOT%{_libdir}/ovis-ldms/libstore_rabbitv3.so; then
	(cd $RPM_BUILD_ROOT%{_libdir}/ovis-ldms/; ln -s /usr/lib64/librabbitmq.so.4 librabbitmq.so; ln -s /usr/lib64/librabbitmq.so.4 .; ln -s /usr/lib64/librabbitmq.so.4.2.0 . )
fi
# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/ovis-ldms/lib*.la
rm -f $RPM_BUILD_ROOT%{_bindir}/test_*
rm $RPM_BUILD_ROOT%{_bindir}/ldms_ban.sh
find $RPM_BUILD_ROOT%{_docdir}/ovis-ldms-%{version}%{ldmssuffix} -maxdepth 1 -type f -exec mv {} $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/ \;
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/init.d
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system
cp $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}%{ldmssuffix}/sample_init_scripts/genders/sysv/etc/init.d/ldms* $RPM_BUILD_ROOT%{_sysconfdir}/init.d/
cp -ar $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}%{ldmssuffix}/sample_init_scripts/genders/systemd/etc/* $RPM_BUILD_ROOT%{_sysconfdir}
cp -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}%{ldmssuffix}/sample_init_scripts/genders/systemd/services/ldms*.service $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system

mkdir -p -m 755 $RPM_BUILD_ROOT%{_localstatedir}/log/ldmsd
mkdir -p -m 755 $RPM_BUILD_ROOT%{_localstatedir}/run/ldmsd
mkdir -p -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ldms.d/ClusterGenders
mkdir -p -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ldms.d/ClusterSecrets
mkdir -p -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ldms.d/plugins-conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/*
%{_bindir}/*
%{_sbindir}/*
%{_sbindir}/.ldms*
#%{_sbindir}/.ldms-wrapper
%{_datadir}/doc/%{name}-%{version}%{ldmssuffix}/relocation
%{_docdir}/%{name}-%{version}%{ldmssuffix}/COPYING
%{_docdir}/%{name}-%{version}%{ldmssuffix}/AUTHORS
%exclude %{_bindir}/ldms-py*sh
%exclude %{_bindir}/ldms-meminfo.sh
%exclude %{_bindir}/ldms-static-test.sh
%exclude %{_bindir}/ldmsd-wrapper.sh
%exclude %{_bindir}/ldmsd-pre-systemd
%exclude %{_bindir}/ldmsd-pre-sysvinit

#end core

# devel
%package devel
Summary: LDMS devel package
Group: %{ldms_grp}
Requires: ovis-ldms = %{version}
Obsoletes: ovis-devel
%description devel
This is a development package of Lightweight Distributed Metric System (LDMS).
Users who want to implement their own sampler or store must install this
package.

%files devel
%defattr(-,root,root)
%{_includedir}/*/*.h
%{_includedir}/*/*/*.h
%{_includedir}/ovis-ldms-config.h
#end devel

%package test
Summary: LDMS test package
Group: %{ldms_grp}
Requires: ovis-ldms = %{version}
Obsoletes: ovis-test < 4 ldms-all-test
%description test
This is a collection of test scripts for (LDMS).
They also serve as examples, but are not usually of direct 
interest on compute nodes in production clusters.

%files test
%defattr(-,root,root)
%{_bindir}/ldms-py*sh
%{_bindir}/ldms-meminfo.sh
%{_bindir}/ldms-static-test.sh
%{_datadir}/doc/ovis-ldms-%{version}%{ldmssuffix}/examples/static-test
%{_datadir}/doc/ovis-ldms-%{version}%{ldmssuffix}/examples/slurm-test
#end test

# initscripts
%package initscripts-base
Summary: LDMS base initscripts for libgenders control of %{name}
Group: %{ldms_grp}
Requires: ovis-ldms = %{version}
Obsoletes: ovis-initscripts-base < 4
%description initscripts-base
This is the support file set for libgenders based booting of LDMS daemons.
Users normally provide information via /etc/genders (or alternate file)
to make these scripts operate. With a manually written daemon
control file, use of libgenders can be bypassed.

%files initscripts-base
%defattr(-,root,root)
%{_sysconfdir}/sysconfig/ldms.d/README
%{_sysconfdir}/sysconfig/ldms.d/ldmsd
%{_sysconfdir}/sysconfig/ldms.d/ldmsd.all_instances.conf.example
%{_sysconfdir}/sysconfig/ldms.d/ldms-functions
%{_sysconfdir}/sysconfig/ldms.d/ClusterGenders/README
%{_sysconfdir}/sysconfig/ldms.d/plugins-conf/*
%{_sysconfdir}/sysconfig/ldms.d/ClusterSecrets/README
%config(noreplace) %{_sysconfdir}/sysconfig/ldms.d/ClusterSecrets/ldmsauth.conf
%config(noreplace) %{_sysconfdir}/sysconfig/ldms.d/debug/ldmsd.extra.local.conf
%config(noreplace) %{_sysconfdir}/sysconfig/ldms.d/ldmsd.local.conf
%config(noreplace) %{_sysconfdir}/sysconfig/ldms.d/ldmsd.agg.conf
%config(noreplace) %{_sysconfdir}/sysconfig/ldms.d/ClusterGenders/genders.local
%config(noreplace) %{_sysconfdir}/sysconfig/ldms.d/ClusterGenders/genders.agg
%{_bindir}/ldmsd-wrapper.sh


#end initscripts-base

%package initscripts-systemd
Summary: LDMS systemd scripts for libgenders control of %{name}
Group: %{ldms_grp}
Requires: ovis-ldms = %{version} ovis-ldms-initscripts-base = %{version}
Obsoletes: ovis-initscripts-systemd < 4
%description initscripts-systemd
This is the libgenders based systemd scripts for LDMS daemons.
Users normally provide information via /etc/genders (or alternate file)
to make these scripts operate. They are required to fail out of the box.

%files initscripts-systemd
%defattr(-,root,root)
%config %{_prefix}/lib/systemd/system/ldmsd*.service
%config %{_bindir}/ldmsd-pre-systemd

#end initscripts-systemd

# initscripts-sysv
%package initscripts-sysv
Summary: LDMS sysv init scripts for libgenders control of %{name}
Group: %{ldms_grp}
Requires: ovis-ldms = %{version} ovis-ldms-initscripts-base = %{version}
Obsoletes: ovis-initscripts-sysv < 4
%description initscripts-sysv
This is the libgenders based sysv init scripts for LDMS daemons.
Users must provide information via /etc/genders (or alternate file)
to make these scripts operate. They are required to fail out of the box.

%files initscripts-sysv
%defattr(-,root,root)
%config %{_sysconfdir}/init.d/ldms*
%config %{_bindir}/ldmsd-pre-sysvinit

#end initscripts-sysv


%package doc
Summary: Documentation files for %{name}
Group: %{ldms_all}
Obsoletes: ovis-doc < 4
## Requires: %{name}-devel = %{version}-%{release}
%description doc
Doxygen files for ovis package.
%files doc
%defattr(-,root,root)
%{_mandir}/*/*
%{_datadir}/doc/%{name}-%{version}%{ldmssuffix}
%exclude %{_datadir}/doc/%{name}-%{version}%{ldmssuffix}/relocation
%exclude %{_datadir}/doc/ovis-ldms-%{version}%{ldmssuffix}/examples
%docdir %{_datadir}/doc

%package python3
Summary: Python2 files for LDMS
Obsoletes: ovis-python2 < 4
Group: %{ldms_all}
Requires: python
Requires: ovis-ldms = %{version}
BuildRequires: python
BuildRequires: python python-devel
%description python3
Python files for ovis
%files python3
%defattr(-,root,root)
%{_prefix}/lib/python3.6/site-packages/ovis_ldms
%{_prefix}/lib/python3.6/site-packages/ldmsd
#end python2
# see https://fedoraproject.org/wiki/Packaging:Python_Old
# and https://fedoraproject.org/wiki/Packaging:Python

%changelog
* Tue Apr 21 2020 Ben Allan <baallan@sandia.gov> 4.3.4-1
Create 4.3.6 toss non-swig, papi-6
* Tue Apr 21 2020 Ben Allan <baallan@sandia.gov> 4.3.4-1
Create 4.3.4 toss nonrelocatable
* Mon Dec 9 2019 Ben Allan <baallan@sandia.gov> 4.3.1-1
Create 4.3.3 software collection.
