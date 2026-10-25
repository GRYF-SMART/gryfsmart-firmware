# S0804 — reguły RULE

[Dokumentacja główna](README.md) · [Porównanie modułów i ograniczenia](reguly-porownanie.md)

Wersja oprogramowania: **20**. Przykłady zakładają ID modułu **1** i regułę **1**. Każda wysyłana linia kończy się CR; zapis `<CR>` oznacza ten znak, nie dosłowny tekst.

## Jak działa reguła

Moduł ma **16 reguł**, każda zawiera włączenie EN, maski zdarzeń 8 lokalnych wejść, akcje lokalne i **4 sloty zdalne**. Regułę wyzwala zdarzenie własnego wejścia. Odebranie raportu PS/PL innego modułu nie jest warunkiem uruchomienia tej reguły.

| Maska wejścia E | Zdarzenie |
|---|---|
| 0 | wejście nie wyzwala reguły |
| 1 | krótkie naciśnięcie |
| 2 | długie naciśnięcie |
| 4 | wciśnięcie |
| 8 | zwolnienie |

Maski można łączyć sumą bitów, np. 3 = krótkie lub długie; 12 = wciśnięcie lub zwolnienie. Warunki różnych wejść są alternatywą (OR), nie wymogiem jednoczesnego wciśnięcia. Akcja TOGGLE przy masce 12 może przełączyć wyjście dwa razy. Czasy klasyfikowania naciśnięć ustawia KeyTime — [opis wejść](wejscia-komendy.md).

## Ustawienie i odczyt części lokalnej

```text
AT+Rule=ID,NR,EN,E1,...,E8,A1,P1,...,A4,P4,SUMA<CR>
AT+GetRule=ID,NR,SUMA<CR>
Rule=ID,NR,EN,E1,...,E8,A1,P1,...,A4,P4,SUMA
```

ID: 1–35; NR: 1–16; EN: 0 = wyłączona, 1 = włączona; E: 0–15. SUMA jest sumą wszystkich wcześniejszych liczb w danej ramce. GetRule zwraca aktualną konfigurację z RAM, w tym EN. Nie odczytuje oddzielnie EEPROM. Rule nadpisuje maski i akcje lokalne, zachowując sloty zdalne.

Każda roleta ma parę A,P. A: **0** bez akcji, **1** otwórz, **2** zamknij, **3** stop, **4** STEP w górę, **5** STEP w dół, **6** STEP naprzemienny, **7** pozycja procentowa. P: 0–100 i może być niezerowe tylko dla A=7; 0% oznacza zamknięcie, 100% otwarcie. Ruch wymaga odpowiedniej konfiguracji czasów RolTime; pozycjonowanie zależy również od znajomości pozycji. Szczegóły STEP i ograniczeń: [pełna obsługa rolet](rolety-komendy.md).

Przykład: krótkie naciśnięcie wejścia 1 uruchamia STEP rolety 1:

```text
TX: AT+Rule=1,1,1,1,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,10<CR>
RX: RuleOK=1
TX: AT+GetRule=1,1,2<CR>
RX: Rule=1,1,1,1,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,10
```

Aby wyłączyć regułę, wyślij jej pełną ramkę Rule z EN=0 i przelicz SUMA. Nie ma osobnego RuleEnable ani RuleDisable. Wyłączenie reguły nie jest poleceniem wyłączenia przekaźników ani zatrzymania rolety.

## Akcje zdalne: RuleRemote i GetRuleRemote

```text
AT+RuleRemote=ID,NR,SLOT,CEL,TYP,DANE...,SUMA<CR>
AT+GetRuleRemote=ID,NR,SLOT,SUMA<CR>
RuleRemote=ID,NR,SLOT,CEL,TYP,DANE...,SUMA
```

ID to moduł przechowujący regułę, CEL to adres odbiorcy akcji (1–35, inny niż ID), SLOT to 1–4. Typ opisuje format akcji odbiorcy, nie numer modelu z Discovery.

| TYP | DANE | Znaczenie |
|---|---|---|
| 0 | brak | kasowanie slotu; CEL musi być 0 |
| 1 | A1,P1,...,A4,P4 | 4 rolety S0804; kody A/P jak wyżej w dokumentacji rolet |
| 2 | O1,...,O6 | 6 przekaźników R0806T lub ETH0606T; akcje 0/1/2/3 |
| 3 | O1,...,O8 | 8 przekaźników R0808; akcje 0/1/2/3 |
| 4 | AKCJA,PROCENT,RAMPA | zdalny PWM R0806T; akcje 0–4, procent 0–100, rampa 0–50 × 0,1 s |

