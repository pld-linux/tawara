# NOTE: previous names of this projects were: tide, celduin, jonen
#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

%define	snap	20130819
Summary:	Tawara file format implementation
Summary(pl.UTF-8):	Implementacja formatu plików Tawara
Name:		tawara
Version:	0.1.0
Release:	0.%{snap}.2
License:	BSD
Group:		Libraries
Source0:	http://github.com/gbiggs/tawara/archive/master/%{name}-%{snap}.tar.gz
# Source0-md5:	682d240fad7fd3e74026fa7c2a660b1f
Patch0:		%{name}-lib.patch
URL:		http://gbiggs.github.io/tawara/
# filesystem, system, date_time
BuildRequires:	boost-devel
BuildRequires:	cmake >= 2.8
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	python-breathe
BuildRequires:	sphinx-pdg
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An interface, with implementations, for a channel-based system for
storing data that is indexed by time. Multiple channels of data can be
stored. Extensive meta-data is available, including channel names,
stored data type information, and key-value tags (capable of storing
anything that can be converted to binary data).

%description -l pl.UTF-8
Interfejs wraz z implementacjami opartego na kanałach systemu
przechowywania danych indeksowanych po czasie. Pozwala na
przechowywanie wielu kanałów. Dostępne są rozszerzalne metadane, w tym
nazwy kanałów, informacje o przechowywanym typie danych oraz znaczniki
klucz-wartość (pozwalające przechowywać wszystko, co można
przekształcić do danych binarnych).

%package devel
Summary:	Header files for Tawara library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Tawara
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Tawara library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Tawara.

%package apidocs
Summary:	Tawara API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Tawara
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for Tawara library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Tawara.

%prep
%setup -q -n %{name}-master
%patch0 -p1

%build
%cmake . \
	%{!?with_apidocs:-DBUILD_DOCUMENTATION=OFF} \
	-DBUILD_EXAMPLES=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/tawara-0

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.txt
%attr(755,root,root) %{_bindir}/tawara_info
%attr(755,root,root) %{_libdir}/libtawara.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/tawara-0
%{_pkgconfigdir}/tawara.pc
%{_libdir}/tawara
%{_datadir}/tawara-0

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/{_static,doxygen,*.html,*.js}
%endif
