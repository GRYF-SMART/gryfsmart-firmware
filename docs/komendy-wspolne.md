# Wspólne komendy identyfikacji i adresowania GRYFSMART

Dokument opisuje `AT+Search`, odpowiedź `AT+Find`, `AT+Discovery` oraz `AT+Info` na podstawie bieżących źródeł aplikacji. Obsługę w starszym wsadzie należy sprawdzić dla jego wersji. Przykładowe wersje i dane identyfikacyjne poniżej nie są odczytem z fizycznych urządzeń.

## 1. Łącze i oznaczenia

- Łącze serwisowe: **115200 bit/s, 8N1, bez kontroli przepływu**.
- `<CR>` oznacza jeden bajt `0x0D`, a `<LF>` bajt `0x0A`. Nie wpisuj dosłownie znaków `<CR>` do terminala.
- Komendę zakończ CR; odpowiedzi aplikacji są zakończone CRLF. Terminal może wysyłać CRLF.
- `TX` to tekst wysłany przez terminal/sterownik, `RX` to odpowiedź odebrana przez niego.
- W opisie modułu port wejściowy oznacza port, którym przyszła komenda. Moduły liniowe przekazują ją drugim portem, a odpowiedź wraca w stronę nadawcy.
- **ID jest adresem logicznym modułu 1–35, a nie adresem IP.** Adres IP dotyczy osobno konfiguracji sieci Ethernet.
- Liczby w Search i Info są dziesiętne. Parametry HOPS i SEQ w Discovery są **szesnastkowe**.
- Te trzy komendy nie wymagają dodatkowego pola SUMA znanego z komend konfiguracji reguł.

| Komenda | Cel | Wybór modułu | Zapis EEPROM |
|---|---|---|---|
| `AT+Search=LICZNIK,DOCELOWE_ID` | Nadanie ID i identyfikacja | Pozycja liczona od strony nadawcy | Tak, ID wybranego modułu |
| `AT+Discovery` | Identyfikacja modułu lokalnego | Moduł przy terminalu, port logiczny 0 | Nie |
| `AT+Discovery=HOPS,SEQ` | Identyfikacja modułu w linii | Liczba przejść do kolejnych modułów | Nie |
| `AT+Info=ID` | Szczegółowa identyfikacja | Zapisane ID; 0 oznacza moduł lokalny | Nie |

Discovery opisane tutaj obsługują aplikacje R0808, R0806T i S0804 z włączonym `CHAIN_SERVICE`. Aktualna aplikacja ETH0606T nie implementuje tego protokołu. Info jest dostępne również w ETH0606T; jego bramka ma osobne zasady przekazywania, opisane na końcu.

## 2. AT+Search — wyszukanie pozycji i trwałe nadanie ID

### 2.1. Co wysyła sterownik

```text
AT+Search=LICZNIK,DOCELOWE_ID<CR>
```

Spotykany zapis `AT+Search=ID,ILOSC_MODULOW` wymaga doprecyzowania: **pierwsze pole nie jest dotychczasowym ID odbiorcy, a drugie nie oznacza automatycznego ponumerowania wszystkich modułów jedną komendą**.

| Pole | Znaczenie w aktualnej implementacji |
|---|---|
| `LICZNIK` | Liczba pozycji już uwzględnionych przed bieżącym modułem; przy wysyłaniu od początku linii użyj 0 |
| `DOCELOWE_ID` | Docelowa pozycja i jednocześnie nowe ID; zakres 1–35 |

Musi zachodzić `0 <= LICZNIK < DOCELOWE_ID <= 35`. Aby ponumerować N urządzeń od początku linii, sterownik kolejno wysyła `AT+Search=0,1`, `AT+Search=0,2`, ..., `AT+Search=0,N`, oczekując na odpowiedź po każdym wywołaniu.

### 2.2. Co odbiera i wysyła moduł

Każdy moduł liniowy R0808/R0806T/S0804:

1. Odbiera ramkę i zwiększa LICZNIK o 1.
2. Jeżeli wynik jest mniejszy od DOCELOWE_ID, wysyła drugim portem Search ze zwiększonym licznikiem. Nie zmienia własnego ID i nie zapisuje EEPROM.
3. Jeżeli wynik jest równy DOCELOWE_ID, przyjmuje tę wartość jako nowe ID i zapisuje ją do EEPROM. Nie przekazuje Search dalej.
4. Po poprawnym zapisie/weryfikacji odsyła odpowiedź portem, którym przyszła komenda:

```text
AT+Find=ID,WERSJA_FW,TYP<CR><LF>
```

