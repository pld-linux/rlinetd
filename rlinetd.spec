#
# no_libcap
#
Summary:	better replacement for inetd
Summary(pl):	lepszy zamiennik dla inetd
Name:		rlinetd
Version:	0.5.1
Release:	13
License:	GPL
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Vendor:		Mikolaj J. Habryn <dichro-rlinetd@rcpt.to>
Source0:	http://www.eris.rcpt.to/rlinetd/download/%{name}-%{version}.tar.gz
Source1:	%{name}.inet.sh
Patch0:		%{name}-execve.patch
Patch1:		%{name}-tcpwrappers.patch
Patch2:		%{name}-string.h.patch
URL:		http://www.eris.rcpt.to/rlinetd/
Requires:	rc-inetd
Prereq:		rc-scripts
Prereq:		psmisc
Requires:	/etc/rc.d/init.d/rc-inetd
Provides:	inetdaemon
%{?!no_libcap:BuildRequires: libcap-devel}
BuildRequires:	libwrap-devel
BuildRequires:	flex
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	inetdaemon
Obsoletes:	inetd
Obsoletes:	xinetd
Obsoletes:	netkit-base

%define         _sysconfdir     /etc

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
%configure \
	--with-libwrap \
	--with-libcap%{?no_libcap:=no} \
	--with-lsf
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{rc.d/init.d,sysconfig},%{_mandir}/pl/man8}

%{__make} install DESTDIR="$RPM_BUILD_ROOT"
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inet.script

:> $RPM_BUILD_ROOT%{_sysconfdir}/rlinetd.conf

gzip -9nf AUTHORS BUGS ChangeLog NEWS README{,.capabilities,.inetd} \
	THANKS THOUGHTS TODO

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
%doc *.gz
%attr(640,root,root) %ghost %{_sysconfdir}/rlinetd.conf
%attr(755,root,root) %{_sbindir}/rlinetd
%attr(755,root,root) %dir %{_libdir}/rlinetd
%attr(755,root,root) %{_libdir}/rlinetd/*
%attr(640,root,root) /etc/sysconfig/rc-inet.script
%{_mandir}/man[58]/*
