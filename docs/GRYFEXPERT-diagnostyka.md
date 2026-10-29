GRYFEXPERT 0.5.14 — panel Restarty i szybkość działania dla wszystkich pięciu modeli.

Informacje -> Restarty i szybkość działania:
• R0808: czasy pętli, zerowanie statystyk, restart; szczegółowa historia 8 uruchomień w EEPROM wymaga firmware 27+.
• R0806T i S0804: czasy pętli, zerowanie statystyk, restart oraz liczniki i przyczyna ostatniego restartu. Obecny firmware udostępnia podsumowanie, bez listy poszczególnych wpisów.
• ETH0606T: czasy pętli, zerowanie statystyk i restart modułu. Obecny firmware nie udostępnia trwałego logu restartów.
• R0806T-OLD: restart modułu; brak pomiarów pętli i logu restartów w obecnym firmware. Niedostępne przyciski są wyłączone z objaśnieniem.

Czasy minimalny/średni/maksymalny w µs i liczba próbek. Poprawnie rozpoznawane są oba formaty raportów restartów: strumieniowy R0808 i pojedyncze podsumowanie R0806T/S0804. Firmware 27 nie jest wymagane do pomiarów czasu ani restartu R0808. Przy restarcie ETH przez TCP program ponownie łączy się i potwierdza tożsamość; polecenie restartu wysyłane tylko raz.

Walidacja: testy rzeczywistych gniazd TCP dla wszystkich pięciu modeli, obsługa obu formatów raportów, blokada nieobsługiwanych komend OLD/ETH, rozłączenie i ponowne połączenie ETH po restarcie; test przeglądarkowy wszystkich paneli i przycisków na symulatorze. Fizycznych urządzeń nie restartowano ani nie programowano.
Firmware, bootloadery, Programator i Instalator bez zmian: ETH 25, R0808 27, R0806T 27, S0804 27, OLD 4; narzędzia natywne 2.0.13. Nie trzeba wgrywać nowego firmware z powodu tej aktualizacji aplikacji.
