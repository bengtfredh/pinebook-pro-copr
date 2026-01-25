Packager: Bengt Fredh <bengt@fredhs.net>

%define name pinebookpro-suspend
# renovate: datasource=git-refs depName=https://github.com/bengtfredh/pinebook-pro-copr.git currentValue=master
%define commit 65d21d85ade5f07b11dfd5496662c1e01c48a221
%define version 20201112
%define release 1%{?dist}

Summary: Enable suspend2idle
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL2
URL: https://github.com/bengtfredh/pinebook-pro-copr.git
ExclusiveArch: aarch64
Source0: https://raw.githubusercontent.com/bengtfredh/pinebook-pro-copr/%{commit}/pinebookpro-suspend/s2idle.conf
Requires: acpid

%global debug_package %{nil}

%description
Enable suspend2idle

%prep
%setup -c -T

%build

%install
mkdir %{buildroot}/etc/systemd/sleep.conf.d -p
install -Dm644 ${RPM_SOURCE_DIR}/s2idle.conf -t %{buildroot}/etc/systemd/sleep.conf.d/

%files
%config(noreplace) /etc/systemd/sleep.conf.d/s2idle.conf

%post
if [ -f /etc/acpi/events/powerconf ]; then
    sed -i "s/^action=.*/action=/g" /etc/acpi/events/powerconf
fi
systemctl enable acpid || :

%changelog
%autochangelog
