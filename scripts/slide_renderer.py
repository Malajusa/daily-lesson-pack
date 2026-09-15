from __future__ import annotations

from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Iterable
import hashlib
import math
import re

from pptx import Presentation
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE, MSO_VERTICAL_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

from slide_render_model import BlockKind, ContentBlock, RenderPack, SlideRole, SlideSpec

FONT = "Trebuchet MS"
SLIDE_W = 13.333
SLIDE_H = 7.5
RAIL_W = 0.18
LEFT = 0.72
RIGHT = 0.55
TOP_CONTENT = 1.50
BOTTOM = 0.38

ROLE_STYLE = {
    SlideRole.REMINDER: {"panel": "FFF3BF", "accent": "D6A900"},
    SlideRole.MODEL: {"panel": "FFF3BF", "accent": "D6A900"},
    SlideRole.WORKED_EXAMPLE: {"panel": "FFF3BF", "accent": "D6A900"},
    SlideRole.QUESTION: {"panel": "EAF2F8", "accent": "005A9C"},
    SlideRole.READING: {"panel": "EAF2F8", "accent": "005A9C"},
    SlideRole.MORNING_WORK: {"panel": "EAF2F8", "accent": "005A9C"},
    SlideRole.ANSWER: {"panel": "EAF7EE", "accent": "1B7F3A"},
    SlideRole.SUCCESS_CRITERIA: {"panel": "EAF7EE", "accent": "1B7F3A"},
    SlideRole.TRANSITION: {"panel": "FFFFFF", "accent": "103A5E"},
}

LAYOUT_BY_ROLE = {
    SlideRole.QUESTION: "question-primary-v1",
    SlideRole.ANSWER: "answer-primary-v1",
    SlideRole.READING: "reading-measure-v1",
    SlideRole.MORNING_WORK: "morning-work-split-v1",
    SlideRole.SUCCESS_CRITERIA: "success-checklist-v1",
    SlideRole.WORKED_EXAMPLE: "worked-example-v1",
    SlideRole.MODEL: "model-paragraph-v1",
    SlideRole.REMINDER: "reminder-primary-v1",
    SlideRole.TRANSITION: "transition-v1",
}


def _rgb(hexstr: str) -> RGBColor:
    return RGBColor.from_string(hexstr)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass
class SlideRenderRecord:
    slide_number: int
    slide_id: str
    instance_id: str
    role: str
    layout_id: str
    source_blocks: list[str]
    shape_bindings: list[dict]
    groups: dict[str, dict] = field(default_factory=dict)
    metadata_labels: list[str] = field(default_factory=list)
    structural_text: list[dict] = field(default_factory=list)


@dataclass
class RenderManifest:
    schema_version: int
    renderer: str
    renderer_version: str
    slides: list[SlideRenderRecord]
    deck_sha256: str | None = None

    def to_dict(self) -> dict:
        return {
            "schema_version": self.schema_version,
            "renderer": self.renderer,
            "renderer_version": self.renderer_version,
            "deck_sha256": self.deck_sha256,
            "slides": [asdict(s) for s in self.slides],
        }


def estimate_text_lines(text: str, width_inches: float, font_pt: int) -> int:
    # Conservative deterministic approximation tuned for Trebuchet on 16:9 slides.
    if width_inches <= 0:
        return 999
    chars_per_line = max(8, int(width_inches * (96.0 / max(font_pt, 1))))
    lines = 0
    for raw in text.splitlines() or [text]:
        words = raw.split()
        if not words:
            lines += 1
            continue
        current = 0
        line_count = 1
        for word in words:
            needed = len(word) + (1 if current else 0)
            if current + needed > chars_per_line:
                line_count += 1
                current = len(word)
            else:
                current += needed
        lines += line_count
    return max(1, lines)


