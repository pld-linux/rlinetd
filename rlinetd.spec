#
# NOTE:
# - rpc support is incomplete (no pmap_unset on shutdown)
# - "instances 1" is not enough for tcp "wait" emulation
#   (in such case server accept()s, inetd must not!)
#
# Conditional build:
%bcond_without	libcap		# build without libcap support
#
Summary:	better replacement for inetd
Summary(pl):	lepszy zamiennik dla inetd
Name:		rlinetd
Version:	0.5.20
Release:	1
License:	GPL
Group:		Daemons
#Source0:	http://www.rcpt.to/rlinetd/download/%{name}-%{version}.tar.gz
Source0:	http://ftp.debian.org/debian/pool/main/r/rlinetd/%{name}_%{version}.tar.gz
# Source0-md5:	fb40a8816426be89f574e38b984b70e7
Source1:	%{name}.inet.sh
Source2:	%{name}.8.pl
Patch0:		%{name}-no_libnsl.patch
Patch1:		%{name}-dblfree.patch
Patch2:		%{name}-rpc.patch
URL:		http://packages.debian.org/rlinetd
#URL:		http://www.rcpt.to/rlinetd/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
%{?with_libcap:BuildRequires:	libcap-devel}
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	rc-inetd
Requires:	psmisc
Requires:	rc-inetd
Requires:	rc-scripts
Provides:	inetdaemon
Obsoletes:	inetd
Obsoletes:	inetdaemon
Obsoletes:	netkit-base
Obsoletes:	xinetd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
rlinetd is a connection manager which binds and listens to a number of
ports, and performs specified actions when a connection is made. It is
intended as a replacement for the BSD inetd program.

%description -l pl
rlinetd jest zarz±dc± po³±czeñ, który podczepia siê i s³ucha na wielu
portach, wykonuj±c zadane czynno¶ci, kiedy nast±pi po³±czenie. Jest
zaplanowany jako zamiennik dla programu inetd.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__autoheader}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-libwrap \
	--with-libcap%{!?with_libcap:=no} \
	--with-lsf \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inet.script
install -D %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/pl/man8/rlinetd.8

:> $RPM_BUILD_ROOT%{_sysconfdir}/rlinetd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q rc-inetd restart

%preun
if [ "$1" = "0" ]; then
	%service rc-inetd stop
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README{,.capabilities,.inetd} THANKS THOUGHTS TODO
%attr(640,root,root) %ghost %{_sysconfdir}/rlinetd.conf
%attr(755,root,root) %{_sbindir}/rlinetd
%attr(755,root,root) %dir %{_libdir}/rlinetd
%attr(755,root,root) %{_libdir}/rlinetd/*.so
%attr(640,root,root) /etc/sysconfig/rc-inet.script
%{_mandir}/man[58]/*
%lang(pl) %{_mandir}/pl/man8/*
