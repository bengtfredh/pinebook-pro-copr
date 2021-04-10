Packager: Bengt Fredh <bengt@fredhs.net>

%define name pinebookpro-extlinux
%define version 2
%define sourcerelease 3
%define release %{sourcerelease}%{?dist}

Summary: Pinebook Pro exlinux.
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL2
URL: https://github.com/bengtfredh/pinebook-pro-copr.git
ExclusiveArch: aarch64
Source0: https://raw.githubusercontent.com/bengtfredh/pinebook-pro-copr/master/pinebookpro-extlinux/extlinux.conf

%global debug_package %{nil}

%description
Pinebook Pro exlinux.

%prep
%setup -c -T

%build

%install
mkdir %{buildroot}/boot/extlinux -p
install -Dm644 ${RPM_SOURCE_DIR}/extlinux.conf -t %{buildroot}/boot/extlinux/

%files
%config(noreplace) /boot/extlinux/extlinux.conf

%post
# Configure extlinux bootloader
# Get UUID for rootdisk
ROOTUUID=$(findmnt / -o UUID -n)
ROOTFSTYPE=$(findmnt / -o FSTYPE -n)

if [ ! -f /boot/extlinux/extlinux.conf.rpmnew ]; then
   # Edit extlinux.conf
   if [ ${ROOTFSTYPE}=btrfs ]; then
      sed -i -e "s!APPEND.*!APPEND console=tty1 console=ttyS2,1500000 root=UUID=${ROOTUUID} rw rootflags=subvol=root splash plymouth.ignore-serial-consoles rhgb quiet !g" /boot/extlinux/extlinux.conf
   else
      sed -i -e "s!APPEND.*!APPEND console=tty1 console=ttyS2,1500000 root=UUID=${ROOTUUID} rw splash plymouth.ignore-serial-consoles rhgb quiet !g" /boot/extlinux/extlinux.conf
   fi
else
   # Edit extlinux.conf.rpmnew
   if [ ${ROOTFSTYPE}=btrfs ]; then
      sed -i -e "s!APPEND.*!APPEND console=tty1 console=ttyS2,1500000 root=UUID=${ROOTUUID} rw rootflags=subvol=root splash plymouth.ignore-serial-consoles rhgb quiet !g" /boot/extlinux/extlinux.conf.rpmnew
   else
      sed -i -e "s!APPEND.*!APPEND console=tty1 console=ttyS2,1500000 root=UUID=${ROOTUUID} rw splash plymouth.ignore-serial-consoles rhgb quiet !g" /boot/extlinux/extlinux.conf.rpmnew
   fi
fi

%preun

%changelog
* Sat Apr 10 2021 Bengt Fredh <bengt@fredhs.net> - 2-3
- Fix error in script
* Sat Apr 10 2021 Bengt Fredh <bengt@fredhs.net> - 2-2
- Add logic to add UUID extlinux.conf.rpmnew
* Thu Jan 21 2021 Bengt Fredh <bengt@fredhs.net> - 2-1
- Add plymouth boot splash extlinux
* Sat Nov 14 2020 Bengt Fredh <bengt@fredhs.net> - 1-1
- First version
