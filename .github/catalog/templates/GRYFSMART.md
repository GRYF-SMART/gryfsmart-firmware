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
