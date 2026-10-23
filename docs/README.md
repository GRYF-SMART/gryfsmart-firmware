# Dokumentacja poleceń GRYFSMART

Instrukcje obejmują narzędzia **2.0.1** oraz kolejne aktualizacje aplikacji opisane przy modułach. Nowe odczyty rolet wymagają S0804 **0732** i odpowiedniej wersji modułów pośrednich; dostępność funkcji sprawdzaj według wersji konkretnego wsadu, nie samego numeru narzędzia Windows. Komendy podaje się jako tekst ASCII bez spacji i kończy znakiem CR (`\r`; terminal może wysyłać CRLF). Liczby są dziesiętne, chyba że opis komendy podaje HEX — tak jest dla parametrów Discovery/CHAIN1. Typowe łącze serwisowe: **115200 bit/s, 8 bitów danych, bez parzystości, 1 bit stopu (8N1), bez kontroli przepływu**. Zamknij inne programy korzystające z danego portu COM.

## Wybierz moduł

**[S0804 — pełna obsługa rolet: RolTime, RolAct, STEP, procenty, StanRol oraz nowe GetRolTime/GetRolState](rolety-komendy.md)**. Instrukcja dzieli polecenia na parametry, sterowanie i statusy oraz opisuje przekazywanie przez R0808, R0806T i ETH0606T.

Wspólna obsługa przekaźników **R0808, R0806T i ETH0606T**: [SetOut, GetOut oraz raporty O=/o=](wyjscia-komendy.md). R0808 od 0011 ma lokalny GetOut i raport po zmianie; instrukcja wskazuje również różnice formatów w pozostałych modułach.

```text
Ustawienie: AT+SetOut=ID,A1,...,AN<CR>
Odczyt:     AT+GetOut=ID<CR>
Stan:       O=ID,S1,...,SN<CR><LF>
```

Powyższy format stanu jest używany przez R0808 0011; warianty o=/O= oraz CR/CRLF w R0806T i ETH opisuje wspólna instrukcja.

Wspólny opis **Search / Find, Discovery i Info**, z formatami ramek, parametrami odpowiedzi i przykładem adresowania trzech modułów: [Identyfikacja i adresowanie](komendy-wspolne.md).

Pełny opis wejść bez konfiguracji reguł: **[Komendy wejściowe — I, PS, PL, KeyTime, GetInputs, GetKeyTime, SaveConfig, Defaults i KEYERROR](wejscia-komendy.md)**. Instrukcja zawiera sekwencje krótkiego/długiego naciśnięcia, jednostki czasu, sumy kontrolne oraz zasady wysyłania i przekazywania raportów.

| Moduł | Najważniejsze funkcje | Dokument |
|---|---|---|
| R0808 | 8 wyjść przekaźnikowych, reguły, odczyt 2 czujników, łańcuch do 35 modułów; port logiczny 0 = USART3 | [R0808](R0808.md) |
| R0806T | 6 przekaźników, PWM, termostat, 2 kanały temperatury, łańcuch do 35 modułów; port logiczny 0 = USART0 | [R0806T](R0806T.md) |
| S0804 | 4 rolety, reguły lokalne i zdalne, łańcuch do 35 modułów; port logiczny 0 = USART0 | [S0804](S0804.md) |
| ETH0606T | 6 wyjść, USB/USART0 i RS-232/USART1, 5 czujników DS18B20 | [ETH0606T](ETH0606T.md) |

## Ważne odpowiedzi

- `RuleOK=<ID>` — moduł przyjął komendę; dla ruchu rolety nie oznacza zakończenia ruchu.
- `RuleERROR=<ID>` — składnia, zakres, suma kontrolna lub stan modułu uniemożliwiły wykonanie.
- `SaveOK=<ID>` / `SaveERROR=<ID>` — zakończenie zapisu konfiguracji do EEPROM.
- Odpowiedzi i powiadomienia mogą pojawić się asynchronicznie. Filtruj je po prefiksie/ID zamiast zakładać, że kolejna linia należy do ostatniej komendy.

## Zasady bezpieczeństwa konfiguracji

`AT+Search=LICZNIK,DOCELOWE_ID` wybiera jedną pozycję w liniowej sieci i zapisuje jej nowe ID w EEPROM. Aby nadać adresy wszystkim N modułom, wyślij kolejno `AT+Search=0,1` do `AT+Search=0,N`, oczekując na każde `AT+Find=ID,WERSJA,TYP`. Jedno `AT+Search=0,N` adresuje tylko pozycję N. Do rozpoznania bez zmiany ID służy `AT+Discovery` w obsługiwanych modułach; szczegóły i odmienną obsługę ETH opisuje [wspólna instrukcja](komendy-wspolne.md).

`AT+Defaults` czyści konfigurację roboczą. Po zmianach, które mają przetrwać utratę zasilania, wykonaj `AT+SaveConfig`. `AT+RST` resetuje wskazany moduł; `AT+BOOT=1` uruchamia tryb aktualizacji i wyłącza sterowanie wyjściami.

W polach oznaczonych **SUMA** podaj sumę wszystkich wcześniejszych liczb w komendzie. Przykład: `AT+KeyTime=1,1,5,20,27` ma sumę `1+1+5+20=27`.
