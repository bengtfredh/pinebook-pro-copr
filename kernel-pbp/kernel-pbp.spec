# Fedoraish Kernel Pinebook Pro
Packager: Bengt Fredh <bengt@fredhs.net> 

%define linuxrel 6.0
%define version 6.0.3
%define sourcerelease 1
%define rpmrelease 300.fc36
%define release %{sourcerelease}%{?dist}
%define srcdir ${RPM_SOURCE_DIR}/manjaro-linux
%define srccommit 2f5c40f78fa6fe9b6db4f7ac976a35235bce9c53

Summary: Kernel Pinebook Pro
Name: kernel-pbp
Version: %{version}
Release: %{release}
Group: System Environment/Kernel
License: GPL2
URL: https://git.kernel.org/
ExclusiveArch: aarch64
BuildRequires: git-core gcc flex bison openssl-devel bc perl openssl kmod filesystem zlib elfutils-libelf-devel linux-firmware
Source0: https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-%{linuxrel}.tar.xz
Patch0: https://cdn.kernel.org/pub/linux/kernel/v5.x/patch-%{version}.xz
Requires: kernel-pbp-core
Requires: kernel-pbp-modules

%global debug_package %{nil}

%description
Vanilla kernel with Fedora config patched for Pinebook Pro.

%prep
# Clone Manjaro patches and checkout correct commit
git clone https://gitlab.manjaro.org/manjaro-arm/packages/core/linux.git %{srcdir}
cd %{srcdir}
git checkout %{srccommit}

mkdir -p ${RPM_SOURCE_DIR}/fedora-rpm
cd ${RPM_SOURCE_DIR}/fedora-rpm
curl -O https://kojipkgs.fedoraproject.org//packages/kernel/%{version}/%{rpmrelease}/aarch64/kernel-core-%{version}-%{rpmrelease}.aarch64.rpm
rpm2cpio kernel-core-%{version}-%{rpmrelease}.aarch64.rpm | cpio -idmv

# Unpack and apply base patches
%setup -c
cd linux-%{linuxrel}
%patch -P 0 -p1

