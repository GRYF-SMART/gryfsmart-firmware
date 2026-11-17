# 4. Driver RTI

**[Pobierz najnowszą wersję 2.21](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.17-rti-2.21/GRYF.rtidriver)**

GRYF Driver 2.21: menu każdego S0804 ma tylko pięć pozycji zgodnych z układem instalatora. 1. Steruj roletą — wybór rolety i OTWÓRZ, STOP, ZAMKNIJ, ZAMKNIJ-STOP, OTWÓRZ-STOP, STEP; bez pola czasu/procentu. 2. Steruj roletą (czas / procent) — roleta, akcja OTWIERAJ PRZEZ lub ZAMYKAJ PRZEZ (dokładność 0,1 s) albo USTAW POZYCJĘ %, oraz jedna wartość… [Pełny opis wydania](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.17-rti-2.21).

## Trzy ostatnie wersje

| Wersja | Data publikacji | Pobieranie | Zmiany |
|---|---|---|---|
| **2.21** | 2026-11-17 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.17-rti-2.21/GRYF.rtidriver) | GRYF Driver 2.21: menu każdego S0804 ma tylko pięć pozycji zgodnych z układem instalatora. 1. Steruj roletą — wybór rolety i OTWÓRZ, STOP, ZAMKNIJ, ZAMKNIJ-STOP, OTWÓRZ-STOP, STEP; bez pola czasu/procentu. 2. Steruj roletą (czas / procent) — roleta, akcja OTWIERAJ PRZEZ lub ZAMYKAJ PRZEZ (dokładność 0,1 s) albo USTAW POZYCJĘ %, oraz jedna wartość… [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.17-rti-2.21) |
| **2.20** | 2026-11-16 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.16-rti-2.20/GRYF.rtidriver) | GRYF Driver 2.20: osobne funkcje rolet pokazujące tylko potrzebne parametry. Steruj roletą S0804 — ruch / STOP / STEP: wybór rolety i akcji, bez końcowej liczby. Roleta: OTWIERAJ PRZEZ oraz ZAMYKAJ PRZEZ: wybór rolety i czasu. Napis „s, krok 0,1 s” jest widoczny w nazwie funkcji i pola. Np. 11,1 s jest poprawne; 11,11 nie jest obsługiwane. [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.16-rti-2.20) |
| **2.19** | 2026-11-16 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.15-rti-2.19/GRYF.rtidriver) | GRYF Driver 2.19: OTWIERAJ PRZEZ / ZAMYKAJ PRZEZ z nastawą co 0,1 s. Zmieniono nazwy akcji w funkcjach Steruj roletą S0804 i Komponent rolety dla wszystkich ID drivera. Czas wpisuje się w sekundach 0,1–655,3 s, z przecinkiem lub kropką, np. 1,2 albo 1.2. Pozycja pozostaje całkowita 0–100%. [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.15-rti-2.19) |

## Menu S0804 — pięć pozycji w RTI 2.21

Po ustawieniu typu modułu **S0804**, w jego gałęzi ID dostępne są wyłącznie:

| Funkcja | Parametry i akcje |
|---|---|
| **Steruj roletą** | Roleta 1–4 oraz OTWÓRZ, STOP, ZAMKNIJ, ZAMKNIJ-STOP, OTWÓRZ-STOP, STEP. **Bez pola czasu/procentu.** |
| **Steruj roletą (czas / procent)** | Roleta 1–4, akcja OTWIERAJ PRZEZ (dokładność 0,1 s), ZAMYKAJ PRZEZ (dokładność 0,1 s) albo USTAW POZYCJĘ %, oraz jedna wartość czasu/procentu. |
| **Ustaw czasy przejazdu rolety** | Roleta 1–4 oraz czasy pełnego otwierania i zamykania w sekundach co 0,1 s. |
| **Zapisz konfigurację do modułu** | Bez dodatkowych parametrów; zapis ustawień modułu w EEPROM. |
| **Ustaw flagę** | Flaga 1–8 oraz USTAW, SKASUJ albo PRZEŁĄCZ. |

Nazwy rolet i flag pochodzą z konfiguracji drivera, również po imporcie nazw z GRYFEXPERT. W drugiej funkcji wpisz np. `11,1` lub `11.1` dla 11,1 sekundy albo `50` dla 50% otwarcia. Czas ma zakres 0,1–655,3 s, krok 0,1 s; procent jest całkowity, 0–100%. **0% oznacza zamknięcie, 100% pełne otwarcie.** Wpis `11,11` nie spełnia kroku czasu.

