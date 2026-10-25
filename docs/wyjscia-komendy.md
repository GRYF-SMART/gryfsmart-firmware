# Obsługa wyjść — R0808, R0806T i ETH0606T

Wspólny schemat poleceń przekaźnikowych:

```text
Ustawienie: AT+SetOut=ID,A1,...,AN<CR>
Odczyt:     AT+GetOut=ID<CR>
Stan:       O=ID,S1,...,SN<CR><LF>
```

**R0808 realizuje powyższy format odpowiedzi zarówno na zapytanie, jak i po zmianie wyjść.** Istniejące R0806T i ETH0606T mają różnice w wielkości litery O/o oraz zakończeniu ramki, opisane w tabeli poniżej. S0804 i sterowanie roletami są poza zakresem dokumentu.

Dokumentacja dotyczy oprogramowania w wersji **21** wszystkich trzech modułów.

## 1. Parametry wspólne

- ID: adres logiczny **1–35**; ID=0 nie jest obsługiwane dla SetOut i GetOut.
- N: **8 dla R0808**, **6 dla R0806T i ETH0606T**.
- A1..AN: akcje dla kolejnych wyjść WY1..WYN.
- S1..SN: stany sterowania kolejnych przekaźników: 0 = wyłączony, 1 = włączony.
- Liczby dziesiętne, bez spacji; brak dodatkowego pola SUMA w obu komendach i w raporcie.
- [Parametry i zasady komunikacji](komendy-wspolne.md#zasady-komunikacji-i-struktura-sieci).
- `<CR>` to bajt 0x0D, `<LF>` to 0x0A. Nie wpisuj dosłownie znaków `<CR>` do terminala.
- TX/RX w przykładach oznaczają odpowiednio wysłanie i odebranie przez terminal/sterownik.

## 2. Aktualne formaty — porównanie modułów

| Funkcja | R0808 20 | R0806T 20 | ETH0606T 20 |
|---|---|---|---|
| Liczba przekaźników | 8 | 6 | 6 |
| SetOut | ID + 8 akcji | ID + 6 akcji | ID + 6 akcji |
| Odczyt GetOut | Tak | Tak | Tak |
| Odpowiedź GetOut | `O=ID,S1,...,S8` | `o=ID,S1,...,S6` | `O=ID,S1,...,S6` |
| Automatyczny raport po zmianie | `O=ID,S1,...,S8` | `o=ID,S1,...,S6` | `o=ID,S1,...,S6` |
| Zakończenie odpowiedzi/raportu | CRLF | Sam CR | CRLF |
| Porty raportów spontanicznych | Wszystkie 4 porty logiczne | Oba UART-y | RS-232/USART1 i klient TCP; bez kopiowania lokalnego raportu do USB/USART0 |

Sterownik obsługujący wszystkie trzy moduły powinien przyjmować O= oraz o= i rozpoznawać zakończenie CR z opcjonalnym LF. Parametry akcji SetOut są wspólne; liczba pól zależy od modelu.

## 3. AT+SetOut — ustawienie stanu przekaźników

Wartości akcji są takie same we wszystkich trzech modelach:

| Akcja | Znaczenie |
|---|---|
| 0 | Bez zmiany |
| 1 | Włącz |
| 2 | Wyłącz |
| 3 | Przełącz na stan przeciwny |

**Akcja 0 nie oznacza wyłączenia.** Do wyłączenia użyj 2. Nie myl kodów akcji z wartościami 0/1 w odpowiedzi O=.

### 3.1. ETH0606T i R0806T — sześć wyjść

```text
TX: AT+SetOut=1,1,2,3,0,0,0<CR>
RX: RuleOK=1<CR><LF>
```

Moduł ID=1: WY1 włącz, WY2 wyłącz, WY3 przełącz, WY4–WY6 bez zmiany. Stan WY3 po wykonaniu zależy od jego stanu poprzedniego.

Wyłącz wszystkie sześć:

```text
TX: AT+SetOut=1,2,2,2,2,2,2<CR>
RX: RuleOK=1<CR><LF>
```

### 3.2. R0808 — osiem wyjść

```text
TX: AT+SetOut=2,1,2,3,0,0,0,0,0<CR>
RX: RuleOK=2<CR><LF>
```

Ta sama operacja dla modułu ID=2, z ośmioma polami akcji. WY4–WY8 bez zmiany.

Wyłącz wszystkie osiem:

```text
TX: AT+SetOut=2,2,2,2,2,2,2,2,2<CR>
RX: RuleOK=2<CR><LF>
```

Nie dodawaj sumy kontrolnej. Liczba akcji musi odpowiadać lokalnemu modelowi. R0808 może przekazywać sześciowyjściowe polecenie do innego ID, ale odrzuci takie polecenie skierowane do siebie. Analogicznie R0806T wymaga lokalnie sześciu pól.

RuleOK potwierdza przyjęcie i wykonanie polecenia w programie. Nie jest pomiarem rzeczywistego zamknięcia styku przekaźnika. Błędne ID, format, liczba akcji lub akcja spoza 0–3 powodują RuleERROR=ID_MODULU.

## 4. AT+GetOut — odczyt na żądanie

```text
AT+GetOut=ID<CR>
```

Bez SUMY. Poprawny odczyt wysyła dane portem zapytania, bez dodatkowego RuleOK. Nie zmienia przekaźników ani EEPROM i nie usuwa oczekujących raportów automatycznych.

### 4.1. R0808, ID=2, włączone WY1 i WY8

```text
TX: AT+GetOut=2<CR>
RX: O=2,1,0,0,0,0,0,0,1<CR><LF>
```

### 4.2. R0806T, ID=3, włączone WY1 i WY6

```text
TX: AT+GetOut=3<CR>
RX: o=3,1,0,0,0,0,1<CR>
```

### 4.3. ETH0606T, ID=1, włączone WY1 i WY6

```text
TX: AT+GetOut=1<CR>
RX: O=1,1,0,0,0,0,1<CR><LF>
```

W każdym przypadku po ID następują stany WY1, WY2 itd. To osobne pola, a nie pojedyncza maska dziesiętna. Odczytywany jest stan sterowania wyjściami, a nie pomiar styków czy zasilania odbiornika. Raport przekaźników nie zawiera poziomu PWM.

## 5. Kiedy wychodzi automatyczne O=/o=

### 5.1. R0808 od 20

Każda rzeczywista zmiana całej maski wyjść wykonana przez obsługę przekaźników tworzy jeden raport. Dotyczy to SetOut oraz lokalnych akcji zmieniających wyjścia. Jeden SetOut zmieniający kilka wyjść daje jeden raport wynikowy, nie osobny raport dla każdego zmienionego bitu.

Przy wszystkich wyjściach początkowo wyłączonych:

```text
TX: AT+SetOut=2,1,0,0,0,0,0,0,0<CR>
RX: RuleOK=2<CR><LF>
RX: O=2,1,0,0,0,0,0,0,0<CR><LF>
```

Potwierdzenie wraca portem komendy, a raport stanu jest wysyłany na wszystkie porty logiczne. Mapowanie R0808: port 0 = RS-232 USART3, port 1 = RS-232 USART1, port 2 = RS-485 USART0, port 3 = RS-485 USART2. Obsługa elektryczna RS-485 wymaga właściwego mapowania DE na danej płytce.

Ponowne wykonanie tego samego polecenia ON dla już włączonego wyjścia:

```text
TX: AT+SetOut=2,1,0,0,0,0,0,0,0<CR>
RX: RuleOK=2<CR><LF>
```

**Nie powstaje nowe O=**, bo stan się nie zmienił. Polecenie z samymi zerami także nie tworzy raportu zmiany.

Dwa szybkie, rzeczywiste przełączenia są zapamiętywane osobno, nawet jeśli stan końcowy jest taki jak początkowy:

```text
RX: O=2,1,0,0,0,0,0,0,0<CR><LF>  ← włączono WY1
RX: O=2,0,0,0,0,0,0,0,0<CR><LF>  ← następnie wyłączono WY1
```

To obrazy stanu z chwili zmiany; ich wysłanie może być opóźnione. Kolejka mieści 32 raporty i ma niezależny postęp dla każdego portu. Zajęty port nie zatrzymuje sterowania ani raportów na innych portach. Jeżeli jeden port zalega z ponad 32 zmianami, najstarsze niedostarczone raporty tego portu są odrzucane i zwiększa się jego licznik przepełnienia TX. Nie ma gwarancji przesłania nieograniczonej liczby zmian przy niedziałającej transmisji. Po utracie historii aktualny stan można sprawdzić GetOut.

GetOut może zwrócić nowszy stan przed wysłaniem całej kolejki starszych raportów. Odpowiedź na odczyt i raport automatyczny mają ten sam format, bez numeru zapytania i znacznika czasu.

### 5.2. R0806T i ETH0606T

Te moduły wykrywają zmianę przez porównanie bieżącego stanu z ostatnio zgłoszonym w pętli głównej. Po zmianie, również wynikającej z innego lokalnego mechanizmu sterowania, wysyłają raport zgodnie z tabelą formatów.

R0806T wysyła małe o= zakończone CR na oba UART-y. ETH wysyła małe o= zakończone CRLF przez RS-232 i TCP. Ponowienie ON bez rzeczywistej zmiany nie powoduje raportu.

Przy przeciążeniu lub kilku zmianach między sprawdzeniami ich raporty mogą zostać scalone do najnowszego stanu. R0806T i ETH nie mają nowej 32-elementowej kolejki zmian dodanej w R0808. Dokument opisuje tę różnicę, nie deklaruje identycznej implementacji.

### 5.3. Start i restart

Inicjalizacja raportowania przyjmuje początkowy stan bez wysyłania automatycznego raportu. Do poznania stanu po uruchomieniu użyj GetOut. Tymczasowe wyłączenie przekaźników podczas planowanego resetu nie jest zgłaszane jako zwykła zmiana użytkowa. Raporty nie są okresowym sygnałem obecności modułu.

## 6. Przekazywanie po linii i ETH jako bramka

R0808 i R0806T przekazują poprawne SetOut/GetOut skierowane do innego ID na przeciwny port w parze portów. Odebrane O=/o= przekazują jako raporty, bez ustawiania własnych przekaźników. Wielkość litery prefiksu jest rozpoznawana bez rozróżniania O/o, ale moduły nie normalizują całego protokołu do jednego formatu.

Przykład linii: terminal → R0808 ID=2 → R0806T ID=3:

```text
Terminal TX → R0808:  AT+GetOut=3<CR>
R0808 TX → R0806T:    AT+GetOut=3<CR><LF>
R0806T TX → R0808:    o=3,1,0,0,0,0,1<CR>
Terminal RX ← R0808:  o=3,1,0,0,0,0,1<CR><LF>
```

R0808 dodaje CRLF podczas przekazywania odebranej ramki. Z kolei obecny R0806T przy przekazywaniu małego o= stosuje swój format z samym CR. Dlatego odbiornik powinien akceptować oba zakończenia.

ETH jest bramką, nie symetrycznym modułem liniowym. Z TCP kieruje adresowane AT dla ID=2..35 na RS-232; lokalne zapytania dotyczą ETH. Raporty z RS-232 mogą trafić do klienta TCP. Sam odbiór tekstu O=/o= nie zmienia wyjść ETH. Spontaniczne raporty ETH nie są kopiowane na USB; lokalny GetOut wysłany przez USB może jednak otrzymać tam odpowiedź.

## 7. Błędy i trwałość

```text
TX: AT+GetOut=0<CR>
RX: RuleERROR=ID_MODULU<CR><LF>

TX: AT+GetOut=2,2<CR>
RX: RuleERROR=ID_MODULU<CR><LF>

TX: AT+SetOut=2,4,0,0,0,0,0,0,0<CR>
RX: RuleERROR=ID_MODULU<CR><LF>
```

SetOut i GetOut nie zapisują stanu do EEPROM. Nie zakładaj, że SaveConfig utrwala bieżące włączenie odbiorników jako stan startowy. Planowany restart może odtwarzać stan według osobnego mechanizmu modułu; nie jest to skutek zapisania SetOut.

Brak odpowiedzi może oznaczać brak wskazanego ID, starszą aplikację lub problem z linią. Stosuj timeout i sprawdzaj ID źródła raportu. Nie traktuj samego RuleOK ani O= jako elektrycznego potwierdzenia poprawnej pracy odbiornika.
