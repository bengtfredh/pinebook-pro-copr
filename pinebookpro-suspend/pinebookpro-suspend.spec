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

%global debug_package %{nil}

%description
Enable suspend2idle

%prep
%setup -c -T

%build


%install

%files

%post
sed -i "s/^action=.*/action=/g" /etc/acpi/events/powerconf
sed -i "s/^#SuspendState=.*/SuspendState=freeze/g" /etc/systemd/sleep.conf

%preun

%changelog
* Wed Oct 28 2020 Bengt Fredh <bengt@fredhs.net> - 1-1
- First version