Zmiana dotyczy wyłącznie menu poleceń S0804. Pozostałe typy modułów zachowują swoje funkcje i parametry. Z listy wyboru S0804 ukryto pełne listy zgodności, odczyt ręczny, osobne komendy otwierania/zamykania na czas i pozycję oraz polecenia komponentu. Zachowano ich identyfikatory i procedury wykonawcze dla wcześniejszych powiązań. Przy edycji makra wybierz jedną z pięciu pozycji powyżej. Po **Driver Utilities → Update Driver** sprawdź istniejące makra; nie usuwaj instancji drivera.

Zmienne stanu i automatyczne odczyty nadal są dostępne. Wersja firmware S0804 pozostaje **38**; jeśli moduł ma już tę wersję, nie trzeba ponownie wgrywać HEX.

## Ruch rolety przez zadany czas

Dla **OTWIERAJ PRZEZ** i **ZAMYKAJ PRZEZ** wpisz czas w sekundach co **0,1 s**, w zakresie **0,1–655,3 s**, np. `0,1`, `1,2` albo `1.2`. Czas odmierza moduł S0804; po jego upływie zatrzymuje napęd. Przerwa przy zmianie kierunku nie skraca zadanego czasu ruchu. Czasy ułamkowe i dłuższe niż 255 s wymagają **firmware S0804 38 lub nowszego**. Pełne sekundy 1–255 nadal używają dotychczasowego polecenia i działają także ze starszym firmware obsługującym te akcje. Dla USTAW POZYCJĘ wpisz całkowite 0–100%.

W funkcji **Steruj roletą (czas / procent)** wspólne pole wartości przyjmuje tekst. Wpis `10` nadal oznacza 10 sekund. Po aktualizacji istniejącego projektu sprawdź wartości parametrów zapisanych makr.

## Konfiguracja przez GRYFEXPERT — driver RTI 2.21 / GRYFEXPERT 0.5.60 lub nowszy

<!-- RTI-METADATA:BEGIN -->
**GRYF Driver v2.21** · Copyright: 17/11/2026 GRYF
<!-- RTI-METADATA:END -->

Połączenie: **GRYFEXPERT → adres IP procesora RTI + port TCP → RS232 → port 0 pierwszego modułu GRYF**. Odpowiedzi wracają tą samą drogą. Moduł ETH nie jest wymagany. RTI działa jako serwer ze stałym adresem IP; GRYFEXPERT inicjuje połączenie jako klient.

### Ustawienia drivera RTI

W Integration Designer zaktualizuj driver do **2.21**. Wybierz **RS-232**, port procesora połączony z GRYF i **115200, 8N1**. W osobnej sekcji **Konfiguracja przez GRYFEXPERT**:

- włącz konfigurację przez GRYFEXPERT;
- ustaw **Port TCP konfiguracji GRYFEXPERT**: domyślnie **4211**, z możliwością zmiany na wolny port w zakresie 1024–65535;
- wpisz identyfikator RTI oraz klucz parowania (32 znaki hex, skopiowany z GRYFEXPERT).

Port służy wyłącznie do konfiguracji modułów przez GRYFEXPERT; nie jest portem bramki ETH. W driverze **nie wpisuje się IP komputera**. Stały adres IP lub rezerwację DHCP procesora ustaw w konfiguracji sieci RTI. Zapisz i prześlij projekt do procesora. Wymagany runtime RTI 15+ obsługujący GenericServer. Zmienna **Status bramki** informuje o nasłuchu lub błędzie portu.

### Ustawienia GRYFEXPERT

1. Wybierz **Bramka RTI** obok COM i Ethernet ETH.
2. Wpisz **Adres IP RTI** (np. `192.168.0.15`) oraz **Port TCP RTI**. Domyślnie **4211**, można go edytować. Musi być taki sam jak w driverze.
3. Ustaw identyfikator i klucz parowania zgodne z driverem. Zapisz projekt, aby zachować ustawienia.
4. Kliknij **Połącz**. Program łączy się do RTI — nie uruchamia serwera na komputerze. Następnie rozpoznaj moduły i odczytaj konfigurację jak przy bezpośrednim COM.
5. Po zakończeniu kliknij **Rozłącz**. RTI wraca do normalnej pracy i odczytuje stany modułów. Po zmianie ID lub modeli w GRYFEXPERT dostosuj także konfigurację drivera w Integration Designer.

Most obsługuje konfigurację, nazwy, reguły, wykrywanie modułów i diagnostykę. **Nie obsługuje wgrywania HEX ani uruchamiania bootloadera.** Podczas sesji wstrzymane są komendy i odpytywanie tego drivera RTI; moduły nadal wykonują własny program. Drugi klient nie może przejąć aktywnej sesji. Zerwanie połączenia lub brak heartbeat przez ponad 10 s zwalnia most i uruchamia synchronizację. Odrzucone polecenia RTI nie są odtwarzane. Nie używaj drugiej instancji drivera na tym samym COM.

