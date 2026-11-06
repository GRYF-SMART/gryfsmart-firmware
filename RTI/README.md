# GRYF dla RTI Integration Designer

**Aktualna wersja sterownika: 2.09 · 6 listopada 2026**

Pobierz [GRYF.rtidriver](GRYF.rtidriver). W istniejącym projekcie wybierz instancję **GRYF**, otwórz **Driver Utilities → Update Driver** i wskaż pobrany plik. Nową instancję dodaj z pliku w sekcji **Drivers**. Sterownik obsługuje moduły R0806T, R0808, ETH0606T i S0804.

## Zmiany z 6 listopada 2026

| Wersja | Zmiany |
| --- | --- |
| **RTI 2.05** | Osobne, widoczne od razu pola wyboru **TCP/IP** i **RS-232**. Przy obu odznaczonych używany jest wybór zapisany w projekcie. Przy obu zaznaczonych pierwszeństwo ma RS-232. |
| **RTI 2.06** | Osobne polecenia **Ustaw wyjście**, **Ustaw flagę** i **Ustaw PWM**. Dla R0806T dodano włączenie na czas, włączenie po czasie oraz impuls po opóźnieniu. Czasy mają rozdzielczość 0,1 s. Dla impulsu wpisz np. `2,5 / 0,7`, czyli opóźnienie i czas włączenia. Włączenie po czasie wymaga firmware 35 lub nowszego. PWM obsługuje rampę 0–5 s, włączenie na procent, wyłączenie oraz przełączanie z pamięcią i bez pamięci. |
| **RTI 2.07** | Diagnostyka wszystkich modułów lub osobno dla każdego ID. Pokazuje model, wersję firmware, minimum, średnią i maksimum czasu pętli w µs, sumę restartów programowych i watchdog oraz osobny licznik startów. Dostępne są automatyczne odświeżanie i akcja ręczna. |
| **RTI 2.08** | Składanie fragmentów TCP i rozdzielanie wielu ramek z jednego odczytu. Walidacja raportów, kolejka poleceń z priorytetem akcji użytkownika, odstęp między transmisjami i scalanie oczekujących odczytów. Most GRYFEXPERT rozpoczyna sesję przez `Hello` i przekazuje odebrane odpowiedzi oraz zdarzenia bez echa poleceń. |
| **RTI 2.09** | Pełna obsługa sterowania i stanów rolet S0804: pozycja 0–100%, STEP UP/DOWN, czasy przejazdu co 0,1 s, odczyt/zapis konfiguracji, pozycja znana, cel, pozostały czas, ruch, postój, przerwa zmiany kierunku, oczekujący ruch i opis tekstowy. Walidacja sum kontrolnych i wygaszanie nieaktualnych danych. |
| **GRYFEXPERT 0.5.50** | Eksport nazw wejść, wyjść, PWM i flag do pliku `.driverconfig`. Nazwy flag można zapisać w projekcie w zakładce **Flagi**. [Pobierz GRYFEXPERT 0.5.50](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.06-gryfexpert-0.5.50). |

## S0804 — rolety w RTI 2.09

W **Driver Properties** ustaw typ modułu **S0804**. W funkcjach danego ID dostępne są:

- **Steruj roletą S0804** — wybór jednej z czterech rolet, otwarcie, zamknięcie, STOP, STEP UP, STEP DOWN, STEP i otwarcie na zadany procent. 0% oznacza zamknięcie, 100% pełne otwarcie. Pole procentu dotyczy tylko akcji procentowej.
- **Ustaw czasy przejazdu rolety** — osobno pełne otwieranie i zamykanie, z krokiem 0,1 s, np. `20,5`. Aktualny firmware przyjmuje 0,1–655,3 s; starsze wersje mogą ograniczać czas do 600 s. Ustawiaj na postoju. Zmiana czasów unieważnia pozycję.
- **Odczytaj stan i czasy rolety** — ręczne odświeżenie danych.
- **Zapisz konfigurację S0804 w EEPROM** — utrwala konfigurację modułu, w tym czasy wszystkich czterech rolet. Nie utrwala bieżącej pozycji. Używaj po konfiguracji, nie w cyklicznym makrze.

**Otwieranie czasowe** to pełny przejazd przez czas otwierania zapisany przez `RolTime`; analogicznie działa zamykanie. Odliczanie i zatrzymanie wykonuje S0804. Driver nie zmienia czasu kalibracji przy każdej akcji ani nie emuluje osobnego impulsu ruchu przez opóźniony STOP z XP. Do częściowego otwarcia służy pozycja procentowa. Stare makra „Ustaw wyjście” z OPEN/CLOSE/STOP/STEP pozostają zgodne.

