import pathlib

p = pathlib.Path(r'c:\Users\IG Computer\Desktop\Анализ\Анализ_ссылочной_массы_дашборд.html')
content = p.read_text(encoding='utf-8')

# 1. Remove '(или мало)'
content = content.replace('но нет (или мало) у LSR', 'но нет у LSR')

# 2. Remove 'Почему это важно' paragraph
old1 = (
    '            <div class="text">\n'
    '                Почему это важно: в эпоху AI-поиска (GEO) традиционный SEO дополняется необходимостью присутствовать на\n'
    '                <strong>авторитетных, \u00abдоверенных\u00bb площадках</strong>, которые модели используют как первичные источники.\n'
    '                Ссылка с rbc.ru или habr.com имеет для AI-модели значительно больший вес, чем ссылка с каталога.\n'
    '            </div>'
)
content = content.replace(old1, '')

# 3. Fix English terms
content = content.replace('competitive gaps — Areas', 'слабые стороны')
content = content.replace('competitive gaps', 'слабые стороны')
content = content.replace('Areas, где', 'области, где')
content = content.replace(' (Domain Rating)', ' (рейтинг домена)')
content = content.replace('Детализация competitive gaps', 'Детализация пробелов')

# GEO explanation
content = content.replace(
    '<strong>Что такое GEO?</strong> Generative Engine Optimization — это новый подход к продвижению, при котором оптимизируешься не только под поисковые системы (Google, Яндекс), но и под',
    '<strong>GEO</strong> — подход к продвижению, при котором оптимизируешься не только под поисковые системы (Google, Яндекс), но и под'
)

# Table headers
content = content.replace('Referring Domains (всего)', 'Ссылающиеся домены (всего)')
content = content.replace('DR средний (рейтинг домена)', 'DR средний')

p.write_text(content, encoding='utf-8')
print('Done')