from pathlib import Path
import re, html, markdown, json
ROOT=Path(__file__).resolve().parent.parent
SRC=ROOT/'report_sources'
BASE='20261105_Camu_LMS_Software_Engineering_Report'
main=(SRC/'report.md').read_text()
extra='Evidence should be anonymised and retained only as needed for the assignment, with participants informed about how their responses will be used.'
if extra not in main:
 main=main.replace('Direct responses and stakeholder validation remain necessary to satisfy the brief’s real user requirement.', 'Direct responses and stakeholder validation remain necessary to satisfy the brief’s real user requirement. '+extra)
 (SRC/'report.md').write_text(main)
def words(s):
 s=re.sub(r'```mermaid.*?```','',s,flags=re.S)
 s=re.sub(r'<!--.*?-->|<[^>]+>','',s,flags=re.S)
 s=re.sub(r'^\|[\s:|\-]+\|$','',s,flags=re.M)
 return len(re.findall(r'\S+',re.sub(r'[#|]',' ',s)))
count=words(main)
print('Main report words including headings, tables and captions; excluding diagrams:',count)
assert count==2000,count
# A native SVG preserves standard UML actor and ellipse notation.
svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 660 615" role="img" aria-label="LMS use case diagram">','<style>text{font-family:Times New Roman,serif;fill:#111;font-size:17px} .uc{fill:#f7f9fb;stroke:#222;stroke-width:1.2}.assoc{stroke:#333;stroke-width:1.1;fill:none}</style>','<rect x="100" y="8" width="450" height="600" fill="white" stroke="#222"/>','<text x="325" y="31" text-anchor="middle">Proposed University LMS</text>']
uc=[('Enrol in course','FR1',78),('Publish / access materials','FR2',149),('Submit assignment','FR3',220),('Manage / view assessment','FR4',291),('Course communication','FR5',362),('View / export deadlines','FR6',433),('Verify receipt / download','FR7',504),('Administer courses / users','FR8',575)]
# Associations behind ellipses avoid lines over labels.
for i in [0,1,2,3,4,5,6]:svg.append(f'<path class="assoc" d="M 55 252 L 130 {uc[i][2]}"/>')
for i in [1,3,4]:svg.append(f'<path class="assoc" d="M 598 219 L 520 {uc[i][2]}"/>')
svg.append('<path class="assoc" d="M 598 530 L 520 575"/>')
for label,code,y in uc:
 svg.append(f'<ellipse class="uc" cx="325" cy="{y}" rx="195" ry="27"/>')
 svg.append(f'<text x="325" y="{y-3}" text-anchor="middle">{label}</text><text x="325" y="{y+17}" text-anchor="middle">{code}</text>')
for label,x,y in [('Student',38,250),('Lecturer',615,217),('Administrator',615,528)]:
 svg.append(f'<g class="assoc"><circle cx="{x}" cy="{y-18}" r="9"/><path d="M {x} {y-9} V {y+20} M {x-17} {y+2} H {x+17} M {x} {y+20} L {x-15} {y+40} M {x} {y+20} L {x+15} {y+40}"/></g><text x="{x}" y="{y+59}" text-anchor="middle" style="font-size:15px">{label}</text>')
svg.append('</svg>')
usecase='\n'.join(svg)
(SRC/'use_case.svg').write_text(usecase)
main=main.replace('<div class="figure" id="usecase-placeholder"></div>',f'<div class="figure usecase">\n{usecase}\n</div>')
# Accessible HTML matrix, also included in Markdown as editable source.
matrix=['<div class="riskfigure"><table class="riskmatrix"><thead><tr><th>Likelihood</th>']+[f'<th>Impact {i}</th>' for i in range(1,6)]+['</tr></thead><tbody>']
for likelihood in range(5,0,-1):
 matrix.append(f'<tr><th>{likelihood}</th>')
 for impact in range(1,6):
  score=likelihood*impact; level='high' if score>=15 else 'medium' if score>=8 else 'low'
  ids='R1, R2' if (likelihood,impact)==(3,5) else 'R3, R4' if (likelihood,impact)==(4,4) else 'R5' if (likelihood,impact)==(3,4) else str(score)
  matrix.append(f'<td class="{level}">{ids}</td>')
 matrix.append('</tr>')
