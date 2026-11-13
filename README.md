# GRYFSMART — pobieranie i dokumentacja

| Program / integracja | Najnowsza wersja — pobierz | Instrukcja |
|---|---|---|
| 1. Aplikacja GRYFSMART | [**0.5.59 — pobierz**](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.13-shutter-step/GRYFEXPERT-0.5.59-win-x64.zip) | [Otwórz](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/GRYFSMART) |
| 2. GRYFSMART-Programator | [**2.0.25 — pobierz**](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.13-s0804-compatible/GRYFSMART-Programator.exe) | [Otwórz](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/AKTUALIZATOR) |
| 3. Driver Home Assistant | [**0.3.15 — pobierz**](https://github.com/GRYF-SMART/ha-gryfsmart/releases/download/v0.3.15/GRYFSMART-HomeAssistant-0.3.15.zip) | [Otwórz](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/HOME-ASSISTANT) |
| 4. Driver RTI | [**2.16 — pobierz**](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.13-gryfexpert-0.5.60-rti-2.16/GRYF.rtidriver) | [Otwórz](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/RTI) |
| 5. Instalator Bootloader | [**2.0.25 — pobierz**](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.13-s0804-compatible/GRYFSMART-Instalator.zip) | [Otwórz](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/BOOTLOADER) |
| 6. Protokół GRYFSMART | [**Opis i przykłady**](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/PROTOKOL) | [Komendy i konfiguracja](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/PROTOKOL) |
| 7. System i moduły GRYFSMART | [**Opis systemu i tabela modułów**](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/SYSTEM) | [Peryferia i połączenia](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/SYSTEM) |

## 1. Aplikacja GRYFSMART

Program do konfiguracji sieci sterowników GRYFSMART. Pozwala tworzyć zależności przyczynowo-skutkowe między różnymi modułami oraz nadawać nazwy wejściom, wyjściom i flagom. Nazwy można następnie przenieść do integracji Home Assistant lub drivera RTI. System może pracować samodzielnie, bez Home Assistant i RTI.

## 2. GRYFSMART-Programator

Program służy do wgrywania najnowszego oprogramowania do pamięci Flash modułów. Jeżeli w sieci znajduje się moduł ETH, aktualizację można wykonać przez Ethernet. Bez modułu ETH połączenie odbywa się przez PORT 0 RS-232. Aktualizacja może obejmować moduły połączone w sieć, z zainstalowanymi zgodnymi bootloaderami.

## 3. Driver Home Assistant

Integracja pozwala połączyć system GRYFSMART z Home Assistant. W tej sekcji znajdują się driver oraz instrukcja jego instalacji i obsługi.

## 4. Driver RTI

Driver pozwala zintegrować system GRYFSMART z systemem RTI. W tej sekcji znajdują się plik drivera, opis jego funkcji oraz instrukcja instalacji i konfiguracji.

## 5. Instalator Bootloader

Instalator służy do wgrania bootloadera do modułów przez programator ISP/USBasp. Bootloader umożliwia późniejsze wgrywanie oprogramowania przez PORT 0 RS-232 lub Ethernet, zależnie od modułu i połączenia. Wgrywa się go tylko raz; ponowna instalacja jest potrzebna przy aktualizacji samego bootloadera. Nowe moduły mają już zainstalowany bootloader.

## 6. Protokół GRYFSMART

Dokładny opis protokołu komunikacyjnego GRYFSMART: parametry połączenia, komendy sterujące, odczyty stanów modułów oraz przykłady integracji i konfiguracji.

## 7. System i moduły GRYFSMART

W tej sekcji znajduje się opis systemu GRYFSMART oraz wszystkich sterowników wraz ze zdjęciami, parametrami technicznymi, opisem peryferiów i sposobem podłączenia. Tabela modułów prowadzi do szczegółowych informacji o każdym sterowniku.
