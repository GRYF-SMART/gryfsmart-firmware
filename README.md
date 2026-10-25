<p><img src="docs/assets/logo.svg" alt="Logo GRYF" width="320"></p>

# GRYFSMART — oprogramowanie i narzędzia serwisowe

**Bieżąca wersja oprogramowania wszystkich modułów: 21.** Kolejne wersje oprogramowania to 22, 23, 24… Wersje narzędzi Windows i bootloadera są niezależne od wersji oprogramowania modułu.

## Dokumentacja poleceń GRYFSMART

- [Wszystkie instrukcje](docs/README.md)
- [PRZYKLADY — konfiguracja i sterowanie linią pięciu modułów](docs/PRZYKLADY.md)
- [Komendy wspólne: sieć, stan, diagnostyka pętli, identyfikacja i adresowanie](docs/komendy-wspolne.md)
- [R0806T — przekaźniki, lokalny i zdalny PWM, termostat oraz odczyty wejść](docs/R0806T.md)
- [R0808 — przekaźniki, wejścia i temperatura](docs/R0808.md)
- [S0804 — rolety oraz odczyty wejść i progów](docs/S0804.md)
- [ETH0606T — USB/RS-232, Ethernet, wejścia, wyjścia i temperatura](docs/ETH0606T.md)
- [RULE — osobne opisy i porównanie modułów](docs/reguly-porownanie.md)
- [Wejścia — I, PS, PL, KeyTime i odczyty GET](docs/wejscia-komendy.md)
- [Wyjścia — SetOut, GetOut i raporty stanu](docs/wyjscia-komendy.md)
- [Rolety — parametry, sterowanie i statusy](docs/rolety-komendy.md)

R0806T obsługuje RuleRemote typu 4, czyli sterowanie PWM innego modułu. [Format i przykład](docs/R0806T.md#zdalny-pwm-przez-ruleremote).

## Narzędzia i pobieranie

- [Aktualne HEX-y wszystkich modułów — wersja 21](firmware-21/README.md)

- [Opublikowane wydanie i pliki do pobrania](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest)
- [Programator aplikacji](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/GRYFSMART-Programator.zip)
- [Instalator bootloadera przez USBasp](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/GRYFSMART-Instalator.zip)
- [Pełna paczka narzędzi](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/GRYFSMART-Tools.zip)
- [Manifest opublikowanych plików i SHA-256](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/gryfsmart-update.json)

Przed wgrywaniem sprawdź model, wersję oprogramowania i SHA-256 w manifeście konkretnego wydania. Dokumentacja i paczka aplikacji firmware-21 opisują oprogramowanie w wersji 21. Narzędzia Windows i bootloadery mają oddzielne wydania.

| Moduł | Wersja oprogramowania | MCU / zegar | Port serwisowy |
|---|---|---|---|
| R0806T | 21 | ATmega1284P / 18,432 MHz | port logiczny 0 = USART0 |
| R0808 | 21 | ATmega2560 / 18,432 MHz | port logiczny 0 = USART3 |
| S0804 | 21 | ATmega1284P / 18,432 MHz | port logiczny 0 = USART0 |
| ETH0606T | 21 | ATmega2560 / 16 MHz | USB USART0, RS-232 USART1 |

Pierwsza instalacja bootloadera wymaga ISP/USBasp. Późniejsze aktualizacje aplikacji przez RS-232/USB wymagają już zainstalowanego bootloadera. Bootloader zajmuje ostatnie 8 KiB Flash.

[Sposób działania sieci i parametry komunikacji](docs/komendy-wspolne.md#zasady-komunikacji-i-struktura-sieci).

[Wspólna instrukcja sieci, stanu, identyfikacji, resetu i wejścia do bootloadera](docs/komendy-wspolne.md#sieć-i-stan).
