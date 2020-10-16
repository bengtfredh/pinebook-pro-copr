# Maintainer: Dan Johansen <strit@manjaro.org>
# Maintainer: Furkan Kardame <furkan@fkardame.com>

%define name pinebookpro-audio
%define version 1
%define sourcerelease 2
%define release %{sourcerelease}%{?dist}

Summary: Pinebook Pro audio
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL2
URL: https://gitlab.manjaro.org/manjaro-arm/packages/community/pinebookpro-audio.git
ExclusiveArch: aarch64
Source0: https://gitlab.manjaro.org/manjaro-arm/packages/community/pinebookpro-post-install/-/raw/master/asound.state
BuildRequires: git-core
Requires: acpid

%global debug_package %{nil}

%description
Patches for Pinebook Pro audio.

%prep
git clone https://gitlab.manjaro.org/manjaro-arm/packages/community/%{name}.git
cd %{name}
git checkout fcb1538d5be5a6324a18a0684b254b52a9138a76
%setup -c -T

%install
mkdir %{buildroot}/etc/acpi/events -p
mkdir %{buildroot}/usr/bin -p
mkdir %{buildroot}/usr/lib/systemd/system -p
mkdir %{buildroot}/var/lib/alsa -p
install -Dm644 ${RPM_BUILD_DIR}/%{name}/audio_jack_plugged_in -t %{buildroot}/etc/acpi/events/
install -Dm755 ${RPM_BUILD_DIR}/%{name}/audio_jack_plugged_in.sh -t %{buildroot}/etc/acpi/
install -Dm755 ${RPM_BUILD_DIR}/%{name}/sync.sh -t %{buildroot}/usr/bin/
install -Dm644 ${RPM_BUILD_DIR}/%{name}/pinebookpro-audio.service -t %{buildroot}/usr/lib/systemd/system/
install -Dm644 ${RPM_SOURCE_DIR}/asound.state -t %{buildroot}/var/lib/alsa/

%files
/etc/acpi/events/audio_jack_plugged_in
/etc/acpi/audio_jack_plugged_in.sh
/usr/bin/sync.sh
/usr/lib/systemd/system/pinebookpro-audio.service
%config /var/lib/alsa/asound.state

%post
/usr/bin/systemctl enable acpid.service
/usr/bin/systemctl enable pinebookpro-audio.service

%preun
if [ "$1" -eq 0 ]; then
  /usr/bin/systemctl stop pinebookpro-audio.service
  /usr/bin/systemctl disable pinebookpro-audio.service
fi;
:;

%changelog
* Mon Oct 12 2020 Bengt Fredh <bengt@fredhs.net> - 1-2
- First version