Zmienne **Status bramki** oraz **Trwa konfiguracja GRYFEXPERT** można umieścić na panelu RTI. Port i klucz są ustawieniami konkretnej instalacji. Używaj mostu w zaufanym LAN; transmisja nie jest szyfrowana i portu nie należy przekierowywać z Internetu.

**Zmiana względem 0.5.51 / 2.13:** kierunek zestawiania połączenia został odwrócony na GRYFEXPERT → RTI. Zaktualizuj obie strony. Stary klucz i numer portu można zachować, ale w projekcie GRYFEXPERT trzeba podać adres RTI i ponownie potwierdzić przypisanie modułów do połączenia. Testy obejmują symulację RTI i rzeczywiste połączenia TCP na komputerze; test instalacyjny na fizycznym RTI pozostaje do wykonania.

## Akcje rolet S0804 — RTI 2.21

Driver RTI oferuje dziewięć wspólnych akcji: OTWÓRZ, STOP, ZAMKNIJ, ZAMKNIJ-STOP, OTWÓRZ-STOP, STEP (OTWÓRZ → STOP → ZAMKNIJ → STOP), OTWIERAJ PRZEZ, ZAMYKAJ PRZEZ oraz USTAW POZYCJĘ %. Czas obu akcji czasowych podaje się w sekundach co 0,1 s (0,1–655,3 s). Pełny przejazd i STEP zatrzymują się po czasie ustawionym w S0804; STOP i ponowne wywołanie kierunku podczas ruchu zatrzymują napęd. Kod 6 jest zachowany jako zgodny alias STEP.

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

Aktualna paczka ma nazwę **GRYF Driver**. Numer wersji w polu Version i nagłówku pomocy oraz data Copyright są synchronizowane przy budowaniu wydania. Zachowano poprawkę importu z wersji 2.17 oraz dotychczasowe funkcje i identyfikatory. W Integration Designer wybierz istniejącą instancję **GRYF → Driver Utilities → Update Driver** i wskaż nowy `GRYF.rtidriver`. Nie usuwaj istniejącej instancji. Nazwa instancji zapisana wcześniej w projekcie może wymagać osobnej zmiany na **GRYF Driver**.


Stały adres bieżącej paczki: **[GRYF.rtidriver](https://raw.githubusercontent.com/GRYF-SMART/gryfsmart-firmware/main/RTI/GRYF.rtidriver)**.

1. Pobierz driver z linku na górze.
2. W Integration Designer dodaj go w sekcji **Drivers**. Przy aktualizacji istniejącej instancji wybierz **GRYF → Driver Utilities → Update Driver**.
3. W **Driver Properties** wybierz TCP/IP lub RS-232, parametry połączenia, liczbę modułów, ID i modele.
4. Przypisz funkcje i zmienne do panelu. Zapisz projekt i prześlij go do procesora RTI.

Obsługiwane moduły: R0806T, R0808, ETH0606T i S0804. Dostępne są osobne funkcje wyjść, flag i PWM; akcje czasowe co 0,1 s; rampa PWM; diagnostyka modułów; sterowanie i stany rolet, dziewięć akcji z parametrami czasu/pozycji, cel, ruch, pozostały czas oraz ważność danych.

## Gotowy komponent rolety

**[Pobierz komponent](https://raw.githubusercontent.com/GRYF-SMART/gryfsmart-firmware/main/RTI/GRYF-Komponent-Rolety.zip)** — jeden Viewport z przyciskami GÓRA, STOP, DÓŁ, NA PROCENT i STEP, procentem i stanem. Widoczność poszczególnych przycisków jest konfigurowalna. Przycisk procentowy wywołuje ustawiony preset. [Instrukcja komponentu](KOMPONENT-ROLETY.md).

## Import nazw z GRYFEXPERT

1. Zapisz nazwy wejść, wyjść, PWM i flag w projekcie GRYFEXPERT.
2. W RTI wybierz **Driver Utilities → Export Configuration** i zapisz `.driverconfig` dla właściwej instancji GRYF.
3. W GRYFEXPERT użyj eksportu nazw RTI w menu **Plik**, wskaż wyeksportowany plik i zapisz wynik.
4. Zaimportuj wynik do tej samej instancji w RTI. Sprawdź zgodność ID, typów i liczby modułów.

[Pełna instrukcja: nazwy, stany S0804, komunikacja i diagnostyka](INSTRUKCJA.md).




[1. Aplikacja GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/GRYFSMART) · [2. GRYFSMART-Programator](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/AKTUALIZATOR) · [3. Driver Home Assistant](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/HOME-ASSISTANT) · [4. Driver RTI](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/RTI) · [5. Instalator Bootloader](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/BOOTLOADER) · [6. Protokół GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/PROTOKOL) · [7. System i moduły GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/SYSTEM)