def choose_font_size(text: str, role: SlideRole, width_inches: float, height_inches: float) -> int:
    floors = {
        SlideRole.READING: 28,
        SlideRole.MODEL: 28,
        SlideRole.SUCCESS_CRITERIA: 28,
        SlideRole.WORKED_EXAMPLE: 30,
        SlideRole.MORNING_WORK: 26,
        SlideRole.QUESTION: 36,
        SlideRole.ANSWER: 36,
        SlideRole.REMINDER: 30,
        SlideRole.TRANSITION: 30,
    }
    floor = floors[role]
    if role is SlideRole.ANSWER and len(text.strip()) <= 18:
        candidates = [54, 52, 48, 44, 40, 36]
    elif role is SlideRole.QUESTION and len(text.strip()) <= 60:
        candidates = [46, 44, 42, 40, 38, 36]
    elif role in {SlideRole.READING, SlideRole.MODEL}:
        candidates = [32, 30, 28]
    elif role is SlideRole.MORNING_WORK:
        candidates = [32, 30, 28, 26]
    elif role is SlideRole.SUCCESS_CRITERIA:
        candidates = [32, 30, 28]
    else:
        candidates = list(range(max(floor, 40), floor - 1, -2))
    for pt in candidates:
        lines = estimate_text_lines(text, width_inches, pt)
        line_height_in = pt / 72 * 1.24
        if lines * line_height_in <= height_inches:
            return max(pt, floor)
    return floor


def panel_height_for_lines(lines: int, font_pt: int, *, min_height: float, max_height: float) -> float:
    return min(max_height, max(min_height, lines * (font_pt / 72.0) * 1.28 + 0.48))


def split_paragraph_for_projection(text: str, *, max_chars: int = 520) -> tuple[str, ...]:
    text = " ".join(text.split())
    if len(text) <= max_chars:
        return (text,)
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks: list[str] = []
    current = ""
    for sentence in sentences:
        if not sentence:
            continue
        trial = f"{current} {sentence}".strip()
        if current and len(trial) > max_chars:
            chunks.append(current)
            current = sentence
        elif len(sentence) > max_chars:
            words = sentence.split()
            for word in words:
                trial2 = f"{current} {word}".strip()
                if current and len(trial2) > max_chars:
                    chunks.append(current)
                    current = word
                else:
                    current = trial2
        else:
            current = trial
    if current:
        chunks.append(current)
    return tuple(chunks)


def _add_rail(slide, spec: SlideSpec):
    rail = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(RAIL_W), Inches(SLIDE_H))
    rail.name = f"DLP:rail:{spec.id}"
    rail.fill.solid(); rail.fill.fore_color.rgb = _rgb(ROLE_STYLE[spec.role]["accent"])
    rail.line.fill.background()
    return rail


def _add_text(slide, text: str, x: float, y: float, w: float, h: float, *, font_pt: int, bold: bool=False,
              color: str="17324D", align=PP_ALIGN.LEFT, valign=MSO_VERTICAL_ANCHOR.TOP, name: str | None=None,
              margins=(0.06,0.06,0.04,0.04)):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        shape.name = name
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.vertical_anchor = valign
    tf.margin_left = Inches(margins[0]); tf.margin_right = Inches(margins[1]); tf.margin_top = Inches(margins[2]); tf.margin_bottom = Inches(margins[3])
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    p.space_after = Pt(0)
    for run in p.runs:
        run.font.name = FONT
        run.font.size = Pt(font_pt)
        run.font.bold = bold
        run.font.color.rgb = _rgb(color)
    return shape


def _add_panel(slide, x: float, y: float, w: float, h: float, *, fill_hex: str, accent_hex: str | None=None, name: str | None=None, radius=True):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    panel = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        panel.name = name
    panel.fill.solid(); panel.fill.fore_color.rgb = _rgb(fill_hex)
    panel.line.color.rgb = _rgb(accent_hex or fill_hex)
    panel.line.width = Pt(1.2)
    return panel


def _header(slide, spec: SlideSpec, record: SlideRenderRecord):
    accent = ROLE_STYLE[spec.role]["accent"]
    eyebrow = _add_text(slide, spec.eyebrow, LEFT, 0.35, 7.7, 0.33, font_pt=16, bold=True, color=accent,
                        name=f"DLP:meta:eyebrow:{spec.id}")
    title = _add_text(slide, spec.title, LEFT, 0.69, 11.5, 0.62, font_pt=28, bold=True, color="17324D",
                     name=f"DLP:meta:title:{spec.id}")
    record.metadata_labels.extend([spec.eyebrow, spec.title])
    record.structural_text.extend([
        {"shape_id": eyebrow.shape_id, "shape_name": eyebrow.name, "text": spec.eyebrow, "kind": "eyebrow"},
        {"shape_id": title.shape_id, "shape_name": title.name, "text": spec.title, "kind": "title"},
    ])
    return eyebrow, title


