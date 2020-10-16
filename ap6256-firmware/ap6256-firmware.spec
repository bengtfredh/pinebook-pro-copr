# Maintainer: Dan Johansen <strit@manjaro.org>

%define name ap6256-firmware
%define version 2020.02
%define sourcerelease 5
%define release %{sourcerelease}%{?dist}

Summary: ap6256-firmware
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL2
URL: https://gitlab.manjaro.org/manjaro-arm/packages/community/ap6256-firmware.git
ExclusiveArch: aarch64
BuildRequires: git-core

%global debug_package %{nil}

%description
Firmware files for the ap6256 wifi/bt module

%prep
git clone https://gitlab.manjaro.org/manjaro-arm/packages/community/%{name}.git
cd %{name}
git checkout 7074a2e21dd804e229eab1c031bc00246e9173e0
%setup -c -T

%build

%install
mkdir %{buildroot}/usr/lib/firmware/brcm -p
# Bluetooth firmware
install -Dm644 ${RPM_BUILD_DIR}/%{name}/BCM4345C5.hcd -t %{buildroot}/usr/lib/firmware/
install -Dm644 ${RPM_BUILD_DIR}/%{name}/BCM4345C5.hcd %{buildroot}/usr/lib/firmware/brcm/BCM.hcd
install -Dm644 ${RPM_BUILD_DIR}/%{name}/BCM4345C5.hcd -t %{buildroot}/usr/lib/firmware/brcm/
# Wifi firmware
install -Dm644 ${RPM_BUILD_DIR}/%{name}/nvram_ap6256.txt -t %{buildroot}/usr/lib/firmware/
install -Dm644 ${RPM_BUILD_DIR}/%{name}/nvram_ap6256.txt -t %{buildroot}/usr/lib/firmware/brcm/brcmfmac43456-sdio.txt
install -Dm644 ${RPM_BUILD_DIR}/%{name}/fw_bcm43456c5_ag.bin %{buildroot}/usr/lib/firmware/brcm/brcmfmac43456-sdio.bin
install -Dm644 ${RPM_BUILD_DIR}/%{name}/brcmfmac43456-sdio.clm_blob %{buildroot}/usr/lib/firmware/brcm/
install -Dm644 ${RPM_BUILD_DIR}/%{name}/nvram_ap6256.txt %{buildroot}/usr/lib/firmware/brcm/brcmfmac43456-sdio.pine64,pinebook-pro.txt

%files
/usr/lib/firmware/

%post

%preun

%changelog
* Mon Oct 12 2020 Bengt Fredh <bengt@fredhs.net> - 2020.02-5
- First version
