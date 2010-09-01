Summary:	Lightspark - a modern, free, open-source flash player implementation
Name:		lightspark
Version:	0.4.4
Release:	0.1
License:	GPL v3
Group:		X11/Applications/Multimedia
Source0:	http://launchpad.net/lightspark/trunk/lightspark-0.4.4/+download/%{name}-%{version}.tar.gz
# Source0-md5:	6e063d3ee6a566c70cfff614b56fee25
Patch0:		libdir.patch
URL:		http://lightspark.sourceforge.net/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake
BuildRequires:	ffmpeg-devel
BuildRequires:	ftgl-devel
BuildRequires:	glew-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	llvm-devel
BuildRequires:	nasm
BuildRequires:	pcre-cxx-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lightspark is a modern, free, open-source flash player implementation.

%package -n browser-plugin-%{name}
Summary:	Browser plugin for Flash rendering
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	browser-plugins >= 2.0
Requires:	browser-plugins(%{_target_base_arch})
Provides:	browser(flash)

%description -n browser-plugin-%{name}
Browser plugin for rendering Flash content using Lightspark.

%prep
%setup -q
%patch0 -p1
mkdir objs

%build
cd objs
cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_BUILD_TYPE=Release \
	-DCOMPILE_PLUGIN=1 \
	-DLIB_INSTALL_DIR=%{_lib} \
	-DPLUGIN_DIRECTORY=%{_browserpluginsdir} \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

cd objs
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
cd ..

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post -n browser-plugin-%{name}
%update_browser_plugins

%postun -n browser-plugin-%{name}
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog README TODO
%attr(755,root,root) %{_bindir}/lightspark
%attr(755,root,root) %{_bindir}/tightspark
%dir %{_libdir}/lightspark
%attr(755,root,root) %{_libdir}/lightspark/liblightspark.so.*.*.*
%attr(755,root,root) %{_libdir}/lightspark/liblightspark.so.*.*
%attr(755,root,root) %{_libdir}/lightspark/liblightspark.so
%{_datadir}/lightspark
%{_mandir}/man1/lightspark.1*

%files -n browser-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_browserpluginsdir}/liblightsparkplugin.so
