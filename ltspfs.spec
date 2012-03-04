Summary:	LTSP file system, daemon that runs on thin clients
Name:		ltspfs
Version:	1.1
Release:	0.2
License:	GPL v2
Group:		Base
# where are sources?
Source0:	ftp://ftp.debian.org/debian/pool/main/l/ltspfs/%{name}_%{version}.orig.tar.gz
# Source0-md5:	09b88d944bf2b8c4b3d28447784acb35
URL:		http://www.ltsp.org/twiki/bin/view/Ltsp/LtspFS
BuildRequires:	glib2-devel
BuildRequires:	libfuse-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.643
BuildRequires:	xorg-lib-libX11-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Fuse based remote filesystem for LTSP thin clients LtspFS is a remote
filesystem consisting of two parts: 1) A network server daemon that
runs on the LTSP terminal. 2) A FUSE module that runs in userspace on
the server, that connects with the daemon on the client. This package
contains the userspace parts for the LTSP server.

%package -n ltspfsd
Summary:	LTSP file system, userspace FUSE module that runs on a server
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
Fuse based remote filesystem daemon for LTSP thin clients LtspFS is a
remote filesystem consisting of two parts: 1) A network server daemon
that runs on the LTSP terminal. 2) A FUSE module that runs in
userspace on the server, that connects with the daemon on the client.
This package contains the daemon to be run on the LTSP thin client.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
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
%doc COPYING ChangeLog
%attr(755,root,root) %{_bindir}/ltspfs
%attr(4755,root,root) %{_bindir}/lbmount
%attr(755,root,root) %{_sbindir}/ltspfsmounter
%{_mandir}/man1/ltspfs.1*
%{_mandir}/man1/lbmount.1*
%{_mandir}/man1/ltspfsmounter.1*

%files -n ltspfsd
%defattr(644,root,root,755)
/lib/udev/rules.d/ltspfsd.rules
%{systemdtmpfilesdir}/ltspfsd.conf
%attr(755,root,root) /lib/udev/ltspfs_entry
%attr(755,root,root) %{_bindir}/ltspfsd
%attr(755,root,root) %{_sbindir}/cdpinger
%attr(755,root,root) %{_sbindir}/ltspfs_mount
%attr(755,root,root) %{_sbindir}/ltspfs_umount
%{_datadir}/ldm
%dir %{_datadir}/ltsp
%dir %{_datadir}/ltsp/xinitrc.d
%{_datadir}/ltsp/xinitrc.d/I05-set-ltspfs_token
%{_mandir}/man1/ltspfsd.1*
%{_mandir}/man1/cdpinger.1*
%{_mandir}/man1/ltspfs_mount.1*
%{_mandir}/man1/ltspfs_umount.1*
%dir %{_localstatedir}/run/devices
