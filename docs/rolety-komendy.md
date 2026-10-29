# S0804 — parametry, sterowanie i odczyt stanu rolet

## Zmiana kierunków od firmware S0804 27

Od wersji **27** zamieniono sprzętowe kierunki wszystkich czterech rolet względem wersji 26 i starszych: OPEN ustawia DIR=1, CLOSE ustawia DIR=0. Piny DIR to PC6/PC4/PC2/PC0; piny zasilania PWR to PC7/PC5/PC3/PC1. Zasilanie jest wyłączane podczas przerwy zmiany kierunku.

Zmiana obejmuje lokalne przyciski i reguły, RolAct, STEP UP/DOWN, automatyczny STEP oraz pozycję procentową, również przy poleceniach zdalnych. Numery akcji, sumy kontrolne i znaczenie procentów pozostają: OPEN/100% = otwarcie, CLOSE/0% = zamknięcie. Zmienił się kierunek fizycznego napędu. Format R=/RolState pozostaje zgodny z dokumentacją.

Po aktualizacji sprawdź kierunki napędów oraz ponownie ustal pozycję i sprawdź czasy otwierania/zamykania. Zapisane reguły otrzymują odwrócony kierunek bez ich ponownego programowania.


S0804 obsługuje cztery rolety. Dokumentacja dotyczy oprogramowania w wersji **21**. GetRolTime, GetRolState i adresowane StanRol są przekazywane przez R0808, R0806T oraz bramkę ETH.

## 1. Zestawienie

| Kategoria | Komenda / odpowiedź | Działanie |
|---|---|---|
| Parametry | `AT+RolTime=ID,NR,OPEN,CLOSE,SUMA` | Ustawienie czasów pełnego przejazdu |
| Odczyt parametrów | `AT+GetRolTime=ID,NR,SUMA` | Odczyt bieżących czasów z RAM |
| Zapis | `AT+SaveConfig=ID,ID` | Utrwalenie konfiguracji, w tym czasów rolet |
| Ustawienia domyślne | `AT+Defaults=ID,ID` | Szerszy reset konfiguracji RAM, także rolet |
| Sterowanie | `AT+RolAct=ID,NR,AKCJA,PROCENT,SUMA` | OPEN, CLOSE, STOP, STEP, pozycja |
| Status skrócony | `AT+StanRol=ID` | Stan ruchu wszystkich czterech rolet |
| Status szczegółowy | `AT+GetRolState=ID,NR,SUMA` | Ruch, pozycja, ważność pozycji, cel i czas pozostały |
| Raport skrócony | `R=ID,S1,S2,S3,S4` | Odpowiedź StanRol lub raport automatyczny |
| Odpowiedź parametrów | `RolTime=ID,NR,OPEN,CLOSE,SUMA` | Odpowiedź GetRolTime |
| Odpowiedź szczegółowa | `RolState=ID,NR,STAN,ZNANA,POZYCJA,CEL,POZOSTALO,SUMA` | Odpowiedź GetRolState |

