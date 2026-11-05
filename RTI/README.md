# GRYF dla RTI Integration Designer

**Aktualna wersja sterownika: 2.08 · 6 listopada 2026**

Pobierz [GRYF.rtidriver](GRYF.rtidriver). W istniejącym projekcie wybierz instancję **GRYF**, otwórz **Driver Utilities → Update Driver** i wskaż pobrany plik. Nową instancję dodaj z pliku w sekcji **Drivers**. Sterownik obsługuje moduły R0806T, R0808, ETH0606T i S0804.

## Zmiany z 6 listopada 2026

| Wersja | Zmiany |
| --- | --- |
| **RTI 2.05** | Osobne, widoczne od razu pola wyboru **TCP/IP** i **RS-232**. Przy obu odznaczonych używany jest wybór zapisany w projekcie. Przy obu zaznaczonych pierwszeństwo ma RS-232. |
| **RTI 2.06** | Osobne polecenia **Ustaw wyjście**, **Ustaw flagę** i **Ustaw PWM**. Dla R0806T dodano włączenie na czas, włączenie po czasie oraz impuls po opóźnieniu. Czasy mają rozdzielczość 0,1 s. Dla impulsu wpisz np. `2,5 / 0,7`, czyli opóźnienie i czas włączenia. Włączenie po czasie wymaga firmware 35 lub nowszego. PWM obsługuje rampę 0–5 s, włączenie na procent, wyłączenie oraz przełączanie z pamięcią i bez pamięci. |
| **RTI 2.07** | Diagnostyka wszystkich modułów lub osobno dla każdego ID. Pokazuje model, wersję firmware, minimum, średnią i maksimum czasu pętli w µs, sumę restartów programowych i watchdog oraz osobny licznik startów. Dostępne są automatyczne odświeżanie i akcja ręczna. |
| **RTI 2.08** | Składanie fragmentów TCP i rozdzielanie wielu ramek z jednego odczytu. Walidacja raportów, kolejka poleceń z priorytetem akcji użytkownika, odstęp między transmisjami i scalanie oczekujących odczytów. Most GRYFEXPERT rozpoczyna sesję przez `Hello` i przekazuje odebrane odpowiedzi oraz zdarzenia bez echa poleceń. |
| **GRYFEXPERT 0.5.50** | Eksport nazw wejść, wyjść, PWM i flag do pliku `.driverconfig`. Nazwy flag można zapisać w projekcie w zakładce **Flagi**. [Pobierz GRYFEXPERT 0.5.50](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.06-gryfexpert-0.5.50). |

## Jak przenieść nazwy z GRYFEXPERT do RTI

1. W projekcie GRYFEXPERT wpisz nazwy w zakładkach **Wejścia**, **Wyjścia** lub **Rolety** oraz **Flagi**. Nazwę PWM ustaw w zakładce **Wyjścia** modułu R0806T.
2. W projekcie RTI sprawdź liczbę modułów, ich ID i typy. W Integration Designerze wybierz istniejący sterownik **GRYF → Driver Utilities → Export Configuration** i zapisz plik `.driverconfig`.
3. W GRYFEXPERT wybierz **Plik → Eksportuj nazwy do RTI** i wskaż wyeksportowany plik. Program utworzy kopię `*-nazwy.driverconfig` i poda liczbę dopasowanych modułów, zmienionych nazw oraz pominiętych modułów.
4. W tym samym projekcie Integration Designera wybierz **GRYF → Driver Utilities → Import Configuration** i wskaż plik `*-nazwy.driverconfig`. Sprawdź nazwy w **Driver Properties** i listach wyboru w **Tag Editorze**, a następnie zapisz projekt.

Dopasowanie odbywa się według ID i typu modułu oraz numeru kanału. Ustawienia połączenia RS-232 i TCP pozostają takie jak w pliku wyeksportowanym z RTI. Pusta nazwa flagi w GRYFEXPERT zachowuje dotychczasową etykietę w RTI.

SHA-256 paczki: `79f81bc18a38d3b19e584a48216512232c58324df8c53a16230a7e80015a957b`.
