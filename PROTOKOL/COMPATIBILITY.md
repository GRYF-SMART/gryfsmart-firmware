# Zgodność HA 0.3.16 / RTI 2.23 / GRYFEXPERT 0.5.87

Aktualizacja integracji nie wymaga nowego HEX, jeśli moduły mają już poniższe wersje. Nie zmieniono firmware. Wersje odczytaj z urządzeń; numer zapisany w projekcie może być nieaktualny.

| Model | Zweryfikowane firmware |
|---|---|
| R0806T | 39 |
| R0808 | 38 |
| S0804 | 39 |
| ETH0606T | 37 |
| R0806T-OLD | 11 |
| S0804-OLD | 2 |
| R0808-STM | 4 |
| ETH-Mini-GATE | 4 |

## Magistrala i topologia

Komendy adresowane ID 1–35 przechodzą przez moduły przelotowe niezależnie od ich typu i kolejności, przy unikalnych adresach i powyższych firmware. Limit ramki: 199 znaków ASCII bez CR. RS-232: 115200, 8N1. Odwrócenie lub przebudowa łańcucha wymaga poprawnego połączenia par portów i ponownego odczytu pozycji przed aktualizacją CHAIN1.
ETH0606T i ETH-Mini-GATE są początkiem gałęzi, nie dowolnym elementem przelotowym. ETH0606T rezerwuje ID 1; skan CHAIN1 nie liczy bramki jako hop, a Search uwzględnia ją w numeracji. Mini ma jeden klient TCP, domyślnie port 5002. ETH0606T ma domyślnie port 5000 i serwisowy 5002. Dwie integracje nie powinny równocześnie zmieniać tej samej konfiguracji modułu.
Kolejność wykonywania poleceń nadal ma znaczenie (np. ON i toggle). Transport nie zapewnia bezstratnej obsługi dowolnego przeciążenia. Wymagane są kolejkowanie, potwierdzenia zapisu i odczyt kontrolny; po niepewnym wyniku nie powtarzaj automatycznie mutacji.

## Zmiany

- HA: RulePulse bez sumy kontrolnej, THERM z histerezą 0, aktualne modele i możliwości, timery przez mieszane modele, akcje rolety 9/8/10, pojedynczy slot S0804-OLD, odczyt GetOut w R0806T-OLD 11, flagi jako osobne encje oraz warunki flag i harmonogramy w edytorze reguł.
- RTI: 35 slotów z zachowanymi istniejącymi identyfikatorami i GUID; modele 7=R0806T-OLD, 8=S0804-OLD, 9=R0808-STM, 10=ETH-Mini-GATE. OLD nie dostaje komend lokalnego PWM/flag, S0804-OLD nie dostaje pozycji procentowej. Wybór modułu regulatora RTI obejmuje również ID 26–35.
- GRYFEXPERT: eksport nazw do RTI dla wszystkich modeli i ID 1–35; zachowane starsze mapowanie STM jako R0808 i typy RTI 2/3.

## Polecenia zaawansowane

HA: akcja administratora `gryfsmart.protocol_command`, pola `entry_id`, `module_id`, `command`, `parameters` (lista). Opcjonalna odpowiedź zawiera wysłaną komendę i odebrane ramki. Integracja dodaje ID i właściwą sumę; użytkownik ich nie dopisuje. Funkcja wymaga firmware z tabeli.
RTI: funkcja `Komenda protokołu` / `ProtocolCommand(ID, nazwa, parametryCSV)`. Wcześniej musi zostać odebrane Find modułu. Zmienne `ProtocolLastCommand`, `ProtocolLastResponse`, `ProtocolCommandStatus` pokazują kolejkę i ostatnią odebraną ramkę. Przyjęcie do kolejki nie jest potwierdzeniem wykonania w module. Własne makra konfiguracyjne muszą czekać na potwierdzenie i sprawdzać odczyt.
Przykład HA: command `RulePulse`, module_id `1`, parameters `[1,1,2,1,5,0]` daje `AT+RulePulse=1,1,1,2,1,5,0`. Przykład RTI: `ProtocolCommand(1,"RTCSet","1795777200")`. RTC i harmonogramy są funkcją STM; zapis konfiguracji EEPROM jest osobnym poleceniem SaveConfig.
S0804-OLD ma jeden slot zdalny i nie ma procentowego pozycjonowania ani RolTimed. R0806T-OLD nie udostępnia odczytu reguł; konfiguracja przez GRYFEXPERT lub jawne komendy zapisu. Mini nie ma lokalnych wejść/wyjść. Lokalny regulator RTI i termostat zapisany w module to dwie różne funkcje; nie przypisuj obu do tego samego wyjścia bez świadomej koordynacji.