Typ 1 używa akcji rolet 0–7; procent może być niezerowy tylko przy akcji 7. Dla PWM: 0 bez akcji, 1 włącz ostatni niezerowy poziom, 2 wyłącz, 3 przełącz, 4 ustaw procent. Procent inny niż 0 jest dozwolony wyłącznie dla akcji 4. Ten sam CEL może wystąpić w dwóch slotach, gdy jeden jest PWM, a drugi dotyczy przekaźników/rolet. Powtórzenia w tej samej kategorii są odrzucane.

**Zmiana lub usunięcie RuleRemote wyłącza regułę (EN=0).** Najpierw ustaw sloty, następnie włącz regułę pełną komendą Rule. Przykład: slot 1 reguły modułu 1 ma włączać pierwszy przekaźnik modułu 2:

```text
TX: AT+RuleRemote=1,1,1,2,2,1,0,0,0,0,0,8<CR>
RX: RuleOK=1
TX: AT+GetRuleRemote=1,1,1,3<CR>
RX: RuleRemote=1,1,1,2,2,1,0,0,0,0,0,8
```

Po tym przykładzie wyślij ponownie Rule z EN=1. Sloty zdalne nie uruchamiają reguły odbiorcy: wykonawca wysyła do niego SetOut, RolAct lub PWM. Potwierdzenie konfiguracji nie dowodzi odebrania ani wykonania przyszłej akcji przez odbiorcę.

Kasowanie i odczyt pustego slotu:

```text
TX: AT+RuleRemote=1,1,1,0,0,3<CR>
RX: RuleOK=1
TX: AT+GetRuleRemote=1,1,1,3<CR>
RX: RuleRemote=1,1,1,0,0,3
```

SLOT=0, CEL=0, TYP=0 kasuje wszystkie cztery sloty tej reguły: `AT+RuleRemote=1,1,0,0,0,2<CR>`. GetRuleRemote wymaga slotu 1–4; aby odczytać wszystkie, wykonaj cztery zapytania.

## Zapis, odpowiedzi i odczyt stanu

1. Skonfiguruj potrzebne czasy wejść oraz czasy rolet.
2. Ustaw sloty RuleRemote.
3. Wyślij Rule z EN=1; odczytaj GetRule i zajęte GetRuleRemote.
4. Zapisz konfigurację: `AT+SaveConfig=1,1<CR>`; oczekuj `SaveOK=1` albo `SaveERROR=1`.

Zmiany reguł są robocze w RAM; sam RuleOK nie oznacza trwałego zapisu EEPROM. Konfiguracja reguł podczas pracy wykonawcy może zostać odrzucona. RuleOK=ID oznacza przyjęcie komendy, RuleERROR=ID to ogólny błąd składni, zakresu, sumy lub stanu; odpowiedź nie zawiera numeru reguły ani kodu przyczyny. Defaults jest szerokim resetem konfiguracji, nie komendą usunięcia jednej reguły.

**Co można odpytać:** GetRule zwraca konfigurację i EN; GetRuleRemote — sloty. Stan urządzenia odczytasz przez `AT+StanRol=1<CR>` oraz, `AT+GetRolState=1,1,2<CR>`. Czasy: `AT+GetRolTime=1,1,2<CR>`. Wejścia: GetInputs i GetKeyTime — [opis](wejscia-komendy.md).

**Czego nie można odpytać:** brak komendy RuleStatus/GetRuleStatus zwracającej aktywnie wykonywaną regułę, kolejkę, licznik uruchomień, ostatni błąd lub potwierdzenie zdalnych akcji. EN=1 oznacza uzbrojenie reguły, nie jej wykonywanie.

## Wykonanie i transmisja

Akcje lokalne wykonywane są po jednej na obieg pętli, niezależnie od UART i oczekujących transmisji wcześniejszej reguły. Wejścia mają osobną obsługę lokalną i kolejkę raportów. Akcje zdalne czekają na miejsce w UART. [Bufory i ograniczenia](reguly-uart-zmiany.md).

Wszystkie modele przekazują obce Rule, GetRule, RuleRemote, GetRuleRemote, RulePWM i GetRulePWM bez interpretacji układu akcji innego modelu. [Porównanie](reguly-porownanie.md).
