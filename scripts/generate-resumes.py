"""Generate both selectable-text resumes from the website's canonical profile."""
import json
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, KeepTogether, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
profile=json.loads((ROOT/'src/data/profile.json').read_text(encoding='utf-8'))
projects=json.loads((ROOT/'src/data/projects.json').read_text(encoding='utf-8'))
out=ROOT/'public/resumes';out.mkdir(parents=True,exist_ok=True)
def clean(s):
    return escape(s.replace('–','-').replace('—','-').replace('’',"'").replace('·',' | '))
def generate(designed):
    accent=colors.HexColor('#156f70') if designed else colors.black
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='NameR',fontName='Helvetica-Bold',fontSize=26 if designed else 23,leading=30,textColor=accent,spaceAfter=9))
    styles.add(ParagraphStyle(name='RoleR',fontName='Helvetica',fontSize=10.5,leading=15,spaceAfter=8))
    styles.add(ParagraphStyle(name='TextR',fontName='Helvetica',fontSize=9,leading=13,spaceAfter=6))
    styles.add(ParagraphStyle(name='SectionR',fontName='Helvetica-Bold',fontSize=13,leading=17,textColor=accent,spaceBefore=16,spaceAfter=10))
    styles.add(ParagraphStyle(name='JobR',fontName='Helvetica-Bold',fontSize=10,leading=14,spaceBefore=9,spaceAfter=4,keepWithNext=True))
    styles.add(ParagraphStyle(name='MetaR',fontName='Helvetica',fontSize=8.5,leading=12,textColor=colors.HexColor('#44515b'),spaceAfter=7,keepWithNext=True))
    styles.add(ParagraphStyle(name='BulletR',fontName='Helvetica',fontSize=9,leading=13,leftIndent=10,firstLineIndent=-8,spaceAfter=4))
    story=[]
    def para(s,kind='TextR'):return Paragraph(clean(s),styles[kind])
    def add(s,kind='TextR'):story.append(para(s,kind))
    add(profile['name'].upper(),'NameR');add(profile['title'],'RoleR')
    add(f"{profile['location']} | {profile['email']} | {profile['phone']}")
    add('linkedin.com/in/rsks | romanysamir.com')
    add('PROFILE','SectionR');add(profile['summary'])
    add('PROFESSIONAL EXPERIENCE','SectionR')
    for e in profile['experience']:
        add(e['role'],'JobR');add(f"{e['company']} | {e['dates']}",'MetaR')
        for line in e['details']:add('- '+line,'BulletR')
    story.append(PageBreak())
    add('SELECTED PROJECTS','SectionR')
    for p in projects:
        if p['slug'] not in ['interactive-museum','prime-press-e-kit','pushcraft','mobile-3d-map','unity-tools','educational-content']:continue
        story.append(KeepTogether([para(p['name']+' | '+p['status'],'JobR'),para(p['summary'])]))
    add('TECHNICAL SKILLS','SectionR')
    for s in profile['skills']:add(s['name'],'JobR');add(', '.join(s['items']))
    story.append(PageBreak())
    add('EDUCATION','SectionR')
    for e in profile['education']:
        story.append(KeepTogether([para(e['qualification'],'JobR'),para(f"{e['school']} | {e['dates']}"),para(e['note'])]))
    add('CERTIFICATIONS','SectionR')
    for c in profile['certifications']:add(f"{c['name']} - {c['issuer']} | {c['date']}")
    add('LANGUAGES','SectionR')
    for l in profile['languages']:add(l)
    name='Romany_Samir_Professional.pdf' if designed else 'Romany_Samir_ATS.pdf'
    def page(canvas,doc):
        canvas.saveState()
        if designed:
            canvas.setFillColor(accent);canvas.rect(0,A4[1]-10,A4[0],10,fill=1,stroke=0)
        canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#64717a'))
        canvas.drawString(44,28,'Romany Samir | Software Engineering & Interactive Media')
        canvas.drawRightString(A4[0]-44,28,str(doc.page));canvas.restoreState()
    doc=SimpleDocTemplate(str(out/name),pagesize=A4,rightMargin=44,leftMargin=44,topMargin=38,bottomMargin=45,title='Romany Samir - Professional Resume',author='Romany Samir')
    doc.build(story,onFirstPage=page,onLaterPages=page)
    reader=PdfReader(out/name);text='\n'.join(p.extract_text() for p in reader.pages)
    assert all(x in text for x in ['TE Data','Future Academy','Prime Press','Elkhalig','Master','Completion status'])
    assert len(text)>5000
    print(name,len(reader.pages),'pages; verified selectable text and complete career history')
generate(False);generate(True)
