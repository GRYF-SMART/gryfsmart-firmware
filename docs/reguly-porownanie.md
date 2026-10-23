# RULE — porównanie i ocena spójności modułów

[Dokumentacja główna](README.md)

Osobne instrukcje: [R0806T](reguly-R0806T.md), [R0808](reguly-R0808.md), [ETH0606T](reguly-ETH0606T.md), [S0804](reguly-S0804.md).

Analiza bieżących źródeł: R0806T 0019, R0808 0012, ETH0606T 0009, S0804 0732. To opis implementacji i jej ograniczeń, nie deklaracja publikacji nowych wsadów.

## Co jest wspólne

Wszystkie moduły mają 16 reguł, EN=0/1, maski zdarzeń 1/2/4/8, cztery sloty zdalne, sumę kontrolną będącą sumą pól liczbowych oraz nazwy Rule, GetRule, RuleRemote, GetRuleRemote. Reguły uruchamiają zdarzenia własnych wejść. Kilka wejść tworzy alternatywę; to mechanizm zdarzeń i akcji, nie język dowolnych warunków logicznych.

We wszystkich zmiana RuleRemote ustawia EN=0. Zdalne akcje konfiguruj najpierw, a pełne Rule z EN=1 wysyłaj na końcu. Konfigurację utrwala SaveConfig. Odpowiedzi RuleOK/RuleERROR mają ID modułu, bez numeru reguły i szczegółowego kodu błędu.

## Różnice formatów

| Cecha | R0806T | R0808 | ETH0606T | S0804 |
|---|---|---|---|---|
| Lokalne wejścia w Rule | 8 | 8 | 6 | 8 |
| Lokalne akcje w Rule | 6 przekaźników | 8 przekaźników | 6 przekaźników | 4 pary akcja/procent |
| Liczba pól liczbowych z SUMA | 18 | 20 | 16 | 20 |
| Akcja przekaźnika | 0 zachowaj, 1 ON, 2 OFF, 3 TOGGLE | tak samo | tak samo | zdalnie |
| Lokalny PWM | RulePWM / GetRulePWM | brak | brak | brak |
| Zdalny PWM w RuleRemote | brak | typ 4 | typ 4 | typ 4 |
| Duplikat CEL w slotach | zabroniony | zabroniony | zabroniony | dozwolone PWM + jedna akcja innej kategorii |

ETH ma podobne sterowanie sześcioma przekaźnikami do R0806T, ale inną liczbę wejść i długość Rule. **R0808 i S0804 mają po 20 pól, jednak odmienne znaczenie ostatnich ośmiu wartości.** Program konfigurujący musi znać model odbiorcy; sama długość ramki nie identyfikuje schematu.

Wspólne typy RuleRemote: 0 kasowanie, 1 cztery rolety, 2 sześć przekaźników, 3 osiem przekaźników. Typ 4 to PWM (obsługiwany jako akcja reguły w R0808, ETH i S0804). R0806T ma zamiast niego osobną lokalną część RulePWM. Nie każdy model potrafi więc utworzyć identyczną scenę zdalną.

## Czy w każdym module można odpytać o stan?

| Pytanie | Dostępność / komenda |
|---|---|
| Jak skonfigurowano regułę i czy jest włączona? | wszystkie: AT+GetRule=ID,NR,SUMA |
| Jak skonfigurowano slot zdalny? | wszystkie: AT+GetRuleRemote=ID,NR,SLOT,SUMA |
| Jaka jest akcja PWM reguły? | lokalnie R0806T: AT+GetRulePWM=ID,NR,SUMA |
| Jaki jest stan przekaźników? | R0806T, R0808, ETH: AT+GetOut=ID |
| Jaki jest bieżący PWM? | R0806T: AT+GetPWM=ID |
| Czy rolety jadą? | S0804: AT+StanRol=ID |
| Jaka jest pozycja, jej ważność, cel i czas ruchu? | S0804 od 0732: AT+GetRolState=ID,NR,SUMA |
| Jakie są wejścia i progi naciśnięcia? | GetInputs / GetKeyTime; wersje w instrukcji wejść |
| Która reguła jest właśnie wykonywana, ile razy zadziałała, jaki miała błąd? | brak takiej komendy we wszystkich czterech modułach |
| Czy wszystkie zdalne akcje sceny zostały wykonane? | brak zbiorczego statusu lub potwierdzenia wykonania sceny |

