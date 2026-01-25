# Maintainer: Bengt Fredh <bengt@fredhs.net>

%define name pbp-keyboard-hwdb
%define version 20200629
%define sourcerelease 1
%define release %{sourcerelease}%{?dist}

Summary: Pinebook Pro keyboard hwdb
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL2
URL: https://gitlab.manjaro.org/manjaro-arm/packages/community/pinebookpro-post-install.git
ExclusiveArch: aarch64
Source0: https://gitlab.manjaro.org/manjaro-arm/packages/community/pinebookpro-post-install/-/raw/master/10-usb-kbd.hwdb

%global debug_package %{nil}

%description
Hwdb configuration for Pinebook Pro keyboard.

%prep
%setup -c -T

%build

%install
mkdir %{buildroot}/etc/udev/hwdb.d -p
install -Dm644 ${RPM_SOURCE_DIR}/10-usb-kbd.hwdb -t %{buildroot}/etc/udev/hwdb.d/

%files
%config /etc/udev/hwdb.d/10-usb-kbd.hwdb

%changelog
%autochangelog