| Komenda | Parametry po ID, przed sumą | Suma | Odpowiedź | Modele |
|---|---|---|---|---|
| Find | brak | none | AT+Find | R0806T, R0808, S0804, ETH0606T, R0806T-OLD, S0804-OLD, R0808-STM, ETH-Mini-GATE |
| RST | brak | none | ResetOK | R0806T, R0808, S0804, ETH0606T, R0806T-OLD, S0804-OLD, R0808-STM |
| ResetStats | brak | none | RESET | R0806T, R0808, S0804, ETH0606T, R0806T-OLD, S0804-OLD, R0808-STM |
| Info | brak | none | INFO | R0806T, R0808, S0804, ETH0606T, S0804-OLD, R0808-STM |
| Factory | brak | none | FACTORY | R0806T, R0808, S0804, ETH0606T, S0804-OLD, R0808-STM |
| Loop | brak | none | LOOP | R0806T, R0808, S0804, ETH0606T, S0804-OLD, R0808-STM |
| LoopReset | brak | none | LoopOK | R0806T, R0808, S0804, ETH0606T, S0804-OLD, R0808-STM |
| GetOut | brak | none | O | R0806T, R0808, ETH0606T, R0806T-OLD, R0808-STM |
| GetInputs | brak | none | I | R0806T, R0808, S0804, ETH0606T, S0804-OLD, R0808-STM |
| SetOut | akcja1,…,akcja6 lub akcja8 (0 bez zmian, 1 ON, 2 OFF, 3 toggle) | none | RuleOK | R0806T, R0808, ETH0606T, R0806T-OLD, R0808-STM |
| Pulse | wyjście,ticks_0.1s[,restart] | none | RuleOK | R0806T, R0808, ETH0606T, R0806T-OLD, R0808-STM |
| Timed | wyjście,tryb,opóźnienie_0.1s,czas_ON_0.1s,restart | none | RuleOK | R0806T, R0808, R0808-STM |
| Rule | nr_reguły,włączona,zdarzenia_wejść…,akcje_lokalne… (roleta: akcja,parametr) | sum | RuleOK | R0806T, R0808, S0804, ETH0606T, R0806T-OLD, S0804-OLD, R0808-STM |
| GetRule | nr_reguły | sum | Rule | R0806T, R0808, S0804, ETH0606T, S0804-OLD, R0808-STM |
| RuleRemote | nr_reguły,slot,ID_celu,typ,dane… | sum | RuleOK | R0806T, R0808, S0804, ETH0606T, R0806T-OLD, S0804-OLD, R0808-STM |
| GetRuleRemote | nr_reguły,slot | sum | RuleRemote | R0806T, R0808, S0804, ETH0606T, S0804-OLD, R0808-STM |
| RulePWM | nr_reguły,akcja,procent,rampa_0.1s | sum | RuleOK | R0806T |
| GetRulePWM | nr_reguły | sum | RulePWM | R0806T |
| RuleTemp | nr_reguły,tryb,źródło,czujnik,kierunek,próg_0.1C,histereza_0.1C,okres_0.1s | sum | RuleOK | R0806T, R0808, R0808-STM |
| GetRuleTemp | nr_reguły | sum | RuleTemp | R0806T, R0808, R0808-STM |
| RuleFlags | nr_reguły,tryb_AND_OR,flaga1,stan1,flaga2,stan2,flaga3,stan3,akcje_flag_1…8 | sum | RuleOK | R0806T, R0808, S0804, ETH0606T, R0808-STM |
| GetRuleFlags | nr_reguły | sum | RuleFlags | R0806T, R0808, S0804, ETH0606T, R0808-STM |
| RuleTime | nr_reguły,tryb,zdarzenie,maska_dni,rok,miesiąc,dzień,godzina,minuta,sekunda,offset_min+720 | sum16 | RuleOK | R0808-STM |
| GetRuleTime | nr_reguły | sum | RuleTime | R0808-STM |
| RulePulse | nr_reguły,slot,ID_celu,wyjście,ticks_0.1s[,restart] | none | RuleOK | R0806T, R0808, S0804, ETH0606T, R0806T-OLD, S0804-OLD, R0808-STM |
| GetRulePulse | nr_reguły,slot | none | RulePulse | R0806T, R0808, S0804, ETH0606T, S0804-OLD, R0808-STM |
| PWM | akcja,procent[,rampa_0.1s] | sum | RuleOK | R0806T |
| GetPWM | brak | none | PWM | R0806T |
| StanRol | brak | none | R | S0804, S0804-OLD |
| RolAct | roleta,akcja,parametr (7: procent; 8/10: sekundy; inne: 0) | sum | RuleOK | S0804, S0804-OLD |
| RolTime | roleta,otwieranie_0.1s,zamykanie_0.1s | sum | RuleOK | S0804, S0804-OLD |
| GetRolTime | roleta | sum | RolTime | S0804, S0804-OLD |
| GetRolState | roleta | sum | RolState | S0804, S0804-OLD |
| RolTimed | roleta,kierunek_1_open_2_close,ticks_0.1s | sum | RuleOK | S0804 |
| KeyTime | wejście,krótko_0.1s,długo_0.1s | sum | RuleOK | R0806T, R0808, S0804, ETH0606T, R0806T-OLD, S0804-OLD, R0808-STM |
| GetKeyTime | wejście | sum | KeyTime | R0806T, R0808, S0804, ETH0606T, S0804-OLD, R0808-STM |
| SaveConfig | brak | sum | SaveOK | R0806T, R0808, S0804, ETH0606T, R0806T-OLD, S0804-OLD, R0808-STM |
| Defaults | brak | sum | RuleOK | R0806T, R0808, S0804, ETH0606T, R0806T-OLD, S0804-OLD, R0808-STM |
| SetFlag | flaga,akcja_0_nic_1_set_2_clear_3_toggle | sum | RuleOK | R0806T, R0808, S0804, ETH0606T, R0808-STM |
| GetFlags | brak | sum | Flags | R0806T, R0808, S0804, ETH0606T, R0808-STM |
| ReadTemp | czujnik | sum | T | R0808, R0808-STM |
| TempScan | brak | sum | RuleOK | R0808, R0808-STM |
| SetTemp | termostat,tryb,chłodzenie,źródło,czujnik,zadana_0.1C,histereza_0.1C,liczba_wyjść,[ID,typ,nr_wyjścia]… | sum | RuleOK | R0806T, R0808, R0808-STM |
| GetTemp | termostat | sum | THERM | R0806T, R0808, R0808-STM |
| GetTempCfg | termostat | sum | TEMP | R0806T, R0808, R0808-STM |
| NameGet | slot_etykiety | none | Name | R0806T, R0808, S0804, ETH0606T, R0806T-OLD, S0804-OLD, R0808-STM |
| NameSet | slot_etykiety,tekst_HEX | crc16 | NameOK | R0806T, R0808, S0804, ETH0606T, R0806T-OLD, S0804-OLD, R0808-STM |
| RTC | brak | none | RTC | R0808-STM |
| RTCEnable | 0 lub 1 | none | RTC | R0808-STM |
| RTCSet | sekundy_UNIX_UTC | none | RTCSetOK | R0808-STM |
| Board | brak | none | BOARD | R0808-STM |
| BoardNTC | beta (0 lub 2000–6000) | none | BoardNTC | R0808-STM |
| Astro | lokalizacja_aktywna,szerokość_e4+900000,długość_e4+1800000,UTC_min+720,EU_DST,0 | sum16 | RuleOK | R0808-STM |
| GetAstro | brak | sum | Astro | R0808-STM |