Przykłady: GetRule=1,1,2; GetRuleRemote=1,1,1,3. GetRule zwraca RAM i EN, nie osobną kopię EEPROM. EN=1 oznacza uzbrojenie, a nie trwające wykonanie. Szczegółowe odpowiedzi dla urządzeń opisują [wyjścia](wyjscia-komendy.md) i [rolety](rolety-komendy.md). Wielkość O=/o= oraz zakończenia linii raportów przekaźników również nie są jednakowe.

## Przekazywanie przez różne modele

Weryfikacja formatów odbywa się także w modułach pośrednich, przed przekazaniem. Zatem lokalna poprawność komendy nie gwarantuje przejścia całej linii.

| Pośrednik | Akceptacja obcej ramki AT+Rule |
|---|---|
| R0806T | wariant 18 pól oraz 20 pól po walidacji akcji; brak wariantu ETH z 16 polami |
| R0808 | wariant 18 pól oraz 20 pól po walidacji akcji; brak wariantu ETH z 16 polami |
| S0804 | 20 pól, jako akcje rolet albo 8 przekaźników; odrzuca 18 pól R0806T i 16 pól ETH |
| ETH0606T | lokalny parser waliduje wariant 16 pól i konsumuje obce zwykłe ramki RULE; to nie jest uniwersalny pośrednik UART |

ETH ma osobną ścieżkę bramki TCP/RS-232; nie należy przenosić na nią założeń o symetrycznym przekazywaniu łańcucha R/S. Działającą trasę należy sprawdzić dla konkretnego interfejsu.

Dodatkowo S0804 nie rozpoznaje AT+RulePWM ani AT+GetRulePWM jako poleceń przekazywanych. Nie można zakładać, że za nim skonfigurujemy i odczytamy regułę PWM R0806T. GetRule/GetRuleRemote mają bardziej wspólny format żądania niż Rule, ale ich odpowiedzi i ścieżki przekazywania również trzeba zweryfikować dla użytej trasy. Nowa przezroczystość poleceń odczytu rolet nie oznacza automatycznie przezroczystości wszystkich poleceń reguł.

## Ocena i kolejność usprawnień

**Wspólny model reguł jest sensowny, lecz protokół nie jest jeszcze w pełni spójny.** Różne liczby przekaźników i akcje rolet są uzasadnione sprzętem. Nieuzasadnione praktycznie są blokowanie obcego poprawnego formatu przez pośrednika, różne zasady duplikowania celów i brak jednolitej diagnostyki wykonania.

1. **Oddzielić lokalne wykonanie od wolnego UART.** Obecnie wykonawca wszystkich czterech modeli rozpoczyna od sprawdzenia uart_tx_ready(1), także przed lokalnymi akcjami. Zator transmisji może opóźniać lokalną reakcję mimo działającej pętli i odświeżanego watchdog.
2. **Ujednolicić przekazywanie ramek adresowanych do innych urządzeń.** Pośrednik powinien sprawdzać ramkę transportową i adres, a walidację modelowych akcji pozostawiać odbiorcy. Trzeba zachować limity bufora i ochronę przed błędnymi ramkami.
3. **Dodać odczyt możliwości modułu** (liczba wejść, wyjść, slotów, obsługiwane akcje, wersja schematu) i jednolite reguły walidacji. S0804 powinien dzielić nagłówek, maski, zapis i diagnostykę z pozostałymi, zachowując akcje rolet.
4. **Dodać diagnostykę wykonania reguły**: stan oczekuje/wykonuje, licznik uruchomień, ostatni błąd, informacja o scalonych/utraconych zdarzeniach. Nazwa GetRuleStatus byłaby propozycją nowej komendy — obecnie nie istnieje.
5. **Ujednolicić odpowiedzi i aktywację**, np. osobne włączenie reguły po konfiguracji, numer reguły i kod błędu w odpowiedzi. Zmiany protokołu należy wprowadzać wersjonowane, zachowując zgodność obecnych konfiguratorów.

Akcje wykonują się kolejno, po jednej na obieg pętli. Maska oczekujących reguł scala ponowne wyzwolenia już oczekującej reguły; nie jest kolejką każdego naciśnięcia. Reguła nie stanowi transakcji obejmującej wiele modułów. Do automatyki wymagającej potwierdzenia skutku potrzebne są odczyty stanu odbiorców i obsługa przekroczenia czasu.

Ta aktualizacja dodaje dokumentację i ocenę. Powyższe propozycje nie zmieniają firmware.

