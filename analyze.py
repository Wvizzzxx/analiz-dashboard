import csv
import os
from collections import Counter, defaultdict

data_dir = r'все данные с выгрузок'

# Sites to analyze
sites = {
    'LSR (www.lsr.ru)': 'referring domains1-www.lsr.csv',
    'ПИК (pik.ru)': 'pik.ru-refdomains1.csv',
    'Эталон (etalongroup.ru)': 'etalongroup.ru-refdomains1.csv',
    'Самолёт (samolet.ru)': 'samolet.ru-refdomains1.csv',
    'СЕТЛ (setlgroup.ru)': 'setlgroup.ru-refdomains1.csv'
}

backlinks_files = {
    'LSR (www.lsr.ru)': 'backlinks1-www.lsr.csv',
    'ПИК (pik.ru)': 'backlinks_pik.ru1.csv',
    'Эталон (etalongroup.ru)': 'etalongroup.ru-backlinks1.csv',
    'Самолёт (samolet.ru)': 'samolet.ru-backlinks1.csv',
    'СЕТЛ (setlgroup.ru)': 'setlgroup.ru-backlinks1.csv'
}

# Known media/news domains for GEO analysis
media_domains_list = ['rbc.ru', 'ria.ru', 'lenta.ru', 'kommersant', 'tass.ru', 'fontanka.ru', 'e1.ru', 'dp.ru',
                      'gazeta.ru', 'iz.ru', 'rt.com', 'bbc.com', 'bbc.co', 'cnn.com', 'forbes', 'wired.com',
                      'numerama.com', 'habr.com', 'vc.ru', 'spark.ru', 'cossa.ru', 'sostav.ru', 'adindex.ru',
                      'rb.ru', 'dtf.ru', 'sports.ru', 'vesti.ru', 'kp.ru', 'mk.ru',
                      'aif.ru', 'echo.msk.ru', 'meduza.io', 'zona.media', 'novayagazeta.ru',
                      'kommersant.ru', 'tinkoff.ru', 'tbank.ru', 'investing.com', 'smartlab.ru',
                      'inosmi.ru', 'gov.ru', 'mos.ru', 'spb.ru', 'regnum.ru', 'rbcgroup']

review_keywords = ['ratingruneta', 'rating', 'review', 'obzor', 'catalog', 'katalog',
                   'reestr', 'reit', 'vsenovostroyki', 'novostroy-m', 'novostroy', 'bazademlin',
                   'domclick', 'cian', 'realty.yandex', 'realty.ru', 'etagi.com']

# Platform classification keywords
platform_categories = {
    'СМИ/Новости': ['rbc', 'ria', 'lenta', 'kommersant', 'tass', 'gazeta', 'iz.ru', 'bbc', 'cnn', 'forbes',
                     'fontanka', 'e1.ru', 'dp.ru', 'vesti', 'kp.ru', 'mk.ru', 'aif', 'regnum', 'rt.com'],
    'Агрегаторы/Площадки': ['cian', 'domclick', 'novostroy-m', 'vsenovostroyki', 'realty.yandex', 'realty.ru',
                             'etagi', 'bazademlin', 'novostroy', 'reestr'],
    'Форумы/Сообщества': ['forum', 'reddit', 'quora', 'habr', 'vc.ru', 'dtf', 'pikabu', 'livejournal',
                           'zen.yandex', 'dzen.ru', 'smartlab'],
    'Финансовые': ['rbc', 'investing', 'tinkoff', 'tbank', 'vtb', 'smartlab', 'forexpf'],
    'Государственные': ['gov.ru', 'mos.ru', 'spb.ru', 'gosuslugi'],
    'Обзорные/Рейтинги': ['ratingruneta', 'rating', 'obzor', 'review', 'vsenovostroyki', 'novostroy-m'],
    'Отраслевые каталоги': ['catalog', 'katalog', 'reestr', 'directory', 'uprock', '1c.ru']
}

def is_media_domain(domain):
    return any(m in domain for m in media_domains_list)

def is_review_domain(domain):
    return any(r in domain for r in review_keywords)

def classify_platform(domain):
    cats = []
    for cat, keywords in platform_categories.items():
        if any(kw in domain for kw in keywords):
            cats.append(cat)
    return cats if cats else ['Другие']

results = {}

