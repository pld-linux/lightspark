# TODO
# - fix linking
Summary:	Lightspark - a modern, free, open-source flash player implementation
Name:		lightspark
Version:	0.4.4.3
Release:	0.4
License:	GPL v3
Group:		X11/Applications/Multimedia
Source0:	http://edge.launchpad.net/lightspark/trunk/lightspark-0.4.4/+download/%{name}-%{version}.tar.gz
# Source0-md5:	efd2e91d36ffa38c9befa25af5eaac20
URL:		http://lightspark.sourceforge.net/
BuildRequires:	SDL-devel
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake
BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	curl-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	fontconfig-devel
BuildRequires:	ftgl-devel
BuildRequires:	gcc >= 6:4.4
BuildRequires:	gettext
BuildRequires:	glew-devel >= 1.5.4
BuildRequires:	gtkglext-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	libxml++-devel
BuildRequires:	llvm-devel >= 2.7
BuildRequires:	nasm
BuildRequires:	pcre-cxx-devel
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
BuildRequires:	rpmbuild(macros) >= 1.583
BuildRequires:	xulrunner-devel >= 1.9.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Unresolved symbols found in: /usr/lib64/lightspark/liblightspark.so.0.4.4
#        rt sys av_free pt
%define         skip_post_check_so      liblightspark.so.0.4

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

install -d build

%build
cd build
%cmake \
	-DAUDIO_BACKEND=pulse \
	-DCOMPILE_PLUGIN=1 \
	-DLIB_INSTALL_DIR=%{_lib} \
	-DPLUGIN_DIRECTORY=%{_browserpluginsdir} \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --all-name

# rename because we need only SONAME being available
mv $RPM_BUILD_ROOT%{_libdir}/lightspark/liblightspark.so.{0.4.*,0.4}
rm $RPM_BUILD_ROOT%{_libdir}/lightspark/liblightspark.so

# weird size
rm -rf $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/20x20
rm -f $RPM_BUILD_ROOT%{_iconsdir}/hicolor/scalable/apps/lightspark.svg

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
%attr(755,root,root) %{_libdir}/lightspark/liblightspark.so.*.*

%dir %{_libdir}/lightspark/plugins
%attr(755,root,root) %{_libdir}/lightspark/plugins/liblightsparkpulseplugin.so

%{_datadir}/lightspark
%{_mandir}/man1/lightspark.1*
%{_desktopdir}/lightspark.desktop
%{_iconsdir}/hicolor/*/apps/lightspark.png

%files -n browser-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_browserpluginsdir}/liblightsparkplugin.so
