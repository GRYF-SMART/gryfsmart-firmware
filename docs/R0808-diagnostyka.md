R0808 firmware 26 i GRYFEXPERT 0.5.12 — historia restartów i czasy pętli.

R0808: trwała historia 8 ostatnich uruchomień (192 bajty EEPROM, 0xD00–0xDBF), CRC i końcowy znacznik poprawnego zapisu. Liczniki uruchomień, restartów watchdog i restartów z polecenia. Przyczyna resetu, MCUSR i stan EEPROM. AT+ResetStats=ID; AT+ResetLog=ID,INDEX (0–7, najnowszy pierwszy). Historia bez daty/godziny, rozpoczyna się od instalacji wersji 26. Flagi resetu odzyskiwane również z GPIOR0 przekazanego przez obecny bootloader v11. Bootloader bez zmian.

GRYFEXPERT: Informacje -> Restarty i szybkość działania. Przyciski: Odczytaj log restartów, Odczytaj czasy pętli, Wyzeruj statystyki czasu, Restart modułu. Minimalny/średni/maksymalny czas w mikrosekundach, liczba próbek, sygnalizacja nasycenia licznika. Historia i liczniki restartów z opisem przyczyny. Restart wymaga potwierdzenia, chwilowo wyłącza wyjścia, następnie potwierdza tożsamość modułu i odświeża log. Brak ponawiania polecenia restartu. Konfiguracja nie jest kasowana. Diagnostyka wymaga R0808 FW 26+.

Pamięć R0808: Flash aplikacji 45 400 B, stały RAM 7 201 B, pozostaje 991 B na stos i zmienne dynamiczne (bez pomiaru szczytowego użycia stosu). EEPROM logu: 192 B. Brak ciągłego zapisu statystyk pętli do EEPROM.

Walidacja: 61 testów logu, w tym przerwany zapis po kolejnych bajtach i zawijanie historii; 129 testów diagnostyki i routingu na AVR; 6334 sprawdzenia restartu i odtwarzania wyjść; 222 testy GRYFEXPERT; przeglądarka i symulator TCP: historia, czasy min/średni/max, zerowanie pomiarów, pojedynczy restart i ponowny odczyt logu. Fizycznych modułów nie programowano ani nie restartowano.

Pozostałe firmware bez zmian: ETH 25, R0806T 27, S0804 27, OLD 4. Programator i Instalator pozostają 2.0.13. Wszystkie paczki i manifest zawierają aktualny R0808 26. Bootloadery bez zmian.