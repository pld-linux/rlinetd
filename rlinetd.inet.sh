
# proces name
PROCESS_NAME=rlinetd

# inet server config
CONFIG_FILE=/etc/rlinetd.conf

# inet server daemon executable file name
DAEMON=/usr/sbin/rlinetd

# addytional inet server daemon argumments
DAEMON_ARGS=

parse_one_service()
{
	ALL_REQD_PARAMS=1

	[ ${SERVICE_NAME:-not} = "not" ]	&& ALL_REQD_PARAMS=0
	[ ${PROTOCOL:-not} = "not" ]		&& ALL_REQD_PARAMS=0
	[ ${PORT:-not} = "not" ]		&& ALL_REQD_PARAMS=0
	[ ${USER:-not} = "not" ]		&& ALL_REQD_PARAMS=0
	[ ${SERVER:-not} = "not" ]		&& ALL_REQD_PARAMS=0
	[ ${FLAGS:-not} = "not" ]		&& ALL_REQD_PARAMS=0
	[ ${DAEMON:-not} = "not ]		&& ALL_REQD_PARAMS=0

	if [ $ALL_REQD_PARAMS -eq 0 ] ; then
		return 1
	fi

	echo "service \"$SERVICE_NAME\" {"
	echo "	protocol	$PROTOCOL;"
	[ "${FAMILY:-none}" = "none" ] || echo "	family		$FAMILY;"
	echo "	port		$PORT;"
	echo "	user		\"$USER\";"
	[ "${GROUP:-none}" = "none" ] || echo "	group		\"$GROUP\";"
	if [ "$SERVER" = "tcpd" ] ; then
		echo "	tcpd		{ exit; }"
	else
		echo "	server		\"$SERVER\";"
	fi
	echo -n "	exec		\"$DAEMON"
	if [ "${DAEMONARGS:-none}" = "none" ] ; then
		echo "\";"
	else
		echo " $DAEMONARGS\";"
	fi
	if [ "$FLAGS" = "wait" ] ; then
	echo "	instances	1;"
	else
		[ "${MAX_CONNECTIONS:-n}" = "n" ] || echo "	instances	$MAX_CONNECTIONS;"
	fi

	[ "${INTERFACE:-n}" = "n" ]	|| echo "	interface	$INTERFACE;"
	[ "${NICE:-n}" = "n" ]		|| echo "	nice		$NICE;"
	if [ "${RPCNAME:-n}" != "n" ] ; then
		if [ "${RPCVERSION:-n}" != "n" ] ; then
			echo "	rpc {"
			echo "			name \"$RPCNAME\" ; version $RPCVERSION;"
			echo "	}"
		else
			return 2
		fi
	fi
	[ "${CHROOT:-n}" = "n" ]	|| echo "	chroot		\"$CHROOT\";"
	[ "${INITGROUPS:-n}" = "n" ]	|| echo "	initgroups;"
	[ "${BANNER:-n}" = "n" ]	|| echo "	banner		\"$BANNER\";"
	[ "${FILTER:-n}" = "n" ]	|| echo "	filer		\"$FILTER\";"
	[ "${ECHO:-n}" = "n" ]		|| echo "	echo		\"$ECHO\";"
	echo "}"

	return 0
}

status_rc-inetd()
{

}

