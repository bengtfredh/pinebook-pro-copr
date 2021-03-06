# Maintainer: Dan Johansen <strit@manjaro.org>
# Contributor: Kevin Mihelich
# Contributor: Adam <adam900710@gmail.com>
Packager: Bengt Fredh <bengt@fredhs.net>

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
Source0: https://manjaro.moson.org/arm-stable/core/aarch64/uboot-pinebookpro-%{version}-%{sourcerelease}-aarch64.pkg.tar.xz

%global debug_package %{nil}

%description
U-Boot for Pinebook Pro.

%prep
%setup -c

%build

%install
mkdir %{buildroot}/boot -p
install -Dm644 ${RPM_BUILD_DIR}/%{name}-%{version}/boot/idbloader.img -t %{buildroot}/boot/
install -Dm644 ${RPM_BUILD_DIR}/%{name}-%{version}/boot/u-boot.itb -t %{buildroot}/boot/

%files
/boot/idbloader.img
/boot/u-boot.itb

%post
echo "A new U-Boot version can be flashed onto your install drive. Please use lsblk to determine your drive, before proceeding."
echo "You can do this by running:"
echo "# dd if=/boot/idbloader.img of=/dev/mmcblkX seek=64 conv=notrunc,fsync"
echo "# dd if=/boot/u-boot.itb of=/dev/mmcblkX seek=16384 conv=notrunc,fsync"

%preun

%changelog
* Thu Nov 05 2020 Bengt Fredh <bengt@fredhs.net> - 2020.10-1
- Edit postinstall script
* Sun Oct 11 2020 Bengt Fredh <bengt@fredhs.net> - 2020.07-2
- First version
