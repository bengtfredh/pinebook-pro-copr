# AArch64 multi-platform
# Contributor: Kevin Mihelich <kevin@archlinuxarm.org>
# Maintainer: Dan Johansen <strit@manjaro.org>
Packager: Bengt Fredh <bengt@fredhs.net>

%define version 5.13.0
%define sourcerelease 1
%define release %{sourcerelease}%{?dist}

Summary: AArch64 multi-platform
Name: linux-manjaro
Version: %{version}
Release: %{release}
License: GPL2
URL: https://gitlab.manjaro.org/manjaro-arm/packages/core/linux.git
ExclusiveArch: aarch64
Source0: https://repo.ialab.dsu.edu/manjaro/arm-stable/core/aarch64/linux-%{version}-%{sourcerelease}-aarch64.pkg.tar.zst

%global debug_package %{nil}

%description
Manjaro kernel patched for Pinebook Pro and more.

%prep
%setup -c -T

%build

%install
tar -xvpf $RPM_SOURCE_DIR/linux-%{version}-%{sourcerelease}-aarch64.pkg.tar.zst -C %{buildroot} --exclude .PKGINFO --exclude .INSTALL --exclude .MTREE --exclude .BUILDINFO --exclude usr/share --exclude etc/mkinitcpio.d

%files
/boot/*
/usr/lib/modules/*

%post
dracut -f --kernel-image /boot/Image /boot/initramfs-linux.img --kver %{version}-%{sourcerelease}-MANJARO-ARM 1> /dev/null 2>&1

%changelog
* Wed Jul 07 2021 Bengt Fredh <bengt@fredhs.net> - 5.13.0-1
- Bump linux-manjaro version 5.13.0-1
* Sat Jun 19 2021 Bengt Fredh <bengt@fredhs.net> - 5.12.11-1
- Bump linux-manjaro version 5.12.11-1
* Sun Jun 06 2021 Bengt Fredh <bengt@fredhs.net> - 5.12.8-1
- Bump linux-manjaro version 5.12.8-1
* Mon May 18 2021 Bengt Fredh <bengt@fredhs.net> - 5.12.4-1
- Bump linux-manjaro version 5.12.4-1
* Sun May 09 2021 Bengt Fredh <bengt@fredhs.net> - 5.12.2-2
- Bump linux-manjaro version 5.12.2-2
* Wed Apr 28 2021 Bengt Fredh <bengt@fredhs.net> - 5.11.16-1
- Bump linux-manjaro version 5.11.16-1
* Mon Apr 12 2021 Bengt Fredh <bengt@fredhs.net> - 5.11.10-1
- Bump linux-manjaro version 5.11.10-1
* Sun Mar 21 2021 Bengt Fredh <bengt@fredhs.net> - 5.11.6-1
- Bump linux-manjaro version 5.11.6-1
* Thu Mar 18 2021 Bengt Fredh <bengt@fredhs.net> - 5.11.3-1
- Bump linux-manjaro version 5.11.3-1
* Sat Feb 27 2021 Bengt Fredh <bengt@fredhs.net> - 5.11.1-1
- Bump linux-manjaro version 5.11.1-1
* Mon Feb 22 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.17-1
- Bump linux-manjaro version 5.10.17-1
* Fri Jan 29 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.9-1
- Bump linux-manjaro version 5.10.9-1
* Thu Jan 21 2021 Bengt Fredh <bengt@fredhs.net> - 5.10.7-1
- Bump linux-manjaro version 5.10.7-1
* Wed Dec 30 2020 Bengt Fredh <bengt@fredhs.net> - 5.10.2-1
- Bump linux-manjaro version 5.10.2-1
* Thu Dec 10 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.13-1
- Bump linux-manjaro version 5.9.13-1
* Thu Dec 10 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.11-2
- Bump linux-manjaro version 5.9.11-2
* Thu Nov 24 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.9-2
- Bump linux-manjaro version 5.9.9-2
* Thu Nov 09 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.6-1
- Bump version 5.9.6-1
* Thu Oct 29 2020 Bengt Fredh <bengt@fredhs.net> - 5.9.1-3
- Bump version 5.9.1-3
* Fre Oct 16 2020 Bengt Fredh <bengt@fredhs.net> - 5.8.14-1
- Bump version
* Wed Sep 30 2020 Bengt Fredh <bengt@fredhs.net> - 5.8.10-2
- First version
