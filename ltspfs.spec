Summary:	LTSP file system, daemon that runs on thin clients
Summary(pl.UTF-8):	System plików LTSP - demon działający na "cienkich klientach"
Name:		ltspfs
Version:	1.4
Release:	0.1
License:	GPL v2+
Group:		Base
# where are sources?
Source0:	http://ftp.debian.org/debian/pool/main/l/ltspfs/%{name}_%{version}.orig.tar.gz
# Source0-md5:	c25775a308059f228697176119551325
URL:		http://wiki.ltsp.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
# only checked for
BuildRequires:	glib2-devel >= 1:2.6.0
BuildRequires:	libfuse-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.643
BuildRequires:	xorg-lib-libX11-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LtspFS is a remote filesystem consisting of two parts:
 1) A network server daemon that runs on the LTSP terminal.
 2) A FUSE module that runs in userspace on the server, that connects
    with the daemon on the client.

This package contains the userspace parts for the LTSP server.

%description -l pl.UTF-8
LtspFS to zdalny system plików składający się z dwóch części:
 1) demona serwera sieciowego działającego na terminalu LTSP,
 2) modułu FUSE działającego w przestrzeni użytkownika na serwerze,
    łączącego się z demonem na kliencie.

Ten pakiet zawiera elementy przestrzeni użytkownika dla serwera LTSP.

%package -n ltspfsd
Summary:	LTSP file system, userspace FUSE module that runs on a server
Summary(pl.UTF-8):	System plików LTSP - moduł FUSE działający na serwerze
Group:		Base
Requires:	xorg-app-xdpyinfo
Requires:	xorg-app-xev
Requires:	xorg-app-xlsatoms
Requires:	xorg-app-xlsclients
Requires:	xorg-app-xlsfonts
Requires:	xorg-app-xprop
Requires:	xorg-app-xvinfo
Requires:	xorg-app-xwininfo

%description -n ltspfsd
LtspFS is a remote filesystem consisting of two parts:
 1) A network server daemon that runs on the LTSP terminal.
 2) A FUSE module that runs in userspace on the server, that connects
    with the daemon on the client.

This package contains the daemon to be run on the LTSP thin client.

%description -n ltspfsd -l pl.UTF-8
LtspFS to zdalny system plików składający się z dwóch części:
 1) demona serwera sieciowego działającego na terminalu LTSP,
 2) modułu FUSE działającego w przestrzeni użytkownika na serwerze,
    łączącego się z demonem na kliencie.

Ten pakiet zawiera demona uruchamianego na "cienkich klientach" LTSP.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	UDEV_RULES_PATH=/lib/udev/rules.d
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	UDEV_RULES_PATH=/lib/udev/rules.d \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_localstatedir}/run/devices
install -d $RPM_BUILD_ROOT%{systemdtmpfilesdir}
echo 'd %{_localstatedir}/run/devices 0755 root root -' > $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}d.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog doc/examples/*
%attr(755,root,root) %{_bindir}/ltspfs
%attr(4755,root,root) %{_bindir}/lbmount
%attr(755,root,root) %{_sbindir}/ltspfsmounter
%{_mandir}/man1/ltspfs.1*
%{_mandir}/man1/lbmount.1*
%{_mandir}/man1/ltspfsmounter.1*

%files -n ltspfsd
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ltspfsd
%attr(755,root,root) %{_sbindir}/ltspfs_mount
%attr(755,root,root) %{_sbindir}/ltspfs_umount
%attr(755,root,root) /lib/udev/ltspfs_entry
/lib/udev/rules.d/ltspfsd.rules
%{systemdtmpfilesdir}/ltspfsd.conf
%dir %{_datadir}/ldm
%dir %{_datadir}/ldm/rc.d
%{_datadir}/ldm/rc.d/X10-delayed-mounter
%{_datadir}/ldm/rc.d/X98-delayed-mounter
%dir %{_datadir}/ltsp
%dir %{_datadir}/ltsp/xinitrc.d
%{_datadir}/ltsp/xinitrc.d/I05-set-ltspfs_token
%{_mandir}/man1/ltspfsd.1*
%{_mandir}/man1/ltspfs_mount.1*
%{_mandir}/man1/ltspfs_umount.1*
%dir %{_localstatedir}/run/devices
