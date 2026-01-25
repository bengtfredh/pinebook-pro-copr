# Maintainer: Bengt Fredh <bengt@fredhs.net>

%define name pinebookpro-network
# renovate: datasource=git-refs depName=https://github.com/bengtfredh/pinebook-pro-copr.git currentValue=master
%define commit 03ff2ed0cf68986ffc62e4ce1feee0450e1f7c3a
%define version 20201112
%define release 1%{?dist}

Summary: Pinebook Pro Network fixes
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL2
URL: https://github.com/bengtfredh/pinebook-pro-copr.git
ExclusiveArch: aarch64
Source0: https://raw.githubusercontent.com/bengtfredh/pinebook-pro-copr/%{commit}/pinebookpro-network/disable-random-mac.conf

%global debug_package %{nil}

%description
Pinebook Pro network fixes.

%prep
%setup -c -T

%build

%install
mkdir %{buildroot}/etc/NetworkManager/conf.d/ -p
install -Dm644 ${RPM_SOURCE_DIR}/disable-random-mac.conf -t %{buildroot}/etc/NetworkManager/conf.d/

%files
%config(noreplace) /etc/NetworkManager/conf.d/disable-random-mac.conf

%changelog
%autochangelog
