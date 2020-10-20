# Maintainer: Dan Johansen <strit@manjaro.org>
# Contributor: Kevin Mihelich
# Contributor: Adam <adam900710@gmail.com>

%define name uboot-pinebookpro
%define version 2020.10
%define sourcerelease 1
%define release %{sourcerelease}%{?dist}

Summary: U-Boot Pinebook Pro 
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL2
URL: https://gitlab.manjaro.org/manjaro-arm/packages/core/uboot-pinebookpro.git
ExclusiveArch: aarch64
Source0: https://manjaro.moson.org/arm-testing/core/aarch64/%{name}-%{version}-%{sourcerelease}-aarch64.pkg.tar.xz

%global debug_package %{nil}

%description
U-Boot for Pinebook Pro.

%prep
%setup -c

%build
sed -i 's/LABEL Manjaro ARM/LABEL Fedora ARM/' ${RPM_BUILD_DIR}/%{name}-%{version}/boot/extlinux/extlinux.conf

%install
mkdir %{buildroot}/boot/extlinux -p
install -Dm644 ${RPM_BUILD_DIR}/%{name}-%{version}/boot/idbloader.img -t %{buildroot}/boot/
install -Dm644 ${RPM_BUILD_DIR}/%{name}-%{version}/boot/u-boot.itb -t %{buildroot}/boot/
install -Dm644 ${RPM_BUILD_DIR}/%{name}-%{version}/boot/extlinux/extlinux.conf -t %{buildroot}/boot/extlinux/

%files
/boot/idbloader.img
/boot/u-boot.itb
%config /boot/extlinux/extlinux.conf

%post

%preun

%changelog
* Sun Oct 11 2020 Bengt Fredh <bengt@fredhs.net> - 2020.07-2
- First version
