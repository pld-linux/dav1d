#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
#
Summary:	AV1 decoder library
Summary(pl.UTF-8):	Biblioteka dekodera AV1
Name:		dav1d
Version:	1.1.0
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://download.videolan.org/videolan/dav1d/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	e98a56198b2f47dbd27c747e69a9e140
Patch0:		%{name}-nasm.patch
URL:		https://code.videolan.org/videolan/dav1d
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	meson >= 0.49.0
%ifarch %{ix86} %{x8664} x32
BuildRequires:	nasm >= 2.13.02
%endif
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
dav1d is a new AV1 cross-platform decoder, open-source, and focused on
speed and correctness.

%description -l pl.UTF-8
dav1d to nowy, wieloplatformowy dekoder AV1, mający otwarte źródła,
rozwijany głównie z myślą o szybkości i poprawności.

%package devel
Summary:	Header files for DAV1D library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki DAV1D
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for DAV1D library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki DAV1D.

%package static
Summary:	Static DAV1D library
Summary(pl.UTF-8):	Statyczna biblioteka DAV1D
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static DAV1D library.

%description static -l pl.UTF-8
Statyczna biblioteka DAV1D.

%package apidocs
Summary:	API documentation for DAV1D library
Summary(pl.UTF-8):	Dokumentacja API biblioteki DAV1D
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for DAV1D library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki DAV1D.

%prep
%setup -q
%patch0 -p1

%build
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	-Denable_docs=%{__true_false apidocs}

%ninja_build -C build %{?with_apidocs:doc/html}

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING NEWS README.md THANKS.md doc/PATENTS
%attr(755,root,root) %{_bindir}/dav1d
%attr(755,root,root) %{_libdir}/libdav1d.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdav1d.so.6

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdav1d.so
%{_includedir}/dav1d
%{_pkgconfigdir}/dav1d.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdav1d.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/*
%endif
