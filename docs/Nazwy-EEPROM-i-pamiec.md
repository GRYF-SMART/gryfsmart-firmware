# Nazwy w EEPROM — firmware i GRYFEXPERT 0.5.20

Wersje: ETH0606T 29, R0808 29, R0806T 29, S0804 30, R0806T-OLD 6. Bootloadery pozostają bez zmian.

W GRYFEXPERT: wybierz moduł → Informacje → Nazwy zapisane w module. Zmieniaj nazwy i użyj „Wyślij nazwy do EEPROM”. „Odczytaj nazwy z modułu” odtwarza je w projekcie. Rozpoznawanie nowych firmware również odczytuje nazwy, bez zapisu. Zapis projektu na PC oraz zwykły zapis reguł nie zapisują nazw do procesora.

Nazwy modułu, wejść i wyjść (rolet w S0804) są dostępne we wszystkich modelach. R0806T i R0808 przechowują też nazwy dwóch regulatorów i dwóch czujników temperatury. R0806T dodatkowo nazwę PWM. Modele bez tych funkcji nie rezerwują dla nich pól.

18 znaków to 18 liter/cyfr/spacji/znaków, także polskich, a nie 18 bajtów UTF-8. Obsługiwany alfabet: ASCII 32–126 oraz ĄĆĘŁŃÓŚŹŻąćęłńóśźż. Aplikacja normalizuje polskie litery do NFC. Inne alfabety i emoji są odrzucane. Na przewodzie nazwy są kodowane HEX, więc nie zmieniają dotychczasowych parserów ASCII.

Jeden rekord zajmuje 22 B: znacznik, długość, 18 B treści, CRC16. Każdy moduł ma dodatkowy wspólny dziennik 24 B. Firmware nie ma tablicy nazw w RAM. Używa jednego tymczasowego bufora transmisji 22 B i 4 B stanu; po potwierdzeniu bufor jest zerowany. R0806T potrzebuje dodatkowo jednego bajtu do ochrony migracji dawnego formatu konfiguracji. Zapis następuje wyłącznie po NameSet, tylko przy rzeczywistej zmianie nazwy. Proces zapisuje najwyżej jeden bajt EEPROM na obrót pętli, z eeprom_update_byte. Nie zatrzymuje sterowania na czas całego zapisu. Po zaniku zasilania zatwierdzony dziennik kończy rozpoczęty zapis przy kolejnym uruchomieniu; niezatwierdzony zostawia poprzednią nazwę.

W OLD reguły są pakowane bezstratnie z 55 do 43 B: flagi i adresy mieszczą się w bitach, a dane slotów pozostają bez zmian. Dwa banki po 712 B zastępują dwa banki po 912 B. Migracja zachowuje ważną starą kopię do chwili zatwierdzenia nowej. GRYFEXPERT przed pierwszym zapisem nazw inicjalizuje też drugi nowy bank. Historia restartów oraz metadane bootloadera pozostają na swoich adresach. Po migracji nie wracaj do OLD 5 bez kopii ustawień: starszy firmware nie odczytuje nowego formatu reguł. Zalecana kopia projektu przed aktualizacją.

## Pamięć po kompilacji

Liczby w bajtach. RAM poza danymi statycznymi jest wspólnym miejscem na stos i dane automatyczne; nie jest to gwarantowany zapas stosu. Zarezerwowana EEPROM obejmuje pełną pojemność pól nazw i dzienników, nawet gdy nazwy są puste. Dla R0808 pozostawiono także 96 B na obsługiwane stare rekordy. S0804 zachowuje 1160 B dawnych deklaracji EEPROM.

| Moduł | Flash aplikacji / wolne do bootloadera | RAM statyczny | RAM na stos | EEPROM zarezerwowana / wolna | Najmniejszy zapas stosu zaobserwowany w testach |
|---|---:|---:|---:|---:|---:|
| ETH0606T 29 | 75982 / 177970 | 6135 | 2057 | 2487 / 1609 | 1376 |
| R0808 29 | 49098 / 204854 | 7243 | 949 | 3015 / 1081 | 290 |
| R0806T 29 | 51346 / 71534 | 9568 | 6816 | 3089 / 1007 | 6162 |
| S0804 30 | 38970 / 83910 | 8905 | 7479 | 3772 / 324 | 6821 |
| R0806T-OLD 6 | 29846 / 31594 | 3608 | 488 | 1987 / 61 | 221 |

## Ryzyka i zakres sprawdzenia

Największe ograniczenia mają OLD oraz R0808. OLD ma tylko 61 B bezpiecznie wolnej EEPROM i 488 B RAM poza danymi statycznymi; w teście stosu pozostało 221 B. R0808 ma 949 B poza danymi statycznymi, a test zostawił 290 B. Nie dodawaj w tych modułach dużych lokalnych buforów, rekurencji ani pamięci dynamicznej bez ponownej analizy. ETH pozostawia 2057 B poza statycznymi danymi; jego obecny limit kompilacji 6144 B danych statycznych jest bliski, więc kolejne bufory również wymagają optymalizacji.

Nie zaobserwowano kolizji stosu z danymi w badanych scenariuszach. To pomiar konkretnego przebiegu emulowanego kodu maszynowego, nie formalny dowód najgorszego przypadku wszystkich możliwych zagnieżdżeń przerwań i funkcji. Nie wykonywano pomiaru na fizycznych modułach. Przed dalszą rozbudową OLD/R0808 zalecany pomiar znacznikiem stosu na sprzęcie przy jednoczesnym sterowaniu, komunikacji i diagnostyce.

Sprawdzono: 316 kontroli silnika nazw (w tym 55 punktów przerwania zapisu), 233 kontrole OLD (migracja obu starych banków, przerwania i pełne szerokości pól reguł), rzeczywiste HEX-y pięciu modeli (18 polskich znaków, ostatnie pole, odczyt po restarcie, diagnostyka, niezmieniona nazwa bez zapisu), ETH z dwoma klientami TCP i przekazywaniem nazwy OLD, testy GRYFEXPERT na symulowanym TCP dla wszystkich modeli. Fizycznych modułów nie programowano.

## Protokół

Indeksy od zera: 0 nazwa modułu, następnie wejścia, wyjścia/rolety; w R0806T/R0808 potem 2 regulatory i 2 czujniki; na końcu R0806T ma PWM. Liczba pól: ETH 13, R0808 21, R0806T 20, S0804 13, OLD 15.

`AT+NameGet=ID,INDEKS` → `Name=ID,INDEKS,HEX,CRC16`.

`AT+NameSet=ID,INDEKS,HEX,CRC16` → `NameOK=ID,INDEKS` dopiero po zapisie i weryfikacji; błąd `NameERROR=ID,INDEKS,POWOD`. CRC16-CCITT (FFFF/1021), po znakach ASCII od ID do końca HEX, bez końcowego przecinka/CRC. Pusta nazwa to pusty HEX. NameGet nie zmienia EEPROM. MIGRATE oznacza konieczność jawnego SaveConfig starego formatu przed pierwszym NameSet. BUSY nie oznacza zapisania nazwy; nie ponawiaj niepewnych zapisów bez odczytu.
