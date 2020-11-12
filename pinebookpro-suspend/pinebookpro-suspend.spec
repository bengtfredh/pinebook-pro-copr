Packager: Bengt Fredh <bengt@fredhs.net>

%define name pinebookpro-suspend
%define version 2
%define sourcerelease 2
%define release %{sourcerelease}%{?dist}

Summary: Enable suspend2idle
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL2
URL: https://github.com/bengtfredh/pinebook-pro-copr.git
ExclusiveArch: aarch64
Source0: https://raw.githubusercontent.com/bengtfredh/pinebook-pro-copr/master/pinebookpro-suspend/freeze.conf
Requires: acpid

%global debug_package %{nil}

%description
Enable suspend2idle

%prep
%setup -c -T

%build

%install
mkdir %{buildroot}/etc/systemd/sleep.conf.d -p
install -Dm644 ${RPM_SOURCE_DIR}/s2idle.conf -t %{buildroot}/etc/systemd/sleep.conf.d/s2idle.conf

%files
%config(noreplace) /etc/systemd/sleep.conf.d/s2idle.conf

%post
sed -i "s/^action=.*/action=/g" /etc/acpi/events/powerconf
systemct enable acpid

%preun

%changelog
* Thu Nov 12 2020 Bengt Fredh <bengt@fredhs.net> - 2-2
- Fix source path
* Thu Nov 12 2020 Bengt Fredh <bengt@fredhs.net> - 2-1
- Changed following man sleep.conf
* Wed Oct 28 2020 Bengt Fredh <bengt@fredhs.net> - 1-1
- First version
