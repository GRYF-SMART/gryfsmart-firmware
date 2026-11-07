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
