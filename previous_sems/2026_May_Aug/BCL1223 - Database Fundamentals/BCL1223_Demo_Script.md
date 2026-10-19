# BCL1223 Database Fundamentals — Demo Script

**Student:** Chan Jing Yi

**ID:** SUOL2500321

**Date:** Saturday, 8 August 2026 (Week 11, 4th Live Session)  
**Platform:** MS Teams — screen share + camera on  
**Duration:** ~5-7 minutes  

---

## Before Demo (have these ready)

- [ ] **Browser 1**: Oracle Live SQL with the database already populated
- [ ] **Browser 2** or PDF: Your report open
- [ ] **Camera**: On. No need to dress up, just be presentable
- [ ] **Mute notifications** on your PC

---

## Demo Flow

### 1. ERD & Design → "What I built" (1.5 min)

**Share your report PDF**, scroll to the ERD diagram.

> *"Good morning. I built a database for the SEGi Student Clubs and Societies system. I have **11 tables** total.
> The core entities are FACULTY, STUDENT, CLUB, ADVISOR, VENUE, EVENT, and SEMESTER.
> 
> The first important design decision was the **MEMBERSHIP** table. STUDENT and CLUB have a many-to-many relationship because a student can join several clubs and each club can have many students. A direct many-to-many relationship cannot be implemented cleanly in a relational database, so MEMBERSHIP resolves it into two one-to-many relationships. It also stores `date_registered` and `membership_status`, because those values describe a student's membership in a particular club rather than the student or club independently.
>
> **EVENT_REGISTRATION** is separate from MEMBERSHIP because joining a club and registering for one of its events are different facts. A member may attend some events and skip others. This table records the event, student, registration date, and attendance status. Its composite foreign keys also ensure that the event belongs to the stated club and that the registering student is a member of that same club.
>
> **CLUB_PRESIDENT** is another separate relationship. Its composite foreign key points to MEMBERSHIP, which means a student cannot become president of a club unless that exact student-club membership already exists. Keeping this rule in the database prevents invalid data regardless of which application enters it.
> 
> The design is normalized to Third Normal Form. There are no repeating groups, each non-key attribute depends on its complete key, and descriptive data is stored only with the entity it describes. For example, the faculty name is stored in FACULTY rather than being repeated in every STUDENT row. This reduces duplication and prevents update inconsistencies."*

**Point at several relationships on the ERD while speaking:**

- `FACULTY` 1:M `STUDENT`
- `ADVISOR` 1:M `CLUB`
- `STUDENT` M:N `CLUB`, resolved by `MEMBERSHIP`
- `CLUB` 1:M `EVENT`
- `VENUE` 1:M `EVENT`
- `SEMESTER` 1:M `EVENT`

### 2. Switch to Oracle Live SQL → "Show it working" (1.5 min)

**Share your Oracle Live SQL tab.**

> *"The schema was verified on Oracle AI Database 26ai Free, and I am using Oracle Live SQL today to demonstrate the same Oracle SQL."*

Run the table count:

```sql
SELECT COUNT(*) AS table_count
FROM user_tables
WHERE table_name IN (
    'FACULTY', 'ADVISOR', 'VENUE_PIC', 'SEMESTER', 'STUDENT',
    'CLUB', 'VENUE', 'MEMBERSHIP', 'CLUB_PRESIDENT',
    'EVENT', 'EVENT_REGISTRATION'
);
```

Run the total seed-row count:

```sql
SELECT
    (SELECT COUNT(*) FROM faculty) +
    (SELECT COUNT(*) FROM advisor) +
    (SELECT COUNT(*) FROM venue_pic) +
    (SELECT COUNT(*) FROM semester) +
    (SELECT COUNT(*) FROM student) +
    (SELECT COUNT(*) FROM club) +
    (SELECT COUNT(*) FROM venue) +
    (SELECT COUNT(*) FROM membership) +
    (SELECT COUNT(*) FROM club_president) +
    (SELECT COUNT(*) FROM event) +
    (SELECT COUNT(*) FROM event_registration)
    AS total_seed_rows
FROM dual;
```

> *"The schema contains 11 assessment tables and 228 rows of seed data."*

