#!/usr/bin/env python3
"""Add the assignment-focused interactive visual lab to BCL1223."""

import json
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "progress.db"
COURSE_ID = "bcl1223"
TUTORIAL_ID = "bcl1223_assignment_lab"


GLOSSARY = {
    "Entity": "A distinguishable real-world object or concept about which the database stores facts, such as STUDENT, CLUB, or EVENT.",
    "Relationship": "An association between entities. For example, a STUDENT joins a CLUB through a MEMBERSHIP.",
    "Multiplicity": "The minimum and maximum number of occurrences that may participate at one end of a relationship, such as 0..* or exactly 1.",
    "Cardinality": "The maximum number of times one entity instance may be associated with instances of the related entity: one or many.",
    "Ordinality": "The minimum number of times one entity instance must participate in a relationship: zero means optional and one means mandatory.",
    "Optionality": "Whether participation may be zero. This is the zero case of ordinality and is shown by a circle in Crow's Foot notation.",
    "Associative Entity": "An entity introduced to resolve a many-to-many relationship and store facts about that relationship. MEMBERSHIP is an associative entity.",
    "Junction Table": "The relational-table implementation of an associative entity. It contains foreign keys to both parent tables and often uses them as a composite key.",
    "Composite Foreign Key": "A foreign key made from two or more columns that references a matching composite candidate or primary key.",
    "Crow's Foot Notation": "A visual notation for entity relationships. Bars mean one, circles mean optional participation, and a three-pronged foot means many.",
    "Third Normal Form": "A relation is in 3NF when it is in 2NF and non-key attributes do not depend transitively on the key through another non-key attribute.",
}


def lab_widget(lab_type, title, instructions, config):
    """Return a data-driven lab placeholder; all scenario data remains in SQLite."""
    config_json = json.dumps(config, ensure_ascii=False).replace("</", "<\\/")
    return f"""
<div class="interactive-lab" data-lab-type="{lab_type}">
  <div class="lab-heading">
    <span class="lab-badge">Interactive Lab</span>
    <h4>{title}</h4>
    <p>{instructions}</p>
  </div>
  <div class="lab-stage" aria-live="polite"></div>
  <div hidden class="lab-config">{config_json}</div>
</div>
"""


def step(title, body, diagram=None):
    return {"title": title, "body": body, "diagram": diagram}


def lesson(number, title, intro, steps, recap):
    return {
        "number": number,
        "title": title,
        "intro": intro,
        "steps": steps,
        "recap": recap,
    }