matrix.append('</tbody></table><p class="legend">Low: 1 to 7 · Medium: 8 to 14 · High: 15 to 25</p></div>')
main=main.replace('<div class="figure" id="risk-matrix-placeholder"></div>','\n'.join(matrix))
refs=[
('Intellectual Property Corporation of Malaysia (n.d.) <em>Copyright Act</em>. Available at: ', 'https://www.myipo.gov.my/copyright-act/'),
('Kiruba, S. (2026) ‘Review of MyCamu Lite’, <em>Google Play</em>, 3 August. Available at: ', 'https://play.google.com/store/apps/details?id=com.octoze.camu.mycamuapp'),
('OWASP (n.d.) <em>File Upload Cheat Sheet</em>. Available at: ', 'https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html'),
('Personal Data Protection Department (n.d.) <em>Akta Perlindungan Data Peribadi (Pindaan) 2024</em>. Available at: ', 'https://www.pdp.gov.my/akta/akta-pdppindaan-2024/'),
('Punay, A.R. (2026) ‘Submitting Outputs’, <em>Mapúa Malayan Digital College Support</em>, updated 19 June. Available at: ', 'https://support.mmdc.mcl.edu.ph/hc/en-us/articles/17566038499341-Submitting-Outputs'),
('Schwaber, K. and Sutherland, J. (2020) <em>The Scrum Guide</em>. November. Available at: ', 'https://scrumguides.org/scrum-guide.html'),
('Suriyakumar, P. (2021) ‘Review of MyCamu Lite’, <em>Google Play</em>, 10 January. Available at: ', 'https://play.google.com/store/apps/details?id=com.octoze.camu.mycamuapp'),
('W3C (2024) <em>Web Content Accessibility Guidelines (WCAG) 2.2</em>. Recommendation, 12 December. Available at: ', 'https://www.w3.org/TR/WCAG22/')]
refhtml='<h1>References</h1><div class="references">'+''.join(f'<p>{a}<a href="{u}">{u}</a> (Accessed: 5 November 2026).</p>' for a,u in refs)+'</div>'
appendix='''
# Appendix A. Real user elicitation instrument
## A.1 Interview questions
| Item | Question and requirement link |
| :--- | :--- |
| Q1 | What do you use Camu for most often? Which tasks matter most? Scope and priorities. |
| Q2 | Please show how you find a course file or deadline. Where do difficulties occur? FR2 and FR6. |
| Q3 | How do you confirm that your submission was received? What evidence would help? FR3 and FR7. |
| Q4 | How do lecturers manage assignments, grades and messages? Who should access them? FR4 and FR5. |
| Q5 | What happens if your connection fails or the session expires? Describe the device and outcome. NFR2 and NFR6. |
| Q6 | What difficulties arise on a phone, with larger text or assistive technology? NFR5. |

## A.2 Survey and evidence record
Ask respondents to rate the importance of finding materials, viewing deadlines, confirming submissions, protecting grades and receiving messages from 1 (least important) to 5 (most important). Ask separately how often each difficulty occurs and allow an explanation. Do not calculate percentages until responses have been collected.

Record participant code and role, date, consent, task context, anonymised response, interpretation, linked requirement and validation status. Avoid names, passwords, grades or other unnecessary personal information. Invite participants to confirm the interpretation.

## A.3 Outstanding research
Direct SEGi interviews or survey responses have not been supplied. The project summary is preliminary input and the two public reviews are secondary evidence. These sources cannot substitute for conducting the real user elicitation required by the brief. No test execution or prototype evaluation is claimed.
'''
cover='''<div class="cover">
<p>SEGi University</p><p>Faculty of Engineering, Built Environment and Information Technology</p>
<h1>BCL2113 Software Engineering</h1><p>Continuous Assessment: 40%</p>
<h1>Applying Software Engineering Methodologies in LMS Development</h1>
<p class="subtitle">A Camu informed proposal for a private university</p>
<div class="identity"><p>Student name: Chan Jing Yi</p><p>Student ID: SUOL2500321</p><p>Report date: 5 November 2026</p></div>
<p class="count">Main report: 2,000 words<br/>Including headings, tables and captions; excluding diagram labels, references, front matter and Appendix A.</p>
</div>'''
contents='''<h1>Table of contents</h1><div class="contents">
<a href="#page-1"><span>1. Planning and analysis</span><span>1</span></a>
<a href="#page-1"><span>2. Requirements engineering</span><span>1</span></a>
<a class="sub" href="#page-2"><span>Functional requirements and analysis</span><span>2</span></a>
<a class="sub" href="#page-3"><span>Nonfunctional requirements and validation</span><span>3</span></a>
<a href="#page-4"><span>3. Scrum process model</span><span>4</span></a>
<a href="#page-4"><span>4. System design</span><span>4</span></a>
<a href="#page-7"><span>5. Team roles and project planning</span><span>7</span></a>
<a href="#page-8"><span>6. Software quality and testing</span><span>8</span></a>
<a href="#page-9"><span>7. Risk management</span><span>9</span></a>
<a href="#page-10"><span>8. Ethical and legal considerations</span><span>10</span></a>
<a href="#page-11"><span>References</span><span>11</span></a>
<a href="#page-12"><span>Appendix A. Real user elicitation instrument</span><span>12</span></a>
</div><h1>List of figures</h1><div class="contents">
<a href="#page-5"><span>Figure 1. Proposed LMS use case diagram</span><span>5</span></a>
<a href="#page-6"><span>Figure 2. Assignment submission domain classes</span><span>6</span></a>
<a href="#page-9"><span>Figure 3. Likelihood and impact risk matrix</span><span>9</span></a>
</div><h1>List of tables</h1><div class="contents">
<a href="#page-2"><span>Table 1. Functional requirements and acceptance conditions</span><span>2</span></a>
<a href="#page-3"><span>Table 2. Nonfunctional requirements and verification</span><span>3</span></a>
<a href="#page-7"><span>Table 3. Proposed lifecycle timeline</span><span>7</span></a>
<a href="#page-8"><span>Table 4. Submission test cases and expected outcomes</span><span>8</span></a>
<a href="#page-9"><span>Table 5. Risk responses and owners</span><span>9</span></a>
</div>'''
css='''
@font-face{font-family:ReportTimes;src:url("file:///System/Library/Fonts/Supplemental/Times%20New%20Roman.ttf");font-weight:400}
@font-face{font-family:ReportTimes;src:url("file:///System/Library/Fonts/Supplemental/Times%20New%20Roman%20Bold.ttf");font-weight:700}
@font-face{font-family:ReportTimes;src:url("file:///System/Library/Fonts/Supplemental/Times%20New%20Roman%20Italic.ttf");font-style:italic}
@page{size:A4;margin:0}*{box-sizing:border-box}html,body{margin:0;padding:0;background:#e5e5e5;font-family:ReportTimes,"Times New Roman",serif;font-size:12pt;color:#111}
.sheet{width:210mm;height:297mm;background:white;margin:0 auto;position:relative;break-after:page;padding:19mm 20mm 18mm;overflow:hidden}.sheet:last-of-type{break-after:auto}
.header{height:8mm;position:absolute;left:20mm;right:20mm;top:8mm;border-bottom:.5pt solid #aaa;font-size:10pt;display:flex;justify-content:space-between;align-items:flex-start}
.content{height:260mm;position:relative}h1,h2,h3{font-size:14pt;font-weight:700;line-height:1.25;margin:0 0 9pt}h1:not(:first-child){margin-top:15pt}h2{margin-top:11pt}p{font-size:12pt;line-height:1.5;margin:0 0 9pt;text-align:justify;orphans:2;widows:2}
.footer{position:absolute;bottom:8mm;left:20mm;right:20mm;border-top:.5pt solid #aaa;padding-top:4pt;display:flex;justify-content:space-between;font-size:10pt}
table{width:100%;border-collapse:collapse;margin:6pt 0 11pt;table-layout:fixed;font-size:12pt;line-height:1.25}th,td{padding:6pt;border:.5pt solid #888;vertical-align:top;font-weight:400;overflow-wrap:break-word}th{font-weight:700;background:#edf1f5}table p{line-height:1.25;margin:0}th:first-child,td:first-child{width:17%}thead{display:table-header-group}tr{break-inside:avoid}.caption{font-size:12pt;font-weight:700;line-height:1.3;margin:8pt 0}a{color:inherit;text-decoration:none;overflow-wrap:anywhere}
.cover{text-align:center;padding-top:12mm}.cover p{text-align:center;margin-bottom:17pt}.cover h1{font-size:14pt;line-height:1.5;margin:23pt 0}.cover .identity{margin-top:28mm}.cover .identity p{margin-bottom:8pt}.cover .count{margin-top:23mm;line-height:1.5}
.contents{margin-bottom:16pt}.contents a{display:flex;justify-content:space-between;gap:8pt;margin:0 0 5pt;font-size:12pt;line-height:1.25}.contents a span:first-child{flex:1;border-bottom:1px dotted #aaa}.contents a.sub{padding-left:14pt}.contents a span:last-child{min-width:16pt;text-align:right}.figure svg{width:100%;height:auto;display:block;margin:auto}.usecase svg{max-height:175mm}.mermaid svg{max-width:100%!important;max-height:166mm!important;width:100%!important;height:auto!important}.mermaid{margin:4mm 0}.mermaid .nodeLabel,.mermaid text{font-family:ReportTimes,"Times New Roman",serif!important}.references p{text-align:left;padding-left:20pt;text-indent:-20pt;line-height:1.5;margin-bottom:10pt}.riskmatrix{text-align:center;margin-top:12pt}.riskmatrix th,.riskmatrix td{font-size:12pt;padding:8pt 3pt;text-align:center}.riskmatrix th:first-child,.riskmatrix td:first-child{width:20%}.low{background:#eef4ee}.medium{background:#f8f0d8}.high{background:#f5dddd}.legend{text-align:center;margin-bottom:10pt}
#page-8 th:nth-child(1),#page-8 td:nth-child(1){width:20%}#page-8 th:nth-child(2),#page-8 td:nth-child(2){width:37%}#page-8 th:nth-child(3),#page-8 td:nth-child(3){width:43%}
#page-9 .content > table th:nth-child(1),#page-9 .content > table td:nth-child(1){width:26%}#page-9 .content > table th:nth-child(2),#page-9 .content > table td:nth-child(2){width:20%}#page-9 .content > table th:nth-child(3),#page-9 .content > table td:nth-child(3){width:54%}
@media print{html,body{background:white}.sheet{margin:0;box-shadow:none}}
'''
def render_md(text):
 def m(m):return '<div class="mermaid">'+html.escape(m.group(1).strip())+'</div>'
 text=re.sub(r'```mermaid\n(.*?)```',m,text,flags=re.S)
 return markdown.markdown(text,extensions=['tables'])
