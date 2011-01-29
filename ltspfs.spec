Summary:	LTSP file system, daemon that runs on thin clients
Name:		ltspfs
Version:	0.5.12
Release:	0.1
License:	GPL v2
Group:		Base
# where are sources?
Source0:	ftp://ftp.debian.org/debian/pool/main/l/ltspfs/%{name}_%{version}.orig.tar.gz
# Source0-md5:	b2b952863788ca0909dc43293c5071e7
URL:		http://www.ltsp.org/twiki/bin/view/Ltsp/LtspFS
BuildRequires:	glib2-devel
BuildRequires:	libfuse-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-pythonprov
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
Requires:	xorg-x11-utils

%description -n ltspfsd
Fuse based remote filesystem daemon for LTSP thin clients LtspFS is a
remote filesystem consisting of two parts: 1) A network server daemon
that runs on the LTSP terminal. 2) A FUSE module that runs in
userspace on the server, that connects with the daemon on the client.
This package contains the daemon to be run on the LTSP thin client.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_localstatedir}/run/devices

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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/88-ltsp.rules
%attr(755,root,root) /lib/udev/ltspfs_entry
%attr(755,root,root) %{_bindir}/ltspfsd
%attr(755,root,root) %{_sbindir}/cdpinger
%attr(755,root,root) %{_sbindir}/ltspfs_mount
%attr(755,root,root) %{_sbindir}/ltspfs_umount
%{_datadir}/ldm
%{_mandir}/man1/ltspfsd.1*
%{_mandir}/man1/cdpinger.1*
%{_mandir}/man1/ltspfs_mount.1*
%{_mandir}/man1/ltspfs_umount.1*
%dir %{_localstatedir}/run/devices
