# GRYF — jeden komponent rolety S0804

Komponent jest natywnym **Viewport** w Integration Designer 11: jednym obiektem na stronie, zawierającym procent otwarcia, krótki stan oraz przyciski **GÓRA / STOP / DÓŁ / NA PROCENT / STEP**. Wnętrze edytuje się przez prawy przycisk myszy → **Edit Viewport**. Nie wymaga serwera WWW ani przeglądarki.

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

Przy kopii dla **innej** rolety nadaj jej własne tagi (np. `GRYF Roleta 2: ...`), aby zmiana makra nie zmieniła również pierwszej rolety. W pięciu makrach wybierz funkcję **ID N → Komponent rolety**, numer rolety 1–4 i odpowiedni przycisk. Zaktualizuj również tagi tekstowe i zmienne widoczności:

| Element | Powiązanie dla rolety R, modułu ID N |
| --- | --- |
| GÓRA / STOP / DÓŁ / NA PROCENT / STEP | `ShutterComponentN(R, 1 / 3 / 2 / 7 / 6)` |
| Procent | `R{R}_POSITION_TEXT_ID{N}` |
| Krótki stan | `R{R}_MOTION_TEXT_ID{N}` |
| Etykieta NA PROCENT | `R{R}_PRESET_TEXT_ID{N}` |
| Widoczność przycisków | `R{R}_SHOW_UP_ID{N}`, `SHOW_STOP`, `SHOW_DOWN`, `SHOW_PERCENT`, `SHOW_STEP` |

Zmień tytuł wewnątrz Viewport na nazwę okna. Widoczność oraz preset ustaw osobno w kategorii konfiguracji tej rolety.

Sprawdzono otwarcie komponentu i wyświetlanie powiązanych tekstów w Integration Designer 11, strukturę makr, kompilację paczki RTI oraz 154 testy offline drivera dla TCP i RS-232. Nie wykonano próby ruchu na fizycznej rolecie ani testu kopiowania do istniejącego projektu użytkownika.
