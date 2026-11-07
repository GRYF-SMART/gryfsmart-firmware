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

## 5. Szybkie konfiguracje i scenariusze

Przykłady dotyczą jawnie wskazanego modułu i kanału. Przed zmianą istniejącej reguły odczytaj jej konfigurację; poniższa reguła zastępuje ustawienia reguły 1. Nie wysyłaj wszystkich przykładów jako jednego skryptu.

### 5.1. Przycisk WE1 przełącza przekaźnik WY1 — R0806T ID 3

Ustaw krótki próg 0,5 s, długi 2 s, a następnie regułę 1: krótkie naciśnięcie WE1 → TOGGLE WY1.

```text
AT+KeyTime=3,1,5,20,29<CR>
AT+Rule=3,1,1,1,0,0,0,0,0,0,0,3,0,0,0,0,0,9<CR>
AT+SaveConfig=3,3<CR>
```

W Rule: ID, numer reguły, EN, osiem masek wejść, sześć akcji wyjść, SUMA. Maska 1 oznacza krótkie naciśnięcie, akcja 3 przełączenie. Po KeyTime i Rule oczekuj `RuleOK=3`, po zapisie `SaveOK=3`. Przed uruchomieniem sprawdź również sloty zdalne i dodatkowe akcje tej reguły — mogą mieć wcześniej zapisane ustawienia.

### 5.2. Światło na 10 sekund — R0806T ID 3, WY1

```text
AT+Pulse=3,1,100,1<CR>
AT+GetOut=3<CR>
```

Pierwsza komenda włącza wyjście, a moduł wyłącza je po 10 s. Powtórzenie Pulse odnawia czas. Jest to bieżące sterowanie, nie zapis konfiguracji — SaveConfig nie jest potrzebne.

### 5.3. PWM 60% z łagodnym rozjaśnieniem 1 s — R0806T ID 3

```text
AT+PWM=3,4,60,10,77<CR>
AT+GetPWM=3<CR>
```

Odczyt pokazuje poziom bieżący i docelowy. Gdy rampa trwa, wartości mogą być różne. Nie zapisuj EEPROM po każdym ustawieniu jasności.

### 5.4. Kalibracja czasu i pozycja 50% — S0804 ID 4, roleta 1

Na postoju ustaw zmierzone pełne czasy: przykładowo 20 s otwierania i 22 s zamykania.

```text
AT+RolTime=4,1,200,220,425<CR>
AT+SaveConfig=4,4<CR>
AT+RolAct=4,1,2,0,7<CR>
```

Poczekaj na pełne zamknięcie, odczytując `AT+GetRolState=4,1,5`. Po potwierdzeniu znanej pozycji 0%, postoju i braku oczekującego ruchu wyślij:

```text
AT+RolAct=4,1,7,50,62<CR>
AT+GetRolState=4,1,5<CR>
```

Stan odświeżaj do zakończenia ruchu; nie zakładaj osiągnięcia 50% po samym RuleOK. Czasy 20/22 s są przykładem — wpisz rzeczywiste czasy swojego napędu.

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
