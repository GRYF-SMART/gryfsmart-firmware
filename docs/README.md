<p><img src="assets/logo.svg" alt="Logo GRYF" width="320"></p>

# Dokumentacja poleceń GRYFSMART

**Aktualna wersja oprogramowania wszystkich modułów: 20.** Kolejne aktualizacje są numerowane 21, 22, 23… Wersja oprogramowania jest niezależna od wersji narzędzi Windows i bootloadera.

[Sposób działania sieci, dwa porty linii, prędkość, limit 35 modułów i ramki ASCII](komendy-wspolne.md#zasady-komunikacji-i-struktura-sieci).

## Komendy wspólne

- [Sieć i stan — Loop, LoopReset, ResetStats, Discovery, ModuleInfo, Search, reset i bootloader](komendy-wspolne.md#sieć-i-stan)
- [Identyfikacja i adresowanie — szczegółowe formaty Search/Find, Discovery i Info](komendy-wspolne.md)
- [Wejścia — I, PS, PL, KeyTime, GetInputs, GetKeyTime, SaveConfig i Defaults](wejscia-komendy.md)
- [Wyjścia przekaźnikowe — SetOut, GetOut i raporty O=/o=](wyjscia-komendy.md)

## Moduły

| Moduł | Wersja oprogramowania | Główna instrukcja | Reguły |
|---|---|---|---|
| R0806T | 20 | [6 przekaźników, PWM, termostat, wejścia i ich odczyty](R0806T.md) | [RULE i zdalny PWM typu 4](reguly-R0806T.md) |
| R0808 | 20 | [8 przekaźników, wejścia i temperatura](R0808.md) | [RULE](reguly-R0808.md) |
| S0804 | 20 | [4 rolety, wejścia i ich odczyty](S0804.md) | [RULE rolet](reguly-S0804.md) |
| ETH0606T | 20 | [6 wejść i wyjść, USB/RS-232, Ethernet, 5 czujników](ETH0606T.md) | [RULE](reguly-ETH0606T.md) |

[S0804 — pełna instrukcja parametrów, sterowania, procentów i statusów rolet](rolety-komendy.md).

[Porównanie reguł wszystkich modułów](reguly-porownanie.md) · [Zdalny PWM w R0806T](R0806T.md#zdalny-pwm-przez-ruleremote) · [Lokalne sterowanie i bufory transmisji](reguly-uart-zmiany.md).

## Odpowiedzi i zapis

RuleOK=ID potwierdza przyjęcie komendy, a nie zakończenie ruchu rolety lub całej sceny. RuleERROR=ID oznacza błąd składni, zakresu, sumy albo stanu. SaveOK/SaveERROR informuje o zakończeniu zapisu EEPROM. Odpowiedzi mogą pojawiać się asynchronicznie — sprawdzaj prefiks i ID.

Zmiany konfiguracji utrwala SaveConfig. Defaults czyści konfigurację roboczą. W polu SUMA podaje się sumę wszystkich wcześniejszych liczb, np. KeyTime=1,1,5,20,27.
