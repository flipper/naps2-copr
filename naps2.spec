Name:           naps2
Version:        8.2.1
Release:        1%{?dist}
Summary:        NAPS2 GTK desktop application

License:        GPL-2.0-or-later
URL:            https://www.naps2.com/
Source0:        https://codeload.github.com/cyanfish/naps2/tar.gz/refs/tags/v%{version}

ExclusiveArch:  x86_64 aarch64

BuildRequires:  dotnet-sdk-9.0
BuildRequires:  gtk3-devel

Requires:       gtk3
AutoReqProv:    no

%description
NAPS2 (Not Another PDF Scanner 2) is a document scanning application.
This package builds and ships the GTK desktop application.

%ifarch x86_64
%global dotnet_rid linux-x64
%endif
%ifarch aarch64
%global dotnet_rid linux-arm64
%endif

# Keep RPM post-processing from mutating the .NET single-file apphost bundle.
%define __spec_install_post %{nil}
%define debug_package %{nil}
%define __os_install_post %{_dbpath}/brp-compress

%prep
%autosetup -n naps2-%{version}

%build
dotnet restore NAPS2.App.Gtk/NAPS2.App.Gtk.csproj

dotnet publish NAPS2.App.Gtk/NAPS2.App.Gtk.csproj \
    -c Release \
    -r %{dotnet_rid} \
    --self-contained \
    -p:DebugType=None \
    -p:DebugSymbols=false \
    -o %{_builddir}/publish

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/naps2
cp -a %{_builddir}/publish/. %{buildroot}%{_libdir}/naps2/

install -d %{buildroot}%{_bindir}
ln -s "$(realpath --relative-to=%{buildroot}%{_bindir} %{buildroot}%{_libdir}/naps2/naps2)" %{buildroot}%{_bindir}/naps2

install -d %{buildroot}%{_datadir}/applications
install -pm 0644 NAPS2.Setup/config/linux/com.naps2.Naps2.desktop \
    %{buildroot}%{_datadir}/applications/

install -d %{buildroot}%{_datadir}/metainfo
install -pm 0644 NAPS2.Setup/config/linux/com.naps2.Naps2.metainfo.xml \
    %{buildroot}%{_datadir}/metainfo/

install -d %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
install -pm 0644 NAPS2.Lib/Icons/scanner-128.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/com.naps2.Naps2.png

%files
%license LICENSE
%doc README.md
%{_bindir}/naps2
%{_libdir}/naps2/
%{_datadir}/applications/com.naps2.Naps2.desktop
%{_datadir}/metainfo/com.naps2.Naps2.metainfo.xml
%{_datadir}/icons/hicolor/128x128/apps/com.naps2.Naps2.png
