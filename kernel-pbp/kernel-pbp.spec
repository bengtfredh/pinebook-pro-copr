# Fedoraish Kernel Pinebook Pro
Packager: Bengt Fredh <bengt@fredhs.net> 

%define linuxrel 5.14
%define version 5.14.13
%define sourcerelease 1
%define rpmrelease 200.fc34
%define release %{sourcerelease}%{?dist}
%define srcdir ${RPM_SOURCE_DIR}/manjaro-linux
%define srccommit 85991138cf1eabd5c622b2ad607cf144028e91a2

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

  # ALARM patches
  patch -Np1 -i "%{srcdir}/0001-net-smsc95xx-Allow-mac-address-to-be-set-as-a-parame.patch"             #All

  # Manjaro ARM Patches
  patch -Np1 -i "%{srcdir}/0002-arm64-dts-amlogic-add-support-for-Radxa-Zero.patch"                     #Radxa Zero
  patch -Np1 -i "%{srcdir}/0003-arm64-dts-allwinner-add-hdmi-sound-to-pine-devices.patch"               #Pine64
  patch -Np1 -i "%{srcdir}/0004-arm64-dts-allwinner-add-ohci-ehci-to-h5-nanopi.patch"                   #Nanopi Neo Plus 2
  patch -Np1 -i "%{srcdir}/0005-drm-bridge-analogix_dp-Add-enable_psr-param.patch"                      #Pinebook Pro
  patch -Np1 -i "%{srcdir}/0006-gpu-drm-add-new-display-resolution-2560x1440.patch"                     #Odroid
  patch -Np1 -i "%{srcdir}/0007-nuumio-panfrost-Silence-Panfrost-gem-shrinker-loggin.patch"             #Panfrost
  patch -Np1 -i "%{srcdir}/0008-arm64-dts-rockchip-Add-Firefly-Station-p1-support.patch"                #Firelfy Station P1
  patch -Np1 -i "%{srcdir}/0009-typec-displayport-some-devices-have-pin-assignments-reversed.patch"     #DP Alt Mode
  patch -Np1 -i "%{srcdir}/0010-usb-typec-add-extcon-to-tcpm.patch"                                     #DP Alt Mode
  patch -Np1 -i "%{srcdir}/0011-arm64-rockchip-add-DP-ALT-rockpro64.patch"                              #DP Alt mode - RockPro64
  patch -Np1 -i "%{srcdir}/0012-ayufan-drm-rockchip-add-support-for-modeline-32MHz-e.patch"             #DP Alt mode
  patch -Np1 -i "%{srcdir}/0013-rk3399-rp64-pcie-Reimplement-rockchip-PCIe-bus-scan-delay.patch"        #RockPro64
  patch -Np1 -i "%{srcdir}/0014-phy-rockchip-typec-Set-extcon-capabilities.patch"                       #DP Alt mode
  patch -Np1 -i "%{srcdir}/0015-usb-typec-altmodes-displayport-Add-hacky-generic-altmode.patch"         #DP Alt mode
  patch -Np1 -i "%{srcdir}/0018-drm-meson-add-YUV422-output-support.patch"                              #G12B
  patch -Np1 -i "%{srcdir}/0019-arm64-dts-meson-add-initial-Beelink-GT1-Ultimate-dev.patch"             #Beelink
  patch -Np1 -i "%{srcdir}/0020-add-ugoos-device.patch"                                                 #Ugoos
  patch -Np1 -i "%{srcdir}/0021-drm-panfrost-Handle-failure-in-panfrost_job_hw_submit.patch"            #AMLogic
  patch -Np1 -i "%{srcdir}/0022-arm64-dts-rockchip-Add-pcie-bus-scan-delay-to-rockpr.patch"             #RockPro64

  # Pinebook Pro patches
  patch -Np1 -i "%{srcdir}/0016-arm64-dts-rockchip-add-typec-extcon-hack.patch"                         #DP Alt mode
  patch -Np1 -i "%{srcdir}/0017-arm64-dts-rockchip-setup-USB-type-c-port-as-dual-data-role.patch"       #USB-C charging

  # Pinebook, PinePhone and PineTab patches
  patch -Np1 -i "%{srcdir}/0001-Bluetooth-Add-new-quirk-for-broken-local-ext-features.patch"            #Bluetooth
  patch -Np1 -i "%{srcdir}/0002-Bluetooth-btrtl-add-support-for-the-RTL8723CS.patch"                    #Bluetooth
  patch -Np1 -i "%{srcdir}/0003-arm64-allwinner-a64-enable-Bluetooth-On-Pinebook.patch"                 #Bluetooth
  patch -Np1 -i "%{srcdir}/0004-arm64-dts-allwinner-enable-bluetooth-pinetab-pinepho.patch"             #Bluetooth
  patch -Np1 -i "%{srcdir}/0005-staging-add-rtl8723cs-driver.patch"                                     #Wifi
  patch -Np1 -i "%{srcdir}/0006-pinetab-accelerometer.patch"                                            #accelerometer
  patch -Np1 -i "%{srcdir}/0007-enable-jack-detection-pinetab.patch"                                    #Audio
  patch -Np1 -i "%{srcdir}/0008-enable-hdmi-output-pinetab.patch"                                       #HDMI
  patch -Np1 -i "%{srcdir}/0009-drm-panel-Adjust-sync-values-for-Feixin-K101-IM2BYL02-panel.patch"      #Display

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
