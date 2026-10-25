# R0806T 20 — zdalny PWM w RuleRemote

W aplikacji **20** reguła R0806T obsługuje zdalny PWM jako typ 4, tak samo jak R0808, ETH0606T i S0804. Lokalny RulePWM/GetRulePWM pozostaje dostępny i może działać razem z akcją zdalną.

## Konfiguracja i odczyt

```text
AT+RuleRemote=ID,NR,SLOT,CEL,4,AKCJA,PROCENT,RAMPA,SUMA<CR>
AT+GetRuleRemote=ID,NR,SLOT,SUMA<CR>
RuleRemote=ID,NR,SLOT,CEL,4,AKCJA,PROCENT,RAMPA,SUMA<CR><LF>
```

ID: moduł przechowujący regułę (1–35); NR: reguła 1–16; SLOT: 1–4; CEL: inny moduł 1–35, posiadający PWM. Ten sam CEL nie może być powtórzony w kilku slotach danej reguły, zgodnie z dotychczasowymi zasadami R0806T oraz R0808/ETH.

| AKCJA | Działanie |
|---|---|
| 0 | Bez akcji; nie nadaje ramki PWM |
| 1 | Włącz ostatni niezerowy poziom odbiorcy |
| 2 | Wyłącz |
| 3 | Przełącz |
| 4 | Ustaw PROCENT |

PROCENT: 0–100, niezerowy wyłącznie dla akcji 4. RAMPA: 0–50 w jednostkach 0,1 s; 0 oznacza zmianę natychmiastową. SUMA jest sumą wszystkich wcześniejszych liczb.

Przykład: moduł 1 ma ustawiać PWM modułu 2 na 50%, z rampą 1 s:

```text
TX: AT+RuleRemote=1,1,1,2,4,4,50,10,73<CR>
RX: RuleOK=1
TX: AT+GetRuleRemote=1,1,1,3<CR>
RX: RuleRemote=1,1,1,2,4,4,50,10,73<CR><LF>
```

Następnie trzeba włączyć regułę pełną komendą Rule (zmiana slotu ustawia EN=0). Przykład wyzwalania krótkim naciśnięciem wejścia 1, bez lokalnych akcji przekaźników:

```text
TX: AT+Rule=1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,4<CR>
RX: RuleOK=1
TX: AT+SaveConfig=1,1<CR>
RX: SaveOK=1
```

Po zdarzeniu wejścia R0806T nada na oba porty linii:

```text
AT+PWM=2,4,50,10,66<CR><LF>
```

Odbiorca wykonuje komendę bez uruchamiania własnej reguły. Wynik można sprawdzić przez AT+GetPWM=2. Slot typu 4 nie modyfikuje lokalnego PWM modułu 1. Suma przykładu wynosi 73.

## Trwałość i kolejki

Slot PWM w EEPROM ma trzy znaczące bajty danych (akcja, procent, rampa) i pięć zerowych bajtów rezerwowych. Układ pól i rozmiar reguły są zachowane; zapis utrwala SaveConfig.

Lokalne akcje nadal działają niezależnie od UART. Zdalna akcja czeka na wolne miejsce, zachowując kursor wykonania; nie jest wielokrotnie nadawana w wyniku ponawiania sprawdzenia kolejki. Nie dodano potwierdzania wykonania całej sceny.


