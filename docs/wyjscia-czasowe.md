# Wyjścia czasowe — firmware 22

Obsługa lokalnych przekaźników: R0808 (WY1–8), R0806T i ETH0606T (WY1–6).
S0804 przekazuje polecenia i może wyzwalać czasowe akcje zdalne ze swoich 16 reguł. Nie wykonuje impulsów na wyjściach roletowych.

## Komenda bezpośrednia

`AT+Pulse=ID,WYJŚCIE,CZAS,RESET`

- ID: 1–35. Polecenie do innego adresu przechodzi na sparowany port łańcucha.
- CZAS: 16 bitów bez znaku, 0–65535, jednostka 0,1 s. 100 = 10 s. Maksimum to 6553,5 s (1 h 49 min 13,5 s).
- RESET=1: ponowienie rozpoczyna pełny czas od nowa; zwykłe ON/OFF/TOGGLE anuluje timer i wykonuje żądaną akcję.
- RESET=0: aktywny impuls jest chroniony. Ponowne Pulse (także z innym RESET i czasem 0), ON, OFF oraz TOGGLE są ignorowane aż do upływu pierwotnego czasu. KEEP nie wpływa na timer.
- Pominięty RESET oznacza 1. O rozpoczętym impulsie decyduje jego pierwotny parametr; kolejna komenda nie może zdjąć ochrony.
- CZAS=0 przy braku ochrony wyłącza wyjście i anuluje timer. Nie rozpoczyna nowego impulsu.

Przykłady (każda linia zakończona bajtem CR):

```text
AT+Pulse=2,6,100,1
AT+Pulse=2,6,100,0
AT+Pulse=2,6,0,1
```

Odpowiedź na poprawne lokalne polecenie: RuleOK=ID. Błędny zakres lub nieistniejące lokalne wyjście: RuleERROR=ID. RuleOK oznacza przyjęcie poprawnej komendy; chroniony impuls może pozostać bez zmian. Nie jest potwierdzeniem fizycznych styków.

## Konfiguracja RULE / SLOT

`AT+RulePulse=ID,REGUŁA,SLOT,CEL,WYJŚCIE,CZAS,RESET`

REGUŁA=1–16, SLOT=1–4, CEL=1–35. CEL równy ID oznacza lokalne wyjście. S0804 wymaga celu zdalnego. RESET można pominąć (1).
Komenda ustawia akcję w istniejącym slocie, zachowuje wyzwalacze i pozostałe akcje, a regułę wyłącza. Po konfiguracji slotów należy włączyć ją komendą Rule. Cztery sloty mogą wskazywać ten sam moduł. Przy kilku akcjach na jedno wyjście kolejność slotów ma znaczenie.

`AT+GetRulePulse=ID,REGUŁA,SLOT`

Odpowiedź: `RulePulse=ID,REGUŁA,SLOT,CEL,WYJŚCIE,CZAS,RESET`. Dla slotu innego typu ostatnie cztery pola wynoszą zero. Komendy Pulse/RulePulse/GetRulePulse nie mają sumy kontrolnej, podobnie jak istniejące SetOut. Zapytania i odpowiedzi przechodzą przez moduły pośrednie.

### Krótkie naciśnięcie WE1 → lokalne WY6 na 10 s

Najpierw slot, potem włączenie reguły z maską SHORT=1:

```text
AT+RulePulse=1,1,1,1,6,100,1
```

R0806T:

```text
AT+Rule=1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,4
AT+SaveConfig=1,1
```

R0808:

```text
AT+Rule=1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4
AT+SaveConfig=1,1
```

ETH0606T (ID=1):

```text
AT+Rule=1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,4
AT+SaveConfig=1,1
```

Dla zdalnego WY6 modułu ID=2 zmień CEL na 2. Dla impulsu chronionego ustaw ostatni parametr na 0. SaveConfig utrwala ustawienia dopiero po SaveOK, nie zapisuje aktualnego odliczania.

## Format istniejącego RuleRemote i EEPROM

Nowy typ slotu: **5**. Dane w istniejących ośmiu bajtach: WYJŚCIE, CZAS_LO, CZAS_HI, RESET, 0, 0, 0, 0.
RuleRemote wysyła dla typu 5 cztery pola danych i dotychczasową sumę kontrolną, np.:

```text
AT+RuleRemote=1,1,1,2,5,6,255,255,0,526
```

To zdalne WY6 na 6553,5 s, chronione. GetRuleRemote odczytuje tę samą reprezentację. Układ i rozmiar rekordów EEPROM pozostają bez zmian; walidacja dopuszcza nowy typ 5. Starsze firmware nie obsługują tych akcji: wszystkie moduły pośrednie i docelowe wymagają aktualizacji do wersji 22. Przed powrotem do starszego firmware należy wykonać kopię i usunąć akcje typu 5.

## Działanie

Timery są niezależne dla każdego wyjścia, wykonywane bez opóźnień blokujących w pętli głównej. Czas jest liczony zegarem 2 ms z rozdzielczością nastawy 0,1 s, poprawnie przy przepełnieniu zegara. Zajęty UART nie blokuje lokalnego wyzwolenia ani wyłączenia po czasie. Ramki zdalnych slotów czekają na miejsce w kolejce UART. Polecenia i termostaty korzystające ze wspólnej obsługi wyjść respektują ochronę.

Odliczanie nie jest zapisywane w EEPROM i nie jest odtwarzane po restarcie lub utracie zasilania. Przy kontrolowanym RST aktywne wyjścia czasowe są wyłączane i wykluczane z migawki przywracanych wyjść. Ochrona dotyczy poleceń sterowania, nie blokuje restartu urządzenia.

## Weryfikacja

Testy AVR obejmują 0,1 s, 10 s, 65535 jednostek, przepełnienie zegara, niezależność wyjść, ponowienie, anulowanie, ochronę przed OFF/TOGGLE, zakresy parametrów, wszystkie 16 reguł i 4 sloty, zapis/odczyt EEPROM oraz przekazywanie poleceń. ETH ma dodatkowy test wykonywania produkcyjnego HEX w emulatorze z rzeczywistymi przerwaniami Timer2 i UART. Próba na fizycznych modułach pozostaje do wykonania.
