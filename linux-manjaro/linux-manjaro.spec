# AArch64 multi-platform
# Contributor: Kevin Mihelich <kevin@archlinuxarm.org>
# Maintainer: Dan Johansen <strit@manjaro.org>

%define version 5.8.14
%define sourcerelease 1
%define release %{sourcerelease}%{?dist}

Summary: AArch64 multi-platform
Name: linux-manjaro
Version: %{version}
Release: %{release}
License: GPL2
URL: https://gitlab.manjaro.org/manjaro-arm/packages/core/linux.git
ExclusiveArch: aarch64
Source0: https://manjaro.moson.org/arm-stable/core/aarch64/linux-%{version}-%{sourcerelease}-aarch64.pkg.tar.xz

%global debug_package %{nil}

%description
Manjaro kernel patched for Pinebook Pro and more.

%prep
%setup -c -T

%build

%install
tar -xvpf $RPM_SOURCE_DIR/linux-%{version}-%{sourcerelease}-aarch64.pkg.tar.xz -C %{buildroot} --exclude .PKGINFO --exclude .INSTALL --exclude .MTREE --exclude .BUILDINFO --exclude usr/share --exclude etc/mkinitcpio.d

%files
/boot/*
/usr/lib/modules/*

%post
dracut -f --kernel-image /boot/Image /boot/initramfs-linux.img --kver %{version}-%{sourcerelease}-MANJARO-ARM

%changelog
* Fro Oct 16 2020 Bengt Fredh <bengt@fredhs.net> - 5.8.14-1
- Bump version
* Wed Sep 30 2020 Bengt Fredh <bengt@fredhs.net> - 5.8.10-2
- First version
