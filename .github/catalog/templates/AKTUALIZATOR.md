## Aktualizacja aplikacji modułu

**GRYFSMART-Programator** służy do wgrywania najnowszej wersji oprogramowania do pamięci Flash modułów. Program automatycznie pobiera najnowszy firmware z GitHuba lub pozwala ręcznie wybrać plik z komputera.

Program automatycznie rozpoznaje moduł oraz zainstalowane oprogramowanie. Jeżeli w module znajduje się tylko bootloader, bez aplikacji, program rozpoznaje bootloader i nie pokazuje wersji firmware aplikacji, ponieważ nie jest ona wgrana. Można wtedy pobrać najnowszą aplikację z GitHuba albo wskazać plik ręcznie i wgrać go do modułu.

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
