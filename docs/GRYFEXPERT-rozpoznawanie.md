GRYFEXPERT 0.5.10: dwa przyciski rozpoznawania modułów przez COM lub Ethernet.

• Rozpoznaj moduły i nadaj ID — kolejno AT+Search=0,1; AT+Search=0,2; itd. Moduły otrzymują adresy zgodne z pozycją i zapisują je w EEPROM. ETH zachowuje zapisane ID 1; za nim moduły ID 2,3,4… Odpowiedź AT+Find z oczekiwanym ID potwierdza zapis. Program nie wysyła SaveConfig ani nie zapisuje pozostałej konfiguracji.
• Rozpoznaj moduły tylko — odczyt pozycji CHAIN1 lub zapisanych ID, bez Search i zmiany adresów.
• Pierwszy brak odpowiedzi przez 2 s kończy oba tryby. Brak odpytywania dalszych pozycji i ponawiania zapisów. Granica 35 modułów.
• Po błędzie/anulowaniu wcześniejsze potwierdzone adresy pozostają zapisane i trafiają do projektu. Nazwy i ustawienia projektu zachowane według znanych pozycji i modeli, także przy zamianie ID dwóch identycznych modułów. Po nadaniu ID wymagany jest ponowny odczyt konfiguracji. Sprawdź adresy docelowe istniejących reguł: program nie zmienia ich automatycznie.

Walidacja: 213 testów aplikacji, rzeczywiste gniazda TCP z symulatorem pięciu modeli (ETH0606T, R0808, R0806T, S0804, OLD), limity czasu, utracone odpowiedzi, błędne potwierdzenie, odrzucenie zapisu, anulowanie i granica 35. Test przeglądarkowy obu przycisków oraz szerokości 1440/760/390/320. Fizycznym modułom nie nadawano ID podczas przygotowania wydania.
Programator i Instalator pozostają w wersji 2.0.13, firmware i bootloadery bez zmian: ETH 25, R0808 25, R0806T 27, S0804 27, OLD 4. Z powodu tej zmiany programu nie trzeba ponownie wgrywać bootloadera ani aplikacji modułów.
