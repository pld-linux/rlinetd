Summary:	better replacement for inetd
Summary(pl):	lepszy zamiennik dla inetd
Name:		rlinetd
Version:	0.3
Release:	1
Group:		Daemons
Group(pl):	Serwery
Copyright:	GPL
Source0:	http://www.eris.rcpt.to/rlinetd/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Patch:		rlinetd-temporary.patch
URL:		http://www.eris.rcpt.to/rlinetd/
Provides:	inetd
BuildRequires:	libcap-devel
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
%patch -p1

%build
CFLAGS="$RPM_OPT_FLAGS" \
./configure \
	--prefix=/usr \
	--exec-prefix=/usr \
	--sysconfdir=/etc

make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

touch $RPM_BUILD_ROOT/etc/rlinetd.conf
make install DESTDIR="$RPM_BUILD_ROOT" mandir="%{_mandir}"
cp %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/rlinetd

gzip -9nf $RPM_BUILD_ROOT/usr/share/man/man{1,5,8}/*
gzip -9nf {AUTHORS,BUGS,ChangeLog,INSTALL,NEWS,README,README.capabilities,README.inetd,THANKS,THOUGHTS,TODO}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/inetd.conf ] && ! [ -f /etc/rlinetd.conf ]; then
	/usr/sbin/inetd2rlinetd /etc/inetd.conf > /etc/rlinetd.conf
	echo 
	echo Configuration file /etc/rlinetd.conf was generated using existing
	echo /etc/inetd.conf file.
	echo
	echo To start rlinetd daemon type /etc/rc.d/init.d/rlinetd start
	echo Make sure inetd is not running!
	echo
fi

%preun
if [ -f /var/lock/subsys/rlinetd ]; then
	/etc/rc.d/init.d/rlinetd stop
fi

%files
%defattr(644, root, root, 755)
%doc {AUTHORS,BUGS,ChangeLog,INSTALL,NEWS,README,README.capabilities,README.inetd,THANKS,THOUGHTS,TODO}.gz
%ghost /etc/rlinetd.conf
%attr(755, root, root) /usr/sbin/*
/usr/lib/rlinetd
%attr(755, root, root) /etc/rc.d/init.d/rlinetd
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
