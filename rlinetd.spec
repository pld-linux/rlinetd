Summary:	better replacement for inetd
Summary(pl):	lepszy zamiennik dla inetd
Name:		rlinetd
Version:	0.5.1
Release:	1
Group:		Daemons
Group(pl):	Serwery
Copyright:	GPL
Vendor:		Mikolaj J. Habryn <dichro-rlinetd@rcpt.to>
Source0:	http://www.eris.rcpt.to/rlinetd/download/%{name}-%{version}.tar.gz
Source1:	rlinetd.init
Source2:	rlinetd.inet.sh
URL:		http://www.eris.rcpt.to/rlinetd/
Requires:	rc-inetd
Requires:	/etc/rc.d/init.d/rc-inetd
Provides:	inetdaemon
BuildPrereq:	libcap-devel
BuildPrereq:	libwrap-devel
Buildroot:      /tmp/%{name}-%{version}-root

%define         _sysconfdir     /etc

%description
rlinetd is a connection manager which binds and listens to a number of ports,
and performs specified actions when a connection is made. It is intended as a
replacement for the BSD inetd program.

%description -l pl
rlinetd jest zarz±dc± po³±czeñ, który podczepia siê i s³ucha na wielu portach,
wykonuj±c zadane czynno¶ci, kiedy nast±pi po³±czenie. Jest zaplanowany jako
zamiennik dla programu inetd.

%prep
%setup -q

%build
LDFLAGS="-s"; export LDFLAGS
%configure \
	--with-libwrap \
	--with-libcap \
	--with-lsf
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

make install DESTDIR="$RPM_BUILD_ROOT"
install	%{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rc-inet.script

:> $RPM_BUILD_ROOT%{_sysconfdir}/rlinetd.conf

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man{1,5,8}/* \
	{AUTHORS,BUGS,ChangeLog,NEWS,README} \
	{README.capabilities,README.inetd,THANKS,THOUGHTS,TODO}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start rlinetd" 1>&2
fi

%preun
if [ -f /var/lock/subsys/rc-initd ]; then
	/etc/rc.d/init.d/rlinetd stop
fi

%files
%defattr(644, root, root, 755)
%doc *.gz
%attr(640,root,root) %ghost /etc/rlinetd.conf
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %dir %{_libdir}/rlinetd
%attr(755,root,root) %{_libdir}/rlinetd/*
%attr(755,root,root) /etc/rc.d/init.d/rlinetd
%attr(640,root,root) /etc/sysconfig/rc-inet.script
%{_mandir}/man[158]/*
