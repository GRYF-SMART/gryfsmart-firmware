# Dokumentacja poleceń GRYFSMART

Instrukcje opisują firmware opublikowane w wydaniu **2.0.1**. Wszystkie komendy podaje się jako tekst ASCII, liczby dziesiętne bez spacji i kończy znakiem CR (`\r`; terminal może wysyłać CRLF). Typowe łącze serwisowe: **115200 bit/s, 8 bitów danych, bez parzystości, 1 bit stopu (8N1), bez kontroli przepływu**. Zamknij inne programy korzystające z danego portu COM.

## Wybierz moduł

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

`AT+Search` rozdziela kolejne ID w liniowej sieci i zapisuje nowe ID w EEPROM. Nie jest odczytem ani skanowaniem bez skutków ubocznych. Użyj go tylko wtedy, gdy zamierzasz ponumerować moduły i znasz kierunek liczenia. Do odczytu sieciowego użyj programatora albo polecenia `AT+Discovery` w obsługiwanych modułach.

`AT+Defaults` czyści konfigurację roboczą. Po zmianach, które mają przetrwać utratę zasilania, wykonaj `AT+SaveConfig`. `AT+RST` resetuje wskazany moduł; `AT+BOOT=1` uruchamia tryb aktualizacji i wyłącza sterowanie wyjściami.

W polach oznaczonych **SUMA** podaj sumę wszystkich wcześniejszych liczb w komendzie. Przykład: `AT+KeyTime=1,1,5,20,27` ma sumę `1+1+5+20=27`.