ERD_CONFIG = {
    "title": "SEGi Student Clubs & Societies ERD",
    "subtitle": "Click an entity or relationship. Use a guided focus to trace one business rule at a time.",
    "layers": [
        {"id": "catalogs", "label": "Level 1", "title": "Master Catalogs"},
        {"id": "core", "label": "Level 2", "title": "Core Entities"},
        {"id": "junctions", "label": "Level 3", "title": "Junctions & Operations"},
        {"id": "locks", "label": "Level 4", "title": "Multi-Key Locks"},
    ],
    "legend": [
        {"value": "1", "label": "Exactly one", "symbol": "||", "ordinality": "Mandatory (minimum 1)", "cardinality": "One (maximum 1)"},
        {"value": "0..1", "label": "Zero or one", "symbol": "o|", "ordinality": "Optional (minimum 0)", "cardinality": "One (maximum 1)"},
        {"value": "0..*", "label": "Zero or many", "symbol": "o{", "ordinality": "Optional (minimum 0)", "cardinality": "Many (maximum many)"},
        {"value": "1..*", "label": "One or many", "symbol": "|{", "ordinality": "Mandatory (minimum 1)", "cardinality": "Many (maximum many)"},
    ],
    "entities": [
        {
            "id": "faculty", "name": "FACULTY", "layer": "catalogs", "kind": "master",
            "description": "Academic faculty master. Every STUDENT references one faculty.",
            "columns": [
                {"name": "faculty_id", "type": "VARCHAR2(6)", "keys": ["PK"]},
                {"name": "faculty_name", "type": "VARCHAR2(100)", "keys": ["UK"]},
            ],
            "constraints": ["PK (faculty_id)", "UNIQUE (faculty_name)"],
        },
        {
            "id": "advisor", "name": "ADVISOR", "layer": "catalogs", "kind": "master",
            "description": "Lecturer master used by CLUB. One advisor may be assigned to several clubs.",
            "columns": [
                {"name": "advisor_id", "type": "VARCHAR2(6)", "keys": ["PK"]},
                {"name": "advisor_name", "type": "VARCHAR2(100)", "keys": []},
                {"name": "office_room", "type": "VARCHAR2(10)", "keys": []},
                {"name": "office_phone", "type": "VARCHAR2(20)", "keys": ["UK"]},
            ],
            "constraints": ["PK (advisor_id)", "UNIQUE (office_phone)"],
        },
        {
            "id": "venue_pic", "name": "VENUE_PIC", "layer": "catalogs", "kind": "master",
            "description": "Staff member responsible for one or more physical venues.",
            "columns": [
                {"name": "pic_id", "type": "VARCHAR2(6)", "keys": ["PK"]},
                {"name": "pic_name", "type": "VARCHAR2(100)", "keys": []},
                {"name": "phone_number", "type": "VARCHAR2(20)", "keys": ["UK"]},
                {"name": "office_room", "type": "VARCHAR2(10)", "keys": []},
            ],
            "constraints": ["PK (pic_id)", "UNIQUE (phone_number)"],
        },
        {
            "id": "student", "name": "STUDENT", "layer": "core", "kind": "core",
            "description": "Student profile. Membership facts are deliberately kept outside this table.",
            "columns": [
                {"name": "student_id", "type": "VARCHAR2(6)", "keys": ["PK"]},
                {"name": "student_name", "type": "VARCHAR2(100)", "keys": []},
                {"name": "phone_number", "type": "VARCHAR2(20)", "keys": ["UK"]},
                {"name": "faculty_id", "type": "VARCHAR2(6)", "keys": ["FK"]},
                {"name": "approval_form", "type": "CHAR(1)", "keys": ["CHECK"]},
                {"name": "scholarship", "type": "CHAR(1)", "keys": ["CHECK"]},
            ],
            "constraints": ["FK faculty_id → FACULTY", "CHECK student ID format", "CHECK Y/N flags"],
        },
        {
            "id": "club", "name": "CLUB", "layer": "core", "kind": "core",
            "description": "Student organisation supervised by one advisor.",
            "columns": [
                {"name": "club_id", "type": "VARCHAR2(6)", "keys": ["PK"]},
                {"name": "club_name", "type": "VARCHAR2(100)", "keys": ["UK"]},
                {"name": "advisor_id", "type": "VARCHAR2(6)", "keys": ["FK"]},
                {"name": "club_notes", "type": "VARCHAR2(500)", "keys": []},
            ],
            "constraints": ["FK advisor_id → ADVISOR", "UNIQUE (club_name)"],
        },
        {
            "id": "venue", "name": "VENUE", "layer": "core", "kind": "core",
            "description": "Room or facility used by events and managed by one venue PIC.",
            "columns": [
                {"name": "venue_id", "type": "VARCHAR2(6)", "keys": ["PK"]},
                {"name": "venue_name", "type": "VARCHAR2(100)", "keys": ["UK"]},
                {"name": "venue_type", "type": "VARCHAR2(30)", "keys": ["CHECK"]},
                {"name": "capacity", "type": "NUMBER(4)", "keys": ["CHECK"]},
                {"name": "pic_id", "type": "VARCHAR2(6)", "keys": ["FK"]},
            ],
            "constraints": ["FK pic_id → VENUE_PIC", "CHECK capacity > 0"],
        },
        {
            "id": "membership", "name": "MEMBERSHIP", "layer": "junctions", "kind": "junction",
            "description": "Associative entity resolving STUDENT ↔ CLUB. The complete pair identifies one membership.",
            "columns": [
                {"name": "club_id", "type": "VARCHAR2(6)", "keys": ["PK", "FK"]},
                {"name": "student_id", "type": "VARCHAR2(6)", "keys": ["PK", "FK"]},
                {"name": "date_registered", "type": "DATE", "keys": []},
                {"name": "membership_status", "type": "VARCHAR2(10)", "keys": ["CHECK"]},
            ],
            "constraints": ["Composite PK (club_id, student_id)", "FK club_id → CLUB", "FK student_id → STUDENT"],
        },
        {
            "id": "club_president", "name": "CLUB_PRESIDENT", "layer": "junctions", "kind": "lock",
            "description": "Current leadership appointment. The composite FK proves the president is a member of that club.",
            "columns": [
                {"name": "club_id", "type": "VARCHAR2(6)", "keys": ["PK", "FK"]},
                {"name": "student_id", "type": "VARCHAR2(6)", "keys": ["FK"]},
                {"name": "appointment_date", "type": "DATE", "keys": []},
            ],
            "constraints": ["PK (club_id)", "Composite FK (club_id, student_id) → MEMBERSHIP"],
        },
        {
            "id": "event", "name": "EVENT", "layer": "junctions", "kind": "operation",
            "description": "Club activity scheduled in a venue and semester under the current president.",
            "columns": [
                {"name": "event_id", "type": "VARCHAR2(8)", "keys": ["PK"]},
                {"name": "club_id", "type": "VARCHAR2(6)", "keys": ["FK"]},
                {"name": "venue_id", "type": "VARCHAR2(6)", "keys": ["FK"]},
                {"name": "semester_id", "type": "VARCHAR2(8)", "keys": ["FK"]},
                {"name": "president_student_id", "type": "VARCHAR2(6)", "keys": ["FK"]},
                {"name": "activity_name", "type": "VARCHAR2(150)", "keys": []},
                {"name": "event_date", "type": "DATE", "keys": []},
            ],
            "constraints": ["FK club_id → CLUB", "FK venue_id → VENUE", "Composite FK (club_id, president_student_id) → CLUB_PRESIDENT"],
        },
        {
            "id": "semester", "name": "SEMESTER", "layer": "locks", "kind": "master",
            "description": "Academic reporting period that supplies stable date boundaries for events.",
            "columns": [
                {"name": "semester_id", "type": "VARCHAR2(8)", "keys": ["PK"]},
                {"name": "semester_name", "type": "VARCHAR2(30)", "keys": ["UK"]},
                {"name": "start_date", "type": "DATE", "keys": ["CHECK"]},
                {"name": "end_date", "type": "DATE", "keys": ["CHECK"]},
            ],
            "constraints": ["CHECK end_date > start_date", "UNIQUE (semester_name)"],
        },
        {
            "id": "event_registration", "name": "EVENT_REGISTRATION", "layer": "locks", "kind": "junction",
            "description": "Event signup. Two composite foreign keys prove that the event and student membership share the same club.",
            "columns": [
                {"name": "event_id", "type": "VARCHAR2(8)", "keys": ["PK", "FK"]},
                {"name": "club_id", "type": "VARCHAR2(6)", "keys": ["FK"]},
                {"name": "student_id", "type": "VARCHAR2(6)", "keys": ["PK", "FK"]},
                {"name": "registration_date", "type": "DATE", "keys": []},
                {"name": "attendance_status", "type": "VARCHAR2(10)", "keys": ["CHECK"]},
            ],
            "constraints": ["Composite PK (event_id, student_id)", "Composite FK (event_id, club_id) → EVENT", "Composite FK (club_id, student_id) → MEMBERSHIP"],
        },
    ],
    "relationships": [
        {"id": "faculty_students", "from": "faculty", "to": "student", "label": "has", "fromMultiplicity": "1", "toMultiplicity": "0..*", "rule": "A faculty may have zero or many students; every student belongs to exactly one faculty.", "constraint": "STUDENT.faculty_id → FACULTY.faculty_id", "example": "Faculty of Engineering (FENG) has 350 students; Faculty of Medicine (FMED) admitted 0 this intake — the 0..* allows both. Every student MUST have a valid faculty_id."},
        {"id": "student_memberships", "from": "student", "to": "membership", "label": "holds", "fromMultiplicity": "1", "toMultiplicity": "1..*", "rule": "A participating student holds one or more memberships; every membership belongs to one student.", "constraint": "MEMBERSHIP.student_id → STUDENT.student_id", "example": "ST0001 holds 3 memberships (Debate, Robotic, Photography). Each MEMBERSHIP row points back to ST0001 only. A student with zero memberships simply has no rows here."},
        {"id": "club_memberships", "from": "club", "to": "membership", "label": "receives", "fromMultiplicity": "1", "toMultiplicity": "1..*", "rule": "A participating club contains one or more members; every membership belongs to one club.", "constraint": "MEMBERSHIP.club_id → CLUB.club_id", "example": "Debate Club (CL001) has 25 members — 25 MEMBERSHIP rows share club_id CL001. No row can reference a club that does not exist."},
        {"id": "advisor_clubs", "from": "advisor", "to": "club", "label": "advises", "fromMultiplicity": "1", "toMultiplicity": "0..*", "rule": "An advisor may currently advise zero or many clubs; every club has exactly one advisor.", "constraint": "CLUB.advisor_id → ADVISOR.advisor_id", "example": "Dr. Tan (AD001) advises Debate Club and Robotic Club (2 clubs); new hire Dr. Lim (AD002) has 0 clubs assigned. Each club has exactly one advisor_id."},
        {"id": "membership_president", "from": "membership", "to": "club_president", "label": "qualifies", "fromMultiplicity": "1", "toMultiplicity": "0..1", "rule": "Every presidency uses one valid membership; most memberships are not presidency appointments.", "constraint": "CLUB_PRESIDENT.(club_id, student_id) → MEMBERSHIP.(club_id, student_id)", "example": "Debate Club has 25 members but only 1 president (ST0001). The composite FK proves the pair (CL001, ST0001) exists in MEMBERSHIP. The other 24 memberships have no presidency row — the 0..1 allows that."},
        {"id": "club_president", "from": "club", "to": "club_president", "label": "elects", "fromMultiplicity": "1", "toMultiplicity": "1", "rule": "Each modelled club has exactly one current president; each presidency belongs to one club.", "constraint": "CLUB_PRESIDENT.club_id is both PK and FK", "example": "CL001 has exactly 1 president row (ST0001). CL002 has exactly 1 president row (ST0005). The 1:1 constraint prevents a club from having zero or two presidents, and prevents a presidency from floating without a club."},
        {"id": "pic_venues", "from": "venue_pic", "to": "venue", "label": "manages", "fromMultiplicity": "1", "toMultiplicity": "1..*", "rule": "A modelled venue PIC manages one or more venues; each venue has exactly one PIC.", "constraint": "VENUE.pic_id → VENUE_PIC.pic_id", "example": "Mr. Raju (VPC001) manages Dewan Serbaguna and Bilik Kuliah 1. Every venue must have exactly one PIC assigned — a venue without a responsible person is not allowed."},
        {"id": "club_events", "from": "club", "to": "event", "label": "organises", "fromMultiplicity": "1", "toMultiplicity": "1..*", "rule": "Each modelled club runs one or more events; every event belongs to one club.", "constraint": "EVENT.club_id → CLUB.club_id; minimum child count needs an audit", "example": "Debate Club ran 4 events this semester (inter-varsity debate, workshop, etc). Each EVENT row references CL001. A club with zero events simply means no rows exist — the 1..* is a business policy, not enforced by the FK alone."},
        {"id": "venue_events", "from": "venue", "to": "event", "label": "hosts", "fromMultiplicity": "1", "toMultiplicity": "0..*", "rule": "A venue may host zero or many events; every event uses exactly one venue.", "constraint": "EVENT.venue_id → VENUE.venue_id", "example": "Dewan Serbaguna hosted 8 events this semester; Bilik Mesyuarat hosted 0 — the 0..* allows an unused venue. An event cannot exist without a venue_id."},
        {"id": "semester_events", "from": "semester", "to": "event", "label": "schedules", "fromMultiplicity": "1", "toMultiplicity": "0..*", "rule": "A semester may contain zero or many events; every event occurs in exactly one semester.", "constraint": "EVENT.semester_id → SEMESTER.semester_id", "example": "Semester 2, 2026 hosted 12 events; Semester 3, 2026 might host 0 — the 0..* permits either. An event without a semester is rejected by the FK."},
        {"id": "president_events", "from": "club_president", "to": "event", "label": "oversees", "fromMultiplicity": "1", "toMultiplicity": "1..*", "rule": "The elected president oversees the club's events; every event names one responsible president.", "constraint": "EVENT.(club_id, president_student_id) → CLUB_PRESIDENT.(club_id, student_id)", "example": "President ST0001 is recorded on all 4 Debate Club events. The composite FK matches the pair (CL001, ST0001) against CLUB_PRESIDENT, proving the named student is indeed the president of that club."},
        {"id": "event_registrations", "from": "event", "to": "event_registration", "label": "receives", "fromMultiplicity": "1", "toMultiplicity": "0..*", "rule": "An event may receive zero or many registrations; every registration refers to exactly one event.", "constraint": "EVENT_REGISTRATION.(event_id, club_id) → EVENT.(event_id, club_id)", "example": "Cybersecurity Talk (EV010) has 45 registrations so far; Cultural Night (EV011) has 0 registrations. Each registration row references a valid (event_id, club_id) pair."},
        {"id": "membership_registrations", "from": "membership", "to": "event_registration", "label": "permits", "fromMultiplicity": "1", "toMultiplicity": "0..*", "rule": "A membership may permit many registrations; each registration must match one membership in the organising club.", "constraint": "EVENT_REGISTRATION.(club_id, student_id) → MEMBERSHIP.(club_id, student_id). Status ACTIVE is not enforced by this FK.", "example": "ST0001's Debate Club membership (CL001, ST0001) permits them to register for any Debate Club event. ST0002 cannot register — the FK rejects (CL001, ST0002) if no membership exists. Note: the FK does not check membership_status = 'ACTIVE'; that needs application logic."},
    ],
    "presets": [
        {"id": "junctions", "label": "M:N Junction", "title": "Resolve STUDENT ↔ CLUB", "description": "MEMBERSHIP turns one many-to-many fact into two one-to-many relationships and stores the join date.", "entities": ["student", "club", "membership"], "relationships": ["student_memberships", "club_memberships"]},
        {"id": "composite", "label": "Composite Keys", "title": "Keys that work as pairs", "description": "Highlight the two junction tables and follow the composite identifiers that prevent duplicate memberships and registrations.", "entities": ["membership", "event_registration", "event"], "relationships": ["event_registrations", "membership_registrations"]},
        {"id": "president", "label": "President Rule", "title": "A president must be a member", "description": "The club-and-student pair must already exist in MEMBERSHIP before the presidency row is valid.", "entities": ["club", "student", "membership", "club_president"], "relationships": ["student_memberships", "club_memberships", "membership_president", "club_president"]},
        {"id": "registration", "label": "Registration Lock", "title": "Event and member must share a club", "description": "Two composite foreign keys make club_id the common lock between EVENT, MEMBERSHIP, and EVENT_REGISTRATION.", "entities": ["event", "membership", "event_registration"], "relationships": ["event_registrations", "membership_registrations"]},
    ],
}


