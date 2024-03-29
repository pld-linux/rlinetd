#
# Conditional build:
%bcond_without	libcap		# build without libcap support
#
Summary:	better replacement for inetd
Summary(pl.UTF-8):	lepszy zamiennik dla inetd
Name:		rlinetd
Version:	0.7
Release:	1
License:	GPL
Group:		Daemons
Source0:	http://rlinetd.alioth.debian.org/download/rlinetd/%{name}-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a60b4242b5872e9afcf027bb0f5c86ba
Source1:	%{name}.inet.sh
URL:		http://rlinetd.alioth.debian.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
%{?with_libcap:BuildRequires:	libcap-devel}
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
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

%description -l pl.UTF-8
rlinetd jest zarządcą połączeń, który podczepia się i słucha na wielu
portach, wykonując zadane czynności, kiedy nastąpi połączenie. Jest
zaplanowany jako zamiennik dla programu inetd.

%prep
%setup -q

%build
%configure \
	--with-libwrap \
	--with-libcap%{!?with_libcap:=no} \
	--with-lsf \
	--without-libnsl

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inet.script

:> $RPM_BUILD_ROOT%{_sysconfdir}/rlinetd.conf

rm -f $RPM_BUILD_ROOT%{_libdir}/rlinetd/*.la
rm -f $RPM_BUILD_ROOT{%{_sbindir}/inetd2rlinetd,%{_mandir}/man8/inetd2rlinetd.8}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q rc-inetd restart

%preun
if [ "$1" = "0" ]; then
	%service rc-inetd stop
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README{,.capabilities,.inetd} THANKS THOUGHTS TODO
%attr(640,root,root) %ghost %{_sysconfdir}/rlinetd.conf
%attr(755,root,root) %{_sbindir}/rlinetd
%attr(755,root,root) %dir %{_libdir}/rlinetd
%attr(755,root,root) %{_libdir}/rlinetd/libparse.so
%attr(640,root,root) /etc/sysconfig/rc-inet.script
%{_mandir}/man5/rlinetd.conf.5*
%{_mandir}/man8/rlinetd.8*
%lang(pl) %{_mandir}/pl/man[58]/*
