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

## Synchronizacja stanów — wersja 2.12

Po starcie driver wysyła zapytania co **0,1 s**. Każdy etap przechodzi od najwyższego skonfigurowanego ID do ID 1:

1. Wyjścia przekaźnikowe R0806T, R0808 i ETH0606T (`GetOut`).
2. Rolety S0804: stan zbiorczy (`StanRol`) oraz szczegółowy stan czterech napędów (`GetRolState`).
3. PWM modułów R0806T (`GetPWM`).
4. Wejścia (`GetInputs`).
5. Flagi wirtualne (`GetFlags`) w obsługujących je modułach.
6. Temperatury R0808: oba kanały (`ReadTemp`). R0806T i ETH0606T wysyłają pomiary temperatury automatycznie; driver odbiera te raporty, ponieważ ich firmware nie obsługuje lokalnego zapytania `ReadTemp`.

Sekwencja korzysta z liczby i modeli modułów ustawionych w Driver Properties; nie wykrywa samoczynnie nowych ID. Dotyczy TCP i RS-232. Odczyty nie zmieniają wyjść. Polecenia użytkownika mają pierwszeństwo i mogą wydłużyć synchronizację. Odpytywanie w tle nie wtrąca zapytań do sekwencji startowej.

### Odświeżanie podczas pracy

Po zakończeniu sekwencji startowej działa **jeden cykl: co 10 sekund kolejny moduł**. Po 10 s odpytywany jest ID 1, po 20 s ID 2, następnie kolejne ID, a po ostatnim cykl wraca do ID 1. Pełny obieg N modułów trwa N × 10 s.

Dla wybranego ID driver kolejkuje odczyty wyjść (dla S0804 stan rolet), PWM tylko dla R0806T, wejść oraz flag. Komendy są wysyłane kolejno przez wspólną kolejkę transmisji. Usunięto wcześniejsze osobne cykle 8,1 s i 10,504 s. Raporty asynchroniczne modułów oraz szczegółowe odświeżanie rolet pozostają aktywne.

Brak odpowiedzi lub błąd pojedynczej transmisji nie blokuje następnych modułów. Wyświetlenie stanu wymaga odpowiedzi modułu. Restart drivera ponawia pełną sekwencję startową; samo ponowne połączenie TCP nie uruchamia osobnej sekwencji.

## Instalacja sterownika

Stały adres bieżącej paczki: **[GRYF.rtidriver](https://raw.githubusercontent.com/GRYF-SMART/gryfsmart-firmware/main/RTI/GRYF.rtidriver)**.

1. Pobierz driver z linku na górze.
2. W Integration Designer dodaj go w sekcji **Drivers**. Przy aktualizacji istniejącej instancji wybierz **GRYF → Driver Utilities → Update Driver**.
3. W **Driver Properties** wybierz TCP/IP lub RS-232, parametry połączenia, liczbę modułów, ID i modele.
4. Przypisz funkcje i zmienne do panelu. Zapisz projekt i prześlij go do procesora RTI.

Obsługiwane moduły: R0806T, R0808, ETH0606T i S0804. Dostępne są osobne funkcje wyjść, flag i PWM; akcje czasowe co 0,1 s; rampa PWM; diagnostyka modułów; sterowanie i stany rolet, pozycja, cel, ruch, pozostały czas oraz ważność danych.

## Gotowy komponent rolety

**[Pobierz komponent](https://raw.githubusercontent.com/GRYF-SMART/gryfsmart-firmware/main/RTI/GRYF-Komponent-Rolety.zip)** — jeden Viewport z przyciskami GÓRA, STOP, DÓŁ, NA PROCENT i STEP, procentem i stanem. Widoczność poszczególnych przycisków jest konfigurowalna. Przycisk procentowy wywołuje ustawiony preset. [Instrukcja komponentu](KOMPONENT-ROLETY.md).

## Import nazw z GRYFEXPERT

1. Zapisz nazwy wejść, wyjść, PWM i flag w projekcie GRYFEXPERT.
2. W RTI wybierz **Driver Utilities → Export Configuration** i zapisz `.driverconfig` dla właściwej instancji GRYF.
3. W GRYFEXPERT użyj eksportu nazw RTI w menu **Plik**, wskaż wyeksportowany plik i zapisz wynik.
4. Zaimportuj wynik do tej samej instancji w RTI. Sprawdź zgodność ID, typów i liczby modułów.

[Pełna instrukcja: nazwy, stany S0804, komunikacja i diagnostyka](INSTRUKCJA.md).
