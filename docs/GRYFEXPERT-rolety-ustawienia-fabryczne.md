GRYFEXPERT 0.5.16 i S0804 firmware 29.
Rolety: domyslnie 50 s otwierania i 50 s zamykania przy tworzeniu nowego modulu w projekcie oraz w ustawieniach fabrycznych firmware. Rozpoznawanie nie nadpisuje istniejacej konfiguracji sprzetu.
Czas przejazdu co 0,1 s: od 0,1 do 655,3 s (uint16_t w krokach 10 ms). GRYFEXPERT blokuje krotsze czasy i bledne wartosci przed wyslaniem. Ponad 600 s wymaga S0804 29.
Kazdy modul, zakladka Informacje: Przywroc ustawienia fabryczne i wgraj do modulu. Potwierdzenie uzytkownika, sprawdzenie tozsamosci, AT+Defaults z suma, potwierdzenie RuleOK, AT+SaveConfig, oczekiwanie na SaveOK; odczyt kontrolny w modelach udostepniajacych konfiguracje. ID pozostaje zachowane. Reset kasuje reguly i moze wylaczyc wyjscia. OLD udostepnia potwierdzenia, bez odczytu konfiguracji.
Nie zmieniono bootloaderow ani aplikacji pozostalych modeli. Pelny zestaw aktualnych plikow w paczce. Nie programowano fizycznych modulow.
Testy AVR granic i zapisu EEPROM oraz testy GRYFEXPERT z symulowanym TCP dla wszystkich pieciu modeli.
