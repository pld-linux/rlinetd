#
# Conditional build:
# _without_libcap
#
Summary:	better replacement for inetd
Summary(pl):	lepszy zamiennik dla inetd
Name:		rlinetd
Version:	0.5.1
Release:	17
License:	GPL
Group:		Daemons
Vendor:		Mikolaj J. Habryn <dichro-rlinetd@rcpt.to>
Source0:	http://www.eris.rcpt.to/rlinetd/download/%{name}-%{version}.tar.gz
# Source0-md5:	a36623b7902d2d29260e20b2be077f31
Source1:	%{name}.inet.sh
Source2:	%{name}.8.pl
Patch0:		%{name}-execve.patch
Patch1:		%{name}-tcpwrappers.patch
Patch2:		%{name}-string.h.patch
Patch3:		%{name}-no_libnsl.patch
Patch4:		%{name}-ac25x.patch
Patch5:		%{name}-gcc3.patch
URL:		http://www.eris.rcpt.to/rlinetd/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
%{!?_without_libcap:BuildRequires:	libcap-devel}
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
PreReq:		rc-scripts
PreReq:		psmisc
Requires:	rc-inetd
Requires:	/etc/rc.d/init.d/rc-inetd
Provides:	inetdaemon
Obsoletes:	inetdaemon
Obsoletes:	inetd
Obsoletes:	xinetd
Obsoletes:	netkit-base

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
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
rm -f aux/missing
%{__libtoolize}
%{__autoheader}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-libwrap \
	--with-libcap%{?_without_libcap:=no} \
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
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start rlinetd" 1>&2
fi

%preun
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd stop
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README{,.capabilities,.inetd} THANKS THOUGHTS TODO
%attr(640,root,root) %ghost %{_sysconfdir}/rlinetd.conf
%attr(755,root,root) %{_sbindir}/rlinetd
%attr(755,root,root) %dir %{_libdir}/rlinetd
%attr(755,root,root) %{_libdir}/rlinetd/*.so*
%attr(640,root,root) /etc/sysconfig/rc-inet.script
%{_mandir}/man[58]/*
%lang(pl) %{_mandir}/pl/man8/*
