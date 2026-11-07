# 6. Protokół GRYFSMART — szybka integracja

System można skonfigurować i połączyć z innym systemem za pomocą złącza **RS-232** oraz **Ethernet TCP/IP**, podając adres IP bramki i numer portu TCP.

**[Pobierz przykład klienta TCP w Pythonie](https://raw.githubusercontent.com/GRYF-SMART/gryfsmart-firmware/main/PROTOKOL/przyklad_tcp.py)** · **[Pełny katalog komend](../docs/README.md)** · **[Przykłady konfiguracji instalacji](../docs/PRZYKLADY.md)**

Ten przewodnik pokazuje drogę od połączenia do sterowania i odbioru stanów w innym urządzeniu: kontrolerze, panelu, aplikacji lub systemie automatyki. Dotyczy nowego protokołu AT modułów GRYF. Przykładowe ID trzeba zastąpić adresami własnych modułów; pokazane odpowiedzi są ilustracjami, nie odczytami urządzeń.

## 1. Połączenie

### RS-232 — parametry komunikacji

| Parametr | Ustawienie |
|---|---|
| Prędkość | **115200 bit/s** |
| Liczba bitów danych | **8** |
| Parzystość | **Brak (N)** |
| Bity stopu | **1** |
| Kontrola przepływu | **Brak** — bez RTS/CTS i XON/XOFF |
| Typ interfejsu | **RS-232 z dodatnimi i ujemnymi poziomami napięcia**, potocznie „RS na ±12 V”; nie UART TTL 3,3/5 V |
| Sygnały | TX, RX i masa sygnałowa GND; TX jednej strony połącz z RX drugiej według opisu złącza |
| Zakończenie komendy | CR, bajt `0x0D` |
| Zakończenie odpowiedzi | CR lub CRLF — odbiornik obsługuje oba warianty |

Określenie „RS na 12 V” opisuje rodzaj interfejsu, a nie wymagane stałe napięcie na przewodzie danych. Rzeczywista amplituda zależy od nadajnika i obciążenia; np. transceiver MAX232 wytwarza poziomy RS-232 z zasilania 5 V. Nie podawaj stałego +12 V na TX/RX. Użyj adaptera **USB–RS232**, nie USB–TTL. [Dane producenta MAX232](https://www.ti.com/product/MAX232).

### Ethernet — adres IP i port

| Transport | Parametry | Zastosowanie |
|---|---|---|
| RS-232 | 115200 bit/s, 8N1, bez kontroli przepływu | Port logiczny 0 pierwszego modułu; kolejne moduły przez port 1 |
| ETH0606T | TCP do IP bramki; 5000 dla integracji, 5002 dla konfiguratora w aktualnym firmware | Ta sama składnia AT, bramka do RS-232 |
| ETH Mini GATE | Domyślnie `192.168.1.201:5002`, jeden klient | Przezroczysty most AT do RS-232 |

TCP 5001 jest portem bootloadera, **nie** portem normalnego sterowania. RS-232 wymaga właściwego interfejsu elektrycznego, nie bezpośredniego UART TTL.

Utrzymuj połączenie TCP zamiast otwierać nowe dla każdej komendy. Połącz moduły liniowo, nadaj unikalne ID 1–35 i przechowuj mapę ID → model. ID modułu nie jest adresem IP. Nie używaj `Search` jako odczytu: nadaje ID i zapisuje EEPROM. Do odczytu identyfikacji służy `Info`; szczegóły trasowania i Discovery opisuje [dokumentacja sieci](../docs/komendy-wspolne.md).

## 2. Ramki i sumy

Wysyłaj ASCII, bez spacji, zakończone **CR (0x0D)**. Przykład w kodzie: `b"AT+GetOut=2\r"`. Zapis `<CR>` poniżej oznacza bajt, nie tekst do wysłania.

Odbieraj linie zakończone CR z opcjonalnym LF. Akceptuj raporty przekaźników `O=` i `o=`. Odczyt z gniazda może zawierać pół ramki, kilka ramek lub końcówkę poprzedniej. Zachowuj bufor między odczytami i rozdzielaj dopiero po terminatorze.

Niektóre komendy mają **SUMA**: zwykłą sumę wcześniejszych pól liczbowych w zapisie dziesiętnym. To nie CRC ani suma znaków ASCII. Przykład: `AT+RolAct=4,1,7,50,62`, bo 4+1+7+50=62. Nie dopisuj sumy do komend, które jej nie mają (`SetOut`, `GetOut`, `Pulse`, `Timed`).

## 3. Komendy sterujące — wysyłanie poleceń

| Funkcja | Komenda | Moduły |
|---|---|---|
| Włącz / wyłącz / przełącz przekaźniki | `AT+SetOut=ID,A1,...,AN` | R0806T, R0808, ETH0606T |
| Włącz przekaźnik na czas | `AT+Pulse=ID,WY,CZAS,RESTART` | R0806T, R0808, ETH0606T |
| Wyłącz po czasie / impuls z opóźnieniem | `AT+Timed=ID,WY,TRYB,OPÓŹNIENIE,CZAS_ON,RESTART` | R0806T i R0808 FW33+ |
| Włącz po czasie i pozostaw ON | `AT+Timed=ID,WY,3,OPÓŹNIENIE,0,RESTART` | R0806T FW35+ |
| Poziom PWM i rampa | `AT+PWM=ID,AKCJA,WARTOŚĆ[,RAMPA],SUMA` | R0806T |
| Ustaw / skasuj / przełącz flagę | `AT+SetFlag=ID,NR,AKCJA,SUMA` | R0806T, R0808, ETH0606T, S0804 z obsługą flag |
| Otwórz / zamknij / STOP / STEP / procent | `AT+RolAct=ID,NR,AKCJA,PROCENT,SUMA` | S0804 |

Przykłady przyjmują: ID 2 = R0808, ID 3 = R0806T, ID 4 = S0804. ETH Mini przekazuje komendy do modułów — sama nie ma przekaźników, PWM ani rolet. Po każdym poleceniu obsłuż odpowiedź przed wysłaniem następnego. `RuleOK=ID` potwierdza przyjęcie, `RuleERROR=ID` odrzucenie.

### 3.1. Przekaźniki i czas

`AT+SetOut=ID,A1,...,AN` — akcja 0 pozostawia stan, 1 włącza, 2 wyłącza, 3 przełącza. **0 nie oznacza OFF.**

```text
AT+SetOut=2,1,0,0,0,0,0,0,0<CR>  R0808: włącz WY1
AT+SetOut=3,2,0,0,0,0,0<CR>      R0806T: wyłącz WY1
AT+Pulse=3,1,25,1<CR>             R0806T: włącz WY1 na 2,5 s
AT+Timed=3,1,3,50,0,1<CR>         R0806T FW35+: włącz WY1 po 5 s
AT+Timed=3,1,2,50,7,1<CR>         R0806T: impuls 0,7 s po 5 s
```

Komentarze po `<CR>` są objaśnieniem — nie wysyłaj ich. `Timed=ID,WY,TRYB,OPÓŹNIENIE,CZAS_ON,RESTART` używa dziesiątych części sekundy: 25 = 2,5 s. Tryb 1 wyłącza po opóźnieniu, 2 wykonuje opóźniony impuls, 3 włącza po opóźnieniu (wymaga firmware z tą funkcją). W trybie 3 obecny stan jest zachowany podczas oczekiwania, a po zakończeniu wyjście pozostaje ON.

Nie zakładaj, że każdy model/firmware obsługuje każdy tryb `Timed`. W przykładach celowo użyto R0806T FW35. `Pulse` jest dostępne także dla przekaźników R0808 i ETH0606T; nie steruj nim napędami S0804. RESTART=1 pozwala odnawiać timer. RESTART=0 chroni aktywny timer przed ponowieniem i zwykłym ON/OFF/TOGGLE. [Szczegóły Pulse](../docs/wyjscia-czasowe.md) · [Wyjścia i raporty](../docs/wyjscia-komendy.md).

### 3.2. PWM — R0806T

`AT+PWM=ID,AKCJA,WARTOŚĆ[,RAMPA],SUMA`.

```text
AT+PWM=3,4,60,10,77<CR>   ustaw 60%, rampa 1 s
AT+PWM=3,2,0,5<CR>       wyłącz
AT+PWM=3,1,0,4<CR>       włącz zapamiętany poziom
AT+PWM=3,3,0,6<CR>       przełącz z pamięcią
AT+GetPWM=3<CR>          odczytaj stan
```

Akcje: 0 bez zmian, 1 włącz zapamiętany poziom, 2 wyłącz, 3 przełącz z pamięcią, 4 ustaw procent. Rampa 0–50 w jednostkach 0,1 s. Dla przełączania bez pamięci sprawdź poziom: jeśli jest niezerowy, wyślij OFF; jeśli zero, wyślij ustawienie żądanego procentu. Jest to sekwencja klienta, nie nowy numer akcji protokołu.

Raport: `PWM=ID,POZIOM,CEL,ZAPAMIĘTANY,RAMPA_AKTYWNA,CZĘSTOTLIWOŚĆ_HZ`. [Pełny opis R0806T](../docs/R0806T.md).

### 3.3. Flagi — zmienne wirtualne

Moduł ma osiem flag w firmware obsługującym `SetFlag/GetFlags`. Bieżące wartości są w RAM i po restarcie wracają do zera. Nie są lampkami ani wyjściami fizycznymi.

```text
AT+SetFlag=3,1,1,5<CR>   ustaw flagę 1
AT+SetFlag=3,1,2,6<CR>   skasuj flagę 1
AT+SetFlag=3,1,3,7<CR>   przełącz flagę 1
AT+GetFlags=3,3<CR>      odczytaj flagi
Flags=3,5,8<CR><LF>      przykład: maska 5 = flagi 1 i 3 ustawione
```

SUMA w zapytaniu GetFlags to ID; w odpowiedzi to ID+MASKA. Bit 0 maski oznacza flagę 1. Po zmianie odczytaj `GetFlags`, zamiast zakładać otrzymanie osobnego zdarzenia o zmianie flagi.

### 3.4. S0804 — pełna obsługa rolety

`AT+RolAct=ID,ROLETA,AKCJA,PROCENT,SUMA`. ROLETA=1–4. Akcje: 1 OPEN, 2 CLOSE, 3 STOP, 4 STEP UP, 5 STEP DOWN, 6 STEP, 7 procent. Dla akcji 1–6 PROCENT=0.

```text
AT+RolTime=4,1,200,220,425<CR>  pełny przejazd: 20 s w górę, 22 s w dół
AT+SaveConfig=4,4<CR>          utrwal konfigurację
AT+RolAct=4,1,1,0,6<CR>        otwórz
AT+RolAct=4,1,3,0,8<CR>        STOP
AT+RolAct=4,1,2,0,7<CR>        zamknij
AT+RolAct=4,1,6,0,11<CR>       STEP
AT+RolAct=4,1,7,50,62<CR>      otwórz do 50%
AT+GetRolState=4,1,5<CR>       szczegółowy stan
AT+GetRolTime=4,1,5<CR>        czasy przejazdu
```

Komendy pokazują składnię, nie scenę do wysłania jedna po drugiej. Czasy `RolTime` ustawiaj na postoju. W aktualnym S0804 zakres wynosi 1–6553 (0,1–655,3 s), starsze wersje ograniczały go do 6000. Zmiana czasów i restart unieważniają pozycję. Pełny przejazd do końca przywraca jej znajomość; dopiero wtedy używaj pośrednich 1–99%. **0% zamknięta, 100% otwarta.** Pozycja jest estymacją czasową.

Odpowiedź: `RolState=ID,NR,STAN,ZNANA,POZYCJA,CEL,POZOSTAŁO,SUMA`.

| Pole | Znaczenie |
|---|---|
| STAN | 0 postój, 1 zamykanie, 2 otwieranie, 3 przerwa zmiany kierunku |
| ZNANA | 0 brak ustalonej pozycji, 1 pozycja znana |
| POZYCJA | 0–100%; wartość nieznaną traktuj jako niedostępną |
| CEL | 0–100%; 255 oznacza brak celu |
| POZOSTAŁO | Czas w jednostkach 0,1 s |
| SUMA | Suma wcześniejszych pól odpowiedzi |

Przykład poprawnej ramki: `RolState=4,1,2,1,35,70,82,195` = otwieranie, znana pozycja 35%, cel 70%, pozostało 8,2 s. Postój z celem i dodatnim czasem może oznaczać oczekiwanie na start. Sam STAN=0 nie dowodzi zakończenia dojazdu. „Zatrzymano po otwieraniu” klient wyznacza z poprzedniego potwierdzonego kierunku; po utracie komunikacji usuń tę pamięć.

STEP to cykl ruch/STOP/kierunek przeciwny/STOP, nie skok o określony procent. Raport `R=ID,S1,S2,S3,S4` informuje skrótowo o ruchu; do procentów odczytuj `GetRolState`. [Pełna specyfikacja](../docs/rolety-komendy.md).

## 4. Komendy pobierające stan i konfigurację

### 4.1. Wspólne dla modułów wykonawczych

Poniższe komendy dotyczą R0806T, R0808, S0804 i ETH0606T z firmware obsługującym daną funkcję. **Nie oznacza to broadcastu** — podaj ID jednego modułu i powtórz zapytanie dla kolejnych ID. ETH Mini jest bramką i ma osobne komendy lokalne w tabeli 4.3.

| Odczyt | Przykład wysłania | Odpowiedź / wynik |
|---|---|---|
| Model i wersja firmware | `AT+Info=3` | `ID=3,FW=...,MODEL=R0806T,...` |
| Stan wszystkich wejść jednego modułu | `AT+GetInputs=3` | `I=3,S1,...,SN`; 0 rozwarte, 1 zwarte |
| Osiem flag wirtualnych | `AT+GetFlags=3,3` | `Flags=3,MASKA,SUMA` |
| Minimum, średnia i maksimum pętli | `AT+Loop=3` | `LOOP=3,N=...,MIN_US=...,AVG_US=...,MAX_US=...,SAT=...` |
| Liczniki i przyczyny restartów | `AT+ResetStats=3` | Raport diagnostyczny; odczyt nie zeruje liczników |
| Progi naciśnięcia wejścia 1 | `AT+GetKeyTime=3,1,4` | `KeyTime=3,1,SHORT,LONG,SUMA` |
| Konfiguracja reguły 1 | `AT+GetRule=3,1,4` | `Rule=...`; liczba pól zależy od modelu |
| Konfiguracja zdalnego slotu 1 reguły 1 | `AT+GetRuleRemote=3,1,1,5` | `RuleRemote=...`; typ określa znaczenie danych |

GetRule odczytuje konfigurację, a nie informację o aktualnym wykonywaniu reguły. Wszystkie przykłady wysyłaj z końcowym CR.

### 4.2. Odczyty zależne od modelu

| Moduł / funkcja | Przykład wysłania | Odpowiedź / znaczenie |
|---|---|---|
| R0808 — 8 przekaźników | `AT+GetOut=2` | `O=2,S1,...,S8` |
| R0806T — 6 przekaźników | `AT+GetOut=3` | `o=3,S1,...,S6` |
| ETH0606T — 6 przekaźników, przykładowo ID 1 | `AT+GetOut=1` | `O=1,S1,...,S6`; akceptuj również raporty `o=` |
| R0806T — aktualny PWM | `AT+GetPWM=3` | `PWM=3,POZIOM,CEL,ZAPAMIĘTANY,RAMPA_AKTYWNA,HZ` |
| R0806T — akcja PWM reguły 1 | `AT+GetRulePWM=3,1,4` | Konfiguracja PWM reguły; nie bieżąca jasność |
| S0804 — ruch czterech rolet | `AT+StanRol=4` | `R=4,S1,S2,S3,S4` |
| S0804 — pełny stan rolety 1 | `AT+GetRolState=4,1,5` | `RolState=...`: ruch, ważność pozycji, procent, cel, pozostały czas i suma |
| S0804 — czasy rolety 1 | `AT+GetRolTime=4,1,5` | `RolTime=4,1,OPEN,CLOSE,SUMA`; czasy co 0,1 s |

Temperatury i regulatory mają dodatkowe odczyty zależne od modelu oraz konfiguracji czujników: [R0806T](../docs/R0806T.md), [R0808](../docs/R0808.md), [ETH0606T](../docs/ETH0606T.md). Nie odpytuj funkcji nieobecnej w danym module, np. GetPWM w S0804.

### 4.3. ETH Mini — lokalny odczyt bramki

| Komenda przez RS-232 | Wynik |
|---|---|
| `AT+Find=1` | Identyfikacja bramki |
| `AT+Net=1` lub `AT+NetFind` | Adres IP, maska, brama, DNS i stan W5500 |

Stan przekaźników i rolet za Mini odczytuj komendami do ich własnych ID przez TCP 5002. Nie wysyłaj do Mini odczytów wyjść, których nie posiada.

### 4.4. Przykładowa wymiana

```text
TX: AT+GetOut=2<CR>
RX: O=2,1,0,0,0,0,0,0,0<CR><LF>
TX: AT+GetInputs=2<CR>
RX: I=2,0,1,0,0,0,0,0,0<CR><LF>
TX: AT+GetFlags=3,3<CR>
RX: Flags=3,5,8<CR><LF>
TX: AT+GetRolState=4,1,5<CR>
RX: RolState=4,1,2,1,35,70,82,195<CR><LF>
```

Wynik: WY1 modułu 2 jest włączone, WE2 zwarte; flagi 1 i 3 modułu 3 są ustawione; roleta 1 modułu 4 otwiera się z pozycji 35% do 70%, zostało 8,2 s.

## 5. Szybkie przykłady — polecenia z zewnętrznego systemu

Polecenia wysyłasz z zewnętrznego kontrolera, terminala lub aplikacji przez RS-232 albo TCP bramki. **ID wskazuje moduł docelowy**; nie trzeba przełączać kabla do każdego modułu. Przykłady zakładają już nadane, unikalne adresy. Każdą komendę zakończ bajtem CR; po wysłaniu obsłuż odpowiedź przed kolejnym poleceniem. Nie wpisuj dosłownie oznaczeń TX, RX ani `<CR>`.

### 5.1. Zapal światło — moduł ID 3, wyjścia 1, 2 i 3

Dla **R0806T lub ETH0606T** z sześcioma przekaźnikami:

```text
TX: AT+SetOut=3,1,1,1,0,0,0<CR>
RX: RuleOK=3<CR><LF>
TX: AT+GetOut=3<CR>
```

Dla **R0808** z ośmioma przekaźnikami użyj zamiast tego:

```text
TX: AT+SetOut=3,1,1,1,0,0,0,0,0<CR>
RX: RuleOK=3<CR><LF>
TX: AT+GetOut=3<CR>
```

| Pole | Znaczenie |
|---|---|
| Pierwsze `3` | Adres modułu ID 3 |
| Pierwsze trzy akcje `1,1,1` | Włącz WY1, WY2 i WY3 |
| Pozostałe akcje `0` | Pozostaw pozostałe wyjścia bez zmian |

**Wybierz jedną wersję komendy zgodną z modelem**, nie wysyłaj obu. SetOut nie ma sumy kontrolnej. GetOut zwróci `O=3,...` lub `o=3,...`; pierwsze trzy stany powinny wynosić 1, pozostałe zależą od poprzedniego stanu. Aktywny chroniony timer może blokować zwykłe sterowanie — zawsze sprawdzaj odczyt. Do bieżącego włączenia światła nie używaj SaveConfig.

### 5.2. Ustaw PWM na 50% — R0806T, ID 3

```text
TX: AT+PWM=3,4,50,57<CR>
TX: AT+GetPWM=3<CR>
```

ID=3, akcja 4 oznacza ustawienie poziomu, wartość=50%, SUMA=3+4+50=57. To polecenie steruje wyjściem PWM modułu R0806T, a nie przekaźnikiem. Obsłuż potwierdzenie pierwszej komendy, następnie odczytaj raport `PWM=3,...` i sprawdź poziom docelowy 50%.

Wariant z rampą **1 s**:

```text
AT+PWM=3,4,50,10,67<CR>
```

RAMPA=10 oznacza 1 s, SUMA=3+4+50+10=67. Podczas rampy bieżący poziom może jeszcze różnić się od docelowego. SaveConfig nie jest potrzebne.

### 5.3. Otwórz rolety 1 i 2 na 50% — S0804, ID 5

Warunek: obie rolety mają ustawione rzeczywiste czasy pełnego otwierania/zamykania i znaną pozycję. Po restarcie albo zmianie czasów najpierw wykonaj pełny przejazd do końca. **0% oznacza zamknięcie, 100% pełne otwarcie.**

```text
TX: AT+RolAct=5,1,7,50,63<CR>
RX: RuleOK=5<CR><LF>
TX: AT+RolAct=5,2,7,50,64<CR>
RX: RuleOK=5<CR><LF>
```

| Roleta | ID | Akcja | Cel | Suma |
|---|---|---|---|---|
| 1 | 5 | 7 — pozycja procentowa | 50% | 5+1+7+50=63 |
| 2 | 5 | 7 — pozycja procentowa | 50% | 5+2+7+50=64 |

Są to dwie oddzielne komendy, nie jedna transakcja równoczesnego startu. Odczytuj stan każdej rolety:

```text
AT+GetRolState=5,1,6<CR>
AT+GetRolState=5,2,7<CR>
```

RuleOK potwierdza przyjęcie, a nie dojazd do 50%. Zakończenie potwierdź znaną pozycją 50%, postojem i brakiem oczekującego ruchu. Gdy roleta startuje powyżej 50%, dojedzie do celu w kierunku zamykania. Błąd lub nieznana pozycja nie oznacza osiągnięcia celu. Te komendy nie zmieniają czasów przejazdu ani EEPROM.

### 5.4. Wszystkie wejścia modułu ID 2 — krótkie 0,4 s, długie 2 s

Format: `AT+KeyTime=ID,WEJŚCIE,SHORT,LONG,SUMA`. Czasy mają jednostkę **0,1 s**: SHORT=4 to 0,4 s, LONG=20 to próg 2 s. SUMA=ID+WEJŚCIE+SHORT+LONG.

Dla **R0806T, R0808 albo S0804** ustaw wszystkie osiem wejść osobnymi komendami:

```text
AT+KeyTime=2,1,4,20,27<CR>
AT+KeyTime=2,2,4,20,28<CR>
AT+KeyTime=2,3,4,20,29<CR>
AT+KeyTime=2,4,4,20,30<CR>
AT+KeyTime=2,5,4,20,31<CR>
AT+KeyTime=2,6,4,20,32<CR>
AT+KeyTime=2,7,4,20,33<CR>
AT+KeyTime=2,8,4,20,34<CR>
```

Dla **ETH0606T** wykonaj tylko pierwsze sześć komend, ponieważ ten model ma sześć wejść. ETH Mini nie ma takich wejść przyciskowych. Po każdej komendzie oczekuj `RuleOK=2`; jeżeli wystąpi RuleERROR, sprawdź model i numer wejścia. Po poprawnym ustawieniu wszystkich wejść zapisz konfigurację jednym poleceniem:

```text
TX: AT+SaveConfig=2,2<CR>
RX: SaveOK=2<CR><LF>
```

Sprawdzenie ustawień wejścia 1:

```text
TX: AT+GetKeyTime=2,1,3<CR>
RX: KeyTime=2,1,4,20,27<CR><LF>
```

Dla pozostałych wejść zmień numer WE i sumę zapytania na `2+WE`.

| Przytrzymanie | Raport |
|---|---|
| Do 0,4 s, następnie puszczenie | `PS=2,WE` — krótkie naciśnięcie po puszczeniu |
| Powyżej 0,4 s, ale krócej niż 2 s | Brak PS i PL; nadal są raporty zwarcia/rozwarcia `I=2,...` |
| Osiągnięcie progu 2 s i dalsze trzymanie | Jedno `PL=2,WE` — długie naciśnięcie podczas trzymania |

Firmware wyzwala LONG **po osiągnięciu progu**, więc potoczne „powyżej 2 sekund” przy ustawieniu 20 oznacza zdarzenie od 2 s. Jeśli wymagane jest ściśle więcej niż 2 s, najbliższy próg to **2,1 s (LONG=21)**; w każdej komendzie powyżej zwiększ LONG i SUMA o 1. Czasy liczone są od potwierdzonych stanów wejścia, z uwzględnieniem filtrowania styków. KeyTime ustawia rozpoznawanie naciśnięć; przypisanie akcji przekaźnika lub rolety wymaga osobnej reguły albo obsługi PS/PL w systemie zewnętrznym.

## 6. Odbiór, błędy i synchronizacja

| Ramka | Znaczenie / działanie klienta |
|---|---|
| `I=ID,...` | Stan wejść: 0 rozwarte, 1 zwarte |
| `PS=ID,WE`, `PL=ID,WE` | Krótkie / długie naciśnięcie; zdarzenie, nie stały stan |
| `O=ID,...` / `o=ID,...` | Aktualne stany sterowania przekaźnikami 0/1 |
| `RuleOK=ID` | Przyjęcie komendy; nie potwierdza fizycznego styku ani zakończenia ruchu |
| `RuleERROR=ID` | Niepoprawna składnia, suma, zakres lub stan modułu |
| `SaveOK=ID`, `SaveERROR=ID` | Wynik zapisu konfiguracji |
| `KEYERROR=ID,...`, `PWMERROR=ID,...` | Diagnostyka; zaloguj i ponownie odczytaj odpowiedni stan |

Odpowiedzi i zdarzenia mogą się przeplatać. Kojarz je według prefiksu i ID, a dla odczytów kanału także numeru wejścia/rolety. Protokół nie nadaje każdej komendzie unikalnego identyfikatora transakcji; kolejkuj operacje i unikaj kilku równoległych komend oczekujących na identyczne `RuleOK`.

Zalecenie dla klienta: rozpocznij od timeoutu 1–2 s i odstępu między zapytaniami, dobierz je do długości linii. To ustawienia klienta, nie gwarantowane czasy protokołu. Po timeoutach oznacz dane jako nieaktualne. Po ponownym połączeniu odczytaj stan na nowo. Nie ponawiaj automatycznie TOGGLE, STEP lub impulsu — powtórzenie może wykonać akcję drugi raz. Zwykłe odczyty można ponowić z ograniczeniem liczby prób.

Kontroluj długość ramki, liczbę pól, zakresy, ID i sumę tam, gdzie występuje. TCP nie zapewnia granic komend aplikacyjnych. Nie interpretuj pustej odpowiedzi, utraty połączenia ani nieznanej pozycji jako OFF/0%.

## 7. Zapis konfiguracji i dalsza dokumentacja

Konfigurację roboczą zapisuje `AT+SaveConfig=ID,ID`; wykonuj go po zmianach, nie w każdej pętli odświeżania. `Defaults`, `Search`, reset i BOOT mają skutki uboczne i nie należą do zwykłego odczytu stanu.

Diagnostyka: `AT+Info=ID`, `AT+Loop=ID`, `AT+ResetStats=ID`. Loop podaje minimum/średnią/maksimum czasu pętli; ResetStats odczytuje liczniki i przyczyny restartów. [Formaty odpowiedzi](../docs/komendy-wspolne.md).

- [Wejścia, PS/PL, KeyTime i odczyty](../docs/wejscia-komendy.md)
- [Reguły i różnice między modułami](../docs/reguly-porownanie.md)
- [R0806T, PWM i temperatury](../docs/R0806T.md)
- [R0808](../docs/R0808.md), [ETH0606T](../docs/ETH0606T.md), [S0804](../docs/S0804.md)

Starsze rozdziały szczegółowe wskazują wersję, dla której opisano daną funkcję. Nie traktuj ich starych numerów jako numerów najnowszego wydania; [bieżące HEX-y i wersje](../HEX) są zestawione osobno. Nową funkcję sprawdzaj w module docelowym i modułach pośrednich.


[1. Aplikacja GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/GRYFSMART) · [2. GRYFSMART-Programator](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/AKTUALIZATOR) · [3. Driver Home Assistant](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/HOME-ASSISTANT) · [4. Driver RTI](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/RTI) · [5. Instalator Bootloader](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/BOOTLOADER) · [6. Protokół GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/PROTOKOL) · [7. System i moduły GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/SYSTEM)
