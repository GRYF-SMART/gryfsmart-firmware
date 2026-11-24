# 2. GRYFSMART-Programator

**[Pobierz najnowszą wersję 2.0.30](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.24-s0804-old-1/GRYFSMART-Programator.exe)**

Nowy moduł GRYF S0804 OLD: ATmega644PA, kwarc 11,0592 MHz. Firmware 1: lokalnie tylko OTWÓRZ, STOP, ZAMKNIJ, ZAMKNIJ/STOP i OTWÓRZ/STOP. 16 reguł; jedna zdalna akcja SLOT na regułę. Bez STEP, zadawania procentu, ruchu czasowego i flag lokalnych. Cztery pary przekaźników zasilanie/kierunek: PC0/PC1, PC2/PC3, PC4/PC5, PC6/PC7. Bezpieczny start, wyłączenie… [Pełny opis wydania](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.24-s0804-old-1).

## Trzy ostatnie wersje

| Wersja | Data publikacji | Pobieranie | Zmiany |
|---|---|---|---|
| **2.0.30** | 2026-11-24 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.24-s0804-old-1/GRYFSMART-Programator.exe) | Nowy moduł GRYF S0804 OLD: ATmega644PA, kwarc 11,0592 MHz. Firmware 1: lokalnie tylko OTWÓRZ, STOP, ZAMKNIJ, ZAMKNIJ/STOP i OTWÓRZ/STOP. 16 reguł; jedna zdalna akcja SLOT na regułę. Bez STEP, zadawania procentu, ruchu czasowego i flag lokalnych. Cztery pary przekaźników zasilanie/kierunek: PC0/PC1, PC2/PC3, PC4/PC5, PC6/PC7. Bezpieczny start, wyłączenie… [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.24-s0804-old-1) |
| **2.0.27** | 2026-11-17 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.17-jtag-unified/GRYFSMART-Programator.exe) | R0806T i R0808: ochrona przed JTAG ujednolicona z S0804. Instalator 2.0.27 wyłącza JTAGEN także dla R0806T i R0808: HIGH 98/99 → D8, albo D0 przy zaprogramowanym EESAVE. Zachowuje EESAVE i EXTENDED; sprawdza zapis ponownym odczytem. Polityka ETH0606T/OLD bez zmian. R0806T: JTAG PC2–PC5 współdzieli wyjścia WY6–WY3. R0808: JTAG PF4–PF7 współdzieli wejścia… [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.17-jtag-unified) |
| **2.0.26** | 2026-11-17 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.17-s0804-jtag/GRYFSMART-Programator.exe) | S0804 39 — zwolnienie pinów rolet 2 i 3 zajmowanych przez JTAG. Poprzedni instalator zachowywał JTAGEN; fabryczne HIGH=99 przechodziło na 98, co pozostawiało JTAG na PC2–PC5. To piny zasilania i kierunku rolet 2/3. Raporty czasu mogły działać bez sterowania fizycznymi przekaźnikami. Aplikacja S0804 39 i bootloader v13-chain1-jtag-off zerują przekaźniki i… [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.17-s0804-jtag) |

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
