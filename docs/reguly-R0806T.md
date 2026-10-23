# R0806T — reguły RULE

[Dokumentacja główna](README.md) · [Porównanie modułów i ograniczenia](reguly-porownanie.md)

Opis sprawdzony względem bieżących źródeł (0019). Dostępność we wcześniejszych wsadach wymaga sprawdzenia ich wersji. Przykłady zakładają ID modułu **1** i regułę **1**. Każda wysyłana linia kończy się CR; zapis `<CR>` oznacza ten znak, nie dosłowny tekst.

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
AT+Rule=ID,NR,EN,E1,...,E8,O1,...,O6,SUMA<CR>
AT+GetRule=ID,NR,SUMA<CR>
Rule=ID,NR,EN,E1,...,E8,O1,...,O6,SUMA
```

ID: 1–35; NR: 1–16; EN: 0 = wyłączona, 1 = włączona; E: 0–15. SUMA jest sumą wszystkich wcześniejszych liczb w danej ramce. GetRule zwraca aktualną konfigurację z RAM, w tym EN. Nie odczytuje oddzielnie EEPROM. Rule nadpisuje maski i akcje lokalne, zachowując sloty zdalne oraz konfigurację RulePWM.

Każde O jest akcją przekaźnika: **0** bez zmiany, **1** włącz, **2** wyłącz, **3** przełącz (TOGGLE). Są to kody akcji; odczyt stanu wyjścia używa wartości 0/1.

Przykład: krótkie naciśnięcie wejścia 1 przełącza przekaźnik 1:

```text
TX: AT+Rule=1,1,1,1,0,0,0,0,0,0,0,3,0,0,0,0,0,7<CR>
RX: RuleOK=1
TX: AT+GetRule=1,1,2<CR>
RX: Rule=1,1,1,1,0,0,0,0,0,0,0,3,0,0,0,0,0,7
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

R0806T nie obsługuje typu 4 we własnych slotach RuleRemote. Lokalny PWM konfiguruje RulePWM. Nie należy utożsamiać obsługi przekazywania obcych ramek typu 4 z obsługą takiej akcji przez własną regułę.

Typ 1 używa akcji rolet 0–7; procent może być niezerowy tylko przy akcji 7. Ten sam CEL nie może zajmować kilku slotów tej samej reguły, także przy różnych typach akcji.

**Zmiana lub usunięcie RuleRemote wyłącza regułę (EN=0).** Najpierw ustaw sloty, następnie włącz regułę pełną komendą Rule. Przykład: slot 1 reguły modułu 1 ma włączać pierwszy przekaźnik modułu 2:

```text
TX: AT+RuleRemote=1,1,1,2,2,1,0,0,0,0,0,8<CR>
RX: RuleOK=1
TX: AT+GetRuleRemote=1,1,1,3<CR>
RX: RuleRemote=1,1,1,2,2,1,0,0,0,0,0,8
```

Po tym przykładzie wyślij ponownie Rule z EN=1. Sloty zdalne nie uruchamiają reguły odbiorcy: wykonawca wysyła do niego SetOut, RolAct. Potwierdzenie konfiguracji nie dowodzi odebrania ani wykonania przyszłej akcji przez odbiorcę.

Kasowanie i odczyt pustego slotu:

```text
TX: AT+RuleRemote=1,1,1,0,0,3<CR>
RX: RuleOK=1
TX: AT+GetRuleRemote=1,1,1,3<CR>
RX: RuleRemote=1,1,1,0,0,3
```

SLOT=0, CEL=0, TYP=0 kasuje wszystkie cztery sloty tej reguły: `AT+RuleRemote=1,1,0,0,0,2<CR>`. GetRuleRemote wymaga slotu 1–4; aby odczytać wszystkie, wykonaj cztery zapytania.

## Lokalny PWM: RulePWM i GetRulePWM

```text
AT+RulePWM=ID,NR,AKCJA,PROCENT[,RAMPA],SUMA<CR>
AT+GetRulePWM=ID,NR,SUMA<CR>
RulePWM=ID,NR,AKCJA,PROCENT,RAMPA,SUMA
```

AKCJA: 0 bez zmiany, 1 włącz ostatni niezerowy poziom, 2 wyłącz, 3 przełącz, 4 ustaw procent. PROCENT: 0–100, niezerowy tylko dla akcji 4. RAMPA: 0–50 w jednostkach 0,1 s (maksymalnie 5 s); pominięcie ustawia 0. Odczyt zawsze zawiera rampę. Zmiana RulePWM wyłącza regułę, dlatego Rule z EN=1 wysyłaj na końcu.

```text
TX: AT+RulePWM=1,1,4,50,10,66<CR>
RX: RuleOK=1
TX: AT+GetRulePWM=1,1,2<CR>
RX: RulePWM=1,1,4,50,10,66
```

Po włączeniu reguły i wystąpieniu jej zdarzenia PWM przejdzie do 50% w 1 s. Zakończenie działania kolejki reguły nie oznacza zakończenia rampy. RulePWM z akcją 0 i procentem 0 usuwa akcję PWM; samo wyzerowanie przekaźników w Rule jej nie usuwa.

## Zapis, odpowiedzi i odczyt stanu

1. Skonfiguruj potrzebne czasy wejść.
2. Ustaw sloty RuleRemote i lokalny RulePWM.
3. Wyślij Rule z EN=1; odczytaj GetRule i zajęte GetRuleRemote oraz GetRulePWM.
4. Zapisz konfigurację: `AT+SaveConfig=1,1<CR>`; oczekuj `SaveOK=1` albo `SaveERROR=1`.

Zmiany reguł są robocze w RAM; sam RuleOK nie oznacza trwałego zapisu EEPROM. Konfiguracja reguł podczas pracy wykonawcy może zostać odrzucona. RuleOK=ID oznacza przyjęcie komendy, RuleERROR=ID to ogólny błąd składni, zakresu, sumy lub stanu; odpowiedź nie zawiera numeru reguły ani kodu przyczyny. Defaults jest szerokim resetem konfiguracji, nie komendą usunięcia jednej reguły.

**Co można odpytać:** GetRule zwraca konfigurację i EN; GetRuleRemote — sloty; GetRulePWM — lokalną akcję PWM. Stan wyjść odczytasz przez `AT+GetOut=1<CR>` — [format odpowiedzi i wersje](wyjscia-komendy.md). Bieżący PWM: `AT+GetPWM=1<CR>`. Wejścia: GetInputs i GetKeyTime — [opis i wymagane wersje](wejscia-komendy.md).

**Czego nie można odpytać:** brak komendy RuleStatus/GetRuleStatus zwracającej aktywnie wykonywaną regułę, kolejkę, licznik uruchomień, ostatni błąd lub potwierdzenie zdalnych akcji. EN=1 oznacza uzbrojenie reguły, nie jej wykonywanie.

## Ograniczenia wykonania

Akcje wykonywane są etapami, po jednej na obieg pętli, a nie atomowo. Oczekujące uruchomienia przechowuje maska bitowa: powtarzające się wyzwolenia już oczekującej reguły mogą się scalić. Na początku wykonawca sprawdza dostępność UART; niedostępna kolejka może opóźnić także akcje lokalne, mimo że główna pętla nadal pracuje. Watchdog samej pętli tego nie wykryje. Nie ma gwarancji czasu reakcji ani potwierdzenia zakończenia całej sceny przez wszystkie urządzenia.

Przed użyciem przez mieszaną linię sprawdź [ograniczenia przekazywania RULE](reguly-porownanie.md); obsługa komendy na docelowym module nie gwarantuje, że każdy pośrednik przepuści jej format.

