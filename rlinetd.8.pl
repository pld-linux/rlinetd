.\" {PTM/PW/0.1/10-09-1999/"jeszcze jeden super-serwer Internetu"}
.\" Translation update: Robert Luberda <robert@debian.org>, Aug 2001, rlinetd 0.5.4
.\" {$Id$
.\"
.TH RLINETD 8 "8 lipca 2001" "Debian" "rlinetd"
.SH NAZWA
rlinetd - jeszcze jeden super-serwer Internetu
.SH SK�ADNIA
.B rlinetd
.RB [ -d ]
.RB [ -h ]
.RB [ -f
.IR "<plik konfiguracyjny>" ]
.RB [ -p
.IR "<modu� parsera>" ]
.SH OPIS
.B rlinetd
jest zarz�dc� po��cze�, kt�ry pod��cza si� i nas�uchuje na
pewnych portach, podejmuj�c okre�lone dzia�ania, gdy dokonywane
jest po��czenie. 
.SH OPCJE
Program akceptuje kilka parametr�w:
.TP
.B -d
zwi�ksza poziom debugowania. Mi�dzy innymi zapobiega od��czeniu si� programu
od jego terminala steruj�cego i wypisuje komunikaty do stderr.
.TP
.B -h
wy�wietla kr�tkie podsumowania opcji programu.
.TP
.BI -f " <plik konfiguracyjny>"
okre�la alternatywny plik konfiguracyjny, kt�ry b�dzie czytany. 
.TP
.BI -p " <modu� parsera>"
okre�la alternatywny modu� modu� analizuj�cy sk�adni� u�ywany do parsowania
pliku konfiguracyjnego.
.SH PLIKI
.TP
.I /etc/rlinetd.conf
domy�lny plik konfiguracyjny.
.TP
.I /usr/lib/rlinetd/libparse.so
domy�lny modu� analizy sk�adni.
.SH ZOBACZ TAK�E
.BR rlinetd.conf (5)
.SH AUTOR
Ten podr�cznik ekranowy napisa� Mikolaj J. Habryn <dichro-doc@rcpt.to>