> *"I count the assessment tables from Oracle's `USER_TABLES` data dictionary. I count the seed records directly from the 11 tables instead of relying on metadata statistics, because metadata row estimates may be outdated until statistics are gathered. The total consists of 10 faculties, 10 advisors, 10 venue PICs, 3 semesters, 30 students, 15 clubs, 10 venues, 50 memberships, 15 presidents, 45 events, and 30 event registrations."*

**Run rejection test** (the most impressive part):

```sql
SAVEPOINT before_demo_test;

-- bb1002 is a student, but is not a member of club C001
UPDATE club_president
SET student_id = 'bb1002'
WHERE club_id = 'C001';

ROLLBACK TO before_demo_test;
```

> *"Here I deliberately try to replace the president of club C001 with student bb1002. The student exists, but the pair C001 and bb1002 does not exist in MEMBERSHIP. Oracle therefore rejects the update through the composite foreign key named `fk_president_membership`.
>
> This is stronger than checking only the student ID. A normal foreign key to STUDENT would prove that bb1002 is a valid student, but it would not prove membership in C001. Referencing the combined club and student key proves both facts together. The savepoint and rollback protect the demonstration data, so this test does not leave any permanent change."*

**Expected outcome:** an Oracle integrity-constraint error naming `FK_PRESIDENT_MEMBERSHIP`.

**If asked why this is useful:**

> *"Business rules remain protected even if data is inserted through another program, an import script, or a different user interface. The rule is enforced at the database level."*

### 3. Run 3 Queries Live → "Reports" (2-3 min)

**Query 1 — Multi-club advisors** (JOIN + GROUP BY + HAVING):

```sql
SELECT a.advisor_name,
       COUNT(c.club_id) AS number_of_clubs,
       LISTAGG(c.club_name, '; ') WITHIN GROUP (ORDER BY c.club_name) AS assigned_clubs
FROM advisor a
JOIN club c ON c.advisor_id = a.advisor_id
GROUP BY a.advisor_id, a.advisor_name
HAVING COUNT(c.club_id) > 1
ORDER BY a.advisor_name;
```

> *"Management wanted to identify lecturers who advise more than one club. The inner JOIN matches each advisor with the CLUB rows containing that advisor's ID. `GROUP BY` creates one result group per advisor, and `COUNT` calculates the number of clubs in each group. `HAVING` is used instead of `WHERE` because the condition is applied after the groups have been counted. `LISTAGG` combines the matching club names into one readable value, so the result shows both the workload count and the actual club assignments."*

**Expected result:** four advisors. Dr. Aisha Rahman has three clubs; Dr. Kelvin Wong, Mr. Daniel Lee, and Ms. Nur Izzati each have two.

**Query 2 — Missing approval forms** (correlated subquery):

```sql
SELECT s.student_id, s.student_name, s.phone_number
FROM student s
WHERE s.approval_form = 'N'
  AND EXISTS (
      SELECT 1 FROM membership m WHERE m.student_id = s.student_id
  )
ORDER BY s.student_name;
```

> *"This query produces a contact list for students who joined at least one club but have not submitted their faculty approval form. The first condition selects students whose approval flag is N. The correlated `EXISTS` subquery then checks MEMBERSHIP using the current student's ID.
>
> I used `EXISTS` because the question only asks whether at least one membership is present; Oracle can stop searching after it finds the first match. It also avoids duplicate student rows when a student belongs to several clubs. The final `ORDER BY` makes the calling list easier for staff to use."*

**Expected result:** 10 students with missing approval forms.

**Query 3 — Pivot by semester** (cross-tab report):

```sql
SELECT advisor_name,
       NVL(may_aug_2026, 0) AS may_aug_2026,
       NVL(sep_dec_2026, 0) AS sep_dec_2026,
       NVL(jan_apr_2027, 0) AS jan_apr_2027
FROM (
    SELECT a.advisor_name, s.semester_name, e.event_id
    FROM advisor a
    LEFT JOIN club c ON c.advisor_id = a.advisor_id
    LEFT JOIN event e ON e.club_id = c.club_id
    LEFT JOIN semester s ON s.semester_id = e.semester_id
)
PIVOT (
    COUNT(event_id)
    FOR semester_name IN (
        'May-Aug 2026' AS may_aug_2026,
        'Sep-Dec 2026' AS sep_dec_2026,
        'Jan-Apr 2027' AS jan_apr_2027
    )
)
ORDER BY advisor_name;
```

