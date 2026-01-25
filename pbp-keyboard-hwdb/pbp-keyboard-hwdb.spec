# Credits: Dan Johansen <strit@manjaro.org>
Packager: Bengt Fredh <bengt@fredhs.net>

%define name pbp-keyboard-hwdb
# renovate: datasource=git-refs depName=https://gitlab.manjaro.org/manjaro-arm/packages/community/pinebookpro-post-install.git currentValue=master
%define commit 20740eb361f24d5a52568888096390bf164c6438
%define version 20220720
%define release 1%{?dist}

Summary: Pinebook Pro keyboard hwdb
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL2
URL: https://gitlab.manjaro.org/manjaro-arm/packages/community/pinebookpro-post-install.git
ExclusiveArch: aarch64
Source0: https://gitlab.manjaro.org/manjaro-arm/packages/community/pinebookpro-post-install/-/raw/%{commit}/10-usb-keyboard.hwdb

%global debug_package %{nil}

%description
Hwdb configuration for Pinebook Pro keyboard.

%prep
%setup -c -T

%build

%install
mkdir %{buildroot}/etc/udev/hwdb.d -p
install -Dm644 ${RPM_SOURCE_DIR}/10-usb-keyboard.hwdb -t %{buildroot}/etc/udev/hwdb.d/

%files
%config /etc/udev/hwdb.d/10-usb-keyboard.hwdb

%changelog
%autochangelog
