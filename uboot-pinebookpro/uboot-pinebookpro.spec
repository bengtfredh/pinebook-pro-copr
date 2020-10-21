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
Source1: https://github.com/bengtfredh/pinebook-pro-copr/blob/test/uboot-pinebookpro/extlinux.conf

%global debug_package %{nil}

%description
U-Boot for Pinebook Pro.

%prep
%setup -c

%build

%install
mkdir %{buildroot}/boot/extlinux -p
install -Dm644 ${RPM_BUILD_DIR}/%{name}-%{version}/boot/idbloader.img -t %{buildroot}/boot/
install -Dm644 ${RPM_BUILD_DIR}/%{name}-%{version}/boot/u-boot.itb -t %{buildroot}/boot/
install -Dm644 ${RPM_SOURCE_DIR}/extlinux.conf -t %{buildroot}/boot/extlinux/

%files
/boot/idbloader.img
/boot/u-boot.itb
%config(noreplace) /boot/extlinux/extlinux.conf

%post
if [ ! -f /boot/extlinux/extlinux.conf.rpmnew ]; then
# Get UUID for rootdisk
ROOTUUID=$(findmnt / -o UUID -n)
# Edit extlinux.conf
sed -i -e "s!APPEND.*!APPEND console=tty1 console=ttyS2,1500000 root=UUID=${ROOTUUID} rw rhgb quiet !g" ${TMPDIR}/root/boot/extlinux/extlinux.conf
fi

echo "A new U-Boot version can be flashed onto your install drive. Please use lsblk to determine your drive, before proceeding."
echo "You can do this by running:"
echo "# dd if=/boot/idbloader.img of=/dev/mmcblkX seek=64 conv=notrunc,fsync"
echo "# dd if=/boot/u-boot.itb of=/dev/mmcblkX seek=16384 conv=notrunc,fsync"


%preun

%changelog
* Sun Oct 11 2020 Bengt Fredh <bengt@fredhs.net> - 2020.07-2
- First version