for site_key, filename in sites.items():
    filepath = os.path.join(data_dir, filename)
    domains = []
    dr_values = []
    high_dr_domains = []
    media_domains_found = []
    review_domains_found = []
    platform_counts = Counter()
    
    with open(filepath, 'r', encoding='utf-16') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            domain = row.get('Domain', '').strip().strip('"')
            dr = row.get('DR', '').strip().strip('"')
            
            try:
                dr_val = float(dr)
                dr_values.append(dr_val)
                if dr_val >= 70:
                    high_dr_domains.append((domain, dr_val))
                if is_media_domain(domain):
                    media_domains_found.append((domain, dr_val))
                if is_review_domain(domain):
                    review_domains_found.append((domain, dr_val))
                for cat in classify_platform(domain):
                    platform_counts[cat] += 1
            except:
                pass
            domains.append(domain)
    
    total = len(domains)
    avg_dr = sum(dr_values)/len(dr_values) if dr_values else 0
    dr_sorted = sorted(dr_values)
    median_dr = dr_sorted[len(dr_sorted)//2] if dr_sorted else 0
    high_dr_count = len(high_dr_domains)
    
    results[site_key] = {
        'total_domains': total,
        'avg_dr': avg_dr,
        'median_dr': median_dr,
        'high_dr_count': high_dr_count,
        'media_count': len(media_domains_found),
        'media_domains': media_domains_found,
        'review_count': len(review_domains_found),
        'review_domains': review_domains_found,
        'platform_counts': platform_counts,
        'top_domains': sorted(zip(domains, dr_values), key=lambda x: x[1], reverse=True)[:15]
    }

# === Part 2: Backlinks Analysis (anchors, platforms) ===
print('='*80)
print('АНАЛИЗ ССЫЛОЧНЫХ ПРОФИЛЕЙ САЙТОВ НЕДВИЖИМОСТИ')
print('='*80)
print('\nСайты: LSR, ПИК, Эталон, Самолёт, СЕТЛ Груп\n')

print('### 1. СРАВНИТЕЛЬНАЯ ТАБЛИЦА REFERRING DOMAINS ###\n')
header = "{:<35} {:<12} {:<12} {:<12} {:<12} {:<12}".format('Метрика', 'LSR', 'ПИК', 'Эталон', 'Самолёт', 'СЕТЛ')
print(header)
print('-'*95)

site_keys = list(results.keys())
for metric_name, metric_key in [
    ('Referring Domains (всего)', 'total_domains'),
    ('DR средний', 'avg_dr'),
    ('DR медианный', 'median_dr'),
    ('Доменов с DR >= 70', 'high_dr_count'),
    ('Доменов-СМИ', 'media_count'),
    ('Доменов обзорных/рейтинговых', 'review_count'),
]:
    vals = []
    for sk in site_keys:
        v = results[sk][metric_key]
        if isinstance(v, float):
            vals.append(f'{v:.1f}')
        else:
            vals.append(str(v))
    print(f'{metric_name:<35} {vals[0]:<12} {vals[1]:<12} {vals[2]:<12} {vals[3]:<12} {vals[4]:<12}')

print('\n### 2. ПЛАТФОРМЫ И ИХ ТИПЫ (для каждого сайта) ###\n')
for site_key in site_keys:
    r = results[site_key]
    print(f'--- {site_key} ---')
    for platform, count in sorted(r['platform_counts'].items(), key=lambda x: -x[1]):
        print(f'  {platform}: {count}')
    print()

print('\n### 3. ТОП-ДОМЕНА ПО DR (для каждого сайта) ###\n')
for site_key in site_keys:
    r = results[site_key]
    print(f'--- {site_key} ---')
    for d, dr in r['top_domains'][:10]:
        media_tag = ' [СМИ]' if is_media_domain(d) else ''
        review_tag = ' [ОБЗОР]' if is_review_domain(d) else ''
        print(f'  {d:<45} DR={dr:.0f}{media_tag}{review_tag}')
    print()

print('\n### 4. СМИ И ИНФОРМАЦИОННЫЕ РЕСУРСЫ (ключевые для GEO) ###\n')
for site_key in site_keys:
    r = results[site_key]
    print('--- {}: {} доменов СМИ ---'.format(site_key, r['media_count']))
    for d, dr in sorted(r['media_domains'], key=lambda x: -x[1])[:15]:
        print(f'  {d:<45} DR={dr:.0f}')
    print()

# Backlinks platform analysis
print('\n### 5. АНАЛИЗ ПЛАТФОРМ ССЫЛОК (из backlinks) ###\n')
for site_key, filename in backlinks_files.items():
    filepath = os.path.join(data_dir, filename)
    platform_counter = Counter()
    total_backlinks = 0
    nofollow_count = 0
    dofollow_count = 0
    
    with open(filepath, 'r', encoding='utf-16') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            total_backlinks += 1
            platform = row.get('Platform', '').strip().strip('"')
            if platform:
                platform_counter[platform] += 1
            nofollow_val = row.get('Nofollow', '').strip().strip('"')
            if nofollow_val.lower() == 'true':
                nofollow_count += 1
            else:
                dofollow_count += 1
    
    print(f'--- {site_key} ({total_backlinks} backlinks) ---')
    print(f'  Dofollow: {dofollow_count} ({100*dofollow_count/max(total_backlinks,1):.1f}%)')
    print(f'  Nofollow: {nofollow_count} ({100*nofollow_count/max(total_backlinks,1):.1f}%)')
    print(f'  Топ платформ:')
    for plat, cnt in platform_counter.most_common(15):
        print(f'    {plat:<30} {cnt}')
    print()

# === GEO Analysis: key insights for AI models ===
print('\n### 6. GEO-АНАЛИЗ: ПРИОРИТЕТЫ ДЛЯ AI-МОДЕЛЕЙ ###\n')
print('Ключевые площадки, которые индексируются AI-моделями:')
print('  - СМИ (rbc.ru, ria.ru, lenta.ru, kommersant.ru) — высший приоритет')
print('  - Агрегаторы (cian.ru, domclick, novostroy-m.ru) — важны для коммерческих запросов')
print('  - Обзорные/рейтинговые (ratingruneta.ru) — формируют мнение AI')
print('  - Форумы/сообщества (vc.ru, habr.com, pikabu) — упоминания в обсуждениях')
print('  - Wikipedia — базовый источник для верификации')
print()

lsr = results['LSR (www.lsr.ru)']
pik = results['ПИК (pik.ru)']

print('LACUNAS (чего не хватает LSR по сравнению с конкурентами):')
lsr_media = set(d for d, _ in lsr['media_domains'])
pik_media = set(d for d, _ in pik['media_domains'])
missing_media = pik_media - lsr_media
if missing_media:
    print(f'  СМИ, где есть ПИК, но нет LSR: {missing_media}')

print(f'\n  LSR: {lsr["media_count"]} доменов СМИ, {lsr["total_domains"]} всего RD')
print(f'  ПИК: {pik["media_count"]} доменов СМИ, {pik["total_domains"]} всего RD')
print(f'  Разница в RD: {pik["total_domains"] - lsr["total_domains"]} в пользу ПИК')