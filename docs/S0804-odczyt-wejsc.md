# Odczyt wejść i progów przycisków — S0804 0731

Od firmware **0731** S0804 obsługuje `AT+GetInputs` i `AT+GetKeyTime` na obu UART-ach, zgodnie z formatem R0808 i R0806T 0018. Odczyty nie zmieniają konfiguracji, wyjść rolet ani EEPROM, nie wykonują reguł i nie usuwają oczekujących zdarzeń przycisków.

## GetInputs

```text
TX: AT+GetInputs=2<CR>
RX: I=2,1,0,0,0,0,0,0,1<CR><LF>
```

Zapytanie ma format `AT+GetInputs=ID`, bez sumy kontrolnej. ID: 1–35; 0 nie jest obsługiwane. Po ID odpowiedź zawiera stany WE1–WE8: 1 = zwarcie do masy, 0 = rozwarcie. Przykład pokazuje zwarte wejścia 1 i 8. Moduł odczytuje jedną maskę potwierdzonych stanów po filtrowaniu drgań, a nie surowy stan pinów.

Automatyczne raporty po zmianach wejść również zaczynają się od I=. Ich nadejście nie musi oznaczać odpowiedzi na zapytanie.

## GetKeyTime

```text
TX: AT+GetKeyTime=2,1,3<CR>
RX: KeyTime=2,1,5,20,28<CR><LF>
```

Zapytanie: `AT+GetKeyTime=ID,WEJSCIE,SUMA`; WEJSCIE=1–8, SUMA=ID+WEJSCIE. Odpowiedź: `KeyTime=ID,WEJSCIE,SHORT,LONG,SUMA`. Jednostka SHORT/LONG to 0,1 s; w przykładzie 0,5 s i 2 s. Suma odpowiedzi: 2+1+5+20=28. Zakres progów: `1 <= SHORT < LONG <= 250`.

Odczyt dotyczy aktualnego RAM. Progi ustawia się KeyTime, a utrwala przez SaveConfig:

```text
TX: AT+KeyTime=2,1,5,20,28<CR>
RX: RuleOK=2<CR><LF>
TX: AT+GetKeyTime=2,1,3<CR>
RX: KeyTime=2,1,5,20,28<CR><LF>
TX: AT+SaveConfig=2,2<CR>
RX: SaveOK=2<CR><LF>
```

Poprawne zapytanie do innego ID przechodzi drugim UART-em bez zmiany treści. Odpowiedzi I= i KeyTime= są przekazywane w przeciwną stronę. Błędny format/zakres/suma zwraca `RuleERROR=ID_MODULU`; poprawny odczyt nie wysyła dodatkowego RuleOK. Starsze moduły pośrednie bez tej obsługi mogą zatrzymać zapytanie lub odpowiedź.

Łącze: 115200 8N1. `<CR>` oznacza bajt 0x0D, odpowiedzi kończą się CRLF. Nie wpisuj dosłownie znaków `<CR>` do terminala.
