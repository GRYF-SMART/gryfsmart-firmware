# RULE: przezroczyste przekazywanie i lokalne sterowanie niezależne od UART

Dokumentacja wykonawcy reguł w oprogramowania w wersji **20** wszystkich czterech modułów.

## Przekazywanie komend

Wszystkie cztery modele przekazują komendy adresowane do innego ID: Rule, GetRule, RuleRemote, GetRuleRemote, RulePWM i GetRulePWM. Obsługiwane są ramki RULE z 16, 18 i 20 polami liczbowymi, bez interpretowania układu wejść/akcji przez pośrednika. Sprawdzane są pełna nazwa komendy, ID 1–35, składnia liczb, maksymalnie 20 pól, wartości do 65535 oraz suma kontrolna. Znaczenie pól i możliwości sprzętu sprawdza moduł docelowy.

Odpowiedzi Rule, RuleRemote, RulePWM, RuleOK i RuleERROR przechodzą również przez S0804 oraz ETH. R/S kierują ramkę na przeciwległy port linii. ETH: USB (port 0) do RS-232 (1), RS-232 do USB; istniejąca bramka TCP nadal wysyła obce polecenia do RS-232 i przekazuje odbierane odpowiedzi do TCP. ETH nie staje się symetrycznym modułem o dwóch portach RS-232.

R0806T obsługuje własny PWM przez RulePWM oraz zdalny PWM przez RuleRemote typu 4. R0808, ETH i S0804 obsługują zdalny PWM typu 4; lokalnego PWM nie mają.

## Lokalne akcje i zdarzenia wejść

Wykonawca ma oddzielny stan części lokalnej i zdalnej. Lokalne akcje przekaźników, rolet i PWM są wykonywane po jednej na obieg, bez czekania na miejsce w UART. Kolejna reguła może wykonać lokalną część, gdy wcześniejsza czeka na transmisję zdalną.

Obsługa wejść przekazuje zdarzenia do reguł przed raportowaniem UART. Kolejne zdarzenie jest pobierane po zakończeniu oczekującej części lokalnej, aby nie scalać kolejnych naciśnięć tylko z powodu wielu lokalnych akcji. Nie czeka na zakończenie transmisji zdalnych. Raporty I/PS/PL mają osobny bufor 16 zdarzeń; po odzyskaniu miejsca są nadawane w kolejności. Przepełnienie tego bufora zwiększa istniejący licznik KEYERROR, a lokalne sterowanie działa dalej. Licznik obejmuje teraz także utratę raportów, nie wyłącznie pierwotną kolejkę zdarzeń wejść.

Część zdalna czeka na miejsce dopiero przed rzeczywistą transmisją. Puste sloty nie wymagają wolnego UART. Każda zakończona część lokalna zwiększa licznik zdalnych wykonań danej reguły, maksymalnie do 255 oczekujących; jest to ograniczony bufor w RAM, nie trwała kolejka. Przy długotrwałym zablokowaniu i przekroczeniu limitu dalsze zdalne wykonania scalają się. Reguły uruchamiane bezpośrednio wielokrotnie przed obsłużeniem ich części lokalnej nadal korzystają z maski oczekujących żądań.

Kolejność między modułami nie jest transakcją: nowe lokalne akcje mogą wyprzedzić oczekujące akcje zdalne starszej reguły. Trasy transmisji muszą pozostawać drożne, aby akcje zdalne dotarły do odbiorców. Watchdog nie potwierdza ich dostarczenia.

## Zgodność i sprawdzenie

Formaty Rule/GetRule, sumy, maski i SaveConfig są wspólne tam, gdzie pozwala na to sprzęt. [Porównanie modeli](reguly-porownanie.md).

Bufory mają skończoną pojemność. Nie ma zbiorczego potwierdzenia wykonania sceny przez wszystkie urządzenia.
