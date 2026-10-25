<p><img src="assets/logo.svg" alt="Logo GRYF" width="320"></p>

# PRZYKLADY

Praktyczne przykłady dla **wersji oprogramowania 20** i pięciu modułów podłączonych w tej kolejności:

```text
Komputer → R0808 → R0806T → R0806T → S0804 → S0804
             1       2        3        4        5
```

Liczby pod modułami oznaczają pozycje w linii, a po wykonaniu przykładu 1 również ich ID.

| Pozycja / docelowe ID | Model | Wejścia | Elementy sterowane |
|---|---|---|---|
| 1 | R0808 | 8 | 8 przekaźników |
| 2 | R0806T | 8 | 6 przekaźników i PWM |
| 3 | R0806T | 8 | 6 przekaźników i PWM |
| 4 | S0804 | 8 | 4 rolety |
| 5 | S0804 | 8 | 4 rolety |

Wszystkie komendy TX wysyłasz **z jednego terminala do portu 0 pierwszego modułu**. Nie trzeba przełączać kabla między modułami. Połączenia i zakończenia linii opisano w [zasadach komunikacji](komendy-wspolne.md#zasady-komunikacji-i-struktura-sieci).

TX oznacza tekst wysłany przez terminal, RX — odpowiedź odebraną w terminalu. Wyślij jedną komendę, poczekaj na jej odpowiedź, następnie wysyłaj kolejną. Zapisów TX/RX i oznaczeń <CR>/<LF> nie wpisuj jako części komendy. Sumy kontrolne poniżej są już obliczone.

Pokazano istotne odpowiedzi; w międzyczasie mogą nadejść raporty wejść, wyjść, temperatur i ruchu rolet. Kolejność raportów asynchronicznych nie jest gwarantowana. Przykłady 3–11 zakładają wykonane adresowanie z przykładu 1 i moduły w stanie pozwalającym na konfigurację. Przykłady sterowania zakładają sprawne podłączenie odpowiednich wyjść i napędów.

## Spis przykładów

1. [Rozpoznanie pięciu modułów i zapis ich ID do EEPROM](#przyklad-1)
2. [Szczegółowe informacje o każdym module](#przyklad-2)
3. [Czasy naciśnięć wszystkich wejść modułu ID=3](#przyklad-3)
4. [Reguła 1 modułu ID=2: przełącz WY5 lokalnie i włącz WY3 modułu ID=3](#przyklad-4)
5. [Czasy otwierania i zamykania czterech rolet modułu ID=4](#przyklad-5)
6. [Wejście 1 modułu ID=1 otwiera rolety 3 i 4 modułu ID=5 na 50%](#przyklad-6)
7. [Sterowanie bezpośrednio z terminala lub programu](#przyklad-7)
8. [Raporty po krótkim naciśnięciu wejścia 8 modułu ID=3](#przyklad-8)
9. [Automatyczny raport po włączeniu wyjść 7 i 8 modułu ID=1](#przyklad-9)
10. [Odczyt wejść, wyjść i PWM modułu ID=2](#przyklad-10)
11. [Stan czterech rolet modułu ID=5, w tym ruch do zadanego procentu](#przyklad-11)

<a id="przyklad-1"></a>

## Przykład 1. Rozpoznanie pięciu modułów i zapis ich ID do EEPROM

Search wybiera moduł według pozycji, nadaje mu ID i zapisuje **ten adres w EEPROM tego modułu**. Odpowiedź Find podaje nadane ID, wersję oprogramowania oraz typ urządzenia. Dotychczasowe ID mogą być inne albo powtarzać się.

**Jedna komenda Search adresuje jedną pozycję.** Aby nadać adresy całej linii, wyślij pięć poleceń, po każdym czekając na Find:

```text
TX: AT+Search=0,1<CR>
RX: AT+Find=1,20,5<CR><LF>

TX: AT+Search=0,2<CR>
RX: AT+Find=2,20,4<CR><LF>

TX: AT+Search=0,3<CR>
RX: AT+Find=3,20,4<CR><LF>

TX: AT+Search=0,4<CR>
RX: AT+Find=4,20,3<CR><LF>

TX: AT+Search=0,5<CR>
RX: AT+Find=5,20,3<CR><LF>
```

Typ 5 oznacza R0808, typ 4 R0806T, typ 3 S0804. Po tej sekwencji otrzymujesz ID 1–5 zgodne z tabelą. Nie jest potrzebne osobne SaveConfig do utrwalenia nadanego przez Search ID. Search nie służy do cyklicznego skanowania — zmienia zapisane adresy.

Przykładowo polecenie Search=0,5 przechodzi przez moduły z licznikami 1, 2, 3, 4; dopiero piąty zapisuje ID=5 i odpowiada. Nie nadaje ono automatycznie ID pozostałym czterem.

<a id="przyklad-2"></a>

## Przykład 2. Szczegółowe informacje o każdym module

Po nadaniu indywidualnych ID użyj **AT+Info=ID**. To najpełniejszy odczyt identyfikacyjny: model, wersja oprogramowania, MCU, rewizja PCB, dane kompilacji, sygnatura i odczytane dane fabryczne. Nie zmienia EEPROM ani wyjść.

W odpowiedziach poniżej pola zapisane jako <PCB1>, <GIT1> itd. oznaczają **rzeczywiste wartości zwracane przez dany egzemplarz**, nie gotowe numery seryjne. Polecenia TX są gotowe do wysłania; wzorców RX nie wysyła się do urządzeń.

```text
TX: AT+Info=1<CR>
RX: ID=1,FW=20,MODEL=R0808,MCU=ATmega2560,PCB=<PCB1>,GIT=<GIT1>,DIRTY=<DIRTY1>,UTC=<UTC1>,SIG=1E9801,CAL=<CAL1>,SERIAL=<SERIAL1>,STATUS=<STATUS1><CR><LF>

TX: AT+Info=2<CR>
RX: ID=2,FW=20,MODEL=R0806T,MCU=ATmega1284P,PCB=<PCB2>,GIT=<GIT2>,DIRTY=<DIRTY2>,UTC=<UTC2>,SIG=1E9705,CAL=<CAL2>,SERIAL=<SERIAL2>,STATUS=<STATUS2><CR><LF>

TX: AT+Info=3<CR>
RX: ID=3,FW=20,MODEL=R0806T,MCU=ATmega1284P,PCB=<PCB3>,GIT=<GIT3>,DIRTY=<DIRTY3>,UTC=<UTC3>,SIG=1E9705,CAL=<CAL3>,SERIAL=<SERIAL3>,STATUS=<STATUS3><CR><LF>

TX: AT+Info=4<CR>
RX: ID=4,FW=20,MODEL=S0804,MCU=ATmega1284P,PCB=<PCB4>,GIT=<GIT4>,DIRTY=<DIRTY4>,UTC=<UTC4>,SIG=1E9705,CAL=<CAL4>,SERIAL=<SERIAL4>,STATUS=<STATUS4><CR><LF>

TX: AT+Info=5<CR>
RX: ID=5,FW=20,MODEL=S0804,MCU=ATmega1284P,PCB=<PCB5>,GIT=<GIT5>,DIRTY=<DIRTY5>,UTC=<UTC5>,SIG=1E9705,CAL=<CAL5>,SERIAL=<SERIAL5>,STATUS=<STATUS5><CR><LF>
```

| Pole | Co odczytujesz |
|---|---|
| ID, MODEL, FW, MCU | Adres, model, wersję oprogramowania i mikrokontroler |
| PCB | Rewizję płytki zadeklarowaną w kompilacji, ewentualnie UNKNOWN |
| GIT, DIRTY, UTC | Rewizję źródeł, informację o lokalnych zmianach oraz czas kompilacji |
| SIG, CAL | Sygnaturę mikrokontrolera i fabryczny bajt kalibracji, w HEX |
| SERIAL | 9 odczytanych bajtów fabrycznych zapisanych jako 18 cyfr HEX |
| STATUS | EMPTY dla samych zer/FF albo UNVERIFIED |

**SERIAL nie jest potwierdzonym unikalnym numerem seryjnym urządzenia.** Gdy STATUS=EMPTY, nie uzyskano użytecznych danych seryjnych; UNVERIFIED również nie gwarantuje unikalności. Oprogramowanie nie udostępnia tu oddzielnego, zweryfikowanego numeru seryjnego producenta.

Info zwraca jedną linię ID=... bez dodatkowego RuleOK. Factory zwraca podzbiór tych danych i nie rozszerza odpowiedzi Info. Do dodatkowej diagnostyki pracy służą Loop i ResetStats — [komendy wspólne](komendy-wspolne.md#sieć-i-stan).

<a id="przyklad-3"></a>

## Przykład 3. Czasy naciśnięć wszystkich wejść modułu ID=3

Dla wejść 1–4 ustaw SHORT=0,5 s i LONG=1,5 s. Dla wejść 5–8 ustaw SHORT=0,3 s i LONG=2 s. KeyTime używa jednostki **0,1 s**. Konfigurację zapisz w EEPROM modułu 3.

```text
TX: AT+KeyTime=3,1,5,15,24<CR>
RX: RuleOK=3<CR><LF>

TX: AT+KeyTime=3,2,5,15,25<CR>
RX: RuleOK=3<CR><LF>

TX: AT+KeyTime=3,3,5,15,26<CR>
RX: RuleOK=3<CR><LF>

TX: AT+KeyTime=3,4,5,15,27<CR>
RX: RuleOK=3<CR><LF>

TX: AT+KeyTime=3,5,3,20,31<CR>
RX: RuleOK=3<CR><LF>

TX: AT+KeyTime=3,6,3,20,32<CR>
RX: RuleOK=3<CR><LF>

TX: AT+KeyTime=3,7,3,20,33<CR>
RX: RuleOK=3<CR><LF>

TX: AT+KeyTime=3,8,3,20,34<CR>
RX: RuleOK=3<CR><LF>

TX: AT+SaveConfig=3,3<CR>
RX: SaveOK=3<CR><LF>
```

Odczytaj progi każdego wejścia, aby sprawdzić konfigurację:

```text
TX: AT+GetKeyTime=3,1,4<CR>
RX: KeyTime=3,1,5,15,24<CR><LF>

TX: AT+GetKeyTime=3,2,5<CR>
RX: KeyTime=3,2,5,15,25<CR><LF>

TX: AT+GetKeyTime=3,3,6<CR>
RX: KeyTime=3,3,5,15,26<CR><LF>

TX: AT+GetKeyTime=3,4,7<CR>
RX: KeyTime=3,4,5,15,27<CR><LF>

TX: AT+GetKeyTime=3,5,8<CR>
RX: KeyTime=3,5,3,20,31<CR><LF>

TX: AT+GetKeyTime=3,6,9<CR>
RX: KeyTime=3,6,3,20,32<CR><LF>

TX: AT+GetKeyTime=3,7,10<CR>
RX: KeyTime=3,7,3,20,33<CR><LF>

TX: AT+GetKeyTime=3,8,11<CR>
RX: KeyTime=3,8,3,20,34<CR><LF>
```

PS jest zgłaszane po puszczeniu, gdy czas przytrzymania nie przekroczył SHORT. PL jest zgłaszane raz podczas trzymania po osiągnięciu progu LONG. Określenie „powyżej” w tym przykładzie oznacza próg długiego naciśnięcia; implementacja sprawdza osiągnięcie tego progu. Puszczenie między SHORT i LONG nie generuje PS ani PL. Czasy dotyczą sygnału po filtracji drgań styków.

<a id="przyklad-4"></a>

## Przykład 4. Reguła 1 modułu ID=2: przełącz WY5 lokalnie i włącz WY3 modułu ID=3

Krótkie naciśnięcie **wejścia 3 modułu 2** ma przełączać jego przekaźnik 5 (0→1 albo 1→0) i zawsze włączać przekaźnik 3 modułu 3. Użyj zdalnego typu 2, czyli sześciu przekaźników.

Poniższa sekwencja zastępuje konfigurację **reguły 1 modułu 2**: czyści jej stare sloty zdalne oraz lokalną akcję PWM. Pozostałe reguły pozostają bez zmian. Dla samodzielnego przykładu ustawia też progi wejścia 3 na 0,5/1,5 s.

```text
TX: AT+KeyTime=2,3,5,15,25<CR>
RX: RuleOK=2<CR><LF>

TX: AT+RuleRemote=2,1,0,0,0,3<CR>
RX: RuleOK=2<CR><LF>

TX: AT+RulePWM=2,1,0,0,0,3<CR>
RX: RuleOK=2<CR><LF>

TX: AT+RuleRemote=2,1,1,3,2,0,0,1,0,0,0,10<CR>
RX: RuleOK=2<CR><LF>

TX: AT+Rule=2,1,1,0,0,1,0,0,0,0,0,0,0,0,0,3,0,8<CR>
RX: RuleOK=2<CR><LF>

TX: AT+SaveConfig=2,2<CR>
RX: SaveOK=2<CR><LF>
```

W Rule jedyną maską wejścia jest E3=1 (SHORT), a jedyną akcją lokalną O5=3 (TOGGLE). W slocie zdalnym CEL=3, TYP=2, akcja O3=1 (ON). Wszystkie pozostałe akcje mają 0 — pozostawiają wyjścia bez zmiany. RuleRemote i RulePWM wyłączają regułę podczas konfiguracji, dlatego Rule z EN=1 wysyłane jest na końcu.

Sprawdzenie odczytem:

```text
TX: AT+GetRule=2,1,3<CR>
RX: Rule=2,1,1,0,0,1,0,0,0,0,0,0,0,0,0,3,0,8<CR><LF>

TX: AT+GetRuleRemote=2,1,1,4<CR>
RX: RuleRemote=2,1,1,3,2,0,0,1,0,0,0,10<CR><LF>
```

Teraz krótko naciśnij i puść wejście 3 modułu 2. Moduł 2 sam nadaje do linii:

```text
AT+SetOut=3,0,0,1,0,0,0<CR><LF>
```

Nie wysyłaj tego SetOut ponownie z terminala jako części konfiguracji — powstaje przy wykonaniu reguły. Możliwe do odebrania raporty to PS=2,3, raporty wyjść i RuleOK=3 z odbiorcy. RuleOK=3 nie jest zbiorczym potwierdzeniem całej reguły.

Dla ilustracji przyjmijmy, że przed próbą wszystkie przekaźniki obu modułów były wyłączone, a inne reguły nie zmieniają wyjść. Po pierwszym krótkim naciśnięciu odczyt daje:

```text
TX: AT+GetOut=2<CR>
RX: o=2,0,0,0,0,1,0<CR>

TX: AT+GetOut=3<CR>
RX: o=3,0,0,1,0,0,0<CR>
```

Po kolejnym krótkim naciśnięciu WY5 modułu 2 będzie wyłączone, a WY3 modułu 3 pozostanie włączone. Małe o= i samo CR są formatem raportu przekaźników R0806T.

<a id="przyklad-5"></a>

## Przykład 5. Czasy otwierania i zamykania czterech rolet modułu ID=4

Rolety 1 i 2: otwieranie **50 s**, zamykanie **52 s**. Rolety 3 i 4: otwieranie **60 s**, zamykanie **61 s**. RolTime przyjmuje czasy w jednostkach 0,1 s, więc wysyłasz 500/520 oraz 600/610. Rolety powinny stać podczas konfiguracji.

```text
TX: AT+RolTime=4,1,500,520,1025<CR>
RX: RuleOK=4<CR><LF>

TX: AT+RolTime=4,2,500,520,1026<CR>
RX: RuleOK=4<CR><LF>

TX: AT+RolTime=4,3,600,610,1217<CR>
RX: RuleOK=4<CR><LF>

TX: AT+RolTime=4,4,600,610,1218<CR>
RX: RuleOK=4<CR><LF>

TX: AT+SaveConfig=4,4<CR>
RX: SaveOK=4<CR><LF>
```

Kontrola ustawionych czasów:

```text
TX: AT+GetRolTime=4,1,5<CR>
RX: RolTime=4,1,500,520,1025<CR><LF>

TX: AT+GetRolTime=4,2,6<CR>
RX: RolTime=4,2,500,520,1026<CR><LF>

TX: AT+GetRolTime=4,3,7<CR>
RX: RolTime=4,3,600,610,1217<CR><LF>

TX: AT+GetRolTime=4,4,8<CR>
RX: RolTime=4,4,600,610,1218<CR><LF>
```

RolTime zmienia parametry i unieważnia znajomość pozycji danej rolety. Nie uruchamia ruchu. Przed zadaniem pozycji pośredniej wykonaj pełne otwarcie albo zamknięcie. Ustawienia modułu 4 nie zmieniają czasów modułu 5.

<a id="przyklad-6"></a>

## Przykład 6. Wejście 1 modułu ID=1 otwiera rolety 3 i 4 modułu ID=5 na 50%

Krótkie naciśnięcie wejścia 1 modułu R0808 uruchomi regułę 1, której slot zdalny steruje roletami 3 i 4 S0804 o ID=5. Rolety 1 i 2 nie otrzymują akcji.

### A. Przygotowanie czasów i pozycji modułu 5

W tym przykładzie **przyjmujemy dodatkowo czasy 60 s otwierania i 61 s zamykania** dla rolet 3 i 4 modułu 5. Dla rzeczywistych napędów podaj ich zmierzone czasy i przelicz sumy. To osobna konfiguracja — przykład 5 dotyczył modułu 4.

```text
TX: AT+RolTime=5,3,600,610,1218<CR>
RX: RuleOK=5<CR><LF>

TX: AT+RolTime=5,4,600,610,1219<CR>
RX: RuleOK=5<CR><LF>

TX: AT+SaveConfig=5,5<CR>
RX: SaveOK=5<CR><LF>
```

Wykonaj pełne zamknięcie obu rolet, aby uzyskać znaną pozycję 0%. Ta część przykładu powoduje rzeczywisty ruch.

```text
TX: AT+RolAct=5,3,2,0,10<CR>
RX: RuleOK=5<CR><LF>

TX: AT+RolAct=5,4,2,0,11<CR>
RX: RuleOK=5<CR><LF>
```

RuleOK oznacza przyjęcie, nie koniec ruchu. Poczekaj na ukończenie pełnego przejazdu zamykania (czas 61 s, z ewentualną przerwą zmiany kierunku). Odpytuj GetRolState; przejdź dalej dopiero, gdy **STAN=0, ZNANA=1, POZYCJA=0** dla obu rolet. Poniżej odpowiedzi po zakończeniu:

```text
TX: AT+GetRolState=5,3,8<CR>
RX: RolState=5,3,0,1,0,255,0,264<CR><LF>

TX: AT+GetRolState=5,4,9<CR>
RX: RolState=5,4,0,1,0,255,0,265<CR><LF>
```

### B. Konfiguracja reguły 1 modułu 1

Zastępujemy zdalne sloty reguły 1 modułu 1. SHORT wejścia 1 ustawiamy na 0,5 s, LONG na 1,5 s. Typ zdalny 1 oznacza cztery rolety, każda z parą AKCJA,PROCENT; akcja 7 oznacza pozycję procentową.

```text
TX: AT+KeyTime=1,1,5,15,22<CR>
RX: RuleOK=1<CR><LF>

TX: AT+RuleRemote=1,1,0,0,0,2<CR>
RX: RuleOK=1<CR><LF>

TX: AT+RuleRemote=1,1,1,5,1,0,0,0,0,7,50,7,50,123<CR>
RX: RuleOK=1<CR><LF>

TX: AT+Rule=1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4<CR>
RX: RuleOK=1<CR><LF>

TX: AT+SaveConfig=1,1<CR>
RX: SaveOK=1<CR><LF>
```

Sprawdź konfigurację:

```text
TX: AT+GetRule=1,1,2<CR>
RX: Rule=1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4<CR><LF>

TX: AT+GetRuleRemote=1,1,1,3<CR>
RX: RuleRemote=1,1,1,5,1,0,0,0,0,7,50,7,50,123<CR><LF>
```

### C. Wyzwolenie i odczyt wyniku

Krótko naciśnij i puść wejście 1 modułu 1. Nie wysyłaj PS z terminala — to raport, nie komenda symulacji przycisku. R0808 automatycznie wyśle akcje:

```text
AT+RolAct=5,3,7,50,65<CR><LF>
AT+RolAct=5,4,7,50,66<CR><LF>
```

Moduł 5 przyjmie obie komendy, odpowiadając RuleOK=5 na każdą. W terminalu mogą pojawić się PS=1,1 oraz raporty R=5,... o zmianach ruchu. Kolejność tych ramek nie jest potwierdzeniem zakończenia dojazdu.

Z pozycji zamkniętej przejazd do 50% trwa około 30 s przy ustawionym czasie otwierania 60 s, z ewentualną przerwą przed zmianą kierunku. Po zakończeniu odczytaj:

```text
TX: AT+GetRolState=5,3,8<CR>
RX: RolState=5,3,0,1,50,255,0,314<CR><LF>

TX: AT+GetRolState=5,4,9<CR>
RX: RolState=5,4,0,1,50,255,0,315<CR><LF>
```

STAN=0 oznacza postój, ZNANA=1 znaną estymację, POZYCJA=50 osiągnięte 50%, CEL=255 brak aktywnego celu i POZOSTALO=0 koniec ruchu. Procent jest estymowany czasowo, nie mierzony czujnikiem. Po ponownym uruchomieniu modułu pozycję trzeba ponownie ustalić pełnym przejazdem przed użyciem 50%; zapis czasów i reguły nie zastępuje ustalenia pozycji.

<a id="przyklad-7"></a>

## Przykład 7. Sterowanie bezpośrednio z terminala lub programu

Polecenia konfiguracyjne z poprzednich przykładów przygotowują moduły, ale samym sterowaniem można zarządzać **bez reguł i bez naciskania przycisku**. Terminal lub program wysyła polecenie do odpowiedniego ID; moduły pośrednie przekazują je do odbiorcy.

Poniższe komendy wysyłasz tak samo przez port 0 pierwszego R0808. Zmiany stanów nie wymagają wysyłania SaveConfig po każdej komendzie sterującej.

### A. Moduł ID=2: PWM 90% z rampą 2 s

Akcja PWM=4 ustawia poziom. Procent=90, rampa=20 × 0,1 s = 2 s. SUMA=2+4+90+20=116. Zmiana następuje od aktualnego poziomu PWM do 90%; nie jest to opóźnione, skokowe włączenie po dwóch sekundach.

```text
TX: AT+PWM=2,4,90,20,116<CR>
RX: RuleOK=2<CR><LF>
```

RuleOK=2 potwierdza przyjęcie. Po zakończeniu rampy moduł wysyła automatyczny raport:

```text
RX: PWM=2,90,90,90,0,2000<CR><LF>
```

Znaczenie: ID=2, bieżący poziom 90%, cel 90%, zapamiętany niezerowy poziom 90%, rampa nieaktywna (0), częstotliwość PWM 2000 Hz. Jeśli wyjście już miało zadane 90%, nie ma potrzeby wykonywania pełnej dwusekundowej zmiany.

Możesz również odczytać wynik na żądanie. Po zakończeniu rampy:

```text
TX: AT+GetPWM=2<CR>
RX: PWM=2,90,90,90,0,2000<CR><LF>
```

Podczas rampy GetPWM może pokazać inny bieżący procent, cel=90 i RAMPA_AKTYWNA=1. Nie wysyłaj ponownie AT+PWM w pętli tylko po to, żeby sprawdzić postęp — używaj GetPWM.

### B. Moduł ID=1: przełączenie wyjścia 4 na stan przeciwny

R0808 ma osiem przekaźników. W SetOut ustaw O4=3 (TOGGLE), a pozostałe akcje na 0 (bez zmiany). Polecenie nie ma sumy kontrolnej.

```text
TX: AT+SetOut=1,0,0,0,3,0,0,0,0<CR>
RX: RuleOK=1<CR><LF>
```

Jeśli WY4 było wyłączone, zostanie włączone. Jeśli było włączone, zostanie wyłączone. Pozostałe wyjścia zachowają stany.

Przykładowy raport automatyczny, **gdy przed poleceniem wszystkie osiem wyjść było wyłączonych**:

```text
RX: O=1,0,0,0,1,0,0,0,0<CR><LF>
```

Odczyt na żądanie dla tego samego stanu:

```text
TX: AT+GetOut=1<CR>
RX: O=1,0,0,0,1,0,0,0,0<CR><LF>
```

Rzeczywiste pozostałe pola O= zależą od wcześniejszych stanów przekaźników. Kolejne wysłanie tej samej komendy przełączy WY4 ponownie, dlatego program nie powinien bezwarunkowo ponawiać TOGGLE po utracie odpowiedzi. Najpierw odczytaj GetOut.

### C. Moduł ID=5: pełne otwarcie wszystkich czterech rolet

Pełne otwarcie oznacza **100%**. Można użyć akcji OPEN=1 z polem procentu 0. To pole musi mieć 0 przy akcji OPEN — procent 100 występuje przy odrębnej akcji pozycjonowania 7. Pełne OPEN pozwala również ustalić pozycję, jeśli była nieznana.

**Każda roleta musi mieć ustawione czasy przejazdu.** Przykład 6 skonfigurował w module 5 tylko rolety 3 i 4. Aby otworzyć wszystkie cztery w tej samej konfiguracji, uzupełnij czasy rolet 1 i 2. Poniżej przyjmujemy 50 s otwierania i 52 s zamykania — na rzeczywistej instalacji użyj zmierzonych czasów. Jeśli czasy są już prawidłowo zapisane, pomiń ten blok.

```text
TX: AT+RolTime=5,1,500,520,1026<CR>
RX: RuleOK=5<CR><LF>

TX: AT+RolTime=5,2,500,520,1027<CR>
RX: RuleOK=5<CR><LF>

TX: AT+SaveConfig=5,5<CR>
RX: SaveOK=5<CR><LF>
```

Teraz wyślij cztery komendy sterujące, po jednej na roletę:

```text
TX: AT+RolAct=5,1,1,0,7<CR>
RX: RuleOK=5<CR><LF>

TX: AT+RolAct=5,2,1,0,8<CR>
RX: RuleOK=5<CR><LF>

TX: AT+RolAct=5,3,1,0,9<CR>
RX: RuleOK=5<CR><LF>

TX: AT+RolAct=5,4,1,0,10<CR>
RX: RuleOK=5<CR><LF>
```

Moduł odsyła RuleOK=5 za każdą przyjętą komendę. Po uruchomieniu wszystkich napędów może pojawić się raport:

```text
RX: R=5,2,2,2,2<CR><LF>
```

W tym raporcie 2 oznacza otwieranie. Mogą pojawić się również raporty pośrednie, gdy kolejne rolety zaczynają lub kończą ruch; **RuleOK nie oznacza osiągnięcia 100%**.

Po zakończeniu pełnych przejazdów odczytaj ruch i pozycje:

```text
TX: AT+StanRol=5<CR>
RX: R=5,0,0,0,0<CR><LF>

TX: AT+GetRolState=5,1,6<CR>
RX: RolState=5,1,0,1,100,255,0,362<CR><LF>

TX: AT+GetRolState=5,2,7<CR>
RX: RolState=5,2,0,1,100,255,0,363<CR><LF>

TX: AT+GetRolState=5,3,8<CR>
RX: RolState=5,3,0,1,100,255,0,364<CR><LF>

TX: AT+GetRolState=5,4,9<CR>
RX: RolState=5,4,0,1,100,255,0,365<CR><LF>
```

Odpowiedzi RolState pokazują postój (0), znaną pozycję (1), otwarcie 100%, brak aktywnego celu (255) i pozostały czas 0. Są to odpowiedzi **po zakończeniu ruchu**. W trakcie jazdy odczyt będzie inny — odpytuj aż do osiągnięcia oczekiwanego stanu.

<a id="przyklad-8"></a>

## Przykład 8. Raporty po krótkim naciśnięciu wejścia 8 modułu ID=3

Jednostka sterująca może odbierać zdarzenia przycisków bez ciągłego odpytywania wejść. W tej linii **moduł 3 to R0806T**. Po krótkim naciśnięciu jego wejścia 8 raporty przechodzą przez moduły 2 i 1 do jednostki sterującej — np. RTI, Home Assistant lub komputera PC.

W tym przykładzie wejścia 1–7 modułu 3 są rozwarte, a wejście 8 na początku również jest rozwarte. Po wykonaniu przykładu 3 próg SHORT wejścia 8 wynosi 0,3 s, a LONG 2 s. Naciśnij i puść wejście krótko, np. po około 0,2 s.

### A. Co wysyła moduł 3

Po potwierdzeniu naciśnięcia przez filtr wejścia moduł wysyła obraz stanów:

```text
I=3,0,0,0,0,0,0,0,1<CR><LF>
```

Po ID=3 występuje osiem stanów WE1–WE8. Ostatnia jedynka oznacza zwarte wejście 8.

Po potwierdzeniu puszczenia wysyła obraz rozwarcia, a następnie zdarzenie SHORT:

```text
I=3,0,0,0,0,0,0,0,0<CR><LF>
PS=3,8<CR><LF>
```

Cała oczekiwana sekwencja dla tej próby:

```text
I=3,0,0,0,0,0,0,0,1<CR><LF>
I=3,0,0,0,0,0,0,0,0<CR><LF>
PS=3,8<CR><LF>
```

**PS=3,8** oznacza: „moduł ID=3 zgłosił krótkie naciśnięcie wejścia 8”. PS powstaje po puszczeniu, a nie w chwili rozpoczęcia naciśnięcia. PL nie pojawi się przy tym krótkim naciśnięciu.

### B. Jak raporty przechodzą przez linię

```text
R0806T ID=3   →   R0806T ID=2   →   R0808 ID=1   →   RTI / Home Assistant / PC
    port 0          port 1 RX         port 1 RX
                    port 0 TX         port 0 TX
```

Każdy pośrednik zachowuje treść raportu, w tym źródłowe ID=3:

| Droga | Odebrany i przekazany tekst |
|---|---|
| Moduł 3 → moduł 2 | `I=3,0,0,0,0,0,0,0,1<CR><LF>` |
| Moduł 3 → moduł 2 | `I=3,0,0,0,0,0,0,0,0<CR><LF>` |
| Moduł 3 → moduł 2 | `PS=3,8<CR><LF>` |
| Moduł 2 → moduł 1 | `I=3,0,0,0,0,0,0,0,1<CR><LF>` |
| Moduł 2 → moduł 1 | `I=3,0,0,0,0,0,0,0,0<CR><LF>` |
| Moduł 2 → moduł 1 | `PS=3,8<CR><LF>` |
| Moduł 1 → jednostka sterująca | `I=3,0,0,0,0,0,0,0,1<CR><LF>` |
| Moduł 1 → jednostka sterująca | `I=3,0,0,0,0,0,0,0,0<CR><LF>` |
| Moduł 1 → jednostka sterująca | `PS=3,8<CR><LF>` |

Moduł 2 nie zmienia ID na 2, a moduł 1 na 1. Druga liczba w PS=3,8 jest numerem wejścia, nie adresem kolejnego modułu.

### C. Co odbiera i interpretuje jednostka sterująca

```text
RX: I=3,0,0,0,0,0,0,0,1<CR><LF>
RX: I=3,0,0,0,0,0,0,0,0<CR><LF>
RX: PS=3,8<CR><LF>
```

Jednostka sterująca rozpoznaje prefiks:

- I= — obraz stanów wejść modułu wskazanego przez ID.
- PS= — zdarzenie krótkiego naciśnięcia; kolejne pola to ID modułu i numer wejścia.
- PL= — zdarzenie długiego przytrzymania; w tej próbie go nie ma.

Jeśli ma wykonać automatyzację po krótkim naciśnięciu, powinna obsłużyć **PS=3,8**. Sam raport I= po zwarciu nie oznacza jeszcze krótkiego naciśnięcia — przycisk może być nadal trzymany.

Są to samoczynne **raporty zdarzeń i stanu**, a nie polecenia AT wysyłane przez jednostkę sterującą. Nie wymagają zapytania GetInputs ani odpowiedzi RuleOK z RTI/Home Assistant/PC. Pośrednik również nie odsyła RuleOK za samo przekazanie raportu i nie uruchamia własnej reguły tylko dlatego, że odebrał cudze PS.

Jeżeli inne wejścia modułu 3 są zwarte, odpowiednie pola I= będą miały wartość 1; PS=3,8 pozostanie takie samo. Przy równoległych zdarzeniach mogą pojawić się dodatkowe linie. Odbiornik powinien rozdzielać ramki znakami końca linii i rozpoznawać prefiks, ID oraz numer wejścia. RTI/Home Assistant wymagają obsługi tego protokołu w użytym sterowniku lub integracji.

<a id="przyklad-9"></a>

## Przykład 9. Automatyczny raport po włączeniu wyjść 7 i 8 modułu ID=1

Moduł 1 to R0808. Załóżmy, że wyjścia 1–6 są wyłączone, a wyjścia 7 i 8 zmieniły stan na włączony. Jednostka sterująca otrzyma **samoczynny raport stanu**, bez wysyłania GetOut:

```text
RX: O=1,0,0,0,0,0,0,1,1<CR><LF>
```

Po ID=1 występuje osiem stanów WY1–WY8: 0 oznacza wyłączone, 1 włączone. Dwie końcowe jedynki oznaczają załączone WY7 i WY8.

Raport O= powstaje po rzeczywistej zmianie stanu sterowania wyjściami, niezależnie od źródła zmiany: komendy SetOut, lokalnej reguły, przycisku działającego przez regułę albo akcji zdalnej z innego modułu. Odbiornik nie musi wiedzieć, co spowodowało zmianę, żeby zaktualizować stan wyjść na podstawie O=.

Jeśli przejście z samych zer odbyło się kolejno — najpierw WY7, potem WY8 — można odebrać:

```text
RX: O=1,0,0,0,0,0,0,1,0<CR><LF>
RX: O=1,0,0,0,0,0,0,1,1<CR><LF>
```

Każda linia zawiera cały obraz ośmiu wyjść w danym momencie, a nie wyłącznie numer zmienionego przekaźnika. Nie zakładaj, że kilka zmian tworzy jeden wspólny raport.

Kontrolnie można też odpytać bieżący stan:

```text
TX: AT+GetOut=1<CR>
RX: O=1,0,0,0,0,0,0,1,1<CR><LF>
```

Automatyczne O= i odpowiedź na GetOut mają ten sam format. O= jest raportem stanu sterowania przekaźników, nie niezależnym pomiarem ich styków. Sam raport asynchroniczny nie wymaga potwierdzenia RuleOK od odbiornika. Jeśli wyjścia już mają zadany stan, ponowne polecenie ON nie jest nową zmianą i nie tworzy z tego powodu kolejnego automatycznego raportu.

<a id="przyklad-10"></a>

## Przykład 10. Odczyt wejść, wyjść i PWM modułu ID=2

Moduł 2 to R0806T: ma osiem wejść, sześć wyjść przekaźnikowych oraz PWM. Przyjmijmy:

- wejścia 1 i 2 są aktywne, pozostałe rozwarte;
- wyjścia 5 i 6 są włączone, pozostałe wyłączone;
- PWM osiągnął 60%, cel i zapamiętany poziom wynoszą 60%, rampa już się zakończyła.

### A. Stan ośmiu wejść

```text
TX: AT+GetInputs=2<CR>
RX: I=2,1,1,0,0,0,0,0,0<CR><LF>
```

Po ID=2 występują stany WE1–WE8. Jedynki na dwóch pierwszych pozycjach oznaczają aktywne wejścia 1 i 2. To stany po filtracji drgań styków, a nie zdarzenia krótkiego lub długiego naciśnięcia.

### B. Stan sześciu przekaźników

```text
TX: AT+GetOut=2<CR>
RX: o=2,0,0,0,0,1,1<CR>
```

Po ID=2 występują stany WY1–WY6. Wyjścia 1–4 są wyłączone, 5 i 6 włączone. **R0806T używa małego o= i zakończenia CR**; nie należy oczekiwać identycznego zakończenia jak przy raporcie O= modułu R0808.

### C. Stan PWM

```text
TX: AT+GetPWM=2<CR>
RX: PWM=2,60,60,60,0,2000<CR><LF>
```

| Pole | Wartość | Znaczenie |
|---|---|---|
| ID | 2 | Moduł odpowiadający |
| AKTUALNY | 60 | Bieżący poziom PWM 60% |
| CEL | 60 | Poziom docelowy 60% |
| PAMIĘĆ | 60 | Zapamiętany ostatni niezerowy poziom 60% |
| RAMPA | 0 | Rampa nie jest aktywna |
| HZ | 2000 | Częstotliwość PWM 2 kHz |

PAMIĘĆ i CEL to osobne pola; w tym przykładzie przyjęto takie same wartości jak bieżący poziom. Jeśli trwa zmiana, odpowiedź może pokazać inną wartość CEL i RAMPA=1.

Wszystkie trzy zapytania są odczytami: nie zmieniają wyjść, PWM ani konfiguracji EEPROM i nie uruchamiają reguł. Nie mają pola SUMA. Poprawna odpowiedź zawiera dane I=/o=/PWM=, bez dodatkowego RuleOK. Są to trzy kolejne odczyty, nie jeden jednoczesny pomiar wszystkich stanów.

<a id="przyklad-11"></a>

## Przykład 11. Stan czterech rolet modułu ID=5, w tym ruch do zadanego procentu

Odpytujemy stan — **żadna poniższa komenda nie uruchamia ani nie zatrzymuje ruchu**. Przyjmijmy, że pozycje są znane i w chwili odczytu:

- roleta 1 otwiera się, osiągnęła 60%, a jej celem jest 80%;
- roleta 2 stoi w pozycji w pełni otwartej, 100%;
- rolety 3 i 4 stoją w pozycji zamkniętej, 0%.

Dla rolety 1 przyjmujemy czas pełnego otwarcia **50 s**, ustawiony w przykładzie 7. Pozostałe 20 punktów procentowych oznacza w tym przykładzie około **10 s**, czyli POZOSTALO=100 w jednostkach 0,1 s. Ruch już trwa, więc nie doliczamy przerwy przed zmianą kierunku.

### A. Zbiorczy odczyt ruchu wszystkich rolet

```text
TX: AT+StanRol=5<CR>
RX: R=5,2,0,0,0<CR><LF>
```

Po ID=5 występują stany rolet 1–4:

- 2 przy rolecie 1 — otwieranie;
- 0 przy roletach 2, 3 i 4 — postój.

**R= nie podaje procentów.** Samo 0 nie pozwala rozróżnić rolety otwartej od zamkniętej; do tego służą odczyty szczegółowe poniżej.

### B. Roleta 1: obecnie 60%, otwiera się do 80%

```text
TX: AT+GetRolState=5,1,6<CR>
RX: RolState=5,1,2,1,60,80,100,249<CR><LF>
```

Znaczenie: ID=5, NR=1, STAN=2 (otwieranie), ZNANA=1, POZYCJA=60%, CEL=80%, POZOSTALO=100 × 0,1 s = 10 s. Suma wynosi 249.

Możesz dodatkowo sprawdzić założone czasy rolety 1:

```text
TX: AT+GetRolTime=5,1,6<CR>
RX: RolTime=5,1,500,520,1026<CR><LF>
```

To odczyt 50 s otwierania i 52 s zamykania. Przy innych ustawionych czasach pole POZOSTALO będzie inne, nawet dla tych samych procentów 60→80.

### C. Roleta 2: otwarta na 100%, postój

```text
TX: AT+GetRolState=5,2,7<CR>
RX: RolState=5,2,0,1,100,255,0,363<CR><LF>
```

STAN=0, ZNANA=1, POZYCJA=100%, CEL=255 (brak aktywnego celu), POZOSTALO=0.

### D. Roleta 3: zamknięta, postój

```text
TX: AT+GetRolState=5,3,8<CR>
RX: RolState=5,3,0,1,0,255,0,264<CR><LF>
```

STAN=0, ZNANA=1, POZYCJA=0%, CEL=255, POZOSTALO=0.

### E. Roleta 4: zamknięta, postój

```text
TX: AT+GetRolState=5,4,9<CR>
RX: RolState=5,4,0,1,0,255,0,265<CR><LF>
```

STAN=0, ZNANA=1, POZYCJA=0%, CEL=255, POZOSTALO=0.

### Zestawienie odczytu

| Roleta | Ruch | Pozycja | Aktywny cel | Pozostały czas |
|---|---|---|---|---|
| 1 | otwiera się | 60% | 80% | około 10 s |
| 2 | postój | 100% | brak | 0 |
| 3 | postój | 0% | brak | 0 |
| 4 | postój | 0% | brak | 0 |

Podane odpowiedzi obrazują opisany stan. Zapytania są wykonywane kolejno, a roleta 1 w tym czasie jedzie, więc w rzeczywistym odczycie jej procent i pozostały czas mogą się już zmienić. Odpowiedzi RolState nie są wysyłane automatycznie jako jedna paczka: każda jest wynikiem osobnego GetRolState.

## Dokumenty powiązane

- [Wspólne komendy i zasady komunikacji](komendy-wspolne.md)
- [Wejścia i progi przycisków](wejscia-komendy.md)
- [Reguły R0806T](reguly-R0806T.md)
- [Reguły R0808](reguly-R0808.md)
- [Rolety S0804](rolety-komendy.md)