patch -Np1 -i "%{srcdir}/1001-arm64-dts-allwinner-add-hdmi-sound-to-pine-devices.patch"            # A64-based devices
patch -Np1 -i "%{srcdir}/1002-arm64-dts-allwinner-add-ohci-ehci-to-h5-nanopi.patch"                # Nanopi Neo Plus 2 (by Furkan?)
patch -Np1 -i "%{srcdir}/1003-drm-bridge-analogix_dp-Add-enable_psr-param.patch"                   # Pinebook Pro;  From list: https://patchwork.kernel.org/project/dri-devel/patch/20200626033023.24214-2-shawn@anastas.io/ (no updates since June 2020) (schedule for removal in 6.1-rc1)
patch -Np1 -i "%{srcdir}/1004-gpu-drm-add-new-display-resolution-2560x1440.patch"                  # Odroid;  Not upstreamable
patch -Np1 -i "%{srcdir}/1005-panfrost-Silence-Panfrost-gem-shrinker-loggin.patch"                 # Panfrost (preference patch, might not be upstreamable)
patch -Np1 -i "%{srcdir}/1006-arm64-dts-rockchip-Add-Firefly-Station-p1-support.patch"             # Firefly Station P1 (by Furkan)
patch -Np1 -i "%{srcdir}/1007-rk3399-rp64-pcie-Reimplement-rockchip-PCIe-bus-scan-delay.patch"     # RockPro64 (by @nuumio, perhaps upstreamable?)
patch -Np1 -i "%{srcdir}/1008-arm64-dts-amlogic-add-initial-Beelink-GT1-Ultimate-dev.patch"        # Beelink GT1 Ultimate (by Furkan) (applied in linux-rc)
patch -Np1 -i "%{srcdir}/1009-arm64-dts-amlogic-add-meson-g12b-ugoos-am6-plus.patch"               # Meson Ugoos (by Furkan)
patch -Np1 -i "%{srcdir}/1010-arm64-dts-rockchip-Add-PCIe-bus-scan-delay-to-RockPr.patch"          # RockPro64 (relies on patch 1007)
patch -Np1 -i "%{srcdir}/1011-drm-rockchip-support-gamma-control-on-RK3399.patch"                  # RK3399 VOP;  From list: https://patchwork.kernel.org/project/linux-arm-kernel/cover/20211019215843.42718-1-sigmaris@gmail.com/ (applied in linux-rc)
patch -Np1 -i "%{srcdir}/1012-arm64-dts-rockchip-switch-to-hs200-on-rockpi4.patch"                 # Radxa Rock Pi 4;  Temporary hotfix, not for upstreaming (by Dragan)
patch -Np1 -i "%{srcdir}/1013-arm64-dts-rockchip-Add-PCIe-bus-scan-delay-to-Rock-P.patch"          # Radxa Rock Pi 4 (relies on patch 1007)
patch -Np1 -i "%{srcdir}/1014-ASOC-sun9i-hdmi-audio-Initial-implementation.patch"                  # Allwinner H6 HDMI audio (by Furkan)
patch -Np1 -i "%{srcdir}/1015-arm64-dts-allwinner-h6-Add-hdmi-sound-card.patch"                    # Allwinner H6 HDMI audio (by Furkan)
patch -Np1 -i "%{srcdir}/1016-arm64-dts-allwinner-h6-Enable-hdmi-sound-card-on-boards.patch"       # Allwinner H6 HDMI audio (by Furkan)
patch -Np1 -i "%{srcdir}/1017-arm64-dts-allwinner-add-OrangePi-3-LTS.patch"                        # Orange Pi 3 LTS (by Furkan)
patch -Np1 -i "%{srcdir}/1018-Add-support-for-the-Hardkernel-ODROID-M1-board.patch"                # Odroid M1; V3 From list: https://patchwork.kernel.org/project/linux-rockchip/list/?series=682120 (applied in linux-next)
patch -Np1 -i "%{srcdir}/1019-arm64-dts-rockchip-add-rk3568-station-p2.patch"                      # Firefly Station P2 (by Furkan)
patch -Np1 -i "%{srcdir}/1020-arm64-dts-meson-radxa-zero-add-support-for-the-usb-t.patch"          # Radxa Zero (by Furkan)
patch -Np1 -i "%{srcdir}/1021-arm64-dts-rockchip-add-OrangePi-4-LTS.patch"                         # Orange Pi 4 LTS (by Furkan)
patch -Np1 -i "%{srcdir}/1022-Add-YT8531C-phy-support.patch"                                       # Motorcomm PHY (by Furkan)
patch -Np1 -i "%{srcdir}/1023-add-phy-rockchip-Support-PCIe-v3.patch"                              # Rockchip; (applied in linux-rc) 
patch -Np1 -i "%{srcdir}/1024-arm64-dts-rockchip-rk3568-Add-PCIe-v3-nodes.patch"                   # Rockchip; (applied in linux-rc) 
patch -Np1 -i "%{srcdir}/2001-staging-add-rtl8723cs-driver.patch"                                  # Realtek WiFi;  Not upstreamable
patch -Np1 -i "%{srcdir}/2002-brcmfmac-USB-probing-provides-no-board-type.patch"                   # Bluetooth;  Will be submitted upstream by Dragan
patch -Np1 -i "%{srcdir}/2003-arm64-dts-rockchip-Work-around-daughterboard-issues.patch"           # Pinebook Pro microSD;  Will be submitted upstream by Dragan
patch -Np1 -i "%{srcdir}/3001-irqchip-gic-v3-add-hackaround-for-rk3568-its.patch"                  # Quartz64 and associated patches that are still being upstreamed: START
patch -Np1 -i "%{srcdir}/3002-arm64-dts-rockchip-Enable-video-output-on-Quartz64-B.patch"          # (applied in linux-rc)
patch -Np1 -i "%{srcdir}/3003-arm64-dts-rockchip-Add-hdmi-cec-assigned-clocks-to-r.patch"
patch -Np1 -i "%{srcdir}/3004-arm64-dts-rockchip-Add-PCIe-support-to-Quartz64-B.patch"
patch -Np1 -i "%{srcdir}/3005-arm64-dts-rockchip-Add-Quartz64-B-eeprom.patch"
patch -Np1 -i "%{srcdir}/3006-arm64-dts-rockchip-Add-PCIe-support-to-SoQuartz-CM4-.patch"
patch -Np1 -i "%{srcdir}/3007-arm64-dts-rockchip-Enable-video-output-on-SoQuartz-C.patch"
patch -Np1 -i "%{srcdir}/3008-dt-bindings-Add-Rockchip-rk817-battery-charger-suppo.patch"          # (applied in linux-rc)
patch -Np1 -i "%{srcdir}/3009-mfd-Add-Rockchip-rk817-battery-charger-support.patch"                # (applied in linux-rc)
patch -Np1 -i "%{srcdir}/3010-power-supply-Add-charger-driver-for-Rockchip-RK817.patch"            # (applied in linux-rc)
patch -Np1 -i "%{srcdir}/3011-drm-panel-simple-Add-init-sequence-support.patch"
patch -Np1 -i "%{srcdir}/3012-arm64-dts-rockchip-Move-Quartz64-A-to-mdio-setup.patch"
patch -Np1 -i "%{srcdir}/3013-arm64-dts-rockchip-Add-Quartz64-A-battery-node.patch"
patch -Np1 -i "%{srcdir}/3014-arm64-dts-rockchip-rk356x-update-pcie-io-ranges.patch"               # From https://github.com/neggles/linux-quartz64/commit/2c1e3811e6d7430f7d46dbb01d3773192c51cdcf (by Neggles)
patch -Np1 -i "%{srcdir}/3015-arm64-dts-rockchip-Add-HDMI-sound-node-to-Quartz64-B.patch"          # (applied in linux-rc)
patch -Np1 -i "%{srcdir}/3016-arm64-dts-rockchip-Add-HDMI-sound-node-to-SoQuartz-C.patch"
patch -Np1 -i "%{srcdir}/3017-arm64-dts-rockchip-Add-PCIe-2-nodes-to-quartz64-b.patch"             # Quartz64 and associated patches that are still being upstreamed: END (applied in linux-rc)
patch -Np1 -i "%{srcdir}/3018-arm64-dts-rockchip-Enable-video-output-on-rk3566-roc-pc.patch"       # Station M2; (by Furkan)
patch -Np1 -i "%{srcdir}/3019-board-rock3a-gmac1.patch"                                            # Rock 3A; From Armbian: https://github.com/armbian/build/blob/master/patch/kernel/archive/rockchip64-5.19/board-rock3a-gmac1.patch

