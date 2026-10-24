from pathlib import Path
import html
import markdown
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
NAME = 'ChanJingYi_SUOL2500321_Proposal'
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)

def label(x, y, text, size=16, weight='normal', fill='#26384a'):
    return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}">{html.escape(text)}</text>'

parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="355" viewBox="0 0 900 355"><rect width="900" height="355" fill="white"/>']
for x, title in [(8, 'Spending diary'), (308, 'Weekly summary'), (608, 'Weekly budget')]:
    parts.append(f'<rect x="{x}" y="8" width="280" height="337" rx="12" fill="#f7f9fc" stroke="#bbc7d2" stroke-width="2"/>')
    parts.append(f'<rect x="{x}" y="8" width="280" height="56" rx="12" fill="#173d57"/>')
    parts.append(label(x+18, 43, title, 21, 'bold', 'white'))
parts += [label(26,94,'19-25 October 2026',16,'bold'), label(26,123,'Recorded total: RM160.00',17,'bold'),
 label(26,164,'Lunch / Food and Drinks',15),label(26,188,'22 Oct                         RM12.00',15),
 label(26,226,'Earlier entries           RM148.00',15),
 '<rect x="26" y="253" width="244" height="39" rx="6" fill="#173d57"/>',label(90,279,'+ Add expense',16,'bold','white'),
 label(26,324,'Diary     Summary     Budget',15,'bold'),
 label(326,94,'19-25 October 2026',16,'bold'),label(326,125,'Total: RM160.00',19,'bold'),
 label(326,158,'Food and Drinks  RM64 / 40%',14),
 '<rect x="326" y="168" width="220" height="14" rx="3" fill="#dce5ed"/><rect x="326" y="168" width="88" height="14" rx="3" fill="#173d57"/>',
 label(326,205,'Other categories: RM96 / 60%',14),label(326,239,'Previous week: RM180.00',15),
 label(326,267,'RM20 less recorded (11.1%)',15,'bold'),label(326,304,'Tap a category to view entries',13),
 label(626,94,'Weekly limit: RM200.00',17,'bold'),label(626,127,'Recorded: RM160.00',16),
 '<rect x="626" y="147" width="240" height="20" rx="5" fill="#dce5ed"/><rect x="626" y="147" width="192" height="20" rx="5" fill="#a76c17"/>',
 label(626,201,'80% used',22,'bold','#86540b'),label(626,233,'RM40.00 remaining',17,'bold'),
 label(626,267,'Based on your saved entries',14),label(626,310,'Edit weekly budget',16,'bold'),'</svg>']
(ASSETS/'spending_diary_wireframes.svg').write_text(''.join(parts), encoding='utf-8')

source = (ROOT/f'{NAME}.md').read_text(encoding='utf-8')
pages = source.split('<!-- page -->')
sections=[]
for i, text in enumerate(pages):
    content=markdown.markdown(text, extensions=['extra','sane_lists'])
    content=content.replace('<p><em>Figure ', '<p class="caption"><em>Figure ')
    sections.append(f'<section class="page {"cover" if i==0 else ""}">{content}</section>')
css='''
*{box-sizing:border-box}body{margin:0;color:#202a34;font-family:Arial,sans-serif;font-size:11pt;line-height:1.5}
.page{break-before:page}.page:first-child{break-before:auto}
h1{font-size:17pt;color:#173d57;margin:0 0 5mm;line-height:1.22;border-bottom:1px solid #b8c7d3;padding-bottom:3mm}
h2{font-size:12.5pt;color:#173d57;margin:5mm 0 2.5mm;line-height:1.3;break-after:avoid}
h3{font-size:11pt;color:#173d57;margin:3.2mm 0 1.6mm;line-height:1.3;break-after:avoid}
p{margin:0 0 3.1mm;orphans:3;widows:3}a{color:#173d57;overflow-wrap:anywhere;text-decoration:none}
img{display:block;width:100%;height:auto;margin:3mm 0}p:has(img){margin-bottom:1mm}
p.caption{font-size:9pt;line-height:1.4;color:#4b5b68;margin-bottom:4mm}
.cover{padding:30mm 4mm 0}.cover h1{font-size:34pt;letter-spacing:-1px;border:0;margin:0;padding:0}
.cover h2{font-size:18pt;font-weight:normal;line-height:1.35;margin:5mm 0 14mm;max-width:145mm}
.cover p{line-height:1.8;margin-bottom:8mm}.cover p:first-of-type{color:#173d57;font-size:13pt;margin-bottom:18mm}
'''
document='<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Where Did My Money Go? - Project Proposal</title><style>'+css+'</style></head><body>'+''.join(sections)+'</body></html>'
html_path=ROOT/f'{NAME}.html'
html_path.write_text(document,encoding='utf-8')
with sync_playwright() as p:
    browser=p.chromium.launch(channel='chrome',headless=True)
    page=browser.new_page()
    page.goto(html_path.as_uri(),wait_until='load')
    page.evaluate('document.fonts.ready')
    page.locator('img').evaluate_all('(imgs)=>Promise.all(imgs.map(i=>i.decode()))')
    page.pdf(path=str(ROOT/f'{NAME}.pdf'),format='A4',print_background=True,
        margin={'top':'19mm','right':'20mm','bottom':'20mm','left':'20mm'},
        display_header_footer=True,
        header_template='<div style="width:100%;margin:0 20mm;font-family:Arial;font-size:8px;color:#5b6c7b;border-bottom:1px solid #c6d1d9;padding-bottom:4px">BCL2344 - WEB AND MOBILE DEVELOPMENT<span style="float:right">PROJECT PROPOSAL</span></div>',
        footer_template='<div style="width:100%;margin:0 20mm;font-family:Arial;font-size:8px;color:#5b6c7b;border-top:1px solid #c6d1d9;padding-top:5px">Chan Jing Yi | SUOL2500321<span style="float:right"><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
    browser.close()
print(ROOT/f'{NAME}.pdf')
