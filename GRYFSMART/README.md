# 1. Aplikacja GRYFSMART

**[Pobierz najnowszą wersję 0.5.84](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.27-gryfexpert-0.5.84/GRYFEXPERT-0.5.84-win-x64.zip)**

GRYFEXPERT 0.5.84 — pomiary płytki R0808 STM w zakładce Informacje. Napięcie zasilania w V oraz temperatura płytki z termistora TDK B57330V2103F260, NTC 10 kΩ przy 25°C, B25/100 = 3455 K. Temperatura jest liczona w aplikacji z surowego ADC według przybliżenia beta dla potwierdzonego elementu; wcześniejsze założenie B3950 nie dotyczy tego modelu. Pomiar po… [Pełny opis wydania](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.27-gryfexpert-0.5.84).

## Trzy ostatnie wersje

| Wersja | Data publikacji | Pobieranie | Zmiany |
|---|---|---|---|
| **0.5.84** | 2026-11-26 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.27-gryfexpert-0.5.84/GRYFEXPERT-0.5.84-win-x64.zip) | GRYFEXPERT 0.5.84 — pomiary płytki R0808 STM w zakładce Informacje. Napięcie zasilania w V oraz temperatura płytki z termistora TDK B57330V2103F260, NTC 10 kΩ przy 25°C, B25/100 = 3455 K. Temperatura jest liczona w aplikacji z surowego ADC według przybliżenia beta dla potwierdzonego elementu; wcześniejsze założenie B3950 nie dotyczy tego modelu. Pomiar po… [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.27-gryfexpert-0.5.84) |
| **0.5.83** | 2026-11-26 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.26-r0808-stm-rtc-2/GRYFEXPERT-0.5.83-win-x64.zip) | R0808 STM firmware 2 / GRYFEXPERT 0.5.83 — zegar RTC. Zakładka Czas dla R0808 STM: włączanie/wyłączanie RTC, odczyt daty i godziny, ustawienie czasu komputera lub ręczne, z potwierdzeniem odczytem. Rok, miesiąc, dzień, godzina, minuta i sekunda. Kalendarz gregoriański uwzględnia lata przestępne, również wyjątek roku 2100. Moduł przechowuje UTC, aplikacja… [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.26-r0808-stm-rtc-2) |
| **0.5.82** | 2026-11-26 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.26-gryfexpert-0.5.82/GRYFEXPERT-0.5.82-win-x64.zip) | GRYFEXPERT 0.5.82 — komunikaty głosowe po aktualizacji firmware. Po poprawnym zapisie i weryfikacji aplikacji program odczytuje „Moduł R0806T został zaprogramowany”, z nazwą rzeczywistego modelu. Wspólny mechanizm dla wszystkich modeli i transportów obsługiwanych w panelu; ETH Mini GATE korzysta z dołączonego klasycznego programatora 2.0.32. Pole… [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.26-gryfexpert-0.5.82) |

## Aktualizacja Flash przez RTI — GRYFEXPERT 0.5.76 / GRYF Driver 2.22

Użyj istniejącego ekranu **Aktualizacja firmware**. Połączenie jest zapisane w projekcie; odczyt wersji, pobranie najnowszego HEX, kontrola SHA-256, zapis i weryfikacja mają ten sam przebieg dla obsługiwanych połączeń COM, Ethernet ETH i bramki RTI.

1. W Integration Designer wybierz **Driver Utilities → Update Driver**, wskaż bieżący `GRYF.rtidriver`, a następnie prześlij projekt do procesora RTI. Zachowaj dotychczasową instancję i przypisania.
2. Włącz **Konfiguracja przez GRYFEXPERT**, wybierz właściwy COM i 115200 bit/s, 8N1. Port TCP pozostaje domyślnie **4211** i jest edytowalny. GRYFEXPERT łączy się do IP procesora RTI tym samym portem, identyfikatorem i kluczem parowania.
3. W GRYFEXPERT wybierz moduł i **Odczytaj wersję → Sprawdź i pobierz najnowszy wsad → Aktualizuj soft**. Możesz też wskazać lokalny HEX w istniejącej sekcji programatora. Program sprawdza model, MCU, rozmiar i sumy kontrolne przed zapisem.
4. Dla całej linii wybierz **Sprawdź całą sieć i pobierz najnowsze wsady**, a następnie **Aktualizuj wszystkie wymagające aktualizacji**. Moduły aktualizują się pojedynczo, od najdalszej fizycznej pozycji. Pozycja w przewodzie i ID modułu to odrębne wartości, obie w zakresie 1–35.
5. Po zakończeniu odczytaj konfigurację i zapisz projekt. Rozłącz GRYFEXPERT, aby RTI wznowiło sterowanie i synchronizację stanów.

