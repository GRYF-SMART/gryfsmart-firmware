# 6. Protokół GRYFSMART — szybka integracja

**[Pobierz przykład klienta TCP w Pythonie](https://raw.githubusercontent.com/GRYF-SMART/gryfsmart-firmware/main/PROTOKOL/przyklad_tcp.py)** · **[Pełny katalog komend](../docs/README.md)** · **[Przykłady konfiguracji instalacji](../docs/PRZYKLADY.md)**

Ten przewodnik pokazuje drogę od połączenia do sterowania i odbioru stanów w innym urządzeniu: kontrolerze, panelu, aplikacji lub systemie automatyki. Dotyczy nowego protokołu AT modułów GRYF. Przykładowe ID trzeba zastąpić adresami własnych modułów; pokazane odpowiedzi są ilustracjami, nie odczytami urządzeń.

## 1. Połączenie

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

## 3. Pierwszy odczyt

```text
TX: AT+Info=2<CR>
TX: AT+GetInputs=2<CR>
RX: I=2,0,1,0,0,0,0,0,0<CR><LF>
TX: AT+GetOut=2<CR>
RX: O=2,0,0,0,0,0,0,0,0<CR><LF>
```

W tym przykładzie ID 2 to R0808. Wyślij kolejne zapytanie po obsłużeniu odpowiedzi lub timeoutu. Liczba wejść: R0806T/R0808/S0804 = 8, ETH0606T = 6. Liczba przekaźników: R0806T/ETH0606T = 6, R0808 = 8; S0804 ma cztery rolety, które obsługuj komendami `RolAct`.

## 4. Przekaźniki i czas

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

## 5. PWM — R0806T

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

## 6. Flagi — zmienne wirtualne

Moduł ma osiem flag w firmware obsługującym `SetFlag/GetFlags`. Bieżące wartości są w RAM i po restarcie wracają do zera. Nie są lampkami ani wyjściami fizycznymi.

```text
AT+SetFlag=3,1,1,5<CR>   ustaw flagę 1
AT+SetFlag=3,1,2,6<CR>   skasuj flagę 1
AT+SetFlag=3,1,3,7<CR>   przełącz flagę 1
AT+GetFlags=3,3<CR>      odczytaj flagi
Flags=3,5,8<CR><LF>      przykład: maska 5 = flagi 1 i 3 ustawione
```

SUMA w zapytaniu GetFlags to ID; w odpowiedzi to ID+MASKA. Bit 0 maski oznacza flagę 1. Po zmianie odczytaj `GetFlags`, zamiast zakładać otrzymanie osobnego zdarzenia o zmianie flagi.

## 7. S0804 — pełna obsługa rolety

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

## 8. Odbiór, błędy i synchronizacja

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

## 9. Konfiguracja, diagnostyka i dalsze komendy

Konfigurację roboczą zapisuje `AT+SaveConfig=ID,ID`; wykonuj go po zmianach, nie w każdej pętli odświeżania. `Defaults`, `Search`, reset i BOOT mają skutki uboczne i nie należą do zwykłego odczytu stanu.

Diagnostyka: `AT+Info=ID`, `AT+Loop=ID`, `AT+ResetStats=ID`. Loop podaje minimum/średnią/maksimum czasu pętli; ResetStats odczytuje liczniki i przyczyny restartów. [Formaty odpowiedzi](../docs/komendy-wspolne.md).

- [Wejścia, PS/PL, KeyTime i odczyty](../docs/wejscia-komendy.md)
- [Reguły i różnice między modułami](../docs/reguly-porownanie.md)
- [R0806T, PWM i temperatury](../docs/R0806T.md)
- [R0808](../docs/R0808.md), [ETH0606T](../docs/ETH0606T.md), [S0804](../docs/S0804.md)

Starsze rozdziały szczegółowe wskazują wersję, dla której opisano daną funkcję. Nie traktuj ich starych numerów jako numerów najnowszego wydania; [bieżące HEX-y i wersje](../HEX) są zestawione osobno. Nową funkcję sprawdzaj w module docelowym i modułach pośrednich.
