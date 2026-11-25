"""Render actual stdout screenshots and the Markdown report with Playwright."""
from pathlib import Path
import html
import re
import urllib.request
import markdown
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
STEM = '20261115_ChanJingYi_SUOL2500321_Lab_Assessment_1'
EVIDENCE = ROOT / 'evidence'
BUILD = ROOT / 'build'
BUILD.mkdir(exist_ok=True)
mermaid = BUILD / 'mermaid.min.js'
if not mermaid.exists():
    urllib.request.urlretrieve(
        'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js', mermaid)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(channel='chrome', headless=True)
    page = browser.new_page(viewport={'width': 1050, 'height': 900}, device_scale_factor=2)
    demo = (EVIDENCE / 'demo_output.txt').read_text()
    chunks = re.split(r'(?=^=== TASK )', demo, flags=re.MULTILINE)
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    names = ['01_queue_peek', '02_dequeue_enqueue', '03_stack_peek', '04_stack_pop']
    captures = list(zip(names, chunks))
    captures.append(('05_validation', (EVIDENCE / 'validation_output.txt').read_text().strip()))
    for name, output in captures:
        # Screenshot the unaltered stdout, with a simple evidence heading.
        page.set_content('''<!doctype html><meta charset="utf-8"><style>
            *{box-sizing:border-box}body{margin:0;padding:24px;background:white}
            article{width:1002px;border:1px solid #b6c5d1;border-radius:7px;overflow:hidden}
            header{background:#e9eff4;padding:14px 20px;font:16px Arial;color:#173d57}
            pre{margin:0;padding:20px;font:19px/1.5 "Courier New",monospace;
                color:#182531;background:#fff;white-space:pre}
            </style><article><header>Captured program output | C++17 | BCL1313</header><pre>'''
            + html.escape(output) + '</pre></article>')
        assert page.locator('pre').evaluate('(node) => node.scrollWidth <= node.clientWidth')
        page.locator('article').screenshot(path=str(EVIDENCE / f'{name}.png'))

    source = (ROOT / f'{STEM}.md').read_text()
    sections = []
    for i, section in enumerate(source.split('<!-- page -->')):
        rendered = markdown.markdown(section, extensions=['extra', 'sane_lists'])
        rendered = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>',
                          lambda match: '<div class="mermaid">'
                          + html.escape(html.unescape(match.group(1))) + '</div>',
                          rendered, flags=re.DOTALL)
        sections.append(f'<section class="page {"cover" if i == 0 else ""}">{rendered}</section>')
    css = '''
        *{box-sizing:border-box}body{margin:0;color:#192b3a;font-family:Arial,sans-serif;
        font-size:11pt;line-height:1.5}.page{break-before:page}.page:first-child{break-before:auto}
        h1{font-size:18pt;line-height:1.25;color:#173d57;margin:0 0 5mm;
        padding-bottom:3mm;border-bottom:1px solid #adc0ce;break-after:avoid}
        h2{font-size:12pt;line-height:1.3;color:#173d57;margin:4mm 0 2mm;break-after:avoid}
        p{margin:0 0 3mm;orphans:3;widows:3}table{width:100%;border-collapse:collapse;
        margin:3mm 0;font-size:9.5pt;line-height:1.4;break-inside:avoid}
        th,td{padding:2.2mm 2mm;border:1px solid #bccbd6;text-align:left}
        th{background:#eaf0f5;color:#173d57}tr:nth-child(even){background:#f8fafc}
        pre{background:#f3f6f8;border-left:3px solid #839faf;padding:3mm;
        font:8.8pt/1.4 "Courier New",monospace;white-space:pre-wrap;break-inside:avoid}
        code{font-family:"Courier New",monospace;font-size:9.5pt}pre code{font-size:inherit}
        img{max-width:100%;height:auto;display:block;margin:3mm auto}
        p:has(>em){font-size:9pt;line-height:1.4;color:#4c6070}
        a{color:#173d57;text-decoration:none;overflow-wrap:anywhere}
        .mermaid{text-align:center;margin:2mm 0}.mermaid svg{max-height:100mm;max-width:100%;height:auto}
        .cover{padding:29mm 3mm 0}.cover h1{font-size:29pt;border:0;line-height:1.2;margin-bottom:6mm}
        .cover h2{font-size:19pt;font-weight:normal;line-height:1.35;margin-bottom:12mm}
        .cover p{margin-bottom:8mm;line-height:1.8}.cover p:last-child{margin-top:13mm}
        .page:last-child h2{font-size:11pt;margin-top:3mm;margin-bottom:1.5mm}
        .page:last-child p{font-size:11pt;line-height:1.5;margin-bottom:2.5mm}
        .page:last-child h1:last-of-type ~ p{font-size:9.5pt;line-height:1.4}
        .page:last-child h1:not(:first-child){font-size:14pt;margin-top:5mm;margin-bottom:2mm}
        @media screen{body{width:170mm;margin:0 auto}.page{margin-bottom:15mm}}
    '''
    preview = ROOT / f'{STEM}.html'
    preview.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<title>Restaurant Order Management System</title><style>' + css
        + '</style></head><body>' + ''.join(sections) + '</body></html>')
    page.goto(preview.as_uri(), wait_until='load')
    page.add_script_tag(path=str(mermaid))
    page.evaluate('''async () => {
        mermaid.initialize({startOnLoad:false, theme:'base',
            flowchart:{nodeSpacing:20,rankSpacing:15,padding:7},
            themeVariables:{fontFamily:'Arial',fontSize:'16px',primaryColor:'#eaf0f5',
                primaryTextColor:'#173d57',primaryBorderColor:'#839faf',lineColor:'#49677e'}});
        await mermaid.run({querySelector:'.mermaid'});
        await document.fonts.ready;
        await Promise.all(Array.from(document.images).map(image => image.decode()));
    }''')
    page.wait_for_selector('.mermaid svg', timeout=10000)
    assert page.locator('.mermaid svg').count() == 1
    assert page.locator('img').count() == 5
    # Preserve a preview with the rendered SVG, requiring no CDN for viewing.
    preview.write_text(page.content())
    page.pdf(path=str(ROOT / f'{STEM}.pdf'), format='A4', print_background=True,
        margin={'top':'18mm','right':'20mm','bottom':'18mm','left':'20mm'},
        display_header_footer=True,
        header_template='<div style="width:100%;margin:0 20mm;font-family:Arial;font-size:8px;color:#526a7b;border-bottom:1px solid #bdcbd5;padding-bottom:4px">BCL1313 | ALGORITHMS AND COMPLEXITY<span style="float:right">LAB ASSESSMENT 1</span></div>',
        footer_template='<div style="width:100%;margin:0 20mm;font-family:Arial;font-size:8px;color:#526a7b;border-top:1px solid #bdcbd5;padding-top:5px">Chan Jing Yi | SUOL2500321<span style="float:right"><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
    browser.close()
print(ROOT / f'{STEM}.pdf')