ID: 1–35, NR rolety: 1–4. Liczby są dziesiętne. SUMA jest zwykłą sumą wcześniejszych pól liczbowych. [Zasady komunikacji](komendy-wspolne.md#zasady-komunikacji-i-struktura-sieci). W przykładach `<CR>` i `<LF>` oznaczają bajty, a TX/RX — kierunki względem terminala. Nie wpisuj dosłownego `<CR>`.

Nowe odczyty wymagają ID 1–35. Wyjątek historyczny: StanRol=0 pyta lokalny S0804; nie jest broadcastem ani sposobem przejścia przez moduł przekaźnikowy.

## 2. RolTime — ustawienie parametrów

```text
AT+RolTime=ID,NR,OTWARCIE,ZAMKNIECIE,SUMA<CR>
```

Oba czasy: 1–6000 w jednostkach **0,1 s**, czyli 0,1–600 s. Ustawienie jest możliwe tylko na postoju, bez oczekującej komendy. Unieważnia dotychczasową pozycję rolety. Przykład: otwieranie 20 s, zamykanie 22 s:

```text
TX: AT+RolTime=1,1,200,220,422<CR>
RX: RuleOK=1<CR><LF>
```

Suma: 1+1+200+220=422. Czasy zmieniają RAM. Zapisz je SaveConfig, jeśli mają przetrwać restart.

## 3. GetRolTime — odczyt czasów

```text
TX: AT+GetRolTime=1,1,2<CR>
RX: RolTime=1,1,200,220,422<CR><LF>
```

Zapytanie: `AT+GetRolTime=ID,NR,SUMA`, SUMA=ID+NR. Odpowiedź: `RolTime=ID,NR,OTWARCIE,ZAMKNIECIE,SUMA`; jej suma obejmuje wszystkie cztery poprzednie liczby. Jednostka nadal wynosi 0,1 s.

Brak ustawionych czasów:

```text
TX: AT+GetRolTime=1,2,3<CR>
RX: RolTime=1,2,0,0,3<CR><LF>
```

Odczytywana jest bieżąca konfiguracja RAM, również jeszcze niezapisana. Nie jest to porównanie RAM z EEPROM. Odczyt jest dostępny także podczas ruchu i nie zmienia jego przebiegu. Nie ma dodatkowego RuleOK.

## 4. RolAct — sterowanie

```text
AT+RolAct=ID,NR,AKCJA,PROCENT,SUMA<CR>
```

SUMA=ID+NR+AKCJA+PROCENT. Akcje 0–6 wymagają PROCENT=0:

| Kod | Nazwa | Działanie |
|---:|---|---|
| 0 | NONE | Bez działania |
| 1 | OPEN | Pełne otwieranie przez skonfigurowany czas |
| 2 | CLOSE | Pełne zamykanie przez skonfigurowany czas |
| 3 | STOP | Zatrzymanie i anulowanie oczekującego ruchu |
| 4 | STEP UP | Otwiera; podczas otwierania lub oczekiwania na OPEN — STOP |
| 5 | STEP DOWN | Zamyka; podczas zamykania lub oczekiwania na CLOSE — STOP |
| 6 | STEP | Podczas ruchu STOP; na postoju kierunek przeciwny do ostatniego, początkowo OPEN |
| 7 | POSITION | Docelowe otwarcie 0–100% |

Przykłady dla ID=1 i rolety 1, po każdej przyjętej komendzie RuleOK=1:

```text
AT+RolAct=1,1,1,0,3<CR>      ← OPEN
AT+RolAct=1,1,2,0,4<CR>      ← CLOSE
AT+RolAct=1,1,3,0,5<CR>      ← STOP
AT+RolAct=1,1,4,0,6<CR>      ← STEP UP
AT+RolAct=1,1,5,0,7<CR>      ← STEP DOWN
AT+RolAct=1,1,6,0,8<CR>      ← STEP
AT+RolAct=1,1,7,50,59<CR>    ← pozycja 50%
AT+RolAct=1,1,7,0,9<CR>      ← pełne zamknięcie
AT+RolAct=1,1,7,100,109<CR>  ← pełne otwarcie
```

STEP nie oznacza przesunięcia o zadany dystans: typowa sekwencja to OPEN → STOP → CLOSE → STOP. Zmiana kierunku obejmuje przerwę około 300 ms. Nie ma broadcastu RolAct ani jednego polecenia ruchu wszystkich czterech rolet.

Bez ustawionych czasów przyjmowany jest STOP i NONE, a działania wymagające ruchu są odrzucane. RuleOK potwierdza przyjęcie polecenia, nie osiągnięcie końca ruchu. W obecnej implementacji ponowne zwykłe OPEN/CLOSE może rozpocząć odliczanie pełnego czasu od nowa — nie wysyłaj ich cyklicznie jako odpytywania stanu; do tego służą komendy GET.

## 5. Pozycjonowanie i ważność pozycji

0% oznacza zamknięcie, 100% pełne otwarcie. Procent w RolAct jest pozycją docelową, nie względnym przesunięciem. Moduł wybiera kierunek i oblicza czas potrzebny na zmianę pozycji.

Po restarcie albo zmianie RolTime pozycja jest nieznana. Najpierw zakończ pełny przejazd OPEN/CLOSE lub POSITION 100/0. Dopiero wtedy moduł przyjmie pozycje pośrednie 1–99%. Przerwanie pierwszego pełnego przejazdu przez STOP nie ustala pozycji. STOP po wcześniejszym ustaleniu pozycji zachowuje jej oszacowanie.

Pozycja jest szacowana na podstawie czasu, bez czujnika położenia. Stan ZNANA=1 oznacza dostępne oszacowanie programu, a nie potwierdzenie rzeczywistej pozycji przez sensor.

## 6. GetRolState — odczyt szczegółowy

```text
AT+GetRolState=ID,NR,SUMA<CR>
```

SUMA zapytania=ID+NR. Odpowiedź:

```text
RolState=ID,NR,STAN,ZNANA,POZYCJA,CEL,POZOSTALO,SUMA<CR><LF>
```

| Pole | Znaczenie |
|---|---|
| STAN | 0 postój, 1 zamykanie, 2 otwieranie, **3 trwająca przerwa przed zmianą kierunku** |
| ZNANA | 0 pozycja nieznana, 1 dostępna estymacja pozycji |
| POZYCJA | 0–100% aktualnego otwarcia; **255 przy ZNANA=0** |
| CEL | 0–100% docelowego otwarcia; **255 przy braku aktywnego celu lub oczekującym STOP** |
| POZOSTALO | Szacowany czas do zakończenia polecenia w jednostkach **0,1 s**, z przerwą zmiany kierunku; zaokrąglany w górę |
| SUMA | Suma wszystkich siedmiu wcześniejszych pól liczbowych |

Przykłady dla ID=1, rolety 1:

**Po restarcie: postój, pozycja nieznana:**

```text
TX: AT+GetRolState=1,1,2<CR>
RX: RolState=1,1,0,0,255,255,0,512<CR><LF>
```

**Postój na 50%, brak aktywnego celu:**

```text
RX: RolState=1,1,0,1,50,255,0,308<CR><LF>
```

**Otwieranie z pozycji 30% do 70%, pozostało około 8 s:**

```text
RX: RolState=1,1,2,1,30,70,80,185<CR><LF>
```

**Pierwszy pełny przejazd do 100%, pozycja nadal nieznana, pozostało około 12 s:**

```text
RX: RolState=1,1,2,0,255,100,120,479<CR><LF>
```

**Przerwa przed zamykaniem do 50%, pozycja 100%, pozostało łącznie około 10,3 s:**

```text
RX: RolState=1,1,3,1,100,50,103,259<CR><LF>
```

POZOSTALO może wynieść do 6003 (600 s ruchu + 0,3 s przerwy). Wartość 1 oznacza do około 0,1 s do zakończenia, nie jedną sekundę. Bez aktywnego ruchu/celu wynosi 0.

Stan i pozycja są odczytywane bez wykonywania ruchu i bez pobierania oczekującej komendy. Dlatego tuż po RolAct można zobaczyć STAN=0, ale CEL inny niż 255 i dodatni czas: polecenie już przyjęto, a silnik jeszcze nie ruszył. Podobnie przez krótki czas po upływie timera STAN może nadal wskazywać ruch przy POZOSTALO=0, dopóki normalna obsługa rolet nie wyłączy wyjścia. Odczyt nie wykonuje STOP w zastępstwie tej obsługi.

Przy estymacji używany jest również czas, który upłynął od ostatniej aktualizacji ruchu. Zapytanie nie przestawia pinów, nie zeruje czasu ruchu, nie zużywa oczekującego polecenia, nie wysyła dodatkowego R= i nie zapisuje EEPROM.

## 7. StanRol i automatyczne R= — dotychczasowy format

```text
TX: AT+StanRol=1<CR>
RX: R=1,2,0,1,0<CR><LF>
```

Po ID występują stany rolet 1–4: 0 postój, 1 zamykanie, 2 otwieranie. Kod **3 nie jest dodawany do starego R=**; przerwa zmiany kierunku nadal wygląda w nim jak postój. R= nie zawiera procentów ani czasu pozostałego.

StanRol nie ma SUMY. ID=0 pyta lokalny S0804. Odpowiedź wraca portem zapytania. Skrócony status jest także automatycznie wysyłany na UART0 podczas obsługi rozpoczęcia ruchu, STOP, końca przejazdu i zmiany kierunku. Może być powtórzony po STOP dla już zatrzymanej rolety. Przy zajętym TX wysyłka może być odłożona i scalić zmiany do aktualnego stanu.

Nowe RolState i RolTime są wysyłane **wyłącznie na zapytanie**. Nie zastępują automatycznego R=. Można otrzymać asynchroniczne R= pomiędzy odpowiedziami na odczyty.

## 8. Zapis i Defaults

```text
TX: AT+SaveConfig=1,1<CR>
RX: SaveOK=1<CR><LF>
```

Zapisuje konfigurację, w tym czasy wszystkich rolet; nie zapisuje pozycji, celu ani aktualnego ruchu. Odpowiedź następuje po zapisie i weryfikacji. SaveERROR oznacza błąd rozpoczętego zapisu; RuleERROR — odrzucenie żądania przed rozpoczęciem.

```text
TX: AT+Defaults=1,1<CR>
RX: RuleOK=1<CR><LF>
```

Defaults zatrzymuje rolety, usuwa czasy i ważność pozycji oraz przywraca szerszą konfigurację RAM, w tym reguły i progi wejść. Zachowuje poprawne ID. Sam nie utrwala zmian w EEPROM. Jeśli chcesz zmienić tylko czas jednej rolety, użyj RolTime.

## 9. Przezroczystość modułów pośrednich

| Urządzenie | Wersja oprogramowania | Obsługa |
|---|---|---|
| S0804 | 21 | Wykonuje lokalne odczyty, przekazuje do innego ID |
| R0806T | 21 | Przekazuje GetRolTime, GetRolState i adresowane StanRol oraz odpowiedzi |
| R0808 | 21 | Przekazuje te same zapytania i odpowiedzi w parze portów |
| ETH0606T | 21 | Przekazuje nowe odczyty między USB i RS-232; bramka TCP kieruje zapytania do dalszych ID i przekazuje odpowiedzi |

Moduły przekaźnikowe nie udają lokalnych rolet: zapytanie o własne ID zwraca błąd. Adresowany StanRol przechodzi przez moduły pośrednie; StanRol=0 jest odczytem tylko lokalnego S0804, nie komendą zdalnego skanowania.

Przykładowa linia:

```text
Terminal ── R0808 ID=1 ── R0806T ID=2 ── S0804 ID=3

TX → R0808:         AT+GetRolTime=3,1,4<CR>
R0808 → R0806T:     AT+GetRolTime=3,1,4<CR><LF>
R0806T → S0804:     AT+GetRolTime=3,1,4<CR><LF>
S0804 → R0806T:     RolTime=3,1,200,220,424<CR><LF>
R0806T → R0808:     RolTime=3,1,200,220,424<CR><LF>
RX ← R0808:         RolTime=3,1,200,220,424<CR><LF>
```

Analogicznie wraca RolState. Odpowiedzi są raportami źródłowego S0804; odbiór tekstu RolTime=/RolState= nie konfiguruje modułu pośredniego i nie steruje jego wyjściami. Przekazywanie zachowuje zawartość odpowiedzi, w tym sumę i wartości 255.

ETH: zapytanie z USB do obcego ID wychodzi RS-232. Odpowiedź z RS-232 trafia do USB; jeśli przechodzi przez bramkę, jest też przekazywana do klienta TCP. Ramki nie są odsyłane na ten sam port źródłowy. ETH nadal ma osobne zasady bramkowania i nie staje się modułem CHAIN1.

## 10. Błędy i zgodność

```text
TX: AT+GetRolTime=1,1,3<CR>     ← zła suma, prawidłowo 2
RX: RuleERROR=1<CR><LF>
TX: AT+GetRolState=1,5,6<CR>    ← nie istnieje roleta 5
RX: RuleERROR=1<CR><LF>
TX: AT+GetRolState=0,1,1<CR>    ← ID=0 niedozwolone
RX: RuleERROR=1<CR><LF>
```

Poprawny odczyt zwraca dane bez dodatkowego RuleOK. Moduł pośredni może odrzucić błędny format, zakres lub sumę; ID błędu wskazuje wtedy odrzucający moduł. Brak wskazanego ID lub przerwana linia mogą dać ciszę zamiast błędu — stosuj timeout i sprawdzaj ID, numer rolety, prefiks oraz sumę odpowiedzi.

Stare RolAct, RolTime i R= zachowują format. GetRolState nie dodaje czujnika położenia; jego procent i czas pozostają estymacją czasową, którą mogą zaburzać właściwości mechaniczne rolety.
