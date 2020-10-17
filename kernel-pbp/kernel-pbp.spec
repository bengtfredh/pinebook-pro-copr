# AArch64 multi-platform
# Maintainer: Bengt Fredh <bengt@fredhs.net> 

%define linuxrel 5.8
%define version 5.8.14
%define sourcerelease 1
%define release %{sourcerelease}%{?dist}
%define srcdir ${RPM_SOURCE_DIR}/manjaro-linux

Summary: AArch64 multi-platform
Name: kernel-pbp
Version: %{version}
Release: %{release}
License: GPL2
URL: https://git.kernel.org/
ExclusiveArch: aarch64
BuildRequires: git-core
Source0: https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-%{linuxrel}.tar.xz
Source1: https://raw.githubusercontent.com/bengtfredh/pinebook-pro-copr/test/kernel-pbp/config
Patch0: https://cdn.kernel.org/pub/linux/kernel/v5.x/patch-%{version}.xz

%global debug_package %{nil}

%description
Vanilla kernel patched for Pinebook Pro.

%prep
git clone https://gitlab.manjaro.org/manjaro-arm/packages/core/linux.git %{srcdir}
cd %{srcdir}
git checkout 4e603f4e710b1820e506e54a95c2e0a68b4765c3
cd ${RPM_SOURCE_DIR}
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
patch -Np1 -i "%{srcdir}/0021-pwm-rockchip-Keep-enabled-PWMs-running-while-probing.patch"				#Rockchip

# Pinebook patches
patch -Np1 -i "%{srcdir}/0001-Bluetooth-Add-new-quirk-for-broken-local-ext-features.patch"            #Bluetooth
patch -Np1 -i "%{srcdir}/0002-Bluetooth-btrtl-add-support-for-the-RTL8723CS.patch"                    #Bluetooth
patch -Np1 -i "%{srcdir}/0003-arm64-allwinner-a64-enable-Bluetooth-On-Pinebook.patch"                 #Bluetooth
patch -Np1 -i "%{srcdir}/0004-drm-sun8i-ui-vi-Fix-layer-zpos-change-atomic-modesetting.patch"         #Hardware cursor
patch -Np1 -i "%{srcdir}/0005-drm-sun4i-Mark-one-of-the-UI-planes-as-a-cursor-one.patch"              #Hardware cursor
patch -Np1 -i "%{srcdir}/0006-drm-sun4i-drm-Recover-from-occasional-HW-failures.patch"                #Hardware cursor
patch -Np1 -i "%{srcdir}/0007-arm64-dts-allwinner-enable-bluetooth-pinetab-pinepho.patch"             #Bluetooth on PineTab and PinePhone

cat ${RPM_SOURCE_DIR}/config ${RPM_BUILD_DIR}/%{name}-%{linuxrel}/.config

%build
cd ${RPM_BUILD_DIR}/%{name}-%{linuxrel}
unset LDFLAGS
make ${MAKEFLAGS} Image Image.gz modules
make ${MAKEFLAGS} DTC_FLAGS="-@" dtbs

%install
cd ${RPM_BUILD_DIR}/%{name}-%{linuxrel}
mkdir -p %{buildroot}/{boot,usr/lib/modules}
make INSTALL_MOD_PATH=%{buildroot}/usr modules_install
make INSTALL_DTBS_PATH=%{buildroot}/boot/dtbs dtbs_install
cp arch/$KARCH/boot/Image{,.gz} %{buildroot}/boot

%files
/boot/
/usr/lib/modules/

%post
#dracut -f --kernel-image /boot/Image /boot/initramfs-linux.img --kver %{version}-%{sourcerelease}-pbp

%changelog
* Sat Oct 17 2020 Bengt Fredh <bengt@fredhs.net> - 5.8.14-1
- First version
