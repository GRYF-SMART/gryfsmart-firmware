## Bramka RTI — GRYFEXPERT 0.5.51 / driver RTI 2.13

Połączenie: **GRYFEXPERT ⇄ LAN ⇄ procesor RTI ⇄ RS232 ⇄ port 0 pierwszego modułu GRYF**. Moduł ETH nie jest wymagany. Most obsługuje konfigurację, nazwy, reguły, wykrywanie modułów i diagnostykę. Nie obsługuje wgrywania HEX ani uruchamiania bootloadera.

1. W GRYFEXPERT wybierz **Bramka RTI**. Domyślny port nasłuchu to **4211**, identyfikator **RTI-1**. Program generuje klucz parowania (32 znaki hex); skopiuj go do konfiguracji drivera RTI.
2. W Integration Designer zaktualizuj driver do **2.13**. Wybierz **RS-232**, port procesora połączony z GRYF i **115200, 8N1**. W sekcji **Bramka dla GRYFEXPERT** włącz bramkę, wpisz adres IPv4 komputera w LAN, port, identyfikator i ten sam klucz. Zapisz i prześlij projekt do RTI.
3. W GRYFEXPERT kliknij **Połącz**. Program oczekuje do 60 s; można anulować oczekiwanie. To RTI inicjuje połączenie TCP do komputera. Zezwól GRYFEXPERT na połączenia przychodzące w Zaporze Windows dla prywatnej sieci. Stosuj stały adres lub rezerwację DHCP komputera.
4. Po połączeniu widoczny jest identyfikator RTI i adres połączenia. Rozpoznaj moduły i odczytaj konfigurację tak jak przez bezpośredni COM. Opcja nadawania ID zapisuje adresy modułów; po zmianie ID lub modeli dostosuj również konfigurację drivera w Integration Designer.
5. Po zakończeniu kliknij **Rozłącz**. Driver wznawia normalną pracę i pełną synchronizację stanów.

**Podczas sesji konfiguracji wstrzymane są komendy, logika sterująca przez ten driver i odpytywanie z RTI. Moduły nadal wykonują własny program.** Odpowiedzi modułów są przekazywane do GRYFEXPERT. Zerwanie sesji lub brak heartbeat przez ponad 10 s powoduje zwolnienie mostu i ponowny odczyt stanów. Odrzucone polecenia RTI nie są odtwarzane po sesji. Nie podłączaj drugiej instancji drivera do tego samego portu COM.

Zmienne RTI **Status bramki** i **Trwa konfiguracja GRYFEXPERT** pozwalają wyświetlić stan na panelu. Stary kanał `Hello` na porcie 4210 został zastąpiony parowaną sesją; nie jest uruchamiany. Pozostałe funkcje i identyfikator drivera są zachowane.

Klucz identyfikuje sparowaną instalację; transmisja nie jest szyfrowana. Używaj mostu w zaufanej sieci LAN, bez przekierowania portu z Internetu. Testy obejmują symulację RTI i komunikację TCP na komputerze; poprawność na fizycznym procesorze RTI wymaga testu instalacyjnego.

## Do czego służy program

**GRYFSMART / GRYFEXPERT** to program Windows do konfiguracji sterowników GRYF: modułów, wejść, wyjść, flag, reguł, czasów, PWM i rolet. Nazwa pliku oraz aplikacji pozostaje GRYFEXPERT.

## Uruchomienie

1. Pobierz ZIP z linku na górze, rozpakuj cały katalog i uruchom GRYFEXPERT. Przed podmianą starszej instalacji zapisz projekt i zamknij program; zachowaj swoje projekty.
2. Wybierz **TCP/IP** i adres bramki ETH0606T lub ETH Mini. Dla aktualnego ETH0606T port 5002 służy konfiguratorowi; port 5000 może obsługiwać integrację. ETH Mini domyślnie używa `192.168.1.201:5002` i jednego klienta.
3. Przy połączeniu **RS-232** wybierz port COM, 115200 bit/s, 8N1, bez kontroli przepływu. Port nie może być otwarty w drugim programie.
4. Odczytaj moduły i ich konfigurację. Nadaj nazwy wejściom, wyjściom, roletom i flagom. Zapisz projekt na komputerze; zapis konfiguracji do modułów jest osobną czynnością.
5. Skonfiguruj funkcje odpowiednie dla modelu i wersji firmware, następnie zapisz ustawienia do modułów.

## Nazwy w RTI

W RTI wyeksportuj konfigurację instancji GRYF do `.driverconfig`. W GRYFEXPERT wybierz eksport nazw RTI w menu **Plik**, wskaż ten plik i zapisz wynik. Zaimportuj wynik do tej samej instancji w Integration Designer. ID i typy modułów w obu projektach muszą się zgadzać. [Dokładna instrukcja](../RTI/INSTRUKCJA.md#jak-przenieść-nazwy-z-gryfexpert-do-rti).

[Protokół i przykłady](../PROTOKOL) · [Najnowsze firmware modułów](../HEX)