def _bind(record: SlideRenderRecord, shape, block: ContentBlock, *, split_index: int | None=None):
    source_id = block.id if split_index is None else f"{block.id}#part{split_index}"
    record.shape_bindings.append({
        "source_block_id": source_id,
        "source_task_id": block.source_task_id,
        "source_field": block.source_field,
        "shape_id": shape.shape_id,
        "shape_name": shape.name,
    })
    if source_id not in record.source_blocks:
        record.source_blocks.append(source_id)


def _new_slide(prs: Presentation, spec: SlideSpec, slide_number: int, layout_id: str) -> tuple[object, SlideRenderRecord]:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_rail(slide, spec)
    record = SlideRenderRecord(slide_number, spec.id, spec.instance_id, spec.role.value, layout_id, [], [])
    _header(slide, spec, record)
    return slide, record


def _render_question(prs, spec: SlideSpec, slide_number: int):
    slide, rec = _new_slide(prs, spec, slide_number, "question-primary-v1")
    main = spec.blocks[0]
    max_w = 11.45
    pt = choose_font_size(main.text, SlideRole.QUESTION, max_w-0.5, 3.9)
    lines = estimate_text_lines(main.text, max_w-0.5, pt)
    h = panel_height_for_lines(lines, pt, min_height=1.65, max_height=3.25)
    _add_panel(slide, LEFT, TOP_CONTENT, max_w, h, fill_hex=ROLE_STYLE[spec.role]["panel"], accent_hex=ROLE_STYLE[spec.role]["accent"], name=f"DLP:panel:{spec.id}:primary")
    sh = _add_text(slide, main.text, LEFT+0.28, TOP_CONTENT+0.22, max_w-0.56, h-0.44, font_pt=pt, bold=True,
                   name=f"DLP:block:{main.id}")
    _bind(rec, sh, main)
    y = TOP_CONTENT+h+0.25
    for block in spec.blocks[1:]:
        h2=1.0
        _add_panel(slide,LEFT,y,max_w,h2,fill_hex="FFFFFF",accent_hex="CBD5E1",name=f"DLP:panel:{spec.id}:support")
        sh2=_add_text(slide,block.text,LEFT+0.25,y+0.16,max_w-0.5,h2-0.3,font_pt=30,name=f"DLP:block:{block.id}")
        _bind(rec,sh2,block); y += h2+0.18
    return [(slide,rec)]


def _render_answer(prs, spec: SlideSpec, slide_number: int):
    slide, rec = _new_slide(prs, spec, slide_number, "answer-primary-v1")
    main = spec.blocks[0]
    w=11.45
    pt=choose_font_size(main.text,SlideRole.ANSWER,w-0.6,2.6)
    lines=estimate_text_lines(main.text,w-0.6,pt)
    h=panel_height_for_lines(lines,pt,min_height=1.8,max_height=2.8)
    _add_panel(slide,LEFT,TOP_CONTENT,w,h,fill_hex=ROLE_STYLE[spec.role]["panel"],accent_hex=ROLE_STYLE[spec.role]["accent"],name=f"DLP:panel:{spec.id}:answer")
    sh=_add_text(slide,main.text,LEFT+0.3,TOP_CONTENT+0.2,w-0.6,h-0.4,font_pt=pt,bold=True,color="123B22",name=f"DLP:block:{main.id}")
    _bind(rec,sh,main)
    y=TOP_CONTENT+h+0.28
    for block in spec.blocks[1:]:
        support_pt=min(34,max(28,pt-12))
        lines2=estimate_text_lines(block.text,w-0.5,support_pt)
        h2=panel_height_for_lines(lines2,support_pt,min_height=1.0,max_height=1.65)
        _add_panel(slide,LEFT,y,w,h2,fill_hex="FFFFFF",accent_hex="B8D8C1",name=f"DLP:panel:{spec.id}:explanation")
        sh2=_add_text(slide,block.text,LEFT+0.25,y+0.16,w-0.5,h2-0.3,font_pt=support_pt,bold=False,name=f"DLP:block:{block.id}")
        _bind(rec,sh2,block); y+=h2+0.18
    return [(slide,rec)]


def _reading_parts(spec: SlideSpec):
    paragraph = next((block for block in spec.blocks if block.kind is BlockKind.PARAGRAPH), None)
    others = [block for block in spec.blocks if block is not paragraph]
    return [(paragraph, others)]


