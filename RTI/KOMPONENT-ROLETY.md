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

# GRYF — jeden komponent rolety S0804

<!-- RTI-METADATA:BEGIN -->
**GRYF Driver v2.22** · Copyright: 24/11/2026 GRYF
<!-- RTI-METADATA:END -->

Komponent jest natywnym **Viewport** w Integration Designer 11: jednym obiektem na stronie, zawierającym procent otwarcia, krótki stan oraz akcje **OTWÓRZ / STOP / ZAMKNIJ / ZAMKNIJ-STOP / OTWÓRZ-STOP / STEP / OTWIERAJ PRZEZ / ZAMYKAJ PRZEZ / USTAW POZYCJĘ**. Wnętrze edytuje się przez prawy przycisk myszy → **Edit Viewport**. Nie wymaga serwera WWW ani przeglądarki.

## Uruchomienie wzorca

1. Rozpakuj `GRYF-Komponent-Rolety.zip` i otwórz `GRYF-Rolety.apex` w Integration Designer 11. To osobny projekt wzorcowy, nie projekt Twojej instalacji.
2. W **Global → Drivers → GRYF → Driver Utilities → Update Driver** wskaż aktualny `GRYF.rtidriver` z publicznego katalogu RTI. Następnie wybierz **Enable Driver**, jeżeli instancja pozostaje wyłączona. Publiczny wzorzec zawiera interfejs, makra i definicje powiązań, bez skryptów źródłowych drivera; ten krok instaluje działającą paczkę.
3. Otwórz **Global → Controllers → RTiPanel (Android) → Home**. Cały panel rolety to jeden obiekt. Wzorzec steruje **modułem ID 1, roletą 1**; w driverze moduł ma typ S0804.
4. Ustaw połączenie, procesor i panel odpowiednie dla własnej instalacji. Projekt nie został przesłany do fizycznego XP ani napędu.

W lokalnym pełnym wzorcu `F:/GRYFEXPERT/RTI/GRYF-Rolety.apex` paczka 2.10 jest już osadzona; aktualizacja z kroku 2 dotyczy publicznego wzorca interfejsu.

## Widoczne przyciski i wartość procentowa

W **Driver Properties → Komponent rolety: ID 1 / R1** znajdują się niezależne pola **Pokaż GÓRA**, **Pokaż STOP**, **Pokaż DÓŁ**, **Pokaż NA PROCENT**, **Pokaż STEP** oraz **Docelowe otwarcie [%]**. Domyślnie wszystkie przyciski są widoczne, cel wynosi 50%. Zmiany konfiguracji wymagają ponownego wgrania projektu RTI. Układ zachowuje miejsce ukrytego przycisku.

Przycisk procentowy wykonuje zapisany cel i wyświetla go, np. **NA 70%**. Jest to konfigurowalny preset, a nie klawiatura do wpisywania wartości na panelu. Zakres wynosi 0–100%; błędna wartość konfiguracji daje bezpieczną wartość domyślną 50%. **0% = zamknięta, 100% = otwarta**. STEP korzysta z natywnej sekwencji modułu: otwórz / stop / zamknij.

## Informacja zwrotna

- Procent pochodzi z raportu S0804; `--%` oznacza nieznaną lub nieaktualną pozycję.
- Stan: **Otwieranie**, **Zamykanie**, **Zatrzymana po otwieraniu**, **Zatrzymana po zamykaniu**, **Zmiana kierunku**, **Oczekiwanie na ruch**, **Zatrzymana** lub **Brak danych**.
- Kierunek przed zatrzymaniem jest zapamiętywany na podstawie potwierdzonego ruchu, nie naciśnięcia przycisku. Utrata aktualności danych kasuje tę pamięć. Po uruchomieniu na postoju kierunek wcześniejszego ruchu może być nieznany.
- Procent jest estymacją czasu przejazdu. Po restarcie S0804 lub zmianie czasów trzeba wykonać pełny przejazd, aby moduł znał pozycję.
- W edytorze RTI widać przykładowe `50%` i tekst stanu; nie są to odczyty z urządzenia.

## Przeniesienie i druga roleta

Zaznacz zewnętrzny Viewport i kopiuj go jako całość na stronę docelową. Po przeniesieniu między projektami sprawdź instancję GRYF i powiązania w Tag Editor. Nie zakładaj, że numery urządzeń w dwóch projektach są takie same.

Przy kopii dla **innej** rolety nadaj jej własne tagi (np. `GRYF Roleta 2: ...`), aby zmiana makra nie zmieniła również pierwszej rolety. W gałęzi **ID N** wybierz **Steruj roletą** dla ruchu/STOP/STEP lub **Steruj roletą (czas / procent)** dla ruchu czasowego i pozycji. W nowej funkcji procentowej wpisz cel bezpośrednio w makrze. Starsze powiązania komponentu zachowują cel pobierany z konfiguracji. Zaktualizuj również tagi tekstowe i zmienne widoczności:

| Element | Powiązanie dla rolety R, modułu ID N |
| --- | --- |
| OTWÓRZ / STOP / ZAMKNIJ / ZAMKNIJ-STOP / OTWÓRZ-STOP / STEP | `ShutterBasicN(R, akcja)` |
| OTWIERAJ PRZEZ / ZAMYKAJ PRZEZ / USTAW POZYCJĘ % | `ShutterValueN(R, 8 / 10 / 7, czas_lub_procent)` |
| Procent | `R{R}_POSITION_TEXT_ID{N}` |
| Krótki stan | `R{R}_MOTION_TEXT_ID{N}` |
| Etykieta NA PROCENT | `R{R}_PRESET_TEXT_ID{N}` |
| Widoczność przycisków | `R{R}_SHOW_UP_ID{N}`, `SHOW_STOP`, `SHOW_DOWN`, `SHOW_PERCENT`, `SHOW_STEP` |

Zmień tytuł wewnątrz Viewport na nazwę okna. Widoczność oraz preset ustaw osobno w kategorii konfiguracji tej rolety.

Sprawdzono otwarcie komponentu i wyświetlanie powiązanych tekstów w Integration Designer 11, strukturę makr, kompilację paczki RTI oraz 154 testy offline drivera dla TCP i RS-232. Nie wykonano próby ruchu na fizycznej rolecie ani testu kopiowania do istniejącego projektu użytkownika.
