Name:           hsakmt
Version:        1.0.0
Release:        7%{?dist}
Summary:        AMD's HSA thunk library

Group:          System Environment/Libraries
# The entire source code is MIT except auto-generated file ltmain.sh which is GPLv2
License:        MIT and GPLv2
URL:            http://cgit.freedesktop.org/amd/hsakmt/
Source0:        http://xorg.freedesktop.org/archive/individual/lib/hsakmt-%{version}.tar.bz2
ExcludeArch:    %{arm} %{ix86}
BuildRequires:  automake autoconf libtool

Patch0:         gcc-4-fixes.patch

%description
hsakmt is a thunk library for AMD's HSA Linux kernel driver (amdkfd)

%package devel
Summary: AMD HSA thunk library development package
Group: Development/Libraries
Requires: %{name}%{?isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
Development library for hsakmt.

%prep
%setup -q -n hsakmt-%{version}
%patch0 -p1 -b .gcc-4-fixes

# We need to run autoreconf again so the build calls the right version of
# aclocal (upstream tries to use 1.15, RHEL has 1.13)
autoreconf -ivf

%build
%configure \
  --disable-static

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}

find %{buildroot} -type f -name "*.la" -delete

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%{_libdir}/libhsakmt-1*.so.*

%files devel
%dir %{_includedir}/hsakmt-1
%{_includedir}/hsakmt-1/hsakmt.h
%{_includedir}/hsakmt-1/hsakmttypes.h
%{_libdir}/libhsakmt-1*.so
%{_libdir}/pkgconfig/hsakmt-1.pc

%changelog
* Wed Jun 15 2016 Lyude Paul <cpaul@redhat.com> - 1.0.0-7
- Initial port from Fedora to RHEL 7.3
- Add patch for building with gcc4
- Call autoreconf before starting build
Resolves: rhbz#1311004

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 13 2015 Oded Gabbay <oded.gabbay@gmail.com> 1.0.0-5
- Don't build for arm and i686

* Fri Nov 13 2015 Oded Gabbay <oded.gabbay@gmail.com> 1.0.0-4
- Rename package back to hsakmt

* Sun Nov 1 2015 Oded Gabbay <oded.gabbay@gmail.com> 1.0.0-3
- Rename package to libhsakmt

* Thu Oct 29 2015 Oded Gabbay <oded.gabbay@gmail.com> 1.0.0-2
- Changed doc to license
- Added GPLv2 to license
- Changed RPM_BUILD_ROOT to {buildroot}

* Sat Oct 24 2015 Oded Gabbay <oded.gabbay@gmail.com> 1.0.0-1
- Initial release of hsakmt, ver. 1.0.0