Przez RTI obsługiwane są **R0806T, R0808 i S0804** z bootloaderem **v11-chain1 lub v13-chain1-jtag-off**, a S0804 także **v12-chain1-led-on**. Pierwsza instalacja bootloadera nadal wymaga ISP/USBasp. Ta wersja nie aktualizuje przez RTI ETH0606T, ETH Mini ani modułów OLD; dotychczasowe sposoby ich aktualizacji pozostają dostępne.

**Podczas zapisu zapewnij ciągłe zasilanie.** Driver wstrzymuje swoje komendy i odpytywanie. Potwierdzenie CRC całego obrazu, uruchomienie aplikacji i odczyt jej tożsamości są wymagane do zakończenia sesji. Utracone potwierdzenie zapisu strony jest sprawdzane przez odczyt tej strony.

Jeżeli zapis zostanie przerwany, blokada sterowania pozostaje w pamięci trwałej RTI, również po restarcie procesora. Połącz GRYFEXPERT ponownie, wybierz ten sam moduł z projektu i ponów **Aktualizuj soft**. Wgrywanie rozpoczyna się od początku; nie jest to automatyczny powrót do poprzedniej aplikacji. Nie zmieniaj kolejności przewodów ani ID podczas odzyskiwania. Zmienna **Status bramki** pokazuje niedokończoną aktualizację. Nie usuwaj instancji drivera w celu obejścia blokady.

Sprawdzono pełne obrazy Flash w symulatorze z rzeczywistym kodem bramki RTI i klientem TCP, utratę potwierdzeń, przerwę TCP i blokadę po restarcie. Odbiór na fizycznym procesorze RTI i rzeczywistych modułach wymaga osobnego testu instalacyjnego.

## Konfiguracja przez GRYFEXPERT — driver RTI 2.22 / GRYFEXPERT 0.5.76

Połączenie: **GRYFEXPERT → adres IP procesora RTI + port TCP → RS232 → port 0 pierwszego modułu GRYF**. Odpowiedzi wracają tą samą drogą. Moduł ETH nie jest wymagany. RTI działa jako serwer ze stałym adresem IP; GRYFEXPERT inicjuje połączenie jako klient.

### Ustawienia drivera RTI

W Integration Designer zaktualizuj driver do **2.22**. Wybierz **RS-232**, port procesora połączony z GRYF i **115200, 8N1**. W osobnej sekcji **Konfiguracja przez GRYFEXPERT**:

- włącz konfigurację przez GRYFEXPERT;
- ustaw **Port TCP konfiguracji GRYFEXPERT**: domyślnie **4211**, z możliwością zmiany na wolny port w zakresie 1024–65535;
- wpisz identyfikator RTI oraz klucz parowania (32 znaki hex, skopiowany z GRYFEXPERT).

Port służy do konfiguracji i aktualizacji obsługiwanych modułów przez GRYFEXPERT; nie jest portem bramki ETH. W driverze **nie wpisuje się IP komputera**. Stały adres IP lub rezerwację DHCP procesora ustaw w konfiguracji sieci RTI. Zapisz i prześlij projekt do procesora. Wymagany runtime RTI 15+ obsługujący GenericServer. Zmienna **Status bramki** informuje o nasłuchu lub błędzie portu.

### Ustawienia GRYFEXPERT

1. Wybierz **Bramka RTI** obok COM i Ethernet ETH.
2. Wpisz **Adres IP RTI** (np. `192.168.0.15`) oraz **Port TCP RTI**. Domyślnie **4211**, można go edytować. Musi być taki sam jak w driverze.
3. Ustaw identyfikator i klucz parowania zgodne z driverem. Zapisz projekt, aby zachować ustawienia.
4. Kliknij **Połącz**. Program łączy się do RTI — nie uruchamia serwera na komputerze. Następnie rozpoznaj moduły i odczytaj konfigurację jak przy bezpośrednim COM.
5. Po zakończeniu kliknij **Rozłącz**. RTI wraca do normalnej pracy i odczytuje stany modułów. Po zmianie ID lub modeli w GRYFEXPERT dostosuj także konfigurację drivera w Integration Designer.

