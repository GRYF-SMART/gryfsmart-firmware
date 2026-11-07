"""Public GRYFSMART download catalog. Standard library only; no firmware sources."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import re
import urllib.request

ORG = 'GRYF-SMART'
BASE = 'https://github.com/GRYF-SMART/gryfsmart-firmware'
SECTIONS = [('GRYFSMART', '1. Aplikacja GRYFSMART'), ('AKTUALIZATOR', '2. GRYFSMART-Programator'),
            ('HOME-ASSISTANT', '3. Driver Home Assistant'), ('RTI', '4. Driver RTI'),
            ('BOOTLOADER', '5. Instalator Bootloader'), ('PROTOKOL', '6. Protokół GRYFSMART')]
NOTES = {
    ('AKTUALIZATOR', '2.0.21'): 'Obsługa ETH Mini GATE przez RS-232 i Ethernet, pobieranie HEX z GitHub. Czytelny log: błędy na czerwono, zakończenie weryfikacji na zielono.',
    ('AKTUALIZATOR', '2.0.14'): 'Wydanie narzędzi z obsługą pakietu modułów i bootloadera R0806T-OLD v13; aktualizacja przez USB/RS-232 oraz sieć CHAIN1.',
    ('AKTUALIZATOR', '2.0.13'): 'Poprawka wejścia ETH przez USB w bootloader: oddzielny CR i odstęp przed AT+BOOT zapobiegają utracie komendy.',
    ('BOOTLOADER', '2.0.14'): 'Pakiet instalatora z bootloaderem R0806T-OLD v13-old644p. Pozostałe bootloadery bez zmian.',
    ('BOOTLOADER', '2.0.13'): 'Wydanie pakietu narzędzi 2.0.13. Poprawka USB dotyczy aktualizatora; wsady bootloaderów w tym wydaniu pozostały bez zmian.',
    ('RTI', '2.08'): 'Import nazw z GRYFEXPERT; składanie fragmentów TCP, walidacja raportów, kolejka i priorytet sterowania, odstępy transmisji oraz odświeżanie stanów przez TCP/RS-232.'
}

def get(url):
    headers = {'User-Agent': 'GRYFSMART-public-catalog'}
    if os.getenv('GH_TOKEN') and url.startswith('https://api.github.com/'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as response:
        return json.load(response)

def releases(repo, cache):
    path = cache / (repo + '-releases.json') if cache else None
    if path and path.exists():
        rows = json.loads(path.read_text(encoding='utf-8'))
    else:
        rows = []
        page = 1
        while True:
            batch = get(f'https://api.github.com/repos/{ORG}/{repo}/releases?per_page=100&page={page}')
            rows.extend(batch)
            if len(batch) < 100:
                break
            page += 1
    return sorted((r for r in rows if not r['draft'] and not r['prerelease']),
                  key=lambda r: r['published_at'], reverse=True)

def semver(version):
    return tuple(int(n) for n in re.findall(r'\d+', version))

def item(version, asset, release):
    return dict(version=str(version), url=asset['browser_download_url'],
                release=release['html_url'], date=release['published_at'][:10],
                notes=release.get('body') or release['name'], digest=asset.get('digest'))

def summary(row):
    lines = [s.strip().lstrip('-* ').strip() for s in row['notes'].splitlines()]
    lines = [s for s in lines if s and not s.startswith(('#', '[', '|', 'http', '```'))]
    text = ' '.join(lines[:3])
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'<[^>]+>', '', text).replace('|', '/').replace('`', '').replace('*', '')
    return (text[:360].rsplit(' ', 1)[0] + '…') if len(text) > 360 else text

def table(rows):
    return ('| Wersja | Data publikacji | Pobieranie | Zmiany |\n|---|---|---|---|\n' +
            '\n'.join(f"| **{r['version']}** | {r['date']} | [Pobierz]({r['url']}) | {summary(r)} [Pełny opis]({r['release']}) |" for r in rows) + '\n')

def nav():
    return ' · '.join(f'[{label}]({BASE}/tree/main/{path})' for path, label in SECTIONS)

def collect(cache):
    fw = releases('gryfsmart-firmware', cache)
    ha = releases('ha-gryfsmart', cache)
    groups = {name: {} for name in ['GRYFSMART', 'AKTUALIZATOR', 'BOOTLOADER', 'RTI', 'HOME-ASSISTANT']}
    hexes = {}
    # Oldest first: notes describe the release which introduced a binary/version,
    # rather than a later GRYFEXPERT release that merely copied it.
    for r in reversed(fw):
        for a in r['assets']:
            for group, pattern in [('GRYFSMART', r'GRYF(?:EXPERT|SMART)-(\d+\.\d+\.\d+)-win-x64\.zip'),
                                   ('AKTUALIZATOR', r'GRYFSMART-Programator-(\d+\.\d+\.\d+)\.exe')]:
                match = re.fullmatch(pattern, a['name'])
                if match:
                    groups[group].setdefault(match[1], item(match[1], a, r))
            if a['name'] == 'GRYF.rtidriver':
                match = re.search(r'rti-(\d+\.\d+)', r['tag_name'], re.I)
                if match:
                    groups['RTI'].setdefault(match[1], item(match[1], a, r))
            match = re.fullmatch(r'ETH-Mini-GATE-firmware-v(\d+)\.hex', a['name'])
            if match and (not hexes.get('ETH Mini') or int(match[1]) >= int(hexes['ETH Mini']['version'])):
                hexes['ETH Mini'] = item(match[1], a, r)
    manifests = [(r, a) for r in fw for a in r['assets'] if a['name'] == 'gryfsmart-update.json']
    def load_manifest(pair):
        r, a = pair
        path = cache / ('manifest-' + str(a['id']) + '.json') if cache else None
        if path and path.exists():
            data = json.loads(path.read_text(encoding='utf-8'))
        else:
            data = get(a['browser_download_url'])
            if path:
                path.write_text(json.dumps(data), encoding='utf-8')
        return r, data
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        loaded = list(pool.map(load_manifest, manifests))
    for r, manifest in reversed(loaded):
        assets = {a['name']: a for a in r['assets']}
        for program in manifest.get('programs', []):
            name = program.get('asset', program.get('name', ''))
            group = {'GRYFSMART-Programator.exe': 'AKTUALIZATOR', 'GRYFSMART-Instalator.exe': 'BOOTLOADER'}.get(name)
            if group and name in assets:
                version = str(program['version'])
                if version not in groups[group]:
                    # Prefer the full installer ZIP including AVRDUDE/bootloader HEXs.
                    download = assets.get(name.replace('.exe', '.zip'), assets[name]) if group == 'BOOTLOADER' else assets[name]
                    groups[group][version] = item(version, download, r)
        for app in manifest.get('applications', []):
            model = app.get('model', app.get('name'))
            if model in ['R0806T', 'R0808', 'S0804', 'ETH0606T'] and app['asset'] in assets:
                hexes[model] = item(app['version'], assets[app['asset']], r)
    for r in reversed(ha):
        for a in r['assets']:
            match = re.fullmatch(r'GRYFSMART-HomeAssistant-(\d+\.\d+\.\d+)\.zip', a['name'])
            if match:
                groups['HOME-ASSISTANT'].setdefault(match[1], item(match[1], a, r))
    result = {name: sorted(rows.values(), key=lambda row: semver(row['version']), reverse=True)[:3]
              for name, rows in groups.items()}
    for name, rows in result.items():
        for row in rows:
            row['notes'] = NOTES.get((name, row['version']), row['notes'])
    for name, rows in result.items():
        if len(rows) != 3:
            raise ValueError(f'{name}: expected three distinct released versions, got {len(rows)}')
    if len(hexes) != 5:
        raise ValueError(f'Missing module firmware: {list(hexes)}')
    return dict(products=result, firmware=hexes)

def render(out, templates, catalog, mode):
    def write(path, text):
        p = out / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text.rstrip() + '\n', encoding='utf-8')
    products = catalog['products']
    downloads = '| Program / integracja | Najnowsza wersja — pobierz | Instrukcja |\n|---|---|---|\n'
    for path, label in SECTIONS[:5]:
        row = products[path][0]
        downloads += f"| {label} | [**{row['version']} — pobierz**]({row['url']}) | [Otwórz]({BASE}/tree/main/{path}) |\n"
    downloads += f'| 6. Protokół GRYFSMART | [**Opis i przykłady**]({BASE}/tree/main/PROTOKOL) | [Komendy i konfiguracja]({BASE}/tree/main/PROTOKOL) |\n'
    downloads += f'\n**[Najnowsze HEX-y wszystkich modułów]({BASE}/tree/main/HEX)** · **[Protokół i przykłady integracji]({BASE}/tree/main/PROTOKOL)**\n'
    home = '# GRYFSMART — pobieranie i dokumentacja\n\n' + downloads + '\n' + nav()
    home += '\n\nWybierz sekcję: na górze znajdziesz aktualny plik, następnie trzy ostatnie wersje i instrukcję. Program konfiguracyjny jest obecnie wydawany pod nazwą **GRYFEXPERT**.\n'
    home += '\nAktualizator wgrywa aplikację przez istniejący bootloader. Instalator bootloaderów służy do pierwszej instalacji przez ISP/USBasp.\n'
    if mode == 'profile':
        write('README.md', home)
        return
    if mode == 'ha':
        row = products['HOME-ASSISTANT'][0]
        write('README.md', '# GRYFSMART dla Home Assistant\n\n' + f"**[Pobierz najnowszą integrację {row['version']} ZIP]({row['url']})**\n\n" + table(products['HOME-ASSISTANT']) + '\n' + (templates / 'HOME-ASSISTANT.md').read_text(encoding='utf-8') + '\n' + nav())
        return
    write('README.md', home)
    for path, label in SECTIONS[:5]:
        row = products[path][0]
        body = f"# {label}\n\n**[Pobierz najnowszą wersję {row['version']}]({row['url']})**\n\n"
        body += f"{summary(row)} [Pełny opis wydania]({row['release']}).\n\n"
        body += '## Trzy ostatnie wersje\n\n' + table(products[path]) + '\n'
        body += (templates / (path + '.md')).read_text(encoding='utf-8')
        write(path + '/README.md', body + '\n\n' + nav())
    write('PROTOKOL/README.md', (templates / 'PROTOKOL.md').read_text(encoding='utf-8') + '\n\n' + nav())
    hextable = '# Najnowsze HEX-y aplikacji GRYFSMART\n\n| Moduł | Wersja | Pobierz HEX | Wydanie |\n|---|---|---|---|\n'
    for model in ['R0806T', 'R0808', 'S0804', 'ETH0606T', 'ETH Mini']:
        row = catalog['firmware'][model]
        hextable += f"| {model} | {row['version']} | [**Pobierz HEX**]({row['url']}) | [Opis]({row['release']}) |\n"
    hextable += '\nSą to aplikacje modułów. Dobierz model dokładnie; plik aplikacji nie zastępuje bootloadera. [Instrukcja aktualizacji](../AKTUALIZATOR).\n\n' + nav()
    write('HEX/README.md', hextable)
    write('catalog.json', json.dumps(catalog, ensure_ascii=False, indent=2))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=Path('.'))
    parser.add_argument('--templates', type=Path, default=Path(__file__).parent / 'templates')
    parser.add_argument('--cache', type=Path)
    parser.add_argument('--catalog', type=Path)
    parser.add_argument('--mode', choices=['firmware', 'profile', 'ha'], default='firmware')
    args = parser.parse_args()
    data = json.loads(args.catalog.read_text(encoding='utf-8')) if args.catalog else collect(args.cache)
    render(args.out, args.templates, data, args.mode)

if __name__ == '__main__':
    main()
