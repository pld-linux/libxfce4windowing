#
# Conditional build:
%bcond_without  apidocs         # gtk-doc documentation
%bcond_with     static_libs     # static library

Summary:	Windowing concept abstraction library for X11 and Wayland
Summary(pl.UTF-8):	Biblioteka abstrakcji koncepcji okien dla X11 i Wayland
Name:		libxfce4windowing
Version:	4.20.4
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://archive.xfce.org/src/xfce/libxfce4windowing/4.20/%{name}-%{version}.tar.bz2
# Source0-md5:	b27e6ebf153fbca5184147b6d3775762
Patch0:		%{name}-missing.patch
URL:		https://docs.xfce.org/xfce/libxfce4windowing/start
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gdk-pixbuf2-devel >= 2.42.8
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.72.0
BuildRequires:	gobject-introspection-devel >= 1.72.0
BuildRequires:	gtk+3-devel >= 3.24.10
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.30}
BuildRequires:	libdisplay-info-devel >= 0.1.1
BuildRequires:	libwnck-devel >= 3.14
BuildRequires:	meson >= 0.57.0
BuildRequires:	ninja
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	wayland-devel >= 1.20
BuildRequires:	wayland-protocols >= 1.25
BuildRequires:	xfce4-dev-tools >= 4.20.0
BuildRequires:	xorg-lib-libX11-devel >= 1.6.7
BuildRequires:	xorg-lib-libXrandr-devel >= 1.5.0
Requires:	gdk-pixbuf2 >= 2.42.8
Requires:	glib2 >= 1:2.72.0
Requires:	gtk+3 >= 3.24.10
Requires:	libdisplay-info >= 0.1.1
Requires:	libwnck >= 3.14
Requires:	wayland >= 1.20
Requires:	xfce4-dirs >= 4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libxfce4windowing is an abstraction library that attempts to present
windowing concepts (screens, toplevel windows, workspaces, etc.) in a
windowing-system-independent manner.

Currently, X11 is fully supported, via libwnck. Wayland is partially
supported, through various Wayland protocol extensions. However, the
full range of operations available on X11 is not available on Wayland,
due to missing features in these protocol extensions.

%description -l pl.UTF-8
Libxfce4windowing to biblioteka abstrakcji, która próbuje przedstawić
koncepcje okienkowania (ekrany, okna najwyższego poziomu, obszary
robocze itp.) w sposób niezależny od systemu okienkowania.

Obecnie X11 jest w pełni obsługiwany za pośrednictwem libwnck. Wayland
jest częściowo obsługiwany za pośrednictwem różnych rozszerzeń
protokołu Wayland. Jednak pełny zakres operacji dostępnych w X11 nie
jest dostępny w Wayland, z powodu braku funkcji w tych rozszerzeniach
protokołu.

%package devel
Summary:	Development files for libxfce4util library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libxfce4util
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.72.0
Requires:	gtk+3-devel >= 3.24.10

%description devel
Development files for the libxfce4windowing library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libxfce4windowing.

%package static
Summary:	Static libxfce4windowing library
Summary(pl.UTF-8):	Statyczna biblioteka libxfce4windowing
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libxfce4util library.

%description static -l pl.UTF-8
Statyczna biblioteka libxfce4util.

%package apidocs
Summary:	libxfce4windowing API documentation
Summary(pl.UTF-8):	Dokumentacja API libxfce4util
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
libxfce4util API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libxfce4util.

%prep
%setup -q
%patch -P0 -p1

%build
%meson \
	%{!?with_static_libs:--default-library=shared} \
	%{?with_apidocs:-Dgtk-doc=true} \
	-Dwayland=enabled \
	-Dx11=enabled

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

# not supported by glibc (as of 2.32)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_libdir}/libxfce4windowing-0.so.*.*.*
%ghost %{_libdir}/libxfce4windowing-0.so.0
%attr(755,root,root) %{_libdir}/libxfce4windowingui-0.so.*.*.*
%ghost %{_libdir}/libxfce4windowingui-0.so.0
%{_libdir}/girepository-1.0/Libxfce4windowing-0.0.typelib
%{_libdir}/girepository-1.0/Libxfce4windowingui-0.0.typelib

%files devel
%defattr(644,root,root,755)
%{_libdir}/libxfce4windowing-0.so
%{_libdir}/libxfce4windowingui-0.so
%dir %{_includedir}/xfce4
%{_includedir}/xfce4/libxfce4windowing-0
%{_pkgconfigdir}/libxfce4windowing-0.pc
%{_pkgconfigdir}/libxfce4windowing-x11-0.pc
%{_pkgconfigdir}/libxfce4windowingui-0.pc
%{_datadir}/gir-1.0/Libxfce4windowing-0.0.gir
%{_datadir}/gir-1.0/Libxfce4windowingui-0.0.gir

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libxfce4windowing-0.a
%{_libdir}/libxfce4windowingui-0.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libxfce4windowing-0
%{_gtkdocdir}/libxfce4windowingui-0
%endif