# add sourcerelease to extraversion
sed -ri "s|^(EXTRAVERSION =)(.*)|\1 \2-%{sourcerelease}|" Makefile

# don't run depmod on 'make install'. We'll do this ourselves in packaging
sed -i '2iexit 0' scripts/depmod.sh

# merge Manjaro config with Fedora config as base
sed -i '/CONFIG_CC_VERSION_TEXT/d' %{srcdir}/config
sed -i '/MANJARO/d' %{srcdir}/config
sed -i '/APPARMOR/d' %{srcdir}/config
sed -i '/SELINUX/d' %{srcdir}/config
sed -i '/BOOTSPLASH/d' %{srcdir}/config
sed -i '/LOGO/d' %{srcdir}/config
sed -i '/BTRFS/d' %{srcdir}/config
sed -i '/_BPF/d' %{srcdir}/config
sed -i '/_OCFS2/d' %{srcdir}/config

./scripts/kconfig/merge_config.sh ${RPM_SOURCE_DIR}/fedora-rpm/lib/modules/%{version}-%{rpmrelease}.aarch64/config %{srcdir}/config

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
cp -r %{buildroot}/boot/dtbs %{buildroot}/usr/lib/modules/${_kernver}/

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
dracut -f --kernel-image /boot/Image /boot/initramfs-linux.img --kver %{version}-%{sourcerelease} 1> /dev/null 2>&1

%changelog
%autochangelog
