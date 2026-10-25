# RULE — porównanie modułów

Dokumentacja bieżącego oprogramowania w wersji **20**. Kolejne wersje oprogramowania otrzymują numery 21, 22 itd.

Osobne instrukcje: [R0806T](reguly-R0806T.md), [R0808](reguly-R0808.md), [ETH0606T](reguly-ETH0606T.md), [S0804](reguly-S0804.md).

## Wspólny model

Każdy moduł ma 16 reguł, EN=0/1, maski zdarzeń 1/2/4/8 i cztery sloty zdalne. Reguły uruchamiają zdarzenia własnych wejść. Nazwy komend są wspólne: Rule, GetRule, RuleRemote i GetRuleRemote. SUMA jest sumą wcześniejszych liczb. RuleRemote wyłącza regułę; po konfiguracji slotów trzeba wysłać pełne Rule z EN=1, a następnie SaveConfig.

| Cecha | R0806T | R0808 | ETH0606T | S0804 |
|---|---|---|---|---|
| Wejścia w Rule | 8 | 8 | 6 | 8 |
| Akcje lokalne w Rule | 6 przekaźników | 8 przekaźników | 6 przekaźników | 4 pary akcja/procent |
| Liczba pól z SUMA | 18 | 20 | 16 | 20 |
| Lokalny PWM | RulePWM / GetRulePWM | brak | brak | brak |
| Zdalny PWM w RuleRemote | typ 4 | typ 4 | typ 4 | typ 4 |
| Powtórzenie CEL w slotach | zabronione | zabronione | zabronione | dozwolona para PWM + inna kategoria |

Typy RuleRemote: 0 kasowanie, 1 cztery rolety, 2 sześć przekaźników, 3 osiem przekaźników, 4 PWM. Dla typu 4 dane to AKCJA,PROCENT,RAMPA. Akcje: 0 bez działania, 1 włącz ostatni poziom odbiorcy, 2 wyłącz, 3 przełącz, 4 ustaw procent. Niezerowy procent jest dozwolony wyłącznie dla akcji 4. Rampa 0–50 oznacza 0–5 s.

R0806T może jednocześnie sterować lokalnym PWM przez RulePWM i zdalnym PWM przez RuleRemote. [Przykład i trwałość konfiguracji](R0806T.md#zdalny-pwm-przez-ruleremote).

Różnice liczby wejść i wyjść wynikają ze sprzętu. R0808 i S0804 mają po 20 pól, lecz inne znaczenie ostatnich ośmiu wartości. Konfigurator musi znać model odbiorcy.

## Odczyt konfiguracji i stanu

| Pytanie | Komenda |
|---|---|
| Konfiguracja i EN reguły | wszystkie: AT+GetRule=ID,NR,SUMA |
| Konfiguracja slotu, w tym PWM typu 4 | wszystkie: AT+GetRuleRemote=ID,NR,SLOT,SUMA |
| Lokalna akcja PWM reguły | R0806T: AT+GetRulePWM=ID,NR,SUMA |
| Bieżące przekaźniki | R0806T, R0808, ETH: AT+GetOut=ID |
| Bieżący PWM | R0806T: AT+GetPWM=ID |
| Ruch rolet | S0804: AT+StanRol=ID |
| Pozycja, jej ważność, cel i czas ruchu | S0804: AT+GetRolState=ID,NR,SUMA |
| Wejścia i progi przycisków | GetInputs i GetKeyTime |

GetRule zwraca konfigurację RAM; EN=1 oznacza włączenie reguły, a nie jej bieżące wykonywanie. Żaden moduł nie ma GetRuleStatus, licznika wykonań reguły ani zbiorczego potwierdzenia wykonania sceny zdalnej. RuleOK/RuleERROR zawiera ID, bez numeru reguły i szczegółowego kodu błędu.

## Przekazywanie i wykonanie

Wszystkie modele przekazują komendy Rule, GetRule, RuleRemote, GetRuleRemote, RulePWM i GetRulePWM adresowane do innego ID. Pośrednik sprawdza składnię liczbową, zakres ID, limit 20 pól i sumę; układ wejść i akcji sprawdza odbiorca. R/S przekazuje ramkę drugim portem linii. ETH zachowuje odrębne zasady USB/RS-232 i bramki TCP.

Lokalne akcje nie czekają na UART ani na wysłanie zdalnej części wcześniejszej reguły. Zdalne akcje oczekują na dostępne miejsce. Kolejka raportów wejść jest oddzielona od lokalnego sterowania. [Dokładny opis buforów i ograniczeń](reguly-uart-zmiany.md).

Spójne są nazwy, maski, sumy, aktywacja i typy akcji zdalnych. Do dalszego ujednolicenia pozostają zasady powtarzania CEL w slotach oraz diagnostyka wykonania. Akcje wielu modułów nie stanowią jednej transakcji.