Moduły pośrednie przekazują odpowiedź Find w stronę sterownika. Zapis adresu nie zapisuje całej konfiguracji reguł i czasów; nie wymaga dodatkowego SaveConfig do utrwalenia samego ID.

### 2.3. Parametry odpowiedzi AT+Find

| Pole | Znaczenie | Przykład |
|---|---|---|
| `ID` | Nadany adres logiczny | `3` |
| `WERSJA_FW` | Wersja oprogramowania, z zachowaniem zer na początku | `0730` |
| `TYP` | Numeryczny typ modułu | `3` dla S0804 |

| Typ | Model |
|---|---|
| 3 | S0804 |
| 4 | R0806T |
| 5 | R0808 |
| 6 | ETH0606T |

Nazwa pola `MAC` w starszym kodzie przechowuje tutaj wersję firmware, a nie ethernetowy adres MAC. Odpowiedź ma znak `=`: `AT+Find=...`, nie `AT+Find-...`.

### 2.4. Przykład: trzy moduły w linii

```text
Terminal ── M1: R0808 ── M2: R0806T ── M3: S0804
              ID=1          ID=2          ID=3
```

Powyższe ID są wynikiem procedury. Przed jej wykonaniem mogą być inne lub powtarzać się. Wersje w przykładzie: R0808 0010, R0806T 0017, S0804 0730.

**Krok 1 — adresowanie pierwszego modułu:**

```text
Terminal TX → M1:  AT+Search=0,1<CR>
M1: licznik 0 → 1; zapis ID=1 do EEPROM
Terminal RX ← M1:  AT+Find=1,0010,5<CR><LF>
```

M2 i M3 nie otrzymują tej komendy.

**Krok 2 — adresowanie drugiego modułu:**

```text
Terminal TX → M1:  AT+Search=0,2<CR>
M1 TX → M2:       AT+Search=1,2<CR><LF>
M2: licznik 1 → 2; zapis ID=2 do EEPROM
M2 TX → M1:       AT+Find=2,0017,4<CR><LF>
Terminal RX ← M1:  AT+Find=2,0017,4<CR><LF>
```

M1 tylko przekazuje ramki, nie zapisuje ponownie swojego ID. M3 nie otrzymuje Search.

**Krok 3 — adresowanie trzeciego modułu:**

```text
Terminal TX → M1:  AT+Search=0,3<CR>
M1 TX → M2:       AT+Search=1,3<CR><LF>
M2 TX → M3:       AT+Search=2,3<CR><LF>
M3: licznik 2 → 3; zapis ID=3 do EEPROM
M3 TX → M2:       AT+Find=3,0730,3<CR><LF>
M2 TX → M1:       AT+Find=3,0730,3<CR><LF>
Terminal RX ← M1:  AT+Find=3,0730,3<CR><LF>
```

Samo `AT+Search=0,3` adresuje tylko trzeci moduł, a nie wszystkie trzy. Liczenie zależy od strony podłączenia terminala, nie od dotychczasowych ID.

### 2.5. Odrzucenie i brak odpowiedzi

Niepoprawny format/zakres albo niedozwolony stan, np. wykonywanie reguł lub zajęty zapis konfiguracji, może dać `RuleERROR=ID<CR><LF>`. ID w błędzie identyfikuje moduł odrzucający komendę. Nie traktuj braku odpowiedzi jako potwierdzenia zapisu: nieistniejąca pozycja, zerwana linia lub utracona ramka mogą nie wygenerować żadnego błędu zwrotnego. Sterownik powinien stosować timeout i sprawdzić wynik przed następnym krokiem.

## 3. AT+Discovery — rozpoznanie bez zmiany adresów

### 3.1. Zapytanie lokalne

Sterownik wysyła na port logiczny 0:

```text
AT+Discovery<CR>
```

Moduł przy terminalu odpowiada własną identyfikacją. Komenda bez parametrów **nie rozsyła zapytania do wszystkich urządzeń**. `AT+ModuleInfo` jest aliasem tej operacji w protokole CHAIN1.

Przykład dla lokalnego S0804 o zapisanym ID=3, wejściach i wyjściach równych 0:

```text
TX: AT+Discovery<CR>
RX: Chain=0,OK,S0804;0730;3;APP;ATmega1284P;UNKNOWN;0;0;CHAIN1*129B<CR><LF>
```

### 3.2. Zapytanie do pozycji w linii

```text
AT+Discovery=HOPS,SEQ<CR>
```

