# Maintainer: Bengt Fredh <bengt@fredhs.net>

%define name pinebookpro-suspend
%define version 1
%define sourcerelease 1
%define release %{sourcerelease}%{?dist}

Summary: Enable suspend2idle
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL2
URL: https://github.com/bengtfredh/pinebook-pro-copr.git
ExclusiveArch: aarch64
Source0: https://raw.githubusercontent.com/bengtfredh/pinebook-pro-copr/master/pinebookpro-suspend/powerconf

%global debug_package %{nil}

%description
Enable suspend2idle

%prep
%setup -c -T

%build


%install
install -Dm644 ${RPM_SOURCE_DIR}/powerconf -t %{buildroot}/etc/acpi/events/

%files
%config(noreplace) /etc/acpi/events/powerconf

%post
sed -i s/"#SuspendState=mem standby freeze"/"SuspendState=freeze"/g /etc/systemd/sleep.conf

%preun

%changelog
* Wed Oct 28 2020 Bengt Fredh <bengt@fredhs.net> - 1-1
- First version
