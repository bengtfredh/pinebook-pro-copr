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
URL: https://githun.com/bengtfredh/pinebook-pro-copr.git
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
sed -i s/"#SuspendState=mem standby freeze"/"SuspendState=freeze"/g /etc/systemd/sleep.conf

%preun

%changelog
* Thu Oct 15 2020 Bengt Fredh <bengt@fredhs.net> - 1-1
- First version