`none`: bez sumy; `sum`: suma liczb; `sum16`: suma modulo 65536; `crc16`: CRC16-CCITT tekstu pól. Szczegółowe ograniczenia wartości nadal sprawdza firmware; interfejsy encji i edytor reguł zapewniają dodatkową walidację. Tabela obejmuje komendy aplikacyjne, nie równoważne aliasy historyczne.

## Operacje w osobnej sesji

Search, Discovery, ModuleInfo, Chain, BOOT oraz Net/NetFind/NetSet/NetMAC/NetPorts/NetSave należą do adresowania, konfiguracji sieci i serwisu. Pozostają w obsłudze GRYFEXPERT (HA używa Discovery i Find podczas wykrywania). Nie są zwykłymi poleceniami adresowanymi z dowolnego makra. Flash przez most RTI nadal dotyczy R0806T, R0808 i S0804; pozostałe modele zachowują własne metody aktualizacji.

## Wdrożenie

1. Zainstaluj HA 0.3.16, uruchom HA ponownie i odśwież przeglądarkę.
2. W RTI Integration Designer użyj Driver Utilities → Update Driver dla GRYF 2.23, sprawdź modele i prześlij zapisany projekt do procesora.
3. Uruchom GRYFEXPERT 0.5.87 po zapisaniu bieżącego projektu. Odczytaj identyfikację modułów. Aktualizuj tylko moduły ze starszym firmware; nie zmieniaj samego numeru wersji w pliku projektu.
4. Na sprzęcie sprawdź reprezentatywne wyjścia, rolety, flagi i reguły między odległymi modułami. Testy programowe nie zastępują sprawdzenia okablowania ani rzeczywistych wersji urządzeń.
