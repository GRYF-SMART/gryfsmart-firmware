<p><img src="assets/logo.svg" alt="Logo GRYF" width="320"></p>

# Dokumentacja poleceń GRYFSMART

**Aktualny komplet:** ETH0606T 25, R0808 25, R0806T 27, S0804 27, R0806T-OLD 4. GRYFEXPERT 0.5.16, narzędzia Windows 2.0.13. Numery wersji są niezależne dla modeli.

[Sposób działania sieci, dwa porty linii, prędkość, limit 35 modułów i ramki ASCII](komendy-wspolne.md#zasady-komunikacji-i-struktura-sieci).

## Przykłady konfiguracji i sterowania

[PRZYKLADY — pięć modułów: R0808, R0806T, R0806T, S0804, S0804](PRZYKLADY.md). Jedenaście przykładów: adresowanie, informacje, progi wejść, reguły, rolety, sterowanie z terminala, raporty do RTI/Home Assistant/PC oraz odczyty wejść, wyjść, PWM i szczegółowego stanu rolet. Każdy z komendami i odpowiedziami.

## Komendy wspólne

- [Sieć i stan — Loop, LoopReset, ResetStats, Discovery, ModuleInfo, Search, reset i bootloader](komendy-wspolne.md#sieć-i-stan)
- [Identyfikacja i adresowanie — szczegółowe formaty Search/Find, Discovery i Info](komendy-wspolne.md)
- [Wejścia — I, PS, PL, KeyTime, GetInputs, GetKeyTime, SaveConfig i Defaults](wejscia-komendy.md)
- [Wyjścia przekaźnikowe — SetOut, GetOut i raporty O=/o=](wyjscia-komendy.md)

## Moduły

| Moduł | Wersja oprogramowania | Główna instrukcja | Reguły |
|---|---|---|---|
| R0806T | 28 | [6 przekaźników, PWM, termostat, wejścia i ich odczyty](R0806T.md) | [RULE i zdalny PWM typu 4](reguly-R0806T.md) |
| R0808 | 28 | [8 przekaźników, wejścia i temperatura](R0808.md) | [RULE](reguly-R0808.md) |
| S0804 | 29 | [4 rolety, wejścia i ich odczyty](S0804.md) | [RULE rolet](reguly-S0804.md) |
| ETH0606T | 26 | [6 wejść i wyjść, USB/RS-232, Ethernet, 5 czujników](ETH0606T.md) | [RULE](reguly-ETH0606T.md) |

[S0804 — pełna instrukcja parametrów, sterowania, procentów i statusów rolet](rolety-komendy.md).

[Porównanie reguł wszystkich modułów](reguly-porownanie.md) · [Zdalny PWM w R0806T](R0806T.md#zdalny-pwm-przez-ruleremote) · [Lokalne sterowanie i bufory transmisji](reguly-uart-zmiany.md).

## Odpowiedzi i zapis

RuleOK=ID potwierdza przyjęcie komendy, a nie zakończenie ruchu rolety lub całej sceny. RuleERROR=ID oznacza błąd składni, zakresu, sumy albo stanu. SaveOK/SaveERROR informuje o zakończeniu zapisu EEPROM. Odpowiedzi mogą pojawiać się asynchronicznie — sprawdzaj prefiks i ID.

Zmiany konfiguracji utrwala SaveConfig. Defaults czyści konfigurację roboczą. W polu SUMA podaje się sumę wszystkich wcześniejszych liczb, np. KeyTime=1,1,5,20,27.

[R0806T-OLD — opis i porównanie z aktualnym R0806T](R0806T-OLD.md).

[ETH: Ethernet firmware 25 i bootloader v12](ETH-Ethernet-aktualizacja.md).
