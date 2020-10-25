# Fedorish Kernel Pinebook Pro
Packager: Bengt Fredh <bengt@fredhs.net> 

%define linuxrel 5.8
%define version 5.8.14
%define sourcerelease 1
%define release %{sourcerelease}%{?dist}
%define srcdir ${RPM_SOURCE_DIR}/manjaro-linux

Summary: Kernel Pinebook Pro
Name: kernel-pbp
Version: %{version}
Release: %{release}
Group: System Environment/Kernel
License: GPL2
URL: https://git.kernel.org/
ExclusiveArch: aarch64
BuildRequires: git-core gcc flex bison openssl-devel bc perl openssl kmod
Source0: https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-%{linuxrel}.tar.xz
Source1: https://raw.githubusercontent.com/bengtfredh/pinebook-pro-copr/test/kernel-pbp/config
Patch0: https://cdn.kernel.org/pub/linux/kernel/v5.x/patch-%{version}.xz
Requires: kernel-pbp-core = %{version}
Requires: kernel-pbp-modules = %{version}

%global debug_package %{nil}

%description
Vanilla kernel with Fedora config patched for Pinebook Pro.

%prep
# Clone Manjaro patches and checkout correct commit
git clone https://gitlab.manjaro.org/manjaro-arm/packages/core/linux.git %{srcdir}
cd %{srcdir}
git checkout 4e603f4e710b1820e506e54a95c2e0a68b4765c3

# Unpack and apply base patches
%setup -c
cd linux-%{linuxrel}
%patch -P 0 -p1

# ALARM patches
patch -Np1 -i "%{srcdir}/0001-net-smsc95xx-Allow-mac-address-to-be-set-as-a-parame.patch"             #All

# Manjaro ARM Patches
patch -Np1 -i "%{srcdir}/0007-pbp-support.patch"                                                      #Pinebook Pro
patch -Np1 -i "%{srcdir}/0009-drm-bridge-analogix_dp-Add-enable_psr-param.patch"                      #Pinebook Pro
patch -Np1 -i "%{srcdir}/0017-mmc-core-Add-MMC-Command-Queue-Support-kernel-parame.patch"             #All
patch -Np1 -i "%{srcdir}/0019-revert-fbcon-remove-now-unusued-softback_lines-cursor-argument.patch"   #All
patch -Np1 -i "%{srcdir}/0020-revert-fbcon-remove-soft-scrollback-code.patch"                         #All
patch -Np1 -i "%{srcdir}/0020-nuumio-panfrost-Silence-Panfrost-gem-shrinker-loggin.patch"             #Panfrost
patch -Np1 -i "%{srcdir}/0021-pwm-rockchip-Keep-enabled-PWMs-running-while-probing.patch"             #Rockchip

# Pinebook patches
patch -Np1 -i "%{srcdir}/0001-Bluetooth-Add-new-quirk-for-broken-local-ext-features.patch"            #Bluetooth
patch -Np1 -i "%{srcdir}/0002-Bluetooth-btrtl-add-support-for-the-RTL8723CS.patch"                    #Bluetooth
patch -Np1 -i "%{srcdir}/0003-arm64-allwinner-a64-enable-Bluetooth-On-Pinebook.patch"                 #Bluetooth
patch -Np1 -i "%{srcdir}/0004-drm-sun8i-ui-vi-Fix-layer-zpos-change-atomic-modesetting.patch"         #Hardware cursor
patch -Np1 -i "%{srcdir}/0005-drm-sun4i-Mark-one-of-the-UI-planes-as-a-cursor-one.patch"              #Hardware cursor
patch -Np1 -i "%{srcdir}/0006-drm-sun4i-drm-Recover-from-occasional-HW-failures.patch"                #Hardware cursor
patch -Np1 -i "%{srcdir}/0007-arm64-dts-allwinner-enable-bluetooth-pinetab-pinepho.patch"             #Bluetooth on PineTab and PinePhone

# add sourcerelease to extraversion
sed -ri "s|^(EXTRAVERSION =)(.*)|\1 \2-%{sourcerelease}|" Makefile

# don't run depmod on 'make install'. We'll do this ourselves in packaging
sed -i '2iexit 0' scripts/depmod.sh

# merge Manjaro config with Fedora config as base
sed -i '/MANJARO/d' %{srcdir}/config
sed -i '/APPARMOR/d' %{srcdir}/config
sed -i '/SELINUX/d' %{srcdir}/config
sed -i '/BOOTSPLASH/d' %{srcdir}/config
sed -i '/BTRFS/d' %{srcdir}/config
./scripts/kconfig/merge_config.sh ${RPM_SOURCE_DIR}/config %{srcdir}/config

KARCH=arm64

# Make config accept all default
make -j `nproc` olddefconfig

%build
# Build kernel
cd linux-%{linuxrel}
unset LDFLAGS
make arch=arm64 -j `nproc` Image Image.gz modules
# Generate device tree blobs with symbols to support applying device tree overlays in U-Boot
make arch=arm64 -j `nproc` DTC_FLAGS="-@" dtbs

%install
mkdir -p %{buildroot}/{boot,usr/lib/modules}
cd ${RPM_BUILD_DIR}/%{name}-%{version}/linux-%{linuxrel}
make arch=arm64 -j `nproc` INSTALL_MOD_PATH=%{buildroot}/usr modules_install
make arch=arm64 -j `nproc` INSTALL_DTBS_PATH=%{buildroot}/boot/dtbs dtbs_install
cp arch/arm64/boot/Image{,.gz} %{buildroot}/boot

# get kernel version
_kernver="$(make kernelrelease)"

# remove build and source links
rm %{buildroot}/usr/lib/modules/${_kernver}/{source,build}

# now we call depmod
depmod -b %{buildroot}/usr -F System.map ${_kernver}

# add vmlinux
install -Dt %{buildroot}/usr/lib/modules/${_kernver}/build -m644 vmlinux

%files

%package core
Summary: Kernel Pinebook Pro Core
Group: System Environment/Kernel
%description core
Vanilla kernel Core patched for Pinebook Pro.
%files core
/boot/*

%package modules
Summary: Kernel Pinebook Pro Modules
Group: System Environment/Kernel
%description modules
Vanilla kernel Modules with patched for Pinebook Pro.
%files modules
/usr/lib/modules/*

%post
dracut -f --kernel-image /boot/Image /boot/initramfs-linux.img --kver %{version}-%{sourcerelease}

%changelog
* Sun Oct 25 2020 Bengt Fredh <bengt@fredhs.net> - 5.8.14-1
- First version
