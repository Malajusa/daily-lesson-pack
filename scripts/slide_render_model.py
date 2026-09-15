from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class RenderModelError(ValueError):
    pass


class Visibility(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"


class SlideRole(str, Enum):
    REMINDER = "reminder"
    QUESTION = "question"
    ANSWER = "answer"
    MODEL = "model"
    READING = "reading"
    WORKED_EXAMPLE = "worked_example"
    SUCCESS_CRITERIA = "success_criteria"
    TRANSITION = "transition"
    MORNING_WORK = "morning_work"


class ComponentKind(str, Enum):
    MORNING_WORK = "dlp-morning-work"
    LITERACY_WARMUP = "dlp-literacy-warmup"
    SHARED_READING = "dlp-shared-reading"
    GUIDED_READING = "dlp-guided-reading"
    WRITING = "dlp-writing-lesson"
    NUMERACY_WARMUP = "dlp-numeracy-warmup"
    MATHEMATICS = "dlp-maths-lesson"


class BlockKind(str, Enum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    TASK = "task"
    ANSWER = "answer"
    WORKED_STEP = "worked_step"
    CHECK = "check"
    SUPPORT = "support"
    TEACHER_NOTE = "teacher_note"


@dataclass(frozen=True)
class ProjectionPolicy:
    min_font_pt: int
    preferred_line_chars: int
    max_blocks: int
    split_permitted: bool
    teacher_content_prohibited: bool = True


@dataclass(frozen=True)
class ContentBlock:
    id: str
    source_task_id: str
    source_field: str
    kind: BlockKind
    visibility: Visibility
    text: str
    group: str | None = None


@dataclass(frozen=True)
class SlideSpec:
    id: str
    instance_id: str
    component: ComponentKind
    role: SlideRole
    eyebrow: str
    title: str
    blocks: tuple[ContentBlock, ...]
    policy: ProjectionPolicy
    layout_hint: str


@dataclass(frozen=True)
class RenderPack:
    generation_run_id: str
    date_label: str
    slides: tuple[SlideSpec, ...]


STANDARD_FIELDS = {
    "prompt": (Visibility.STUDENT, BlockKind.TASK, SlideRole.QUESTION),
    "answer": (Visibility.STUDENT, BlockKind.ANSWER, SlideRole.ANSWER),
    "paragraph": (Visibility.STUDENT, BlockKind.PARAGRAPH, SlideRole.READING),
    "why_prompt": (Visibility.STUDENT, BlockKind.SUPPORT, SlideRole.QUESTION),
    "why_answer": (Visibility.STUDENT, BlockKind.SUPPORT, SlideRole.ANSWER),
    "before": (Visibility.STUDENT, BlockKind.PARAGRAPH, SlideRole.MODEL),
    "after": (Visibility.STUDENT, BlockKind.PARAGRAPH, SlideRole.MODEL),
    "reminder": (Visibility.STUDENT, BlockKind.SUPPORT, SlideRole.REMINDER),
    "success_criteria": (Visibility.STUDENT, BlockKind.CHECK, SlideRole.SUCCESS_CRITERIA),
    "teacher_note": (Visibility.TEACHER, BlockKind.TEACHER_NOTE, SlideRole.MODEL),
}

POLICIES = {
    SlideRole.REMINDER: ProjectionPolicy(30, 56, 4, True),
    SlideRole.QUESTION: ProjectionPolicy(36, 52, 4, True),
    SlideRole.ANSWER: ProjectionPolicy(36, 52, 4, True),
    SlideRole.MODEL: ProjectionPolicy(28, 70, 5, True),
    SlideRole.READING: ProjectionPolicy(28, 70, 3, True),
    SlideRole.WORKED_EXAMPLE: ProjectionPolicy(30, 58, 6, True),
    SlideRole.SUCCESS_CRITERIA: ProjectionPolicy(28, 58, 8, True),
    SlideRole.TRANSITION: ProjectionPolicy(30, 60, 2, False),
    SlideRole.MORNING_WORK: ProjectionPolicy(26, 48, 12, True),
}

TITLE_BY_ROLE = {
    SlideRole.REMINDER: "Remember",
    SlideRole.QUESTION: "Your turn",
    SlideRole.ANSWER: "Answer",
    SlideRole.MODEL: "Model",
    SlideRole.READING: "Read and think",
    SlideRole.WORKED_EXAMPLE: "Worked example",
    SlideRole.SUCCESS_CRITERIA: "Success criteria",
    SlideRole.TRANSITION: "Next",
    SlideRole.MORNING_WORK: "Morning Work",
}

EYEBROW = {
    ComponentKind.MORNING_WORK: "MORNING WORK",
    ComponentKind.LITERACY_WARMUP: "LITERACY WARM-UP",
    ComponentKind.SHARED_READING: "SHARED READING",
    ComponentKind.GUIDED_READING: "GUIDED READING",
    ComponentKind.WRITING: "WRITING",
    ComponentKind.NUMERACY_WARMUP: "MATHEMATICS WARM-UP",
    ComponentKind.MATHEMATICS: "MATHEMATICS",
}


def _component(owner: str, instance_id: str) -> ComponentKind:
    try:
        return ComponentKind(owner)
    except ValueError as exc:
        raise RenderModelError(f"{instance_id}: unsupported component owner {owner!r}") from exc


def _field_meta(task: dict, field: str, instance_id: str):
    if field in STANDARD_FIELDS:
        return STANDARD_FIELDS[field]
    explicit = task.get("render_fields", {}).get(field)
    if not isinstance(explicit, dict):
        raise RenderModelError(
            f"{instance_id}/{task.get('id') or '<missing-task-id>'}: unknown render field {field!r}; explicit render_fields metadata is required"
        )
    try:
        visibility = Visibility(explicit["visibility"])
        kind = BlockKind(explicit["kind"])
        role = SlideRole(explicit["role"])
    except (KeyError, ValueError) as exc:
        raise RenderModelError(
            f"{instance_id}/{task.get('id')}: invalid render_fields metadata for {field!r}"
        ) from exc
    return visibility, kind, role


def _block(task: dict, field: str, text: str, instance_id: str, *, suffix: str = "", group: str | None = None) -> tuple[ContentBlock, SlideRole] | None:
    visibility, kind, role = _field_meta(task, field, instance_id)
    if visibility is Visibility.TEACHER:
        return None
    task_id = str(task.get("id", "")).strip()
    if not task_id:
        raise RenderModelError(f"{instance_id}: task id is required for render traceability")
    block_id = f"{task_id}:{field}{suffix}"
    return ContentBlock(block_id, task_id, field, kind, visibility, text.strip(), group), role


def _slide(instance_id: str, component: ComponentKind, role: SlideRole, blocks: Iterable[ContentBlock], index: int, *, hint: str | None = None, title: str | None = None) -> SlideSpec:
    block_tuple = tuple(blocks)
    if not block_tuple:
        raise RenderModelError(f"{instance_id}: cannot create empty {role.value} slide")
    return SlideSpec(
        id=f"{instance_id}-{index:03d}-{role.value}",
        instance_id=instance_id,
        component=component,
        role=role,
        eyebrow=EYEBROW[component],
        title=title or TITLE_BY_ROLE[role],
        blocks=block_tuple,
        policy=POLICIES[role],
        layout_hint=hint or role.value,
    )


def _criteria_blocks(task: dict, text: str, instance_id: str) -> list[ContentBlock]:
    items = [line.strip().lstrip("•-✓☐ ") for line in text.splitlines() if line.strip()]
    if len(items) <= 1 and ";" in text:
        items = [part.strip() for part in text.split(";") if part.strip()]
    task_id = str(task.get("id", "")).strip()
    if not task_id:
        raise RenderModelError(f"{instance_id}: task id is required for render traceability")
    return [
        ContentBlock(f"{task_id}:success_criteria:{i+1}", task_id, "success_criteria", BlockKind.CHECK, Visibility.STUDENT, item)
        for i, item in enumerate(items)
    ]


def _compile_morning_work(instance: dict, tasks: list[dict]) -> list[SlideSpec]:
    instance_id = instance["id"]
    component = ComponentKind.MORNING_WORK
    blocks: list[ContentBlock] = []
    for task in tasks:
        group = str(task.get("render_group", "")).strip().lower()
        if group not in {"maths", "literacy", "extension"}:
            op = str(task.get("operation", "")).lower()
            group = "literacy" if op in {"edit", "read", "write", "grammar", "punctuate", "spell"} else "maths"
        fields = task.get("fields")
        if not isinstance(fields, dict):
            raise RenderModelError(f"{instance_id}/{task.get('id')}: fields must be an object")
        for field, text in fields.items():
            if field == "teacher_note" or field == "answer":
                continue
            if not isinstance(text, str) or not text.strip():
                raise RenderModelError(f"{instance_id}/{task.get('id')}: {field} must be non-empty text")
            result = _block(task, field, text, instance_id, group=group)
            if result:
                blocks.append(result[0])
    return [_slide(instance_id, component, SlideRole.MORNING_WORK, blocks, 1, hint="morning-work-split")]


def _compile_task(instance: dict, task: dict, start_index: int) -> list[SlideSpec]:
    instance_id = instance["id"]
    component = _component(instance["owner"], instance_id)
    task_id = str(task.get("id", "")).strip()
    if not task_id:
        raise RenderModelError(f"{instance_id}: task id is required for render traceability")
    fields = task.get("fields")
    if not isinstance(fields, dict) or not fields:
        raise RenderModelError(f"{instance_id}/{task_id}: fields must be a non-empty object")

    for field, text in fields.items():
        if not isinstance(text, str) or not text.strip():
            raise RenderModelError(f"{instance_id}/{task_id}: {field} must be non-empty text")
        _field_meta(task, field, instance_id)

    slides: list[SlideSpec] = []
    idx = start_index

    if component is ComponentKind.SHARED_READING and "paragraph" in fields:
        reading_blocks: list[ContentBlock] = []
        for field in ("paragraph", "prompt", "why_prompt"):
            if field in fields:
                result = _block(task, field, fields[field], instance_id)
                if result:
                    reading_blocks.append(result[0])
        slides.append(_slide(instance_id, component, SlideRole.READING, reading_blocks, idx, hint="reading-measure"))
        idx += 1
        answer_blocks: list[ContentBlock] = []
        for field in ("answer", "why_answer"):
            if field in fields:
                result = _block(task, field, fields[field], instance_id)
                if result:
                    answer_blocks.append(result[0])
        if answer_blocks:
            slides.append(_slide(instance_id, component, SlideRole.ANSWER, answer_blocks, idx, hint="answer-primary"))
            idx += 1
    else:
        if "reminder" in fields:
            result = _block(task, "reminder", fields["reminder"], instance_id)
            if result:
                slides.append(_slide(instance_id, component, SlideRole.REMINDER, [result[0]], idx))
                idx += 1
        if "prompt" in fields:
            prompt_blocks = []
            result = _block(task, "prompt", fields["prompt"], instance_id)
            if result:
                prompt_blocks.append(result[0])
            if "why_prompt" in fields:
                why = _block(task, "why_prompt", fields["why_prompt"], instance_id)
                if why:
                    prompt_blocks.append(why[0])
            slides.append(_slide(instance_id, component, SlideRole.QUESTION, prompt_blocks, idx, hint="question-primary"))
            idx += 1
        if "answer" in fields:
            answer_blocks = []
            result = _block(task, "answer", fields["answer"], instance_id)
            if result:
                answer_blocks.append(result[0])
            if "why_answer" in fields:
                why = _block(task, "why_answer", fields["why_answer"], instance_id)
                if why:
                    answer_blocks.append(why[0])
            slides.append(_slide(instance_id, component, SlideRole.ANSWER, answer_blocks, idx, hint="answer-primary"))
            idx += 1

    if "before" in fields or "after" in fields:
        model_blocks: list[ContentBlock] = []
        for field in ("before", "after"):
            if field in fields:
                result = _block(task, field, fields[field], instance_id)
                if result:
                    model_blocks.append(result[0])
        slides.append(_slide(instance_id, component, SlideRole.MODEL, model_blocks, idx, hint="model-paragraph"))
        idx += 1

    if "success_criteria" in fields:
        criteria = _criteria_blocks(task, fields["success_criteria"], instance_id)
        slides.append(_slide(instance_id, component, SlideRole.SUCCESS_CRITERIA, criteria, idx, hint="success-checklist"))
        idx += 1

    for field in task.get("render_fields", {}):
        if field not in fields:
            raise RenderModelError(f"{instance_id}/{task_id}: render_fields references missing field {field!r}")
        result = _block(task, field, fields[field], instance_id)
        if result:
            block, role = result
            slides.append(_slide(instance_id, component, role, [block], idx, hint=role.value))
            idx += 1

    return slides


def compile_render_model(context: dict, content: dict, component_record: dict) -> RenderPack:
    if context.get("schema_version") != 2:
        raise RenderModelError("context schema_version must be 2")
    if content.get("schema_version") != 3:
        raise RenderModelError("content schema_version must be 3")
    if component_record.get("schema_version") != 2:
        raise RenderModelError("component record schema_version must be 2")
    instances = context.get("timetable_instances")
    if not isinstance(instances, list) or not instances:
        raise RenderModelError("context timetable_instances are required")
    if content.get("instances") != instances:
        raise RenderModelError("content instances must exactly match context timetable_instances")
    tasks = content.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise RenderModelError("content tasks are required")
    by_instance: dict[str, list[dict]] = {}
    for task in tasks:
        instance_id = str(task.get("instance_id", "")).strip()
        if not instance_id:
            raise RenderModelError("task instance_id is required")
        by_instance.setdefault(instance_id, []).append(task)

    slides: list[SlideSpec] = []
    for instance in instances:
        instance_id = str(instance.get("id", "")).strip()
        if not instance_id:
            raise RenderModelError("timetable instance id is required")
        owner = str(instance.get("owner", "")).strip()
        instance_tasks = by_instance.get(instance_id, [])
        if not instance_tasks:
            raise RenderModelError(f"{instance_id}: no canonical tasks")
        if owner == ComponentKind.MORNING_WORK.value:
            slides.extend(_compile_morning_work(instance, instance_tasks))
        else:
            for task in instance_tasks:
                slides.extend(_compile_task(instance, task, len(slides) + 1))

    date_entry = context.get("date", {})
    date_label = str(date_entry.get("value", "")).strip() if isinstance(date_entry, dict) else ""
    return RenderPack(
        generation_run_id=str(context.get("generation_run_id", "")).strip(),
        date_label=date_label,
        slides=tuple(slides),
    )
