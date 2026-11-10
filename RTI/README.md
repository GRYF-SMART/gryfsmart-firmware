# 4. Driver RTI

**[Pobierz najnowszą wersję 2.12](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.10-rti-2.12/GRYF.rtidriver)**

GRYF RTI 2.12 — wspólny cykl odczytu stanów modułów. Jeden moduł co 10 sekund: ID 1, ID 2, aż do ostatniego i ponownie ID 1. Pełny obieg trwa liczba modułów × 10 s. W każdym cyklu odczyty wyjść / rolet, PWM (R0806T), wejść i flag. Zastępuje osobne okresy 8,1 s oraz 10,504 s. [Pełny opis wydania](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.10-rti-2.12).

## Trzy ostatnie wersje

| Wersja | Data publikacji | Pobieranie | Zmiany |
|---|---|---|---|
| **2.12** | 2026-11-10 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.10-rti-2.12/GRYF.rtidriver) | GRYF RTI 2.12 — wspólny cykl odczytu stanów modułów. Jeden moduł co 10 sekund: ID 1, ID 2, aż do ostatniego i ponownie ID 1. Pełny obieg trwa liczba modułów × 10 s. W każdym cyklu odczyty wyjść / rolet, PWM (R0806T), wejść i flag. Zastępuje osobne okresy 8,1 s oraz 10,504 s. [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.10-rti-2.12) |
| **2.11** | 2026-11-10 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.10-rti-2.11/GRYF.rtidriver) | GRYF RTI 2.11 — szybki odczyt stanów po restarcie procesora RTI. Zapytania co 100 ms, od najwyższego skonfigurowanego ID do ID 1. Etapy: wyjścia przekaźnikowe, rolety (również pozycje i szczegółowe stany), PWM, wejścia, flagi. [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.10-rti-2.11) |
| **2.10** | 2026-11-06 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.06-rti-2.10/GRYF.rtidriver) | GRYF RTI 2.10 — komponent rolety S0804. Jeden natywny Viewport z przyciskami GÓRA, STOP, DÓŁ, NA PROCENT i STEP. Osobna widoczność przycisków oraz cel procentowy w konfiguracji każdej rolety. [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.06-rti-2.10) |

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


[1. Aplikacja GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/GRYFSMART) · [2. GRYFSMART-Programator](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/AKTUALIZATOR) · [3. Driver Home Assistant](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/HOME-ASSISTANT) · [4. Driver RTI](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/RTI) · [5. Instalator Bootloader](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/BOOTLOADER) · [6. Protokół GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/PROTOKOL) · [7. System i moduły GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/SYSTEM)