LESSONS = [
    lesson(
        1,
        "Complete ERD Tutor & Canvas",
        "See the entire Student Clubs schema as one connected system. Use the guided focus buttons to reduce the diagram to one idea, then inspect the exact keys and business rule behind each connection.",
        [
            step(
                "How to read the canvas",
                """
<p>Every entity card shows its attributes and key roles. The connector symbols use {{Crow's Foot Notation}} to show <strong>{{Cardinality}}</strong> (maximum participation) and <strong>{{Ordinality}}</strong> (minimum participation) at both ends.</p>
<table>
  <tr><th>Symbol</th><th>Ordinality: minimum</th><th>Cardinality: maximum</th><th>Combined meaning</th></tr>
  <tr><td><code>||</code></td><td>1 — mandatory</td><td>1</td><td>Exactly one</td></tr>
  <tr><td><code>o|</code></td><td>0 — optional</td><td>1</td><td>Zero or one</td></tr>
  <tr><td><code>o{</code></td><td>0 — optional</td><td>Many</td><td>Zero or many</td></tr>
  <tr><td><code>|{</code></td><td>1 — mandatory</td><td>Many</td><td>One or many</td></tr>
</table>
<div class="highlight-box"><strong>Reading rule:</strong> the endpoint nearest an entity combines its ordinality and cardinality. It tells the minimum and maximum occurrences of that entity for one occurrence at the opposite end.</div>
""",
            ),
            step(
                "Explore the complete Student Clubs ERD",
                lab_widget(
                    "erd-tutor",
                    "Complete relational schema canvas",
                    "Select a guided focus, click an entity, or click a connector to inspect the underlying key and business rule.",
                    ERD_CONFIG,
                ),
            ),
            step(
                "Trace three rules end to end",
                """
<ol>
  <li><strong>Membership:</strong> trace <code>STUDENT → MEMBERSHIP ← CLUB</code>. Explain why <code>date_registered</code> belongs in the middle.</li>
  <li><strong>President:</strong> trace <code>MEMBERSHIP → CLUB_PRESIDENT</code>. Identify the two columns that must match.</li>
  <li><strong>Event registration:</strong> trace both arrows into <code>EVENT_REGISTRATION</code>. Notice how <code>club_id</code> proves the event and member belong to the same club.</li>
</ol>
<div class="example-box">The foreign key proves a membership row exists. It does <strong>not</strong> inspect <code>membership_status</code>; an ACTIVE-only rule needs additional database or application logic.</div>
""",
            ),
        ],
        [
            "A complete ERD is easier to understand when one relationship path is highlighted at a time.",
            "Cardinality and ordinality must be read at both ends of every connector.",
            "Composite foreign keys enforce same-club identity, while status conditions require separate logic.",
        ],
    ),
    lesson(
        1,
        "Entities, Relationships, and Attributes",
        "Start by separating the things the Student Affairs Department tracks from the links between those things. This single distinction makes the whole ERD easier to read.",
        [
            step(
                "Read the model as sentences",
                """
<div class="highlight-box"><strong>{{Entity}}</strong> means a thing with its own identity. A <strong>{{Relationship}}</strong> explains how those things are connected.</div>
<p><code>STUDENT</code> and <code>CLUB</code> can exist independently. The fact that student <code>ST0001</code> joined club <code>CL0003</code> is a different fact, represented by <code>MEMBERSHIP</code>.</p>
<p>An attribute describes one entity or relationship. <code>student_name</code> describes a student, while <code>date_registered</code> describes one particular student–club membership.</p>
""",
                diagram="""flowchart LR
  S[STUDENT] -->|holds| M[MEMBERSHIP]
  C[CLUB] -->|receives| M
  M --> D[date_registered]
  style S fill:#dbeafe,stroke:#3b82f6
  style C fill:#dbeafe,stroke:#3b82f6
  style M fill:#fef3c7,stroke:#f59e0b
  style D fill:#f0fdf4,stroke:#059669
""",
            ),
            step(
                "Classify the assignment facts",
                lab_widget(
                    "classifier",
                    "Entity, relationship, or attribute?",
                    "Choose the best category for each item. Check your reasoning after every choice.",
                    {
                        "categories": ["Entity", "Relationship / associative entity", "Attribute"],
                        "items": [
                            {"label": "STUDENT", "answer": 0, "why": "A student has an independent identifier and descriptive attributes."},
                            {"label": "CLUB", "answer": 0, "why": "A club can exist before any particular student joins it."},
                            {"label": "MEMBERSHIP", "answer": 1, "why": "It records the relationship between one student and one club."},
                            {"label": "date_registered", "answer": 2, "why": "It describes when one membership began, not the student or club alone."},
                            {"label": "EVENT_REGISTRATION", "answer": 1, "why": "It records a student's registration for a particular event."},
                            {"label": "venue_name", "answer": 2, "why": "It is a descriptive property of VENUE."},
                        ],
                    },
                ),
            ),
            step(
                "Why the join date belongs in MEMBERSHIP",
                """
<p>Move <code>date_registered</code> mentally into <code>STUDENT</code>. Which date would you store if the same student joined three clubs on three different days? Now move it into <code>CLUB</code>. Which date would represent thirty different members?</p>
<div class="example-box"><code>date_registered</code> depends on the complete pair <code>(club_id, student_id)</code>, so it belongs to <code>MEMBERSHIP</code>.</div>
""",
            ),
        ],
        [
            "Entities have independent identities; relationships connect entity occurrences.",
            "An attribute belongs where its value describes exactly one row's meaning.",
            "MEMBERSHIP is both a relationship in the conceptual model and a table in the relational model.",
        ],
    ),
    lesson(
        2,
        "Cardinality, Ordinality, and Crow's Foot Notation",
        "Cardinality gives the maximum participation and ordinality gives the minimum participation. Together they define the endpoint symbol at each side of a relationship.",
        [
            step(
                "Decode the four endpoint symbols",
                """
<table>
  <tr><th>Endpoint</th><th>Ordinality: minimum</th><th>Cardinality: maximum</th><th>Crow's Foot idea</th></tr>
  <tr><td><code>0..1</code></td><td>0 — optional</td><td>One</td><td>circle + bar</td></tr>
  <tr><td><code>1</code></td><td>1 — mandatory</td><td>One</td><td>bar + bar</td></tr>
  <tr><td><code>0..*</code></td><td>0 — optional</td><td>Many</td><td>circle + crow's foot</td></tr>
  <tr><td><code>1..*</code></td><td>1 — mandatory</td><td>Many</td><td>bar + crow's foot</td></tr>
</table>
<p>{{Ordinality}} is the minimum. {{Cardinality}} is the maximum. {{Multiplicity}} combines the two into values such as <code>0..*</code>.</p>
""",
            ),
            step(
                "Build ordinality and cardinality from business rules",
                lab_widget(
                    "multiplicity",
                    "Choose both relationship ends",
                    "For each rule, choose the combined minimum–maximum value at both ends. The tutor then explains the ordinality and cardinality represented by your choices.",
                    {
                        "options": ["0..1", "1", "0..*", "1..*"],
                        "scenarios": [
                            {
                                "left": "FACULTY",
                                "verb": "has",
                                "right": "STUDENT",
                                "leftAnswer": "1",
                                "rightAnswer": "0..*",
                                "rule": "Each student belongs to exactly one faculty; a faculty may currently have no students or many students.",
                            },
                            {
                                "left": "ADVISOR",
                                "verb": "advises",
                                "right": "CLUB",
                                "leftAnswer": "1",
                                "rightAnswer": "0..*",
                                "rule": "Each club has exactly one advisor; an advisor master record may be assigned to zero or many clubs.",
                            },
                            {
                                "left": "CLUB",
                                "verb": "organises",
                                "right": "EVENT",
                                "leftAnswer": "1",
                                "rightAnswer": "1..*",
                                "rule": "Every event belongs to one club, and the assignment assumes every participating club runs at least one event.",
                            },
                            {
                                "left": "MEMBERSHIP",
                                "verb": "qualifies",
                                "right": "CLUB_PRESIDENT",
                                "leftAnswer": "1",
                                "rightAnswer": "0..1",
                                "rule": "Every presidency uses one membership, while most memberships do not become presidencies.",
                            },
                        ],
                    },
                ),
            ),
            step(
                "Read from the opposite end",
                """
<p>The symbol beside an entity tells how many of that entity may relate to one occurrence at the opposite end. Read both directions:</p>
<div class="example-box"><strong>FACULTY 1 — 0..* STUDENT</strong><br>One faculty may have zero or many students. Each student must belong to exactly one faculty.</div>
<p>If a minimum count such as “every club runs at least one event” must always hold, a normal foreign key alone cannot prove the parent already has a child. That rule needs application logic, deferred checking, or an audit query.</p>
""",
            ),
        ],
        [
            "Ordinality is the minimum: zero means optional and one means mandatory.",
            "Cardinality is the maximum: one uses a bar and many uses the crow's foot.",
            "Always translate the diagram into two plain-English sentences.",
        ],
    ),
    lesson(
        3,
        "Resolving a Many-to-Many Relationship",
        "A student can join many clubs, and a club can contain many students. Relational tables resolve this many-to-many fact through an associative entity.",
        [
            step(
                "Why a direct M:N link is insufficient",
                """
<p>Putting a list such as <code>CL001, CL004, CL009</code> inside one <code>STUDENT</code> column would break first normal form and make joins, constraints, and updates difficult.</p>
<div class="highlight-box">Create one <code>MEMBERSHIP</code> row for each student–club pairing. The original M:N relationship becomes two 1:M relationships.</div>
""",
                diagram="""flowchart LR
  S[STUDENT] -->|1 to many| M[MEMBERSHIP]
  C[CLUB] -->|1 to many| M
  style S fill:#dbeafe,stroke:#3b82f6
  style C fill:#dbeafe,stroke:#3b82f6
  style M fill:#fef3c7,stroke:#f59e0b
""",
            ),
            step(
                "Build the junction table",
                lab_widget(
                    "junction-builder",
                    "Place each column in its correct table",
                    "Select a destination table for every column, then check the design.",
                    {
                        "tables": ["STUDENT", "MEMBERSHIP", "CLUB"],
                        "columns": [
                            {"label": "student_id (PK)", "answer": 0, "why": "STUDENT owns the student identifier as its primary key."},
                            {"label": "student_name", "answer": 0, "why": "The name depends only on student_id."},
                            {"label": "club_id (PK)", "answer": 2, "why": "CLUB owns the club identifier as its primary key."},
                            {"label": "club_name", "answer": 2, "why": "The club name depends only on club_id."},
                            {"label": "student_id (FK)", "answer": 1, "why": "MEMBERSHIP copies student_id to reference the participating student."},
                            {"label": "club_id (FK)", "answer": 1, "why": "MEMBERSHIP copies club_id to reference the participating club."},
                            {"label": "date_registered", "answer": 1, "why": "The date depends on a particular student–club pairing."},
                            {"label": "membership_status", "answer": 1, "why": "Status describes one membership, not every membership of the student or club."},
                        ],
                    },
                ),
            ),
            step(
                "The pattern appears again",
                """
<p><code>EVENT_REGISTRATION</code> applies the same pattern to students and events. It stores one row for each student–event registration, with <code>registration_date</code> and <code>attendance_status</code> describing that pairing.</p>
<p>This assignment additionally copies <code>club_id</code> into the registration so composite foreign keys can prove the event and member belong to the same club.</p>
""",
            ),
        ],
        [
            "An M:N relationship becomes an associative entity or junction table.",
            "Each junction row represents one pairing.",
            "Attributes of the relationship belong in the junction table.",
        ],
    ),
    lesson(
        4,
        "Composite Keys Without Guesswork",
        "A composite key is necessary when no single column identifies a row, but a combination does. The MEMBERSHIP table is the clearest example in this assignment.",
        [
            step(
                "Test uniqueness one column at a time",
                """
<p><code>club_id</code> cannot identify a membership because one club has many members. <code>student_id</code> cannot identify a membership because one student can join many clubs.</p>
<div class="highlight-box">The pair <code>(club_id, student_id)</code> identifies exactly one membership. Neither part can be removed, so the pair is a candidate key and may be chosen as the composite primary key.</div>
""",
            ),
            step(
                "Create rows and find collisions",
                lab_widget(
                    "composite-key",
                    "Which columns must work together?",
                    "Select key columns, inspect whether the sample rows remain unique, then try adding memberships.",
                    {
                        "columns": ["club_id", "student_id", "date_registered"],
                        "answer": ["club_id", "student_id"],
                        "rows": [
                            {"club_id": "CL001", "student_id": "ST0001", "date_registered": "2026-01-10"},
                            {"club_id": "CL001", "student_id": "ST0002", "date_registered": "2026-01-12"},
                            {"club_id": "CL003", "student_id": "ST0001", "date_registered": "2026-02-02"},
                        ],
                        "candidates": [
                            {"club_id": "CL003", "student_id": "ST0003", "date_registered": "2026-02-04", "valid": True, "why": "This student–club pair does not exist yet."},
                            {"club_id": "CL001", "student_id": "ST0001", "date_registered": "2026-03-01", "valid": False, "why": "The pair (CL001, ST0001) already exists; changing the date does not create a new membership identity."},
                        ],
                    },
                ),
            ),
            step(
                "Primary keys and foreign keys can both be composite",
                """
<p><code>EVENT_REGISTRATION(event_id, student_id)</code> uses a composite primary key so one student registers for an event at most once.</p>
<p>Its <code>(club_id, student_id)</code> pair is also a {{Composite Foreign Key}} referencing <code>MEMBERSHIP(club_id, student_id)</code>. The same columns can participate in more than one constraint because each constraint proves a different rule.</p>
""",
            ),
        ],
        [
            "A composite key is a minimal combination of two or more columns that uniquely identifies a row.",
            "Each key component may repeat by itself; the complete key may not repeat.",
            "Composite foreign keys require the same column order and values as the referenced key.",
        ],
    ),
    lesson(
        5,
        "Foreign Keys as Business-Rule Guards",
        "Foreign keys do more than draw lines between tables. Carefully chosen composite foreign keys make invalid assignment transactions impossible.",
        [
            step(
                "Follow the integrity chain",
                """
<ul>
  <li><code>CLUB_PRESIDENT(club_id, student_id)</code> references <code>MEMBERSHIP(club_id, student_id)</code>.</li>
  <li><code>EVENT(event_id, club_id)</code> identifies the event and its organising club.</li>
  <li><code>EVENT_REGISTRATION(club_id, student_id)</code> references a membership in that same club.</li>
</ul>
<div class="highlight-box">The database verifies identities and relationships from existing rows; it does not trust a text description saying that the rule is true.</div>
""",
                diagram="""flowchart LR
  M[MEMBERSHIP club_id + student_id] --> P[CLUB_PRESIDENT]
  M --> R[EVENT_REGISTRATION]
  E[EVENT event_id + club_id] --> R
  style M fill:#fef3c7,stroke:#f59e0b
  style E fill:#dbeafe,stroke:#3b82f6
  style P fill:#f0fdf4,stroke:#059669
  style R fill:#f0fdf4,stroke:#059669
""",
            ),
            step(
                "Predict which transactions survive",
                lab_widget(
                    "integrity-simulator",
                    "Accept or reject each transaction",
                    "Decide first, then reveal which constraint controls the result.",
                    {
                        "transactions": [
                            {
                                "sql": "Appoint ST0001 as president of CL001",
                                "facts": ["MEMBERSHIP contains (CL001, ST0001)"],
                                "valid": True,
                                "why": "The composite foreign key finds the required membership row.",
                            },
                            {
                                "sql": "Appoint ST0003 as president of CL001",
                                "facts": ["ST0003 exists", "MEMBERSHIP does not contain (CL001, ST0003)"],
                                "valid": False,
                                "why": "Existence as a student is insufficient; the exact club–student membership must exist.",
                            },
                            {
                                "sql": "Register ST0002 for EV010 run by CL003",
                                "facts": ["EVENT contains (EV010, CL003)", "MEMBERSHIP contains (CL003, ST0002)"],
                                "valid": True,
                                "why": "Both the event–club and club–student composite foreign keys match.",
                            },
                            {
                                "sql": "Register ST0002 for EV010 but supply club_id CL001",
                                "facts": ["EVENT EV010 belongs to CL003", "ST0002 is a member of CL001"],
                                "valid": False,
                                "why": "The event composite foreign key rejects (EV010, CL001), preventing a club mismatch.",
                            },
                        ]
                    },
                ),
            ),
            step(
                "What a foreign key cannot prove",
                """
<p>A foreign key can require a referenced parent row, but it cannot normally require a parent to have at least one child. For example, <code>EVENT.club_id → CLUB.club_id</code> proves every event has a club; it does not prove every club has an event.</p>
<div class="example-box">Use the populated dataset and an audit query to verify minimum child counts such as three events per club.</div>
""",
            ),
        ],
        [
            "Foreign keys reject references to non-existent parent keys.",
            "Composite foreign keys can enforce same-club rules across relationships.",
            "Parent minimum-child counts need more than an ordinary foreign key.",
        ],
    ),
    lesson(
        6,
        "Normalization: Put Each Fact in One Place",
        "Normalization becomes practical when you ask what each attribute depends on. The goal is not merely to create more tables; it is to prevent contradictory copies of the same fact.",
        [
            step(
                "Find partial and transitive dependencies",
                """
<p>Imagine one oversized row:</p>
<p><code>(student_id, student_name, faculty_id, faculty_name, club_id, club_name, advisor_id, advisor_name, date_registered)</code></p>
<ul>
  <li><code>student_name</code> depends only on <code>student_id</code>.</li>
  <li><code>club_name</code> and <code>advisor_id</code> depend only on <code>club_id</code>.</li>
  <li><code>advisor_name</code> depends on <code>advisor_id</code>, not directly on the membership pair.</li>
  <li><code>date_registered</code> depends on the complete pair <code>(club_id, student_id)</code>.</li>
</ul>
""",
            ),
            step(
                "Decompose the oversized row",
                lab_widget(
                    "normalization-sorter",
                    "Move every fact to its determinant",
                    "Choose the table where each non-key attribute belongs. The completed model removes repeated names from membership rows.",
                    {
                        "tables": ["STUDENT", "FACULTY", "CLUB", "ADVISOR", "MEMBERSHIP"],
                        "items": [
                            {"label": "student_name", "answer": 0, "why": "student_id determines student_name."},
                            {"label": "faculty_name", "answer": 1, "why": "faculty_id determines faculty_name."},
                            {"label": "club_name", "answer": 2, "why": "club_id determines club_name."},
                            {"label": "advisor_id (assigned FK)", "answer": 2, "why": "The assigned advisor foreign key is a fact about the club."},
                            {"label": "advisor_name", "answer": 3, "why": "advisor_id determines advisor_name."},
                            {"label": "date_registered", "answer": 4, "why": "The complete (club_id, student_id) pair determines the join date."},
                            {"label": "membership_status", "answer": 4, "why": "Status describes one student–club membership."},
                        ],
                    },
                ),
            ),
            step(
                "Connect 1NF, 2NF, and 3NF",
                """
<table>
  <tr><th>Normal form</th><th>Question to ask here</th></tr>
  <tr><td>1NF</td><td>Does every cell contain one atomic value rather than a list of clubs or events?</td></tr>
  <tr><td>2NF</td><td>In a composite-key table, does every non-key attribute depend on the whole key?</td></tr>
  <tr><td>{{Third Normal Form}}</td><td>Does a non-key attribute depend on another non-key attribute that belongs elsewhere?</td></tr>
</table>
<div class="highlight-box">The final design keeps each fact in one authoritative place and connects those places with keys.</div>
""",
            ),
        ],
        [
            "1NF removes repeating groups and multi-valued cells.",
            "2NF removes dependencies on only part of a composite key.",
            "3NF removes transitive dependencies through non-key attributes.",
        ],
    ),
]

