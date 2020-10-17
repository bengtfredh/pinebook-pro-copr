# AArch64 multi-platform
# Maintainer: Bengt Fredh <bengt@fredhs.net> 

%define linuxrel 5.8
%define version 5.8.14
%define sourcerelease 1
%define release %{sourcerelease}%{?dist}

Summary: AArch64 multi-platform
Name: linux-pbp
Version: %{version}
Release: %{release}
License: GPL2
URL: https://git.kernel.org/
ExclusiveArch: aarch64
Source0: https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-%{linuxrel}.tar.xz
Patch0: https://cdn.kernel.org/pub/linux/kernel/v5.x/patch-%{version}.xz

%global debug_package %{nil}

%description
Vanilla kernel patched for Pinebook Pro.

%prep
%setup -c

%build

%install

%files

%post
#dracut -f --kernel-image /boot/Image /boot/initramfs-linux.img --kver %{version}-%{sourcerelease}-pbp

%changelog
* Sat Oct 17 2020 Bengt Fredh <bengt@fredhs.net> - 5.8.14-1
- First version
