## Konfiguracja przez GRYFEXPERT — driver RTI 2.14 / GRYFEXPERT 0.5.52

Połączenie: **GRYFEXPERT → adres IP procesora RTI + port TCP → RS232 → port 0 pierwszego modułu GRYF**. Odpowiedzi wracają tą samą drogą. Moduł ETH nie jest wymagany. RTI działa jako serwer ze stałym adresem IP; GRYFEXPERT inicjuje połączenie jako klient.

### Ustawienia drivera RTI

W Integration Designer zaktualizuj driver do **2.14**. Wybierz **RS-232**, port procesora połączony z GRYF i **115200, 8N1**. W osobnej sekcji **Konfiguracja przez GRYFEXPERT**:

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

# GRYF RTI — pełna instrukcja

[Aktualny driver i trzy ostatnie wersje](README.md)

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

SHA-256 paczki: `fd5176b3856518f58fabc8ab54d462286d063ce2ab674b636f9956fe872ad8ac`.