# The complete canvas is inserted first; keep lesson numbers aligned with display order.
for lesson_number, lesson_data in enumerate(LESSONS, start=1):
    lesson_data["number"] = lesson_number


def clear_tutorial(cursor):
    cursor.execute(
        "DELETE FROM lesson_recaps WHERE lesson_id IN (SELECT id FROM lessons WHERE tutorial_id=?)",
        (TUTORIAL_ID,),
    )
    cursor.execute(
        "DELETE FROM lesson_steps WHERE lesson_id IN (SELECT id FROM lessons WHERE tutorial_id=?)",
        (TUTORIAL_ID,),
    )
    cursor.execute("DELETE FROM lessons WHERE tutorial_id=?", (TUTORIAL_ID,))
    cursor.execute("DELETE FROM tutorials WHERE id=?", (TUTORIAL_ID,))


def migrate(conn):
    cursor = conn.cursor()
    course = cursor.execute("SELECT id FROM courses WHERE id=?", (COURSE_ID,)).fetchone()
    if not course:
        raise RuntimeError("The existing bcl1223 course was not found; refusing to create detached content.")

    clear_tutorial(cursor)

    for term, definition in GLOSSARY.items():
        cursor.execute(
            """
            INSERT INTO glossary (course_id, term, definition) VALUES (?,?,?)
            ON CONFLICT(course_id, term) DO UPDATE SET definition=excluded.definition
            """,
            (COURSE_ID, term, definition),
        )

    cursor.execute(
        """
        INSERT INTO tutorials (id, course_id, title, short_title, c_idx, sort_order)
        VALUES (?,?,?,?,?,?)
        """,
        (
            TUTORIAL_ID,
            COURSE_ID,
            "Assignment Visual Lab — Student Clubs ERD",
            "Assignment Visual Lab",
            2,
            2,
        ),
    )

    for lesson_index, lesson_data in enumerate(LESSONS):
        cursor.execute(
            "INSERT INTO lessons (tutorial_id, number, title, intro, sort_order) VALUES (?,?,?,?,?)",
            (
                TUTORIAL_ID,
                lesson_data["number"],
                lesson_data["title"],
                lesson_data["intro"],
                lesson_index,
            ),
        )
        lesson_id = cursor.lastrowid
        for step_index, step_data in enumerate(lesson_data["steps"]):
            cursor.execute(
                """
                INSERT INTO lesson_steps (lesson_id, title, body_html, diagram_mermaid, sort_order)
                VALUES (?,?,?,?,?)
                """,
                (
                    lesson_id,
                    step_data["title"],
                    step_data["body"].strip(),
                    step_data.get("diagram"),
                    step_index,
                ),
            )
        for recap_index, recap in enumerate(lesson_data["recap"]):
            cursor.execute(
                "INSERT INTO lesson_recaps (lesson_id, text, sort_order) VALUES (?,?,?)",
                (lesson_id, recap, recap_index),
            )

    conn.commit()

    counts = cursor.execute(
        """
        SELECT COUNT(DISTINCT l.id), COUNT(DISTINCT s.id), COUNT(DISTINCT r.id)
        FROM lessons l
        LEFT JOIN lesson_steps s ON s.lesson_id=l.id
        LEFT JOIN lesson_recaps r ON r.lesson_id=l.id
        WHERE l.tutorial_id=?
        """,
        (TUTORIAL_ID,),
    ).fetchone()
    expected = (7, 21, 21)
    if counts != expected:
        raise RuntimeError(f"Unexpected assignment lab counts: {counts}; expected {expected}")
    print(f"Migrated {TUTORIAL_ID}: lessons={counts[0]}, steps={counts[1]}, recaps={counts[2]}")
    return counts


if __name__ == "__main__":
    connection = sqlite3.connect(str(DB_PATH))
    try:
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA foreign_keys=ON")
        migrate(connection)
    finally:
        connection.close()
