# Odczyt wejść i progów przycisków — R0806T 0018

Od firmware **0018** dostępne są GetInputs i GetKeyTime. Komendy działają na obu UART-ach; poprawne zapytanie do innego ID jest przekazywane na drugi port, a odpowiedź wraca przez moduły pośrednie. Łącze: 115200 8N1. `<CR>` to bajt 0x0D; odpowiedzi kończą się CRLF.

## GetInputs

```text
TX: AT+GetInputs=1<CR>
RX: I=1,1,0,0,0,0,0,0,1<CR><LF>
```

Format zapytania: `AT+GetInputs=ID`. ID: 1–35; ID=0 nie jest obsługiwane. Nie dodaje się sumy kontrolnej. Odpowiedź: `I=ID,WE1,WE2,WE3,WE4,WE5,WE6,WE7,WE8`. Stan 1 oznacza potwierdzone zwarcie do masy, 0 — rozwarcie. Przykład pokazuje zwarte wejścia 1 i 8. Jest to jeden spójny odczyt maski po filtracji drgań styków, a nie surowy odczyt pinów.

Komenda nie generuje naciśnięcia, nie wykonuje reguł i nie usuwa oczekujących zdarzeń wejściowych. Nie zmienia wyjść ani EEPROM. Automatyczne raporty zmiany wejść mają ten sam prefiks I= i mogą pojawiać się niezależnie od zapytania.

## GetKeyTime

```text
TX: AT+GetKeyTime=1,1,2<CR>
RX: KeyTime=1,1,5,20,27<CR><LF>
```

Zapytanie: `AT+GetKeyTime=ID,WEJSCIE,SUMA`, gdzie WEJSCIE=1–8, SUMA=ID+WEJSCIE. Odpowiedź: `KeyTime=ID,WEJSCIE,SHORT,LONG,SUMA`; suma odpowiedzi obejmuje cztery poprzednie liczby. W przykładzie 1+1+5+20=27, SHORT=0,5 s, LONG=2 s. Jednostka to 0,1 s, dozwolone progi: `1 <= SHORT < LONG <= 250`.

Odczytywana jest aktualna konfiguracja RAM, również zmieniona i jeszcze niezapisana. Sam odczyt nie dowodzi utrwalenia jej w EEPROM. Ustawianie i zapis:

```text
TX: AT+KeyTime=1,1,5,20,27<CR>
RX: RuleOK=1<CR><LF>
TX: AT+GetKeyTime=1,1,2<CR>
RX: KeyTime=1,1,5,20,27<CR><LF>
TX: AT+SaveConfig=1,1<CR>
RX: SaveOK=1<CR><LF>
```

GetKeyTime nie zmienia progów ani pomiaru aktualnie trzymanego przycisku. Błędny format, ID, numer wejścia lub suma powodują `RuleERROR=ID_MODULU`. Poprawne odczyty zwracają dane bez dodatkowego RuleOK. Moduły pośrednie muszą obsługiwać te zapytania i przekazywanie odpowiedzi KeyTime; odpowiednie wersje to R0806T 0018 i S0804 0731. Starsze wsady mogą zatrzymać ramkę.
