# Wejścia GRYFSMART — komendy, odczyty i raporty I / PS / PL

Kompletna instrukcja protokołu wejść przyciskowych, bez opisu komend RULE i konfiguracji reguł. Obejmuje ustawianie parametrów, odczyt GET, utrwalanie konfiguracji i raporty o zdarzeniach. Dokumentacja dotyczy oprogramowania w wersji **21** wszystkich czterech modeli.

## 1. Moduły i podstawowe zasady

| Moduł | Liczba wejść | Numery wejść | KeyTime / GetInputs / GetKeyTime |
|---|---:|---|---|
| R0808 | 8 | 1–8 | Obsługiwane |
| R0806T | 8 | 1–8 | Wszystkie obsługiwane |
| S0804 | 8 | 1–8 | Wszystkie obsługiwane |
| ETH0606T | 6 | 1–6 | Obsługiwane |

R0806T ma sześć wyjść przekaźnikowych, ale **osiem wejść**. Liczby wejść i wyjść nie są identyczne we wszystkich modelach.

- [Parametry i zasady komunikacji](komendy-wspolne.md#zasady-komunikacji-i-struktura-sieci).
- ID to adres logiczny modułu **1–35**, a nie jego adres IP ani numer wejścia.
- Wszystkie liczby w tej instrukcji są dziesiętne. Wysyłaj komendy bez spacji.
- `<CR>` oznacza jeden bajt 0x0D, `<LF>` — 0x0A; nie wysyłaj dosłownego napisu `<CR>`.
- Zapytania zakończ CR. Odpowiedzi i raporty pokazane poniżej kończą się CRLF. Terminal może wysyłać CRLF.
- `TX` oznacza wysłanie przez terminal/sterownik, `RX` — odebranie przez niego danych od modułu.
- Dla wszystkich pięciu komend AT z poniższej tabeli ID=0 **nie jest obsługiwane**. Nie przenoś tu zasady ID=0 znanej z Info.

## 2. Pełna lista komend i raportów wejściowych

| Ramka | Kierunek i cel | Wpływ na konfigurację |
|---|---|---|
| `AT+KeyTime=ID,WE,SHORT,LONG,SUMA` | Sterownik → moduł: ustaw progi naciśnięcia jednego wejścia | Zmienia RAM |
| `AT+GetKeyTime=ID,WE,SUMA` | Sterownik → moduł: odczytaj progi jednego wejścia | Tylko odczyt |
| `KeyTime=ID,WE,SHORT,LONG,SUMA` | Moduł → sterownik: odpowiedź na GetKeyTime | Nie zmienia konfiguracji |
| `AT+GetInputs=ID` | Sterownik → moduł: odczytaj wszystkie wejścia | Tylko odczyt |
| `I=ID,S1,S2,...,SN` | Moduł → sterownik: zmiana wejścia lub odpowiedź na GetInputs | Raport stanu |
| `PS=ID,WE` | Moduł → sterownik: krótkie naciśnięcie | Raport zdarzenia |
| `PL=ID,WE` | Moduł → sterownik: długie naciśnięcie | Raport zdarzenia |
| `AT+SaveConfig=ID,SUMA` | Sterownik → moduł: utrwal konfigurację, w tym progi wejść | Zapis EEPROM |
| `AT+Defaults=ID,SUMA` | Sterownik → moduł: przywróć domyślną konfigurację roboczą | Zmienia RAM, ma szerszy zakres niż wejścia |
| `RuleOK=ID` / `RuleERROR=ID` | Moduł → sterownik: przyjęcie/odrzucenie komendy | Potwierdzenie, także dla KeyTime i Defaults |
| `SaveOK=ID` / `SaveERROR=ID` | Moduł → sterownik: wynik rozpoczętego zapisu | Potwierdzenie zapisu |
| `KEYERROR=ID,LICZNIK` | Moduł → sterownik: przepełnienie kolejki zdarzeń wejść | Diagnostyka |

Nazwa odpowiedzi RuleOK/RuleERROR jest wspólna dla wielu poleceń — występuje również poza konfiguracją reguł.

Nie ma osobnych komend GetPS, GetPL, GetShort ani GetLong. Nie ma też komendy AT do ustawienia NO/NC, czasu filtrowania styków, okresu próbkowania ani częstotliwości powtarzania PL. GetKeyTime pyta o **jedno** wejście; aby odczytać wszystkie progi, wyślij osobne zapytanie dla każdego wejścia.

## 3. Co oznaczają stany wejścia i kiedy powstaje zdarzenie

| Stan | Znaczenie fizyczne |
|---|---|
| `0` | Wejście rozwarte |
| `1` | Wejście zwarte do masy |

To znaczenie fizyczne, niezależne od tego, czy podłączony przycisk/czujnik jest opisany jako NO czy NC. Protokół nie odwraca automatycznie znaczenia na podstawie typu styku.

Wejścia są próbkowane co **2 ms**. Potwierdzenie zmiany wymaga 11 pełnych odstępów próbkowania, czyli 22 ms od pierwszego odczytu kandydującej zmiany. Przy regularnym próbkowaniu daje to około **22–24 ms od fizycznego zbocza**. Drgania styków mogą rozpocząć potwierdzanie od nowa. Progi SHORT i LONG są liczone od potwierdzonego zwarcia; puszczenie też musi zostać potwierdzone.

Przy starcie moduł przyjmuje wejścia jako rozwarte. Wejście rzeczywiście zwarte przy uruchomieniu może po filtrowaniu wygenerować raport zwarcia, a po dalszym przytrzymaniu — PL. Nie trzeba wysyłać komendy, aby moduł rozpoczął obserwację wejść.

Wykrycie zdarzenia i wysłanie raportu są rozdzielone: zdarzenie trafia do kolejki, a raport wychodzi podczas jej obsługi. Obciążenie komunikacji może opóźnić odebranie raportu. Czas pojawienia się tekstu w terminalu nie jest dokładnym znacznikiem czasu fizycznego naciśnięcia.

## 4. I= — stan wejść po zmianie lub na żądanie

Format dla modułu o ośmiu wejściach:

```text
I=ID,WE1,WE2,WE3,WE4,WE5,WE6,WE7,WE8<CR><LF>
```

Format ETH0606T:

```text
I=ID,WE1,WE2,WE3,WE4,WE5,WE6<CR><LF>
```

Po ID występują osobne stany wejść w kolejności numerów; **nie jest to jedna liczba będąca maską bitową**. Raport nie zawiera sumy kontrolnej.

Przykład: ID=2, zwarte wejścia 1 i 3:

```text
RX: I=2,1,0,1,0,0,0,0,0<CR><LF>
```

Moduł wysyła I= w dwóch sytuacjach:

1. **Automatycznie**, po obsłużeniu potwierdzonego zwarcia lub rozwarcia dowolnego wejścia. Raport zawiera obraz wejść zapisany przy tym zdarzeniu, więc może opisywać wcześniejszy stan niż aktualny w chwili transmisji.
2. **Na żądanie GetInputs**, jako odczyt aktualnej potwierdzonej maski wejść w chwili obsługi komendy.

GetInputs nie generuje naciśnięcia ani puszczenia i nie usuwa oczekujących zdarzeń. Kilka jednocześnie zmieniających się wejść może dać kilka raportów I=, z pośrednimi obrazami stanu.

Automatyczny raport i odpowiedź na GetInputs mają identyczny format, bez numeru zapytania. Sterownik powinien odbierać również raporty asynchroniczne i nie zakładać, że każda następna linia odpowiada ostatniej komendzie.

## 5. PS= — krótkie naciśnięcie

```text
PS=ID,WEJSCIE<CR><LF>
```

Przykład:

```text
RX: PS=2,3<CR><LF>
```

To informacja, że **wejście 3 modułu ID=2 zostało krótko naciśnięte i puszczone**. Drugie pole jest numerem wejścia, a nie jego stanem ani czasem.

PS jest generowane **po potwierdzonym rozwarciu**, gdy zmierzony czas zwarcia był dodatni, nie przekroczył progu SHORT i nie wystąpił wcześniej LONG. Podczas samego trzymania przycisku PS nie jest wysyłane.

Przy SHORT=5, LONG=20 (0,5 s i 2 s), przytrzymanie około 0,3 s powoduje PS po puszczeniu. Dokładne granice zależą od potwierdzonych stanów i próbkowania, a nie wyłącznie od fizycznego czasu styku.

PS nie zawiera pola SUMA i nie jest potwierdzane przez RuleOK.

## 6. PL= — długie naciśnięcie

```text
PL=ID,WEJSCIE<CR><LF>
```

Przykład:

```text
RX: PL=2,3<CR><LF>
```

To informacja, że wejście 3 modułu ID=2 osiągnęło próg LONG. Zdarzenie powstaje **podczas trzymania**, po osiągnięciu ustawionego czasu, a nie dopiero po puszczeniu.

- Jedno nieprzerwane przytrzymanie generuje najwyżej jedno PL.
- Dalsze trzymanie nie powoduje okresowego powtarzania PL.
- Po puszczeniu występuje raport rozwarcia I=, ale nie dodatkowe PS.
- PL nie ma pola SUMA i nie jest potwierdzane przez RuleOK.

## 7. Pełne sekwencje raportów — trzy przykłady

Założenia: moduł o ośmiu wejściach, ID=1, przycisk na wejściu 1, pozostałe wejścia rozwarte, SHORT=0,5 s i LONG=2 s. Brak przepełnień kolejek. Tekst po strzałce opisuje zdarzenie i nie jest częścią ramki.

### 7.1. Krótkie naciśnięcie, około 0,3 s

```text
RX: I=1,1,0,0,0,0,0,0,0<CR><LF>  ← potwierdzone zwarcie
RX: I=1,0,0,0,0,0,0,0,0<CR><LF>  ← potwierdzone rozwarcie
RX: PS=1,1<CR><LF>                 ← krótkie naciśnięcie
```

### 7.2. Czas pośredni, około 1 s

```text
RX: I=1,1,0,0,0,0,0,0,0<CR><LF>  ← potwierdzone zwarcie
RX: I=1,0,0,0,0,0,0,0,0<CR><LF>  ← potwierdzone rozwarcie
```

**Nie ma PS ani PL:** przytrzymanie przekroczyło SHORT, ale nie osiągnęło LONG. SHORT nie oznacza „każde naciśnięcie krótsze niż LONG”.

### 7.3. Długie naciśnięcie, około 3 s

```text
RX: I=1,1,0,0,0,0,0,0,0<CR><LF>  ← potwierdzone zwarcie
RX: PL=1,1<CR><LF>                 ← po około 2 s potwierdzonego zwarcia
RX: I=1,0,0,0,0,0,0,0,0<CR><LF>  ← rozwarcie po puszczeniu
```

Nie ma drugiego PL w trzeciej sekundzie ani PS po puszczeniu. Na innych portach mogą występować równolegle te same raporty; opis portów znajduje się w rozdziale 13.

## 8. AT+KeyTime — ustawienie parametrów jednego wejścia

```text
AT+KeyTime=ID,WEJSCIE,SHORT,LONG,SUMA<CR>
```

| Pole | Zakres / znaczenie |
|---|---|
| ID | 1–35 |
| WEJSCIE | 1–8 dla R0808/R0806T/S0804; 1–6 dla ETH0606T |
| SHORT | Maksymalny czas krótkiego naciśnięcia, w jednostkach 0,1 s |
| LONG | Próg długiego naciśnięcia, w jednostkach 0,1 s |
| SUMA | ID + WEJSCIE + SHORT + LONG |

Warunek: **1 <= SHORT < LONG <= 250**. Najmniejszy SHORT to 0,1 s; największy LONG to 25 s. Przykładowo 5 oznacza 0,5 s, 20 oznacza 2 s. Są to dwa oddzielne progi, a pomiędzy nimi może nie wystąpić żaden raport PS/PL.

```text
TX: AT+KeyTime=1,1,5,20,27<CR>
RX: RuleOK=1<CR><LF>
```

Suma: 1+1+5+20=27. Komenda zmienia tylko progi wejścia 1 w RAM. Inne wejścia zachowują swoje ustawienia. Nie symuluje naciśnięcia i nie zapisuje EEPROM.

Zmiana podczas trzymania przycisku jest widoczna w GetKeyTime od razu, ale trwające przytrzymanie korzysta z progów zapamiętanych przy jego potwierdzonym początku. Nowe progi obowiązują dla kolejnego naciśnięcia.

Przykład ustawienia wszystkich ośmiu wejść na SHORT=0,5 s, LONG=2 s:

```text
TX: AT+KeyTime=1,1,5,20,27<CR>
TX: AT+KeyTime=1,2,5,20,28<CR>
TX: AT+KeyTime=1,3,5,20,29<CR>
TX: AT+KeyTime=1,4,5,20,30<CR>
TX: AT+KeyTime=1,5,5,20,31<CR>
TX: AT+KeyTime=1,6,5,20,32<CR>
TX: AT+KeyTime=1,7,5,20,33<CR>
TX: AT+KeyTime=1,8,5,20,34<CR>
```

Po każdej komendzie oczekuj RuleOK=1 przed wysłaniem następnej. Dla ETH0606T wykonaj tylko sześć pierwszych komend. Do utrwalenia całego zestawu wystarczy potem jedno `AT+SaveConfig=1,1`.

## 9. AT+GetKeyTime — odczyt progów jednego wejścia

```text
AT+GetKeyTime=ID,WEJSCIE,SUMA<CR>
```

SUMA zapytania to ID+WEJSCIE. Zakres ID i numeru wejścia jest taki sam jak w KeyTime.

```text
TX: AT+GetKeyTime=1,1,2<CR>
RX: KeyTime=1,1,5,20,27<CR><LF>
```

Format odpowiedzi:

```text
KeyTime=ID,WEJSCIE,SHORT,LONG,SUMA<CR><LF>
```

Odpowiedź ma własną sumę: ID+WEJSCIE+SHORT+LONG, dlatego w przykładzie suma zapytania to 2, a odpowiedzi 27. Czasy są nadal w jednostkach 0,1 s, a nie w milisekundach.

Dla wejścia 8 modułu ID=1, z takimi samymi progami:

```text
TX: AT+GetKeyTime=1,8,9<CR>
RX: KeyTime=1,8,5,20,34<CR><LF>
```

Moduł odczytuje **bieżące wartości RAM**. GetKeyTime nie odczytuje osobno zapisanej kopii EEPROM i nie potwierdza, że wartości przetrwają restart. Nie ma dodatkowego RuleOK przy poprawnej odpowiedzi danych. ETH0606T odrzuci odczyt wejścia 8, ponieważ ma tylko sześć wejść.

## 10. AT+GetInputs — odczyt wszystkich wejść

```text
AT+GetInputs=ID<CR>
```

Bez dodatkowej SUMY. Przykład dla modułu ID=1 o ośmiu wejściach, z zwartymi wejściami 1 i 8:

```text
TX: AT+GetInputs=1<CR>
RX: I=1,1,0,0,0,0,0,0,1<CR><LF>
```

Przykład ETH0606T, wejście 1 zwarte, pozostałe rozwarte:

```text
TX: AT+GetInputs=1<CR>
RX: I=1,1,0,0,0,0,0<CR><LF>
```

Odpowiedź zawiera jeden spójny obraz potwierdzonych stanów. Nie zmienia pinów, progów ani EEPROM. Nie tworzy dodatkowych PS/PL, nie zeruje czasu trzymania i nie odbiera zdarzeń z kolejki obsługi wejść. Nie jest to odczyt liczby naciśnięć ani historii zdarzeń.

## 11. AT+SaveConfig — utrwalenie parametrów

```text
AT+SaveConfig=ID,SUMA<CR>
```

SUMA jest równa ID, bo to jedyne wcześniejsze pole liczbowe. Dla modułu ID=1:

```text
TX: AT+KeyTime=1,1,5,20,27<CR>
RX: RuleOK=1<CR><LF>
TX: AT+GetKeyTime=1,1,2<CR>
RX: KeyTime=1,1,5,20,27<CR><LF>
TX: AT+SaveConfig=1,1<CR>
RX: SaveOK=1<CR><LF>
```

Zapis obejmuje konfigurację modułu, w tym progi **wszystkich jego wejść**, a nie tylko wejścia ustawionego ostatnio. Obejmuje też inne ustawienia zapisane przez dany model — nie jest oddzielnym zapisem samych wejść. Nie utrwala bieżących zwarć, czasu trzymania ani kolejki PS/PL.

Moduł zapisuje obraz konfiguracji z chwili przyjęcia SaveConfig. Zmiany wykonane później wymagają kolejnego zapisu. Operacja jest etapowa; odczekaj na wynik, który może pojawić się po kilku sekundach i zostać opóźniony przez komunikację:

| Odpowiedź | Znaczenie |
|---|---|
| `SaveOK=ID` | Zapis zakończony i sprawdzony |
| `SaveERROR=ID` | Zapis rozpoczęto, ale weryfikacja wykazała błąd |
| `RuleERROR=ID` | Komenda odrzucona przed rozpoczęciem zapisu, np. zła suma lub zajęty zapis |

RuleOK po KeyTime potwierdza zmianę RAM; dopiero SaveOK potwierdza zakończenie utrwalania. Po restarcie program automatycznie przywraca poprawną zapisaną konfigurację. Jeżeli nie ma poprawnej kopii, wejścia korzystają z wartości domyślnych.

## 12. AT+Defaults — domyślne parametry robocze

```text
TX: AT+Defaults=1,1<CR>
RX: RuleOK=1<CR><LF>
```

Format: `AT+Defaults=ID,SUMA`, SUMA=ID. Domyślne progi dla wszystkich wejść:

```text
SHORT=5   → 0,5 s
LONG=15   → 1,5 s
```

Sprawdzenie wejścia 1 po Defaults:

```text
TX: AT+GetKeyTime=1,1,2<CR>
RX: KeyTime=1,1,5,15,22<CR><LF>
```

**Defaults nie jest resetem parametrów jednego przycisku.** Przywraca szerszą konfigurację RAM: usuwa skonfigurowane reguły, inicjalizuje obsługę wejść i czyści jej kolejkę oraz licznik KEYERROR. S0804 dodatkowo resetuje stan/konfigurację rolet i zatrzymuje ich wyjścia; R0806T przywraca też konfigurację termostatów. Poprawne ID pozostaje zachowane.

Defaults samo nie nadpisuje EEPROM. Aby utrwalić wynik, wyślij SaveConfig i czekaj na SaveOK. Jeśli chcesz zmienić wyłącznie progi, użyj KeyTime dla wskazanych wejść zamiast Defaults. Po ponownej inicjalizacji wejść stale zwarty styk może ponownie zostać rozpoznany jako zwarcie.

## 13. Kto wysyła i kto odbiera I / PS / PL

### 13.1. Moduł z fizycznie podłączonym przyciskiem

Moduł sam wykrywa stan wejścia i generuje raport. Nie trzeba najpierw wysłać mu PS ani PL z komputera. ID w raporcie jest **ID źródła zdarzenia**, a nie adresem odbiorcy rozkazu.

| Model źródłowy | Automatyczne raporty I / PS / PL / KEYERROR |
|---|---|
| S0804 i R0806T | Wysyłane lokalnie przez UART0, port logiczny 0 |
| R0808 | Wysyłane przez oba porty logiczne: 0 = USART3, 1 = USART1 |
| ETH0606T | Wysyłane przez RS-232/USART1 oraz do aktywnego klienta TCP przez bramkę; lokalne raporty spontaniczne nie są kopiowane do USB/USART0 |

Odpowiedź na poprawną komendę GetInputs/GetKeyTime wraca portem, którym nadeszło zapytanie. Dlatego w S0804/R0806T można odpytać wejścia przez UART1, chociaż spontaniczne raporty z lokalnych wejść wychodzą przez UART0. W ETH odczyt lokalny przez USB może zwrócić odpowiedź mimo braku lokalnych powiadomień spontanicznych na USB.

### 13.2. Moduł pośredni w linii

R0808/R0806T/S0804 po odebraniu raportu I=, PS= lub PL= przez jeden port przekazują tekst drugim portem. Nie ustawiają na tej podstawie własnego fizycznego wejścia, nie generują lokalnego pomiaru trzymania i nie odpowiadają RuleOK.

```text
Terminal ── M1: ID=1 ── M2: ID=2 ── M3: ID=3
                                      przycisk WE1

M3 TX → M2:       PS=3,1<CR><LF>
M2 TX → M1:       PS=3,1<CR><LF>
Terminal RX ← M1:  PS=3,1<CR><LF>
```

ID=3 jest zachowane na całej drodze. Analogicznie przesyłane są PL= i I=. Odbiór tekstu `PS=3,1` przez M2 oznacza odebranie raportu o wejściu **innego modułu**, a nie naciśnięcie własnego wejścia M2.

Celowe wysłanie z terminala `PS=ID,WE`, `PL=ID,WE` lub `I=...` do parsera modułu liniowego może spowodować przekazanie tekstu dalej. **Nie jest to komenda do symulowania przycisku**. Raporty te nie są lokalnymi poleceniami sterowania.

Odpowiedzi GetKeyTime (`KeyTime=...`), SaveOK/SaveERROR i KEYERROR również są przekazywane przez moduły liniowe. Wszystkie moduły z oprogramowania w wersji 21 obsługują przekazywanie odczytów wejść i ich odpowiedzi.

### 13.3. ETH jako bramka

ETH nie jest symetrycznym modułem liniowym. Ramki odebrane z RS-232 mogą być przekazywane do klienta TCP, a zapytania AT adresowane do ID=2..35 z TCP są kierowane na RS-232. ETH nie traktuje przychodzącego PS/PL/I jako fizycznego zdarzenia własnych wejść i nie odsyła go bezwarunkowo z powrotem na port źródłowy.

### 13.4. Przykład odczytu z dalszego modułu

```text
Terminal TX → M1:  AT+GetKeyTime=3,1,4<CR>
M1 TX → M2:       AT+GetKeyTime=3,1,4<CR><LF>
M2 TX → M3:       AT+GetKeyTime=3,1,4<CR><LF>
M3 TX → M2:       KeyTime=3,1,5,20,29<CR><LF>
M2 TX → M1:       KeyTime=3,1,5,20,29<CR><LF>
Terminal RX ← M1:  KeyTime=3,1,5,20,29<CR><LF>
```

Suma zapytania: 3+1=4. Suma odpowiedzi: 3+1+5+20=29. Moduły pośrednie nie zmieniają swoich progów. Moduł docelowy nie zapisuje nic do EEPROM.

## 14. KEYERROR — utracone zdarzenia wejść

```text
RX: KEYERROR=2,4<CR><LF>
```

Moduł ID=2 odrzucił łącznie cztery zdarzenia z powodu pełnej kolejki wejść. **4 nie jest numerem wejścia.** Kolejka ma 128 miejsc; przechowuje potwierdzone zdarzenia zwarcia, rozwarcia, SHORT i LONG.

Licznik jest łączny od inicjalizacji obsługi wejść, nasyca się na 65535 i jest zerowany przez restart lub Defaults. Moduł wysyła nową wartość po zauważeniu zmiany licznika i uzyskaniu możliwości transmisji, a nie osobny raport dla każdego utraconego zdarzenia. Fizyczne próbkowanie i potwierdzony stan nadal są aktualizowane, lecz nie wszystkie zdarzenia zostaną dostarczone.

Po takim raporcie GetInputs pozwala odczytać aktualny stan, ale nie odtworzy utraconej historii naciśnięć PS/PL. Nie ma osobnego Get dla licznika KEYERROR. Ogólne IOERROR informuje o stratach w komunikacji UART; nie jest raportem numeru wejścia ani zamiennikiem KEYERROR.

## 15. Błędy i przykłady niepoprawnych poleceń

Przy module ID=1:

```text
TX: AT+KeyTime=1,1,5,20,28<CR>     ← zła suma, powinno być 27
RX: RuleERROR=1<CR><LF>

TX: AT+KeyTime=1,1,20,5,27<CR>     ← LONG nie jest większy od SHORT
RX: RuleERROR=1<CR><LF>

TX: AT+GetKeyTime=1,1,3<CR>        ← zła suma, powinno być 2
RX: RuleERROR=1<CR><LF>

TX: AT+GetInputs=0<CR>             ← ID=0 nie jest obsługiwane
RX: RuleERROR=1<CR><LF>

TX: AT+GetInputs=1,1<CR>           ← GetInputs nie ma pola SUMA
RX: RuleERROR=1<CR><LF>
```

Przykłady dotyczą poleceń obsługiwanych przez właściwą wersję oprogramowania. Stary wsad bez danej komendy może nie odpowiedzieć. Również brak modułu o wskazanym ID lub przerwa w linii nie musi dać jawnego błędu. Sterownik powinien stosować timeout, sprawdzać prefiks i ID, a dla KeyTime również sumę.

## 16. Szybka procedura uruchomienia wejścia

1. Odczytaj stan przez `AT+GetInputs=ID`.
2. Odczytaj progi przez `AT+GetKeyTime=ID,WE,SUMA`; SUMA to obliczona liczba ID+WE, nie wyrażenie wpisywane dosłownie do terminala.
3. W razie potrzeby ustaw KeyTime i oczekuj RuleOK.
4. Sprawdź odczytem GetKeyTime, czy RAM zawiera oczekiwane progi.
5. Wyślij SaveConfig i czekaj na SaveOK, jeśli ustawienia mają przetrwać restart.
6. Naciśnij i puść przycisk: obserwuj I oraz PS. Następnie przytrzymaj do LONG: obserwuj I i pojedynczy PL.

Nie wysyłaj komend RULE do wykonania tej procedury. Samo raportowanie stanów i rozpoznawanie PS/PL działa niezależnie od skonfigurowania działań przypisanych do przycisków.
