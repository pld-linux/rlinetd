.\" {PTM/PW/0.1/10-09-1999/"jeszcze jeden super-serwer Internetu"}
.\" Translation update: Robert Luberda <robert@debian.org>, Aug 2001, rlinetd 0.5.4
.\" {$Id$
.\"
.TH RLINETD 8 "8 lipca 2001" "Debian" "rlinetd"
.SH NAZWA
rlinetd - jeszcze jeden super-serwer Internetu
.SH SK£ADNIA
.B rlinetd
.RB [ -d ]
.RB [ -h ]
.RB [ -f
.IR "<plik konfiguracyjny>" ]
.RB [ -p
.IR "<modu³ parsera>" ]
.SH OPIS
.B rlinetd
jest zarz±dc± po³±czeñ, który pod³±cza siê i nas³uchuje na
pewnych portach, podejmuj±c okre¶lone dzia³ania, gdy dokonywane
jest po³±czenie. 
.SH OPCJE
Program akceptuje kilka parametrów:
.TP
.B -d
zwiêksza poziom debugowania. Miêdzy innymi zapobiega od³±czeniu siê programu
od jego terminala steruj±cego i wypisuje komunikaty do stderr.
.TP
.B -h
wy¶wietla krótkie podsumowania opcji programu.
.TP
.BI -f " <plik konfiguracyjny>"
okre¶la alternatywny plik konfiguracyjny, który bêdzie czytany. 
.TP
.BI -p " <modu³ parsera>"
okre¶la alternatywny modu³ modu³ analizuj±cy sk³adniê u¿ywany do parsowania
pliku konfiguracyjnego.
.SH PLIKI
.TP
.I /etc/rlinetd.conf
domy¶lny plik konfiguracyjny.
.TP
.I /usr/lib/rlinetd/libparse.so
domy¶lny modu³ analizy sk³adni.
.SH ZOBACZ TAK¯E
.BR rlinetd.conf (5)
.SH AUTOR
Ten podrêcznik ekranowy napisa³ Mikolaj J. Habryn <dichro-doc@rcpt.to>
