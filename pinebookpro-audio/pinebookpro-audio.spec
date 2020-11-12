Packager: Bengt Fredh <bengt@fredhs.net>

%define name pinebookpro-audio
%define version 2
%define sourcerelease 1
%define release %{sourcerelease}%{?dist}

Summary: Pinebook Pro audio
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL2
URL: https://github.com/bengtfredh/pinebook-pro-copr.git
ExclusiveArch: aarch64
Source0: https://raw.githubusercontent.com/bengtfredh/pinebook-pro-copr/master/pinebookpro-audio/asound.state

%global debug_package %{nil}

%description
Patches for Pinebook Pro audio.

%prep

%setup -c -T

%install
mkdir %{buildroot}/var/lib/alsa/ -p
install -Dm644 ${RPM_SOURCE_DIR}/asound.state -t %{buildroot}/var/lib/alsa/

%files
%config(noreplace) /var/lib/alsa/asound.state

%post

%preun

%changelog
* Thu Nov 12 2020 Bengt Fredh <bengt@fredhs.net> - 2-1
- Fix errors
* Mon Oct 12 2020 Bengt Fredh <bengt@fredhs.net> - 1-2
- First version
