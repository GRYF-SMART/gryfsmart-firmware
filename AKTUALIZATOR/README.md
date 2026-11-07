# 2. GRYFSMART-Programator

**[Pobierz najnowszą wersję 2.0.21](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.04-gryfexpert-0.5.38/GRYFSMART-Programator-2.0.21.exe)**

Obsługa ETH Mini GATE przez RS-232 i Ethernet, pobieranie HEX z GitHub. Czytelny log: błędy na czerwono, zakończenie weryfikacji na zielono. [Pełny opis wydania](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.04-gryfexpert-0.5.38).

## Trzy ostatnie wersje

| Wersja | Data publikacji | Pobieranie | Zmiany |
|---|---|---|---|
| **2.0.21** | 2026-11-04 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.04-gryfexpert-0.5.38/GRYFSMART-Programator-2.0.21.exe) | Obsługa ETH Mini GATE przez RS-232 i Ethernet, pobieranie HEX z GitHub. Czytelny log: błędy na czerwono, zakończenie weryfikacji na zielono. [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.04-gryfexpert-0.5.38) |
| **2.0.14** | 2026-10-29 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.10.29-restarts-all-0.5.15/GRYFSMART-Programator.exe) | Wydanie narzędzi z obsługą pakietu modułów i bootloadera R0806T-OLD v13; aktualizacja przez USB/RS-232 oraz sieć CHAIN1. [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.10.29-restarts-all-0.5.15) |
| **2.0.13** | 2026-10-29 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.10.29-usb-fix-2.0.13/GRYFSMART-Programator.exe) | Poprawka wejścia ETH przez USB w bootloader: oddzielny CR i odstęp przed AT+BOOT zapobiegają utracie komendy. [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.10.29-usb-fix-2.0.13) |

## Aktualizacja aplikacji modułu

**GRYFSMART-Programator** służy do wgrywania najnowszej wersji oprogramowania do pamięci Flash modułów. Program automatycznie pobiera najnowszy firmware z GitHuba lub pozwala ręcznie wybrać plik z komputera.

Przed rozpoczęciem aktualizacji wybierz **typ modułu**, a następnie **wsad oprogramowania (plik Flash/HEX)** przeznaczony dla wybranego modelu. Przy dostępie do internetu, po wybraniu źródła **GitHub — najnowszy HEX**, program automatycznie łączy się z repozytorium i pobiera najnowszy wsad dla tego modułu. Alternatywnie wybierz **Plik z komputera** i wskaż wsad ręcznie.

Jeżeli w module znajduje się tylko bootloader, bez aplikacji, program rozpoznaje bootloader i nie pokazuje wersji firmware aplikacji, ponieważ nie jest ona wgrana. Można wtedy wgrać wsad pobrany z GitHuba lub wybrany z komputera.

1. Pobierz program z linku na górze. Wybierz dokładny model: R0806T, R0808, S0804, ETH0606T lub ETH Mini GATE.
2. Wybierz źródło **GitHub — najnowszy HEX** albo **Plik z komputera**. [Ręczne pobieranie HEX](../HEX).
3. Wybierz port COM dla RS-232/USB. Parametry aktualizacji: 115200, 8N1. Zamknij inne aplikacje zajmujące port.
4. Kliknij **Sprawdź bootloader**. Dopiero po zgodnym rozpoznaniu modelu wybierz **Wgraj aplikację** i zaczekaj na zakończenie weryfikacji.
5. Sprawdź wersję i działanie modułu po ponownym uruchomieniu.

![UWAGA: Podczas konfiguracji i wgrywania oprogramowania nie można odłączać zasilania. Należy zapewnić ciągłe zasilanie przez cały czas operacji.](../docs/assets/uwaga-zasilanie.svg)

### Ethernet i sieć modułów

Dla ETH0606T użyj **ETH przez Ethernet (v12)**. Port aplikacji i port bootloadera to różne usługi: programowanie ETH korzysta z TCP 5001. W oknie **Sieć — do 35 modułów** dostępne są wykrywanie CHAIN1 i aktualizacja obsługiwanej linii; wybierz transport i sprawdź wykryte modele przed zapisem.

ETH Mini ma osobny wybór RS-232/Ethernet. Bootloader Mini używa `192.168.1.201:5001`; przez Ethernet uruchom go przyciskiem RESET. AUTO przez RS-232 jest obsługiwane od aplikacji Mini v2. Nie myl portu bootloadera 5001 z portem aplikacji Mini 5002.

Jeżeli bootloader nie jest zainstalowany, zacznij od [instrukcji ISP/USBasp](../BOOTLOADER). Wybór niewłaściwego modelu lub brak komunikacji wymaga wyjaśnienia przed zapisem.


[1. Aplikacja GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/GRYFSMART) · [2. GRYFSMART-Programator](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/AKTUALIZATOR) · [3. Driver Home Assistant](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/HOME-ASSISTANT) · [4. Driver RTI](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/RTI) · [5. Instalator Bootloader](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/BOOTLOADER) · [6. Protokół GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/PROTOKOL) · [7. System i moduły GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/SYSTEM)
