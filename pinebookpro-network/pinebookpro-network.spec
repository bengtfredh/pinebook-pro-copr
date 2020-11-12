Packager: Bengt Fredh <bengt@fredhs.net>

%define name pinebookpro-network
%define version 1
%define sourcerelease 1
%define release %{sourcerelease}%{?dist}

Summary: Pinebook Pro Network fixes
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL2
URL: https://github.com/bengtfredh/pinebook-pro-copr.git
ExclusiveArch: aarch64
Source0: https://raw.githubusercontent.com/bengtfredh/pinebook-pro-copr/master/pinebookpro-network/disable-random-mac.conf

%global debug_package %{nil}

%description
Pinebook Pro network fixes.

%prep
%setup -c -T

%build

%install
mkdir %{buildroot}/etc/NetworkManager/conf.d/ -p
install -Dm644 ${RPM_SOURCE_DIR}/disable-random-mac.conf -t %{buildroot}/etc/NetworkManager/conf.d/disable-random-mac.conf

%files
%config(noreplace) /etc/NetworkManager/conf.d/disable-random-mac.conf

%post

%preun

%changelog
* Thu Nov 12 2020 Bengt Fredh <bengt@fredhs.net> - 1-1
- First release