Most obsługuje konfigurację, nazwy, reguły, wykrywanie modułów i diagnostykę. Od GRYF Driver 2.22 i GRYFEXPERT 0.5.76 obsługuje również aktualizację Flash R0806T/R0808/S0804 opisaną powyżej. Podczas sesji wstrzymane są komendy i odpytywanie tego drivera RTI; moduły nadal wykonują własny program. Drugi klient nie może przejąć aktywnej sesji. Po zwykłej konfiguracji zerwanie połączenia lub brak heartbeat przez ponad 10 s zwalnia most i uruchamia synchronizację. Przy niedokończonym zapisie Flash sterowanie pozostaje zablokowane do skutecznego ponowienia aktualizacji. Odrzucone polecenia RTI nie są odtwarzane. Nie używaj drugiej instancji drivera na tym samym COM.

Zmienne **Status bramki** oraz **Trwa konfiguracja GRYFEXPERT** można umieścić na panelu RTI. Port i klucz są ustawieniami konkretnej instalacji. Używaj mostu w zaufanym LAN; transmisja nie jest szyfrowana i portu nie należy przekierowywać z Internetu.

**Zmiana względem 0.5.51 / 2.13:** kierunek zestawiania połączenia został odwrócony na GRYFEXPERT → RTI. Zaktualizuj obie strony. Stary klucz i numer portu można zachować, ale w projekcie GRYFEXPERT trzeba podać adres RTI i ponownie potwierdzić przypisanie modułów do połączenia. Testy obejmują symulację RTI i rzeczywiste połączenia TCP na komputerze; test instalacyjny na fizycznym RTI pozostaje do wykonania.

## Do czego służy program

**GRYFSMART / GRYFEXPERT** to program Windows do konfiguracji sterowników GRYF: modułów, wejść, wyjść, flag, reguł, czasów, PWM i rolet. Nazwa pliku oraz aplikacji pozostaje GRYFEXPERT.

## Uruchomienie

1. Pobierz ZIP z linku na górze, rozpakuj cały katalog i uruchom GRYFEXPERT. Przed podmianą starszej instalacji zapisz projekt i zamknij program; zachowaj swoje projekty.
2. Wybierz **TCP/IP** i adres bramki ETH0606T lub ETH Mini. Dla aktualnego ETH0606T port 5002 służy konfiguratorowi; port 5000 może obsługiwać integrację. ETH Mini domyślnie używa `192.168.1.201:5002` i jednego klienta.
3. Przy połączeniu **RS-232** wybierz port COM, 115200 bit/s, 8N1, bez kontroli przepływu. Port nie może być otwarty w drugim programie.
4. Odczytaj moduły i ich konfigurację. Nadaj nazwy wejściom, wyjściom, roletom i flagom. Zapisz projekt na komputerze; zapis konfiguracji do modułów jest osobną czynnością.
5. Skonfiguruj funkcje odpowiednie dla modelu i wersji firmware, następnie zapisz ustawienia do modułów.

## Nazwy w RTI

W RTI wyeksportuj konfigurację instancji GRYF do `.driverconfig`. W GRYFEXPERT wybierz eksport nazw RTI w menu **Plik**, wskaż ten plik i zapisz wynik. Zaimportuj wynik do tej samej instancji w Integration Designer. ID i typy modułów w obu projektach muszą się zgadzać. [Dokładna instrukcja](../RTI/INSTRUKCJA.md#jak-przenieść-nazwy-z-gryfexpert-do-rti).

[Protokół i przykłady](../PROTOKOL) · [Najnowsze firmware modułów](../HEX)


[1. Aplikacja GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/GRYFSMART) · [2. GRYFSMART-Programator](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/AKTUALIZATOR) · [3. Driver Home Assistant](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/HOME-ASSISTANT) · [4. Driver RTI](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/RTI) · [5. Instalator Bootloader](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/BOOTLOADER) · [6. Protokół GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/PROTOKOL) · [7. System i moduły GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/SYSTEM)