def _render_reading(prs, spec: SlideSpec, slide_number: int):
    outputs=[]
    parts = _reading_parts(spec)
    for part_idx,(paragraph,others) in enumerate(parts,1):
        slide,rec=_new_slide(prs,spec,slide_number+len(outputs),"reading-measure-v1")
        rec.slide_id = spec.id if part_idx==1 else f"{spec.id}-part{part_idx}"
        measure=8.0
        x=LEFT
        pt=30 if paragraph and len(paragraph.text)<360 else 28
        lines=estimate_text_lines(paragraph.text if paragraph else "",measure-0.5,pt)
        required_height=lines*(pt/72.0)*1.28+0.48
        if required_height>4.15:
            raise ValueError(f"{spec.instance_id}/{paragraph.id if paragraph else spec.id}: paragraph requires canonical split before rendering")
        h=panel_height_for_lines(lines,pt,min_height=2.15,max_height=4.15)
        _add_panel(slide,x,TOP_CONTENT,measure,h,fill_hex=ROLE_STYLE[spec.role]["panel"],accent_hex=ROLE_STYLE[spec.role]["accent"],name=f"DLP:panel:{spec.id}:reading")
        if paragraph:
            sh=_add_text(slide,paragraph.text,x+0.26,TOP_CONTENT+0.18,measure-0.52,h-0.36,font_pt=pt,name=f"DLP:block:{paragraph.id}:part{part_idx}")
            _bind(rec, sh, paragraph, split_index=(part_idx if len(parts) > 1 else None))
        y=TOP_CONTENT+h+0.20
        for block in others:
            qpt=32
            qlines=estimate_text_lines(block.text,11.4-0.5,qpt)
            qh=panel_height_for_lines(qlines,qpt,min_height=1.05,max_height=1.55)
            _add_panel(slide,LEFT,y,11.45,qh,fill_hex="FFFFFF",accent_hex="9CC4DE",name=f"DLP:panel:{spec.id}:question")
            q=_add_text(slide,block.text,LEFT+0.25,y+0.14,10.95,qh-0.26,font_pt=qpt,bold=True,name=f"DLP:block:{block.id}")
            _bind(rec,q,block); y += qh+0.15
        outputs.append((slide,rec))
    return outputs


def _render_morning_work(prs,spec:SlideSpec,slide_number:int):
    slide,rec=_new_slide(prs,spec,slide_number,"morning-work-split-v1")
    grouped={}
    for b in spec.blocks:
        grouped.setdefault(b.group or "maths",[]).append(b)
    ordered=[g for g in ("maths","literacy","extension") if g in grouped]
    if len(ordered)>=2:
        col_w=5.55; gap=0.28; positions={ordered[0]:(LEFT,TOP_CONTENT,col_w,5.25),ordered[1]:(LEFT+col_w+gap,TOP_CONTENT,col_w,5.25)}
        if "extension" in ordered[2:]:
            grouped[ordered[1]].extend(grouped["extension"])
    else:
        positions={ordered[0]:(LEFT,TOP_CONTENT,11.38,5.25)}
    for group,(x,y,w,h) in positions.items():
        accent="005A9C" if group=="maths" else "7A4F9D"
        fill="EAF2F8" if group=="maths" else "F3ECF8"
        _add_panel(slide,x,y,w,h,fill_hex=fill,accent_hex=accent,name=f"DLP:group:{group}:{spec.id}")
        group_label=_add_text(slide,group.upper(),x+0.22,y+0.18,w-0.44,0.35,font_pt=18,bold=True,color=accent,name=f"DLP:group-label:{group}:{spec.id}")
        rec.structural_text.append({"shape_id":group_label.shape_id,"shape_name":group_label.name,"text":group.upper(),"kind":"group_label"})
        blocks=grouped[group]
        available=h-0.72
        each=max(0.62,min(1.05,available/max(1,len(blocks))))
        cy=y+0.65
        for b in blocks:
            pt=choose_font_size(b.text,SlideRole.MORNING_WORK,w-0.5,each-0.08)
            sh=_add_text(slide,b.text,x+0.25,cy,w-0.5,each-0.08,font_pt=pt,bold=False,name=f"DLP:block:{b.id}")
            _bind(rec,sh,b); cy += each
        rec.groups[group]={"left_inches":x,"top_inches":y,"width_inches":w,"height_inches":h}
    return [(slide,rec)]