Po restarcie lub zmianie czasów wykonaj pełne otwarcie albo zamknięcie. Dopiero po jego zakończeniu moduł zna pozycję i przyjmie pośrednie 1–99%. Pozycja jest estymacją czasową, nie pomiarem czujnika. Potwierdzenie `RuleOK` oznacza przyjęcie polecenia, a nie zakończenie ruchu; błędne lub niedozwolone polecenie może zwrócić `RuleERROR` w TraceViewer.

### Jak wyświetlić roletę na panelu

W zmiennych sterownika wybierz kategorię **S0804 ID … / Roleta …**, opisaną nazwą wyjścia z projektu (także po imporcie nazw z GRYFEXPERT).

| Element ekranu | Zmienna |
| --- | --- |
| Gotowa informacja na jednym polu tekstowym | **Stan opisowy**, np. `Otwieranie | Otwarcie 35% | Cel 70% | Pozostalo 8.2 s` |
| Wskaźnik/słupek procentowy | **Otwarcie [%]**; pokazuj wartość tylko przy **Pozycja znana** i **Dane aktualne** |
| Strzałki kierunku | **Otwieranie** / **Zamykanie** |
| Animacja ruchu | **W ruchu** |
| Ikona pauzy przy zmianie kierunku | **Przerwa zmiany kierunku** |
| Polecenie przyjęte, napęd jeszcze nie ruszył | **Oczekiwanie na rozpoczęcie ruchu** |
| Ikony końcowych położeń | **Całkowicie otwarta**, **Całkowicie zamknięta** |
| Pozostałe informacje | **Częściowo otwarta**, **Postój bez oczekującego ruchu**, **Cel [%]**, **Cel aktywny**, **Pozostały czas [s] tekst** |
| Konfiguracja czasów | **Czasy przejazdu [s] tekst**, **Czasy odczytane i aktualne**, **Czasy przejazdu ustawione** |

Zmienne liczbowe czasów mają jednostkę 0,1 s (np. 82 = 8,2 s). Zmienne tekstowe pokazują sekundy. Pozycja/cel `-1` oznacza brak wartości; nie należy pokazywać tego jako 0%. Kod stanu: -1 brak aktualnych danych, 0 postój, 1 zamykanie, 2 otwieranie, 3 przerwa zmiany kierunku. Postój z aktywnym celem i dodatnim pozostałym czasem jest dodatkowo oznaczany jako oczekiwanie na ruch.

Driver cyklicznie odpytuje szczegółowy stan każdej rolety, rozkładając odczyty w czasie i dając pierwszeństwo sterowaniu. Jeden odczyt planowany jest co 250 ms: jeden moduł to około 1 s na cykl, więcej modułów wydłuża cykl. Raport `R=` dodatkowo zleca odczyt czterech rolet. Dane bez odpowiedzi wygasają po co najmniej 10 s lub trzech pełnych cyklach; wtedy opis pokazuje brak aktualnych danych, a pozycja ma -1. Czasy przejazdu odczytywane są okresowo i na żądanie.

Szczegółowe odczyty wymagają firmware obsługującego `GetRolState` i `GetRolTime` również w modułach pośrednich (funkcje dostępne od firmware 21). Pakiet zweryfikowano narzędziem RTI PackageDriver i testami offline TCP/RS-232; w tej aktualizacji nie przeprowadzono próby ruchu na fizycznej rolecie.


## Jak przenieść nazwy z GRYFEXPERT do RTI

1. W projekcie GRYFEXPERT wpisz nazwy w zakładkach **Wejścia**, **Wyjścia** lub **Rolety** oraz **Flagi**. Nazwę PWM ustaw w zakładce **Wyjścia** modułu R0806T.
2. W projekcie RTI sprawdź liczbę modułów, ich ID i typy. W Integration Designerze wybierz istniejący sterownik **GRYF → Driver Utilities → Export Configuration** i zapisz plik `.driverconfig`.
3. W GRYFEXPERT wybierz **Plik → Eksportuj nazwy do RTI** i wskaż wyeksportowany plik. Program utworzy kopię `*-nazwy.driverconfig` i poda liczbę dopasowanych modułów, zmienionych nazw oraz pominiętych modułów.
4. W tym samym projekcie Integration Designera wybierz **GRYF → Driver Utilities → Import Configuration** i wskaż plik `*-nazwy.driverconfig`. Sprawdź nazwy w **Driver Properties** i listach wyboru w **Tag Editorze**, a następnie zapisz projekt.

Dopasowanie odbywa się według ID i typu modułu oraz numeru kanału. Ustawienia połączenia RS-232 i TCP pozostają takie jak w pliku wyeksportowanym z RTI. Pusta nazwa flagi w GRYFEXPERT zachowuje dotychczasową etykietę w RTI.

SHA-256 paczki: `a96a8e607852b4eadf7da432d320478f0e8778eff3e28441f1d56b7a441dfe9c`.