| Pole | Znaczenie |
|---|---|
| `HOPS` | Liczba przejść dalej, w HEX; 0 = pierwszy moduł, 1 = drugi, 2 = trzeci; maksymalnie `22` HEX = 34 przejścia |
| `SEQ` | Numer zapytania nadany przez sterownik w HEX, 0–FFFF; odpowiedź zachowuje jego zapis |

Discovery nie wymaga znajomości aktualnego ID. Nie zmienia ID ani typu i nie zapisuje EEPROM. Zwraca model, wersję oraz zapisany adres. Typ rozpoznaje się po nazwie modelu, a nie po polu numerycznym TYP z Find.

Na tej samej linii trzech modułów:

```text
Terminal TX → M1:  AT+Discovery=2,03<CR>
M1 TX → M2:       AT+Discovery=1,03<CR><LF>
M2 TX → M3:       AT+Discovery=0,03<CR><LF>
M3 TX → M2:       Chain=03,OK,S0804;0730;3;APP;ATmega1284P;UNKNOWN;0;0;CHAIN1*F784<CR><LF>
M2 TX → M1:       ta sama odpowiedź Chain
Terminal RX ← M1:  ta sama odpowiedź Chain
```

HOPS maleje na każdym przejściu. SEQ pozostaje bez zmian. Moduły przyjmują zapytania Discovery od strony portu logicznego 0, przekazują je portem 1, a odpowiedzi wracają z portu 1 na port 0. Nie jest to symetryczne adresowanie od dowolnego końca linii, jak w Search.

### 3.3. Format odpowiedzi

```text
Chain=SEQ,OK,MODEL;FW;ID;TRYB;MCU;UNKNOWN;WEJSCIA;WYJSCIA;CHAIN1*CRC16<CR><LF>
```

| Pole | Znaczenie |
|---|---|
| `SEQ` | Numer zapytania; przy komendzie bez parametrów 0 |
| `OK` | Zapytanie obsłużone |
| `MODEL` | R0808, R0806T albo S0804 |
| `FW` | Wersja firmware |
| `ID` | Aktualny adres logiczny, dziesiętnie |
| `TRYB` | `APP` w odpowiedzi działającej aplikacji; bootloader ma osobną implementację |
| `MCU` | Typ mikrokontrolera |
| `UNKNOWN` | Stałe pole tej implementacji; nie jest odczytem numeru seryjnego |
| `WEJSCIA` | Dziesiętna maska stanów wejść, nie liczba wejść |
| `WYJSCIA` | Dziesiętny odczyt PORTC w aktualnych adapterach; interpretacja bitów zależy od modelu, nie jest to liczba wyjść |
| `CHAIN1` | Znacznik obsługi protokołu |
| `CRC16` | Cztery cyfry HEX CRC-16/CCITT; inicjalizacja FFFF, wielomian 1021, zakres od SEQ do CHAIN1, bez `Chain=`, `*` i CRLF |

CRC w przykładach jest policzone dla dokładnie podanych danych. Zmiana ID, wersji lub stanu wejść/wyjść zmieni CRC. Błędne parametry lub brak modułu mogą skutkować ciszą; wymagany jest timeout w sterowniku.

### 3.4. Skanowanie całej linii

Sterownik pyta kolejno `AT+Discovery=0,01`, `AT+Discovery=1,02`, `AT+Discovery=2,03`, itd., za każdym razem czekając na odpowiedź. Wynik daje pozycję, model i dotychczasowe ID bez ich zmiany. Brak odpowiedzi może oznaczać koniec linii, ale też przerwę albo starsze urządzenie bez CHAIN1.

Discovery nie modyfikuje konfiguracji ani wyjść, lecz aktywuje czasowe wyciszanie zwykłych ramek nadawczych przez mechanizm serwisowy `chain_quiet()`. Nie używaj go jako częstego odpytywania podczas sterowania: „bez zapisu EEPROM” nie oznacza braku wpływu na bieżącą komunikację.

## 4. AT+Info — szczegółowe informacje bez zmiany konfiguracji

### 4.1. Co wysyła sterownik

```text
AT+Info=ID<CR>
```

`ID=1..35` wybiera moduł po zapisanym adresie. `ID=0` pyta urządzenie bezpośrednio przy terminalu, nie oznacza broadcastu. Info nie zmienia ID, konfiguracji, stanu wyjść ani zawartości EEPROM.

Moduł liniowy o innym ID przekazuje komendę bez zmiany parametrów drugim portem. Moduł zgodny z ID odpowiada portem wejściowym i nie przekazuje zapytania dalej. Dlatego przy powielonych ID odpowiedź może pochodzić tylko od pierwszego pasującego urządzenia; do rozpoznania pozycji użyj Discovery.

