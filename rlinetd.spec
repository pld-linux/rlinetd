Summary:	better replacement for inetd
Summary(pl):	lepszy zamiennik dla inetd
Name:		rlinetd
Version:	0.5
Release:	1
Group:		Daemons
Group(pl):	Serwery
Copyright:	GPL
Source0:	http://www.eris.rcpt.to/rlinetd/snapshots/%{name}-%{version}.tar.gz
Source1:	%{name}.init
URL:		http://www.eris.rcpt.to/rlinetd/
Vendor:		Mikolaj J. Habryn <dichro-rlinetd@rcpt.to>
Provides:	inetd
BuildPrereq:	libcap-devel
BuildPrereq:	libwrap-devel
Buildroot:      /tmp/%{name}-%{version}-root

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
%configure \
	--sysconfdir=/etc \
	--with-libwrap \
	--with-libcap \
	--with-lsf
make

%install
rm -rf $RPM_BUILD_ROOT

install -d		$RPM_BUILD_ROOT/etc/{rc.d/init.d,rlinetd.d}
touch			$RPM_BUILD_ROOT/etc/rlinetd.conf
make	install		DESTDIR="$RPM_BUILD_ROOT"
install	%{SOURCE1}	$RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

strip			$RPM_BUILD_ROOT%{_sbindir}/* || :
gzip -9nf		$RPM_BUILD_ROOT%{_mandir}/man{1,5,8}/*
gzip -9nf		{AUTHORS,BUGS,ChangeLog,INSTALL,NEWS,README} \
			{README.capabilities,README.inetd,THANKS,THOUGHTS,TODO}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f /etc/rlinetd.conf ]; then
  echo 'directory "/etc/rlinetd.d" ".*" ".*(~$|.rpmsave$|.rpmnew$|.rpmorig$)";' > /etc/rlinetd.conf
  if [ -f /etc/inetd.conf ]; then
    %{_sbindir}/inetd2rlinetd /etc/inetd.conf >> /etc/rlinetd.conf
    echo 
    echo Configuration file /etc/rlinetd.conf was generated using existing
    echo /etc/inetd.conf file.
    echo
    echo To start rlinetd daemon type /etc/rc.d/init.d/rlinetd start
    echo Make sure inetd is not running!
    echo
  fi
  chmod 640 /etc/rlinetd.conf
fi

%preun
if [ -f /var/lock/subsys/rlinetd ]; then
	/etc/rc.d/init.d/rlinetd stop
fi

%files
%defattr(644, root, root, 755)
%doc {AUTHORS,BUGS,ChangeLog,INSTALL,NEWS,README,README.capabilities,README.inetd,THANKS,THOUGHTS,TODO}.gz
%attr(640, root, root) %ghost /etc/rlinetd.conf
%attr(755, root, root) %{_sbindir}/*
%attr(755, root, root) %dir %{_libdir}/rlinetd
%attr(755, root, root) %{_libdir}/rlinetd/*
%attr(755, root, root) %dir /etc/%{name}.d
%attr(755, root, root) /etc/rc.d/init.d/%{name}
%{_mandir}/man[158]/*