def _render_success(prs,spec:SlideSpec,slide_number:int):
    slide,rec=_new_slide(prs,spec,slide_number,"success-checklist-v1")
    n=len(spec.blocks); w=11.45; gap=0.12
    row_h=min(0.82,max(0.58,(5.35-gap*(n-1))/max(n,1)))
    y=TOP_CONTENT
    for i,b in enumerate(spec.blocks,1):
        _add_panel(slide,LEFT,y,w,row_h,fill_hex="EAF7EE",accent_hex="B8D8C1",name=f"DLP:check-panel:{i}:{spec.id}")
        check=slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(LEFT+0.22),Inches(y+0.18),Inches(0.24),Inches(0.24))
        check.name=f"DLP:check:{i}:{spec.id}"
        check.fill.background();check.line.color.rgb=_rgb("1B7F3A");check.line.width=Pt(1.6)
        pt=choose_font_size(b.text,SlideRole.SUCCESS_CRITERIA,w-0.95,row_h-0.08)
        sh=_add_text(slide,b.text,LEFT+0.72,y+0.08,w-0.94,row_h-0.12,font_pt=pt,name=f"DLP:block:{b.id}")
        _bind(rec,sh,b); y+=row_h+gap
    return [(slide,rec)]


def _render_model_like(prs,spec:SlideSpec,slide_number:int,layout_id:str):
    slide,rec=_new_slide(prs,spec,slide_number,layout_id)
    w=9.15; x=LEFT
    total_text="\n\n".join(b.text for b in spec.blocks)
    pt=choose_font_size(total_text,spec.role,w-0.55,4.8)
    lines=estimate_text_lines(total_text,w-0.55,pt)
    h=panel_height_for_lines(lines,pt,min_height=2.0,max_height=4.9)
    _add_panel(slide,x,TOP_CONTENT,w,h,fill_hex=ROLE_STYLE[spec.role]["panel"],accent_hex=ROLE_STYLE[spec.role]["accent"],name=f"DLP:panel:{spec.id}:model")
    cy=TOP_CONTENT+0.20
    each=(h-0.4)/max(1,len(spec.blocks))
    for b in spec.blocks:
        sh=_add_text(slide,b.text,x+0.28,cy,w-0.56,each-0.10,font_pt=pt,bold=(b.kind is BlockKind.WORKED_STEP),name=f"DLP:block:{b.id}")
        _bind(rec,sh,b); cy+=each
    return [(slide,rec)]


def _render_transition(prs,spec:SlideSpec,slide_number:int):
    slide,rec=_new_slide(prs,spec,slide_number,"transition-v1")
    b=spec.blocks[0]
    sh=_add_text(slide,b.text,1.25,2.7,10.8,1.3,font_pt=42,bold=True,align=PP_ALIGN.CENTER,valign=MSO_VERTICAL_ANCHOR.MIDDLE,name=f"DLP:block:{b.id}")
    _bind(rec,sh,b)
    return [(slide,rec)]


def _render_spec(prs,spec:SlideSpec,slide_number:int):
    if spec.role is SlideRole.QUESTION:
        return _render_question(prs,spec,slide_number)
    if spec.role is SlideRole.ANSWER:
        return _render_answer(prs,spec,slide_number)
    if spec.role is SlideRole.READING:
        return _render_reading(prs,spec,slide_number)
    if spec.role is SlideRole.MORNING_WORK:
        return _render_morning_work(prs,spec,slide_number)
    if spec.role is SlideRole.SUCCESS_CRITERIA:
        return _render_success(prs,spec,slide_number)
    if spec.role is SlideRole.WORKED_EXAMPLE:
        return _render_model_like(prs,spec,slide_number,"worked-example-v1")
    if spec.role is SlideRole.MODEL:
        return _render_model_like(prs,spec,slide_number,"model-paragraph-v1")
    if spec.role is SlideRole.REMINDER:
        return _render_model_like(prs,spec,slide_number,"reminder-primary-v1")
    if spec.role is SlideRole.TRANSITION:
        return _render_transition(prs,spec,slide_number)
    raise ValueError(f"unsupported slide role {spec.role}")


def render_presentation(pack: RenderPack, out_path: Path) -> RenderManifest:
    out_path=Path(out_path)
    out_path.parent.mkdir(parents=True,exist_ok=True)
    prs=Presentation()
    prs.slide_width=Inches(SLIDE_W); prs.slide_height=Inches(SLIDE_H)
    records=[]
    slide_number=1
    for spec in pack.slides:
        rendered=_render_spec(prs,spec,slide_number)
        records.extend(rec for _,rec in rendered)
        slide_number += len(rendered)
    prs.save(out_path)
    manifest=RenderManifest(1,"daily-lesson-pack","1.0.0",records,_sha256(out_path))
    return manifest
