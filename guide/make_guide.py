# Generates NPC_Quest_Guide.fodt (LibreOffice flat ODT). Run: python make_guide.py
from xml.sax.saxutils import escape as e

from rows import ROWS


def p(text, style="T"):
    return f'<text:p text:style-name="{style}">{e(text)}</text:p>'


def cell(inner, style="C"):
    return f'<table:table-cell table:style-name="{style}" office:value-type="string">{inner}</table:table-cell>'


def steps_cell(steps):
    items = "".join(f'<text:list-item>{p(s)}</text:list-item>' for s in steps)
    return cell(f'<text:list text:style-name="L">{items}</text:list>')


def next_cell(txt):
    return cell("".join(p(l, "W" if l.startswith("Missable") else "T") for l in txt.split("\n")))


def row(r):
    npc, meet, steps, nxt = r
    return ('<table:table-row>' + cell(p(npc, "N")) + cell(p(meet))
            + steps_cell(steps) + next_cell(nxt) + '</table:table-row>')


def table(name, style, rows):
    hdr = "".join(cell(p(h, "HT"), "H") for h in ("NPC", "Where to meet", "What to do", "Where they go next"))
    return (f'<table:table table:name="{name}" table:style-name="{style}">'
            '<table:table-column table:style-name="c1"/><table:table-column table:style-name="c2"/>'
            '<table:table-column table:style-name="c3"/><table:table-column table:style-name="c4"/>'
            f'<table:table-header-rows><table:table-row>{hdr}</table:table-row></table:table-header-rows>'
            + "".join(row(r) for r in rows) + '</table:table>')


SPLIT = 6  # rows on page 1; rest on page 2

HEAD = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" office:version="1.3" office:mimetype="application/vnd.oasis.opendocument.text">
<office:font-face-decls><style:font-face style:name="Liberation Sans" svg:font-family="'Liberation Sans'"/></office:font-face-decls>
<office:styles>
<style:default-style style:family="paragraph"><style:text-properties style:font-name="Liberation Sans" fo:font-size="7.5pt"/></style:default-style>
<style:style style:name="Title" style:family="paragraph"><style:paragraph-properties fo:margin-bottom="0.03in" fo:text-align="center"/><style:text-properties fo:font-size="14pt" fo:font-weight="bold"/></style:style>
<style:style style:name="Sub" style:family="paragraph"><style:paragraph-properties fo:margin-bottom="0.06in" fo:text-align="center"/><style:text-properties fo:font-size="7.5pt" fo:font-style="italic"/></style:style>
<style:style style:name="T" style:family="paragraph"><style:paragraph-properties fo:margin="0in"/></style:style>
<style:style style:name="N" style:family="paragraph"><style:paragraph-properties fo:margin="0in"/><style:text-properties fo:font-weight="bold" fo:font-size="9pt"/></style:style>
<style:style style:name="W" style:family="paragraph"><style:paragraph-properties fo:margin-top="0.03in"/><style:text-properties fo:font-weight="bold"/></style:style>
<style:style style:name="HT" style:family="paragraph"><style:paragraph-properties fo:margin="0in"/><style:text-properties fo:font-weight="bold" fo:color="#ffffff" fo:font-size="9pt"/></style:style>
<style:style style:name="Foot" style:family="paragraph"><style:paragraph-properties fo:margin-top="0.08in"/><style:text-properties fo:font-size="8pt"/></style:style>
<text:list-style style:name="L"><text:list-level-style-number text:level="1" style:num-suffix="." style:num-format="1"><style:list-level-properties text:list-level-position-and-space-mode="label-alignment"><style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="0.14in" fo:text-indent="-0.14in" fo:margin-left="0.14in"/></style:list-level-properties></text:list-level-style-number></text:list-style>
</office:styles>
<office:automatic-styles>
<style:page-layout style:name="pm1"><style:page-layout-properties fo:page-width="8.5in" fo:page-height="11in" fo:margin-top="0.4in" fo:margin-bottom="0.4in" fo:margin-left="0.45in" fo:margin-right="0.45in"/></style:page-layout>
<style:style style:name="TB" style:family="table"><style:table-properties style:width="7.6in" table:align="margins"/></style:style>
<style:style style:name="TB2" style:family="table"><style:table-properties style:width="7.6in" table:align="margins" fo:break-before="page"/></style:style>
<style:style style:name="c1" style:family="table-column"><style:table-column-properties style:column-width="0.95in"/></style:style>
<style:style style:name="c2" style:family="table-column"><style:table-column-properties style:column-width="1.45in"/></style:style>
<style:style style:name="c3" style:family="table-column"><style:table-column-properties style:column-width="3.5in"/></style:style>
<style:style style:name="c4" style:family="table-column"><style:table-column-properties style:column-width="1.7in"/></style:style>
<style:style style:name="C" style:family="table-cell"><style:table-cell-properties fo:padding="0.035in" fo:border="0.5pt solid #808080"/></style:style>
<style:style style:name="H" style:family="table-cell"><style:table-cell-properties fo:padding="0.035in" fo:border="0.5pt solid #808080" fo:background-color="#3b3b3b"/></style:style>
</office:automatic-styles>
<office:master-styles><style:master-page style:name="Standard" style:page-layout-name="pm1"/></office:master-styles>
<office:body><office:text>
'''

doc = (HEAD
       + p("Elden Ring NPC Quest Guide", "Title")
       + p("Base game, no spoilers. Rest at a grace or leave and return to an area to advance an NPC. Steps are in order; talk to each NPC until their dialogue runs out.", "Sub")
       + table("Page1", "TB", ROWS[:SPLIT])
       + table("Page2", "TB2", ROWS[SPLIT:])
       + p("Source: game-checklists.com/elden-ring/all-quests. Quests can conflict with each other; DLC and spoiler-heavy questlines are left out.", "Foot")
       + '</office:text></office:body></office:document>')

open("NPC_Quest_Guide.fodt", "w", encoding="utf-8").write(doc)
