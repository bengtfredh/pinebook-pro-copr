# Fedoraish Kernel Pinebook Pro
Packager: Bengt Fredh <bengt@fredhs.net> 

%define linuxrel 5.17
%define version 5.17.5
%define sourcerelease 2
%define rpmrelease 200.fc35
%define release %{sourcerelease}%{?dist}
%define srcdir ${RPM_SOURCE_DIR}/manjaro-linux
%define srccommit 693a27d80d1d2feb1fc866428094d9088db66d54

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
  patch -Np1 -i "%{srcdir}/1002-arm64-dts-allwinner-add-ohci-ehci-to-h5-nanopi.patch"                # Nanopi Neo Plus 2
  patch -Np1 -i "%{srcdir}/1003-drm-bridge-analogix_dp-Add-enable_psr-param.patch"                   # Pinebook Pro;  From list: https://patchwork.kernel.org/project/dri-devel/patch/20200626033023.24214-2-shawn@anastas.io/
  patch -Np1 -i "%{srcdir}/1004-gpu-drm-add-new-display-resolution-2560x1440.patch"                  # Odroid
  patch -Np1 -i "%{srcdir}/1005-panfrost-Silence-Panfrost-gem-shrinker-loggin.patch"                 # Panfrost
  patch -Np1 -i "%{srcdir}/1006-arm64-dts-rockchip-Add-Firefly-Station-p1-support.patch"             # Firefly Station P1
  patch -Np1 -i "%{srcdir}/1007-drm-rockchip-add-support-for-modeline-32MHz-e.patch"                 # DP Alt Mode
  patch -Np1 -i "%{srcdir}/1008-rk3399-rp64-pcie-Reimplement-rockchip-PCIe-bus-scan-delay.patch"     # RockPro64
  patch -Np1 -i "%{srcdir}/1009-drm-meson-encoder-add-YUV422-output-support.patch"                   # Meson G12B
  patch -Np1 -i "%{srcdir}/1010-arm64-dts-amlogic-add-initial-Beelink-GT1-Ultimate-dev.patch"        # Beelink GT1 Ultimate
  patch -Np1 -i "%{srcdir}/1011-arm64-dts-amlogic-add-meson-g12b-ugoos-am6-plus.patch"               # Meson Ugoos
  patch -Np1 -i "%{srcdir}/1012-drm-panfrost-scheduler-improvements.patch"                           # Panfrost;  Will be submitted upstream by the author
  patch -Np1 -i "%{srcdir}/1013-arm64-dts-rockchip-Add-PCIe-bus-scan-delay-to-RockPr.patch"          # RockPro64
  patch -Np1 -i "%{srcdir}/1014-drm-rockchip-support-gamma-control-on-RK3399.patch"                  # RK3399 VOP;  From list: https://patchwork.kernel.org/project/linux-arm-kernel/cover/20211019215843.42718-1-sigmaris@gmail.com/
  patch -Np1 -i "%{srcdir}/1015-arm64-dts-rockchip-switch-to-hs200-on-rockpi4.patch"                 # Radxa Rock Pi 4;  Temporary hotfix, not for upstreaming
  patch -Np1 -i "%{srcdir}/1016-arm64-dts-meson-remove-CPU-opps-below-1GHz-for-G12B-boards.patch"    # AMLogic [1/2];  From list: https://patchwork.kernel.org/project/linux-amlogic/patch/20220210100638.19130-2-christianshewitt@gmail.com/
  patch -Np1 -i "%{srcdir}/1017-arm64-dts-meson-remove-CPU-opps-below-1GHz-for-SM1-boards.patch"     # AMLogic [2/2];  From list: https://patchwork.kernel.org/project/linux-amlogic/patch/20220210100638.19130-3-christianshewitt@gmail.com/
  patch -Np1 -i "%{srcdir}/1018-arm64-dts-rockchip-Add-PCIe-bus-scan-delay-to-Rock-P.patch"          # Radxa Rock Pi 4
  patch -Np1 -i "%{srcdir}/1019-ASOC-sun9i-hdmi-audio-Initial-implementation.patch"                  # Allwinner H6 HDMI audio
  patch -Np1 -i "%{srcdir}/1020-arm64-dts-allwinner-h6-Add-hdmi-sound-card.patch"                    # Allwinner H6 HDMI audio
  patch -Np1 -i "%{srcdir}/1021-arm64-dts-allwinner-h6-Enable-hdmi-sound-card-on-boards.patch"       # Allwinner H6 HDMI audio
  patch -Np1 -i "%{srcdir}/1022-arm64-dts-allwinner-add-OrangePi-3-LTS.patch"                        # OrangePi 3 LTS
  patch -Np1 -i "%{srcdir}/2001-Bluetooth-Add-new-quirk-for-broken-local-ext-features.patch"         # Bluetooth;  From list: https://patchwork.kernel.org/project/bluetooth/patch/20200705195110.405139-2-anarsoul@gmail.com/
  patch -Np1 -i "%{srcdir}/2002-Bluetooth-btrtl-add-support-for-the-RTL8723CS.patch"                 # Bluetooth;  From list: https://patchwork.kernel.org/project/bluetooth/patch/20200705195110.405139-3-anarsoul@gmail.com/
  patch -Np1 -i "%{srcdir}/2003-arm64-allwinner-a64-enable-Bluetooth-On-Pinebook.patch"              # Bluetooth;  From list: https://patchwork.kernel.org/project/bluetooth/patch/20200705195110.405139-4-anarsoul@gmail.com/
  patch -Np1 -i "%{srcdir}/2004-arm64-dts-allwinner-enable-bluetooth-pinetab-pinepho.patch"          # Bluetooth;  The PinePhone part is in linux-next
  patch -Np1 -i "%{srcdir}/2005-staging-add-rtl8723cs-driver.patch"                                  # Realtek WiFi;  Not upstreamable
  patch -Np1 -i "%{srcdir}/2006-arm64-dts-allwinner-pinetab-add-accelerometer.patch"                 # PineTab Accelerometer
  patch -Np1 -i "%{srcdir}/2007-arm64-dts-allwinner-pinetab-enable-jack-detection.patch"             # PineTab Audio
  patch -Np1 -i "%{srcdir}/2008-brcmfmac-USB-probing-provides-no-board-type.patch"                   # Bluetooth;  Will be submitted upstream by the author
  patch -Np1 -i "%{srcdir}/2009-dts-rockchip-Adapt-and-adopt-Type-C-support-from-Pin.patch"          # RockPro64 DP Alt Mode;  Not upstreamable
  patch -Np1 -i "%{srcdir}/3170-arm64-dts-rk3399-pinebook-pro-Fix-USB-PD-charging.patch"             # Third set of patches: START
  patch -Np1 -i "%{srcdir}/3172-arm64-dts-rk3399-pinebook-pro-Improve-Type-C-support.patch"          # Pinebook Pro Type-C patches from megous; original patch numbers found
  patch -Np1 -i "%{srcdir}/3174-arm64-dts-rk3399-pinebook-pro-Remove-redundant-pinct.patch"          # on https://xff.cz/kernels/5.17/patches/ are retained, with just the first
  patch -Np1 -i "%{srcdir}/3178-arm64-dts-rk3399-pinebook-pro-Don-t-allow-usb2-phy-d.patch"          # digit changed from 0 to 3, to make tracking easier
  patch -Np1 -i "%{srcdir}/3339-drm-rockchip-cdn-dp-Disable-CDN-DP-on-disconnect.patch"
  patch -Np1 -i "%{srcdir}/3355-usb-typec-fusb302-Set-the-current-before-enabling-pu.patch"
  patch -Np1 -i "%{srcdir}/3359-usb-typec-fusb302-Update-VBUS-state-even-if-VBUS-int.patch"
  patch -Np1 -i "%{srcdir}/3361-usb-typec-fusb302-Add-OF-extcon-support.patch"
  patch -Np1 -i "%{srcdir}/3362-usb-typec-fusb302-Fix-register-definitions.patch"
  patch -Np1 -i "%{srcdir}/3363-usb-typec-fusb302-Clear-interrupts-before-we-start-t.patch"
  patch -Np1 -i "%{srcdir}/3364-usb-typec-typec-extcon-Add-typec-extcon-bridge-drive.patch"
  patch -Np1 -i "%{srcdir}/3365-phy-rockchip-typec-Make-sure-the-plug-orientation-is.patch"
  patch -Np1 -i "%{srcdir}/3372-phy-rockchip-inno-usb2-More-robust-charger-detection.patch"
  patch -Np1 -i "%{srcdir}/3373-usb-typec-extcon-Don-t-touch-charger-proprties.patch"                # Third set of patches: END

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
* Wed May 11 2022 Bengt Fredh <bengt@fredhs.net> - 5.17.5-2
- Bump version kernel-pbp 5.17.5-2
* Sat Apr 30 2022 Bengt Fredh <bengt@fredhs.net> - 5.17.5-1
- Bump version kernel-pbp 5.17.5-1
* Sat Apr 30 2022 Bengt Fredh <bengt@fredhs.net> - 5.16.16-1
- Bump version kernel-pbp 5.16.16-1
* Tue Jan 04 2022 Bengt Fredh <bengt@fredhs.net> - 5.15.11-1
- Bump version kernel-pbp 5.15.11-1
* Tue Dec 21 2021 Bengt Fredh <bengt@fredhs.net> - 5.15.10-1
- Bump version kernel-pbp 5.15.10-1
* Wed Dec 01 2021 Bengt Fredh <bengt@fredhs.net> - 5.15.5-1
- Bump version kernel-pbp 5.15.5-1
* Fri Oct 29 2021 Bengt Fredh <bengt@fredhs.net> - 5.14.13-1
- Bump version kernel-pbp 5.14.13-1
* Sat Oct 22 2021 Bengt Fredh <bengt@fredhs.net> - 5.14.12-1
- Bump version kernel-pbp 5.14.12-1
* Sun Aug 22 2021 Bengt Fredh <bengt@fredhs.net> - 5.13.12-1
- Bump version kernel-pbp 5.13.12-1
* Wed Jul 28 2021 Bengt Fredh <bengt@fredhs.net> - 5.13.4-1
- Bump version kernel-pbp 5.13.4-1
* Sat Jul 03 2021 Bengt Fredh <bengt@fredhs.net> - 5.12.13-1
- Bump version kernel-pbp 5.12.13-1
* Sat Jun 19 2021 Bengt Fredh <bengt@fredhs.net> - 5.12.12-1
- Bump version kernel-pbp 5.12.12-1
* Sat Jun 19 2021 Bengt Fredh <bengt@fredhs.net> - 5.12.11-1
- Bump version kernel-pbp 5.12.11-1
* Sat Jun 19 2021 Bengt Fredh <bengt@fredhs.net> - 5.12.10-1
- Bump version kernel-pbp 5.12.10-1
* Sat Jun 19 2021 Bengt Fredh <bengt@fredhs.net> - 5.12.9-1
- Bump version kernel-pbp 5.12.9-1
* Fri May 28 2021 Bengt Fredh <bengt@fredhs.net> - 5.12.8-1
- Bump version kernel-pbp 5.12.8-1
* Fri May 28 2021 Bengt Fredh <bengt@fredhs.net> - 5.12.7-1
- Bump version kernel-pbp 5.12.7-1
* Thu May 27 2021 Bengt Fredh <bengt@fredhs.net> - 5.12.6-1
- Bump version kernel-pbp 5.12.6-1
* Thu May 20 2021 Bengt Fredh <bengt@fredhs.net> - 5.12.5-1
- Bump version kernel-pbp 5.12.5-1
* Thu May 20 2021 Bengt Fredh <bengt@fredhs.net> - 5.12.4-1
- Bump version kernel-pbp 5.12.4-1
* Thu May 20 2021 Bengt Fredh <bengt@fredhs.net> - 5.12.3-1
- Bump version kernel-pbp 5.12.3-1
* Sun May 09 2021 Bengt Fredh <bengt@fredhs.net> - 5.12.2-2
- Bump version kernel-pbp 5.12.2-2
* Sat Apr 24 2021 Bengt Fredh <bengt@fredhs.net> - 5.11.16-1
- Bump version kernel-pbp 5.11.16-1
* Sat Apr 24 2021 Bengt Fredh <bengt@fredhs.net> - 5.11.15-1
- Bump version kernel-pbp 5.11.15-1
* Sat Apr 24 2021 Bengt Fredh <bengt@fredhs.net> - 5.11.14-1
- Bump version kernel-pbp 5.11.14-1
* Sat Apr 24 2021 Bengt Fredh <bengt@fredhs.net> - 5.11.13-1
- Bump version kernel-pbp 5.11.13-1
* Sat Apr 24 2021 Bengt Fredh <bengt@fredhs.net> - 5.11.12-1
- Bump version kernel-pbp 5.11.12-1
* Wed Mar 24 2021 Bengt Fredh <bengt@fredhs.net> - 5.11.9-1
- Bump version kernel-pbp 5.11.9-1
* Wed Mar 24 2021 Bengt Fredh <bengt@fredhs.net> - 5.11.8-1
- Bump version kernel-pbp 5.11.8-1
* Sun Mar 21 2021 Bengt Fredh <bengt@fredhs.net> - 5.11.7-1
- Bump version kernel-pbp 5.11.7-1
* Fri Feb 19 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.17-2
- Bump version kernel-pbp 5.10.17-2
* Fri Feb 19 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.16-2
- Bump version kernel-pbp 5.10.16-2
* Thu Feb 18 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.17-1
- Bump version kernel-pbp 5.10.17-1
* Thu Feb 18 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.16-1
- Bump version kernel-pbp 5.10.16-1
* Mon Feb 15 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.15-1
- Bump version kernel-pbp 5.10.15-1
* Mon Feb 15 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.14-1
- Bump version kernel-pbp 5.10.14-1
* Mon Feb 15 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.13-1
- Bump version kernel-pbp 5.10.13-1
* Mon Feb 15 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.12-1
- Bump version kernel-pbp 5.10.12-1
* Fri Jan 29 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.11-1
- Bump version kernel-pbp 5.10.11-1
* Fri Jan 29 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.10-1
- Bump version kernel-pbp 5.10.10-1
* Thu Jan 21 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.9-1
- Bump version kernel-pbp 5.10.9-1
* Thu Jan 21 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.8-1
- Bump version kernel-pbp 5.10.8-1
* Thu Jan 21 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.7-1
- Bump version kernel-pbp 5.10.7-1
* Thu Jan 21 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.6-1
- Bump version kernel-pbp 5.10.6-1
* Thu Jan 07 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.5-1
- Bump version kernel-pbp 5.10.5-1
* Mon Jan 04 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.4-1
- Bump version kernel-pbp 5.10.4-1
* Mon Jan 04 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.3-2
- add patch for USB-C data role on PBP
* Mon Jan 04 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.3-1
- Bump version kernel-pbp 5.10.3-1
* Wed Dec 30 2020 Bengt Fredh <bengt@fredhs.net> - 5.10.2-1
- Bump version kernel-pbp 5.10.2-1
* Tue Dec 15 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.14-1
- Bump version kernel-pbp 5.9.14-1
* Mon Dec 14 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.13-1
- Bump version kernel-pbp 5.9.13-1
* Mon Nov 23 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.12-2
- Bump version kernel-pbp 5.9.12-2
* Mon Nov 23 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.11-2
- Bump version kernel-pbp 5.9.11-2
* Mon Nov 23 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.9-4
- Add dtbs to /usr/lib/modules
* Mon Nov 23 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.9-3
- Bump version kernel-pbp 5.9.9-3
* Mon Nov 23 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.9-1
- Bump version kernel-pbp 5.9.9-1
* Tue Nov 17 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.8-1
- Bump version kernel-pbp 5.9.8-1
* Wed Nov 11 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.7-1
- Bump version 5.9.7-1
* Sat Nov 7 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.1-3
- Bump version 5.9.1-3
* Sun Oct 25 2020 Bengt Fredh <bengt@fredhs.net> - 5.8.14-1
- First version