> *"The inner query first connects advisors to clubs, events, and semesters. At that stage, each event is still represented as a separate row. Oracle's `PIVOT` operator groups those rows by advisor, changes the three semester names into columns, and counts the event IDs in each column.
>
> `NVL` converts any missing count to zero instead of displaying null. The output contains all 10 advisors because the query begins with ADVISOR and uses left joins. Each semester column totals 15 events because there are 15 clubs and every club holds one event per semester. Dr. Aisha advises three clubs, so her row shows three events in every semester. Across all three semesters, the pivot reconciles to the 45 EVENT records stored in the database."*

**Expected result:** 10 advisor rows, with column totals of 15, 15, and 15.

### 4. Wrap-up (30 sec)

> *"That covers the main points:
> - 11 normalized tables with 228 rows
> - All PK, FK, CHECK, UNIQUE constraints enforced
> - 6 rejection tests passed (Oracle blocks bad data)
> - All 6 assessment queries return correct results
> 
> The main strength of the design is that its business rules are enforced by relationships and constraints rather than depending only on user input or application code. The queries then turn the normalized records into useful operational reports for Student Affairs.
>
> Thank you."*

---

## If the lecturer asks questions

| Question | Answer |
|----------|--------|
| "Why did you add EVENT_REGISTRATION?" | *"Because attending an event is different from being a club member. A student can be a member but not attend — separate table captures both facts."* |
| "Why not put president in CLUB table?" | *"Then I couldn't enforce that the president must be a member. With CLUB_PRESIDENT, I use a composite FK to MEMBERSHIP."* |
| "Why is date_registered in MEMBERSHIP?" | *"A student may join different clubs on different dates. The date describes one student-club relationship, so it belongs in MEMBERSHIP rather than STUDENT or CLUB."* |
| "Why use a composite key?" | *"Neither club ID nor student ID can uniquely identify a membership by itself. Their combination identifies one student's membership in one club and supports the president and event-registration business rules."* |
| "What is the difference between WHERE and HAVING?" | *"`WHERE` filters individual rows before grouping. `HAVING` filters completed groups, so it is appropriate for the condition `COUNT(c.club_id) > 1`."* |
| "Why use EXISTS?" | *"`EXISTS` checks whether at least one related membership row is present. It avoids duplicate students and expresses the requirement directly."* |
| "Why use LEFT JOIN in the pivot?" | *"It keeps advisors in the report even if they have no related event. `NVL` would then display zero rather than null."* |
| "How do you know there are 228 rows?" | *"I count the records directly from every assessment table: 10 + 10 + 10 + 3 + 30 + 15 + 10 + 50 + 15 + 45 + 30, which equals 228."* |
| "What does 3NF mean here?" | *"Every table represents one entity or relationship, non-key attributes depend on the key, and descriptive facts such as faculty and advisor details are not repeated in unrelated tables."* |
| "What happens if a parent row is deleted?" | *"Dependent data uses cascade deletion only where the dependent fact loses its meaning, such as a registration after its event is deleted. Master data such as advisors, venues, and semesters remains protected by restrictive foreign keys."* |
| "What tool did you use?" | *"Oracle Live SQL — free, no install needed. I also tested the script in SQL*Plus."* |
| "Did you use AI?" | *"I used it for brainstorming ideas and debugging syntax, but I wrote and understand every line. The design decisions are mine."* |
| "What normalization level?" | *"3NF. MEMBERSHIP resolves M:N, no transitive dependencies — faculty name is in FACULTY, not repeated in STUDENT."* |

---

## Quick Reference Sheet

**Your 11 tables:** FACULTY, ADVISOR, VENUE_PIC, SEMESTER, STUDENT, CLUB, VENUE, MEMBERSHIP, CLUB_PRESIDENT, EVENT, EVENT_REGISTRATION

**Your 228 rows:** 10 + 10 + 10 + 3 + 30 + 15 + 10 + 50 + 15 + 45 + 30

**Your 6 queries:** phone list, multi-club advisors, missing forms, event schedule, pivot table, club assignments

**Your DB:** Oracle AI Database 26ai Free 23.26.2.0.0
