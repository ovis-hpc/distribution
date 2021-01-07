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
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /opt/python-2.7/bin/python}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

# Main package
Summary: OVIS SOS Commands and Libraries
Name: sosdb
Version: 4.3.4
Release: desktop_%{build_timestamp}%{?dist}
License: GPLv2 or BSD
Group: %{ldms_all}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source: %{name}-%{version}.tar.gz
Requires: rpm >= 4.8.0
BuildRequires: gcc
#Requires: python2
#Requires: python2-devel
#Requires: python2-numpy
#Requires: python2-cython
#BuildRequires: python2-devel
#BuildRequires: python2-numpy
#BuildRequires: python2-cython
#BuildRequires: doxygen
Url: http://ovis.ca.sandia.gov/


%description
This package provides the OVIS sosdb commands and libraries TOSS 3.


%prep
%setup -q

%build
echo bTMPPATH %{_tmppath}
rm -rf $RPM_BUILD_ROOT
echo bBUILDROOT $RPM_BUILD_ROOT
export CFLAGS="-g -O2 %{optflags} -O1 -g"
%configure  'CC=gcc' 'CXX=g++' '--disable-static' '--prefix=/usr' '--disable-python' '--disable-doc' '--disable-doc-html' '--disable-doc-man' '--disable-doc-graph'

ncores=`grep -c ^processor /proc/cpuinfo`
make V=1 -j $ncores

%install
echo TMPPATH %{_tmppath}
echo BUILDROOT $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} V=1 install

# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/sos/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/*
%{_bindir}/*
#end core

# devel
%package devel
Summary: OVIS SOS DB devel package
Group: %{ldms_grp}
Requires: sosdb = 4.3.4
Obsoletes: ldms-all-devel
%description devel
This is a development package of Scalable Object Store
Users who want to use sosdb from C must install this package.

%files devel
%defattr(-,root,root)
%{_includedir}/*/*.h
#end devel

#%package doc
#Summary: Documentation files for %{name}
#Group: %{ldms_all}
#%description doc
##Doxygen files for ovis sosdb package.
#%files doc
#%defattr(-,root,root)
#%{_mandir}/*/*
#%{_datadir}/doc/%{name}
#%docdir /usr/share/doc

#%package python2
#Summary: Python files for SOS DB
#%description python2
#Python files for ovis sosdb
## install needs
#Requires: sosdb = 4.3.4
## build needs
#BuildRequires: python python-devel cython numpy
#%files python2
#%defattr(-,root,root)
#%{_prefix}/lib/python2.7/site-packages/sosdb
##end sosdb

%changelog
* Fri Jun 21 2019 Ben Allan <baallan@sandia.gov> 4.2.1-1
First packaging of stand-alone sos for TOSS 3. Not relocatable.

