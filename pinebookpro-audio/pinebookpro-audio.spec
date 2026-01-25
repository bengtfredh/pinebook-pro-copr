# Maintainer: Bengt Fredh <bengt@fredhs.net>

%define name pinebookpro-audio
# renovate: datasource=git-refs depName=https://github.com/bengtfredh/pinebook-pro-copr.git currentValue=master
%define commit e3cce91a5e12ecc5c1b7dfdc7cf146db94b6a5f2
%define version 20201112
%define release 1%{?dist}

Summary: Pinebook Pro audio
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL2
URL: https://github.com/bengtfredh/pinebook-pro-copr.git
ExclusiveArch: aarch64
Source0: https://raw.githubusercontent.com/bengtfredh/pinebook-pro-copr/%{commit}/pinebookpro-audio/asound.state

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

%changelog
%autochangelog