### 4.2. Co odsyła moduł

Odpowiedź jest pojedynczą linią zaczynającą się od `ID=`, a nie `AT+Info=`:

```text
ID=ID,FW=WERSJA,MODEL=MODEL,MCU=MIKROKONTROLER,PCB=REWIZJA,GIT=COMMIT,DIRTY=STAN,UTC=BUILD,SIG=SYGNATURA,CAL=KALIBRACJA,SERIAL=DANE,STATUS=STATUS<CR><LF>
```

ETH0606T dodatkowo wstawia `F_CPU=16000000` po polu MCU.

| Pole | Znaczenie |
|---|---|
| `ID`, `FW`, `MODEL`, `MCU` | Adres, wersja aplikacji, model modułu i mikrokontroler |
| `PCB` | Zadeklarowana przy kompilacji rewizja PCB; nie jest automatycznym rozpoznaniem płytki |
| `GIT`, `DIRTY`, `UTC` | Metadane kompilacji: rewizja źródeł, stan zmian i data/czas kompilacji |
| `SIG` | Sygnatura mikrokontrolera, HEX |
| `CAL` | Odczyt fabrycznego bajtu kalibracji, HEX |
| `SERIAL` | Dziewięć odczytanych bajtów fabrycznych, 18 cyfr HEX; nie traktować jako potwierdzonego unikalnego numeru |
| `STATUS` | `EMPTY` dla samych zer lub FF w SERIAL, w pozostałych przypadkach `UNVERIFIED` |

### 4.3. Przykład odczytu trzeciego modułu

```text
Terminal TX → M1:  AT+Info=3<CR>
M1 TX → M2:       AT+Info=3<CR><LF>
M2 TX → M3:       AT+Info=3<CR><LF>
M3 TX → M2:       ID=3,FW=0730,MODEL=S0804,MCU=ATmega1284P,PCB=UNKNOWN,GIT=unknown,DIRTY=unknown,UTC=unknown,SIG=1E9705,CAL=80,SERIAL=000000000000000000,STATUS=EMPTY<CR><LF>
M2 TX → M1:       ta sama odpowiedź ID=...
Terminal RX ← M1:  ta sama odpowiedź ID=...
```

Pola fabryczne i metadane są przykładowe; rzeczywiste wartości zależą od urządzenia i sposobu kompilacji. Zapytanie lokalne `AT+Info=0` zakończyłoby się odpowiedzią M1, nawet gdy jego zapisane ID byłoby inne niż 1.

Przy błędnej komendzie S0804/R0806T mogą odpowiedzieć `RuleERROR=ID`, a R0808/ETH0606T `InfoERROR=ID`. Poprawne Info nie wymaga dodatkowego potwierdzenia RuleOK.

## 5. ETH0606T i rozróżnienie sposobów podłączenia

Przykłady linii M1–M3 dotyczą bezpośredniego podłączenia do R0808/R0806T/S0804. ETH0606T jest bramką/urządzeniem końcowym i nie należy zakładać identycznego przekazywania obu portami.

- Lokalny parser ETH przyjmuje Search i zapisuje ID tylko wtedy, gdy LICZNIK+1 jest równy DOCELOWE_ID; nie realizuje przekazywania Search jak moduł liniowy.
- W ścieżce bramki TCP ETH jest pozycją/ID 1. `AT+Search=0,1` wykonuje odczyt Find urządzenia ETH. Dla kolejnych pozycji bramka przekazuje przez RS-232 np. `AT+Search=1,3` po odebraniu z TCP `AT+Search=0,3`.
- Bramka TCP kieruje adresowane zapytania `AT+Info=2..35` do RS-232. Odczyt lokalny Info dotyczy ETH.
- Aktualne ETH nie obsługuje Discovery/CHAIN1. Nie przenoś przykładu Discovery przez tę bramkę bez osobnego potwierdzenia obsługi w danym firmware.

## 6. Podstawa opisu

- Search i Info: `S0804/src/komendy_at.c`, `R0806T/src/komendy_at.c`, `R0808/src/komendy_at.c`, `R0808/src/diagnostics.c`.
- Discovery: `BOOTLOADER/source/chain/app.inc`, `protocol.h` oraz adaptery `*/src/chain_service.c`.
- ETH: `ETH-0606T/src/komendy_at.c`, `diagnostics.c`, `network/gateway.c`.
- Typy i wersje: `*/src/ustawienia.h`.