def sheet(body,num,kind='main'):
 ident='cover' if kind=='cover' else 'contents' if kind=='contents' else 'page-'+str(num)
 return f'<section class="sheet {kind}" id="{ident}"><div class="header"><span>BCL2113 Software Engineering</span><span>Chan Jing Yi | SUOL2500321</span></div><div class="content">{body}</div><footer class="footer"><span>Chan Jing Yi | SUOL2500321</span><span>{num if kind!="cover" else ""}</span></footer></section>'
parts=re.split(r'<!-- page: (\d+) -->',main)
pages=[sheet(cover,'','cover'),sheet(contents,'i','contents')]
for i in range(1,len(parts),2):pages.append(sheet(render_md(parts[i+1]),int(parts[i])))
pages.append(sheet(refhtml,11));pages.append(sheet(render_md(appendix),12,'appendix'))
script='''<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11.12.1/dist/mermaid.esm.min.mjs';
try { mermaid.initialize({startOnLoad:false,securityLevel:'loose',theme:'neutral',fontFamily:'Times New Roman',themeVariables:{fontFamily:'Times New Roman',fontSize:'18px'},class:{useMaxWidth:true,hideEmptyMembersBox:true}}); await mermaid.run({querySelector:'.mermaid'}); await document.fonts.ready; window.reportReady=true; } catch(e){ window.reportError=String(e); }
</script>'''
htmlpage='<!doctype html><html><head><meta charset="utf-8"><title>LMS Software Engineering Report</title><style>'+css+'</style></head><body>'+''.join(pages)+script+'</body></html>'
(ROOT/(BASE+'.html')).write_text(htmlpage)
refsmd='\n# References\n\n'+'\n\n'.join(re.sub('<[^>]+>','',a)+u+' (Accessed: 5 November 2026).' for a,u in refs)
source='# Applying Software Engineering Methodologies in LMS Development\n\nChan Jing Yi | SUOL2500321 | BCL2113 Software Engineering\n\nMain report: 2,000 words. Count includes headings, tables and captions, and excludes diagram labels, front matter, references and Appendix A.\n\n'+main+refsmd+'\n\n'+appendix
(ROOT/(BASE+'.md')).write_text(source)
(SRC/'word_count.json').write_text(json.dumps({'main_report_words':count,'method':'Whitespace separated words in main report headings, prose, tables and captions; excludes diagrams, front matter, references and appendix.'},indent=2))
print(ROOT/(BASE+'.html'))
