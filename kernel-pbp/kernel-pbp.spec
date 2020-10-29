# Fedoraish Kernel Pinebook Pro
Packager: Bengt Fredh <bengt@fredhs.net> 

%define linuxrel 5.9
%define version 5.9.1
%define sourcerelease 3
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
Source1: https://raw.githubusercontent.com/bengtfredh/pinebook-pro-copr/master/kernel-pbp/config
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
git checkout 3ce552608175131a55cb7a26cf80ec6780ae34fd

# Unpack and apply base patches
%setup -c
cd linux-%{linuxrel}
%patch -P 0 -p1

  # ALARM patches
  patch -Np1 -i "%{srcdir}/0001-net-smsc95xx-Allow-mac-address-to-be-set-as-a-parame.patch"             #All
  patch -Np1 -i "%{srcdir}/0002-arm64-dts-rockchip-add-usb3-controller-node-for-RK33.patch"             #RK3328
  patch -Np1 -i "%{srcdir}/0003-arm64-dts-rockchip-enable-usb3-nodes-on-rk3328-rock6.patch"             #RK3328
  
  # Manjaro ARM Patches
  patch -Np1 -i "%{srcdir}/0001-arm64-dts-rockchip-add-pcie-node-rockpi4.patch"                         #Rock Pi 4
  patch -Np1 -i "%{srcdir}/0002-arm64-dts-rockchip-modify-pcie-node-rockpro64.patch"                    #RockPro64
  patch -Np1 -i "%{srcdir}/0003-text_offset.patch"                                                      #Amlogic
  patch -Np1 -i "%{srcdir}/0004-board-rockpi4-dts-upper-port-host.patch"                                #Rock Pi 4
  patch -Np1 -i "%{srcdir}/0005-arm64-dts-rockchip-add-HDMI-sound-node-for-rk3328-ro.patch"             #Rock64
  patch -Np1 -i "%{srcdir}/0006-arm64-dts-allwinner-add-hdmi-sound-to-pine-devices.patch"               #Pine64
  patch -Np1 -i "%{srcdir}/0007-pbp-support.patch"                                                      #Pinebook Pro
  patch -Np1 -i "%{srcdir}/0008-arm64-dts-allwinner-add-ohci-ehci-to-h5-nanopi.patch"                   #Nanopi Neo Plus 2
  patch -Np1 -i "%{srcdir}/0009-drm-bridge-analogix_dp-Add-enable_psr-param.patch"                      #Pinebook Pro
  patch -Np1 -i "%{srcdir}/0010-PCI-rockchip-Fix-PCIe-probing-in-5.9.patch"                             #Rk3399
  patch -Np1 -i "%{srcdir}/0011-arm64-dts-amlogic-add-odroid-n2-plus.patch"                             #Odroid N2+
  patch -Np1 -i "%{srcdir}/0012-pwm-rockchip-Keep-enabled-PWMs-running-while-probing.patch"             #Rockchip
  patch -Np1 -i "%{srcdir}/0013-nuumio-panfrost-Silence-Panfrost-gem-shrinker-loggin.patch"             #Panfrost
  patch -Np1 -i "%{srcdir}/0014-drm-panfrost-add-Amlogic-integration-quirks.patch"                      #Panfrost
  patch -Np1 -i "%{srcdir}/0015-drm-panfrost-Coherency-support.patch"                                   #Panfrost
  patch -Np1 -i "%{srcdir}/0016-arm64-dts-meson-add-audio-playback-to-odroid-c2.patch"                  #Odroid C2
  patch -Np1 -i "%{srcdir}/0018-arm64-dts-rockchip-Mark-rock-pi-4-as-rock-pi-4a-dts.patch"              #Rock Pi 4A
  patch -Np1 -i "%{srcdir}/0019-arm64-dts-rockchip-Add-Radxa-ROCK-Pi-4B-support.patch"                  #Rock Pi 4B
  patch -Np1 -i "%{srcdir}/0020-arm64-dts-rockchip-Add-Radxa-ROCK-Pi-4C-support.patch"                  #Rock Pi 4C
  patch -Np1 -i "%{srcdir}/0021-arm64-dts-rockchip-Add-Firefly-Station-p1-support.patch"                #Firelfy Station P1
  patch -Np1 -i "%{srcdir}/0022-typec-displayport-some-devices-have-pin-assignments-reversed.patch"     #DP Alt Mode
  patch -Np1 -i "%{srcdir}/0023-usb-typec-tcpm-Add-generic-extcon-for-tcpm-enabled-devices.patch"       #DP Alt mode
  patch -Np1 -i "%{srcdir}/0024-usb-typec-tcpm-Add-generic-extcon-to-tcpm.patch"						#DP Alt mode
  patch -Np1 -i "%{srcdir}/0025-dts-rockpro64-add-type-c-DP-ALT-and-USB3.patch"							#DP Alt mode - RockPro64
  
  # Pinebook patches
  patch -Np1 -i "%{srcdir}/0001-Bluetooth-Add-new-quirk-for-broken-local-ext-features.patch"            #Bluetooth
  patch -Np1 -i "%{srcdir}/0002-Bluetooth-btrtl-add-support-for-the-RTL8723CS.patch"                    #Bluetooth
  patch -Np1 -i "%{srcdir}/0003-arm64-allwinner-a64-enable-Bluetooth-On-Pinebook.patch"                 #Bluetooth
  patch -Np1 -i "%{srcdir}/0004-drm-sun8i-ui-vi-Fix-layer-zpos-change-atomic-modesetting.patch"         #Hardware cursor
  patch -Np1 -i "%{srcdir}/0005-drm-sun4i-Mark-one-of-the-UI-planes-as-a-cursor-one.patch"              #Hardware cursor
  patch -Np1 -i "%{srcdir}/0006-drm-sun4i-drm-Recover-from-occasional-HW-failures.patch"                #Hardware cursor
  patch -Np1 -i "%{srcdir}/0007-arm64-dts-allwinner-enable-bluetooth-pinetab-pinepho.patch"             #Bluetooth on PineTab and PinePhone
  patch -Np1 -i "%{srcdir}/0008-switch-to-new-display-on-pinetab.patch"                                 #PineTab

# add sourcerelease to extraversion
sed -ri "s|^(EXTRAVERSION =)(.*)|\1 \2-%{sourcerelease}|" Makefile

# don't run depmod on 'make install'. We'll do this ourselves in packaging
sed -i '2iexit 0' scripts/depmod.sh

# merge Manjaro config with Fedora config as base
sed -i '/MANJARO/d' %{srcdir}/config
sed -i '/APPARMOR/d' %{srcdir}/config
sed -i '/SELINUX/d' %{srcdir}/config
sed -i '/BOOTSPLASH/d' %{srcdir}/config
sed -i '/LOGO/d' %{srcdir}/config
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
Vanilla kernel Core with Fedora config patched for Pinebook Pro.
%files core
/boot/*

%package modules
Summary: Kernel Pinebook Pro Modules
Group: System Environment/Kernel
%description modules
Vanilla kernel Modules with Fedora config patched for Pinebook Pro.
%files modules
/usr/lib/modules/*

%post core
dracut -f --kernel-image /boot/Image /boot/initramfs-linux.img --kver %{version}-%{sourcerelease}

%changelog
* Thu Oct 29 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.1-3
- Bump version 5.9.1-3
* Sun Oct 25 2020 Bengt Fredh <bengt@fredhs.net> - 5.8.14-1
- First version
