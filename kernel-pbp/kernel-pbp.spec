# Fedoraish Kernel Pinebook Pro
Packager: Bengt Fredh <bengt@fredhs.net> 

%define linuxrel 5.9
%define version 5.9.11
%define sourcerelease 1
%define release %{sourcerelease}%{?dist}
%define srcdir ${RPM_SOURCE_DIR}/pbp-packages
%define srccommiti 810e4687579e90cdb57a04b8fd3072cbba8b974b
%define _patches (
        '0004-tty-serdev-support-shutdown-op.patch'
        '0005-bluetooth-hci_serdev-Clear-registered-bit-on-unregis.patch'
        '0006-bluetooth-hci_bcm-disable-power-on-shutdown.patch'
        '0007-mmc-core-pwrseq_simple-disable-mmc-power-on-shutdown.patch'
        '0024-arm64-dts-rockchip-setup-USB-type-c-port-as-dual-dat.patch'
)

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
# Clone arch patches and checkout correct commit
git clone https://github.com/nadiaholmquist/pbp-packages.git %{srcdir}
cd %{srcdir}
git checkout %{srccommit}

# Unpack and apply base patches
%setup -c
cd linux-%{linuxrel}
%patch -P 0 -p1

# Apply patches
for patch in "%{_patches[@]}"; do
  echo "Applying $patch"
	patch -Np1 -i "%{srcdir}/linux-pbp/$patch"
done

# add sourcerelease to extraversion
sed -ri "s|^(EXTRAVERSION =)(.*)|\1 \2-%{sourcerelease}|" Makefile

# don't run depmod on 'make install'. We'll do this ourselves in packaging
sed -i '2iexit 0' scripts/depmod.sh

# merge Manjaro config with Fedora config as base
sed -i '/CONFIG_LOCALVERSION/d' %{srcdir}/linux-pbp/config
sed -i '/APPARMOR/d' %{srcdir}/linux-pbp/config
sed -i '/SELINUX/d' %{srcdir}/linux-pbp/config
sed -i '/BOOTSPLASH/d' %{srcdir}/linux-pbp/config
sed -i '/LOGO/d' %{srcdir}/linux-pbp/config
sed -i '/BTRFS/d' %{srcdir}/linux-pbp/config
sed -i '/_BPF/d' %{srcdir}/linux-pbp/config

./scripts/kconfig/merge_config.sh ${RPM_SOURCE_DIR}/config %{srcdir}/linux-pbp/config

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
* Mon Nov 30 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.11-1
- Bump version kernel-pbp 5.9.11-1 - switch arch patches
* Mon Nov 23 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.9-1
- Bump version kernel-pbp 5.9.9-1
* Tue Nov 17 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.8-1
- Bump version kernel-pbp 5.9.8-1
* Thu Nov 11 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.7-1
- Bump version 5.9.7-1
* Thu Nov 7 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.1-3
- Bump version 5.9.1-3
* Sun Oct 25 2020 Bengt Fredh <bengt@fredhs.net> - 5.8.14-1
- First version
