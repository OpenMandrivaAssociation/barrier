Summary:	An Open-source KVM software
Name:		barrier
Version:	2.4.0
Release:	1
License:	GPLv2
Group:		Utility
URL:		https://github.com/debauchee/%{name}
Source0:	%{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# https://github.com/debauchee/barrier/issues/1366
Patch0:	fix-includes.patch

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	imagemagick
BuildRequires:	librsvg
BuildRequires:	gulrak-filesystem-devel
BuildRequires:	pkgconfig(avahi-compat-libdns_sd)
BuildRequires:	pkgconfig(gmock)
BuildRequires:	pkgconfig(gtest)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	qt5-qtbase-devel

Requires: hicolor-icon-theme

%description
Barrier is software that mimics the functionality of a KVM switch, which
historically would allow you to use a single keyboard and mouse to control
multiple computers by physically turning a dial on the box to switch the
machine you're controlling at any given moment. Barrier does this in
software, allowing you to tell it which machine to control by moving your
mouse to the edge of the screen, or by using a keypress to switch focus to
a different system.

Barrier was forked from Symless's Synergy 1.9 codebase. Synergy was a
commercialized reimplementation of the original CosmoSynergy written by
Chris Schoeneman.

%files
%license LICENSE
%doc ChangeLog res/Readme.txt doc/barrier.conf.example*
%{_bindir}/%{name}*
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
#{_datadir}/pixmaps/%{name}.ico
%{_datadir}/applications/%{name}.desktop
%{_datadir}/metainfo/%{name}.appdata.xml
%{_mandir}/man1/%{name}*.1*

#----------------------------------------------------------------------------

%prep
%autosetup -p1

# remove test
sed -i -e 's/.*gtest.cmake/#&/' src/CMakeLists.txt

%build
%cmake . \
	-DBARRIER_BUILD_GUI:BOOL=ON \
    -DBARRIER_BUILD_INSTALLER:BOOL=OFF \
    -DBARRIER_BUILD_TESTS:BOOL=OFF \
	-DBARRIER_USE_EXTERNAL_GTEST:BOOL=OFF \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

# man
install -D -p -m 0644 doc/barrierc.1 %{buildroot}%{_mandir}/man1/barrierc.1
install -D -p -m 0644 doc/barriers.1 %{buildroot}%{_mandir}/man1/barriers.1

# icons
for d in 16 32 48 64 72 128 256
do
	install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/
	rsvg-convert -f png -h ${d} -w ${d} res/%{name}.svg \
			-o %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
#	convert -background none -size "${d}x${d}" res/%{name}.svg \
#			%{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
done
install -D -p -m 0644 res/%{name}.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
#install -D -p -m 0644 res/%{name}.ico %{buildroot}%{_datadir}/pixmaps/%{name}.ico

# .desktop
install -D -p -m 0644 res/barrier.desktop %{buildroot}%{_datadir}/applications/barrier.desktop

# .appstream
install -dm 0755 %{buildroot}%{_datadir}/metainfo
cat <<END> %{buildroot}%{_datadir}/metainfo/%{name}.appdata.xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2020 Ding-Yi Chen <dchen@redhat.com> -->
<component type="desktop-application">
  <id>%{name}</id>
  <metadata_license>FSFAP</metadata_license>
  <project_license>GPLv2</project_license>
  <name>%{name}</name>
  <summary>%{summary}</summary>

  <description>
    <p>%{description}</p>
  </description>

  <launchable type="desktop-id">%{name}.desktop</launchable>

  <url type="homepage">%{url}</url>

  <provides>
    <binary>barrier</binary>
    <binary>barrierc</binary>
    <binary>barriers</binary>
  </provides>

  <releases>
    <release version="%{version}" date="2021-11-02" />
  </releases>
</component>
END

