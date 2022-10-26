# AArch64 multi-platform
# Contributor: Kevin Mihelich <kevin@archlinuxarm.org>
# Maintainer: Dan Johansen <strit@manjaro.org>
Packager: Bengt Fredh <bengt@fredhs.net>

%define version 6.0.2
%define sourcerelease 3
%define release %{sourcerelease}%{?dist}

Summary: AArch64 multi-platform
Name: linux-manjaro
Version: %{version}
Release: %{release}
License: GPL2
URL: https://gitlab.manjaro.org/manjaro-arm/packages/core/linux.git
ExclusiveArch: aarch64
Source0: https://manjaro.moson.eu/arm-stable/core/aarch64/linux-%{version}-%{sourcerelease}-aarch64.pkg.tar.zst

%global debug_package %{nil}

%description
Manjaro kernel patched for Pinebook Pro and more.

%prep
%setup -c -T

%build

%install
tar -xvpf $RPM_SOURCE_DIR/linux-%{version}-%{sourcerelease}-aarch64.pkg.tar.zst -C %{buildroot} --exclude .PKGINFO --exclude .INSTALL --exclude .MTREE --exclude .BUILDINFO --exclude usr/share --exclude etc/mkinitcpio.d

%files
/boot/*
/usr/lib/modules/*

%post
dracut -f --kernel-image /boot/Image /boot/initramfs-linux.img --kver %{version}-%{sourcerelease}-MANJARO-ARM 1> /dev/null 2>&1

%changelog
%autochangelog
