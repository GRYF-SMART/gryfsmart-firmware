GRYFEXPERT 0.5.11: nowy projekt i czyste drzewo przy każdym rozpoznawaniu.

Oba przyciski rozpoznawania tworzą od razu nowy projekt z nową nazwą i identyfikatorem. Drzewo instalacji jest czyszczone przed pierwszym zapytaniem. Wynik zastępuje całą poprzednią listę: nie są przenoszone stare moduły offline, nazwy, reguły ani odczytane konfiguracje. Ustawienia połączenia pozostają zachowane. Zapisane wcześniej pliki projektów pozostają na dysku; nowy projekt można zapisać osobno.

Rozpoznaj moduły i nadaj ID: kolejne AT+Search=0,1; AT+Search=0,2; itd. do 35. ETH ma zapisane ID 1, kolejne moduły za nim otrzymują ID 2,3,4… z zapisem w EEPROM potwierdzonym odpowiedzią AT+Find. Nie ma zapisu całej konfiguracji przez SaveConfig. Rozpoznaj moduły tylko: odczyt CHAIN1 lub ID bez zmiany adresów.

Pierwszy brak odpowiedzi przez 2 s kończy skan. Po błędzie/anulowaniu drzewo zawiera tylko moduły potwierdzone w tym przebiegu, bez dopisywania starych wpisów. Brak odpowiedzi już na początku pozostawia puste drzewo i nowy projekt. Wcześniejsze potwierdzone zapisy ID w sprzęcie pozostają wykonane. Istniejące reguły w fizycznych modułach nie są kasowane; po zmianie adresów sprawdź ich cele i odczytaj konfigurację.

Walidacja: 216 testów aplikacji; test przeglądarkowy świeżego projektu, natychmiast pustego drzewa, nowego ID projektu, braku starych nazw/reguł, skrócenia sieci z 5 do 3 modułów, błędu na pozycji 3 (tylko 2 wyniki) oraz pustej sieci. Zweryfikowano kolejność ETH 1, moduły 2–5 i oba tryby rozpoznawania. Fizycznym modułom nie nadawano ID podczas przygotowania wydania.

Programator i Instalator 2.0.13, firmware i bootloadery bez zmian: ETH 25, R0808 25, R0806T 27, S0804 27, OLD 4. Z powodu zmiany programu nie trzeba wgrywać nowego firmware ani bootloaderów.