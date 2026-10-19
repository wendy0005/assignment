# BCL1233 — System Analysis and Design
## Assignment 1: Requirement Analysis for a Hybrid Work Monitoring System

---

## 1. Problem Analysis (20 marks)

### a) Problems in the Current Manual System

**Problem 1: Inaccurate Attendance Tracking**
The current system relies on manual tools such as spreadsheets and chat messages to record employee attendance. Employees may forget to log their hours, submit inconsistent entries, or report incorrect work locations. There is no automated validation mechanism, making the attendance data unreliable.

**Problem 2: Lack of Real-Time Work Visibility for Managers**
Managers currently depend on periodic email updates and individual check-ins to monitor task progress. This creates information delays — a manager may not know that a task is behind schedule until the next status meeting. The absence of a live dashboard prevents proactive intervention.

### b) Impact Analysis

| Impact On | Problem 1: Inaccurate Attendance | Problem 2: Lack of Real-Time Visibility |
|---|---|---|
| **Employees** | Frustration from manually tracking hours; potential payroll errors if hours are misreported; disputes over attendance records | Reduced autonomy as managers compensate by requesting more frequent manual updates; difficulty demonstrating productivity |
| **Managers** | Time wasted manually verifying attendance sheets and correcting entries; inability to trust reported data for decisions | Cannot identify bottlenecks early; forced to rely on intuition rather than data; reactive instead of proactive management |
| **Organization** | Payroll inaccuracies leading to compliance risks; inflated administrative overhead; difficulty justifying hybrid work policy to leadership | Lower project predictability; missed deadlines due to undetected delays; reduced overall operational efficiency |

---

## 2. System Objectives (20 marks)

### Five Objectives of the Hybrid Work Monitoring System

**Objective 1: Automate Attendance Capture**
Replace manual spreadsheets with a digital check-in/check-out system that records employee attendance and work location (remote or office) in real time, eliminating data entry errors and ensuring accurate payroll records.

**Objective 2: Enable Real-Time Task Tracking**
Provide a centralized platform where employees update task status and managers view progress instantly, reducing information latency from days to seconds.

**Objective 3: Centralize Reporting and Analytics**
Consolidate attendance, task completion, and productivity data into a single dashboard that generates on-demand reports for managers, HR, and senior leadership.

**Objective 4: Improve Communication and Notification**
Deliver automated notifications for task deadlines, meeting reminders, and status changes, reducing reliance on fragmented email and chat threads.

**Objective 5: Support Data-Driven Decision Making**
Equip management with historical trends and real-time metrics to evaluate workforce productivity, optimize hybrid schedules, and identify process improvements.

---

## 3. Stakeholder Analysis (10 marks)

### a) & b) Five Stakeholders — Identification, Classification, and Responsibilities

| Stakeholder | Classification | Role & Involvement | Responsibility |
|---|---|---|---|
| **Employees** | Primary / End User | Direct users of the system — check in/out, update task status, receive notifications | Use the system daily to record attendance and task progress; provide feedback for improvements |
| **Managers / Team Leads** | Primary / Operational | Monitor team task progress and attendance; approve requests; generate reports | Review dashboards to track performance; intervene on delayed tasks; approve leave and schedule changes |
| **Human Resources (HR)** | Secondary / Administrative | Oversee attendance data for payroll, compliance, and policy enforcement | Configure attendance rules; audit records; generate compliance reports |
| **IT / System Administrator** | Secondary / Technical | Deploy, maintain, and secure the system; manage user accounts and permissions | Ensure system uptime; perform backups; troubleshoot technical issues; manage access control |
| **Senior Management / Director** | Tertiary / Strategic | Review high-level productivity trends and hybrid-work effectiveness | Use aggregated analytics to inform strategic decisions on work-from-home policy and resource allocation |

---

## 4. System Requirements (20 marks)

### a) Three Functional Requirements

| ID | Functional Requirement | Description |
|---|---|---|
| FR-01 | Digital Check-In/Check-Out | The system shall allow employees to check in and check out using a web or mobile interface, recording the timestamp and geolocation (office or remote) automatically. |
| FR-02 | Task Assignment and Status Tracking | The system shall enable managers to assign tasks to employees with deadlines and priority levels. Employees shall update task status (Not Started, In Progress, Completed) and add progress notes. |
| FR-03 | Notification Engine | The system shall send automated email and in-app notifications for upcoming deadlines, assigned tasks, meeting reminders, and any missed check-ins exceeding a configurable threshold. |

### b) Two Non-Functional Requirements

| ID | Non-Functional Requirement | Description |
|---|---|---|
| NFR-01 | Availability (Uptime) | The system shall achieve at least 99.5% uptime during business hours (Monday–Friday, 8:00 AM – 8:00 PM) to ensure employees can always check in and managers can always access dashboards. |
| NFR-02 | Response Time | The system shall process and display dashboard data within three seconds of a user request, even when supporting up to 500 concurrent users during peak hours. |

---

## 5. Requirement Gathering Technique (10 marks)

### a) Selected Technique

**Structured Interviews**

### b) Justification

Structured interviews are the most suitable technique for this hybrid work monitoring system because:

- The stakeholders are diverse (employees, managers, HR, IT, senior management), each with distinct needs. Interviews allow the analyst to tailor questions to each role while maintaining a consistent core structure.
- The hybrid work context involves sensitive topics — trust, privacy, and performance monitoring — that stakeholders may be reluctant to discuss honestly in a group setting like a focus group. One-on-one interviews encourage candid responses.
- The system requirements involve both operational workflows (check-in, task tracking) and strategic needs (reporting, analytics). Interviews enable deep exploration of each area with follow-up probing questions.

### c) Application in Collecting System Requirements

1. **Planning:** Identify five to six stakeholder groups (employees, managers, HR, IT, senior management). Design a structured question set with sections covering: current pain points, desired features, workflow expectations, and privacy concerns.

2. **Conducting:** Schedule 30–45 minute sessions with 2–3 representatives from each stakeholder group. Ask the prepared questions in a fixed order, but allow clarifying follow-ups. Record responses with permission.

3. **Analysis:** Transcribe each interview and extract candidate requirements using thematic coding — grouping similar responses under functional and non-functional categories.

4. **Validation:** Present the consolidated requirements list back to a subset of interviewees to confirm accuracy and prioritization before finalizing the requirements specification document.

---

## 6. System Function Description (10 marks)

### Selected Function: Digital Check-In/Check-Out

| Component | Description |
|---|---|
| **Function Specification** | Employees record their arrival and departure times through the system, which automatically captures the timestamp, date, and work location (office or remote). The system validates the check-in against the employee's assigned schedule and flags any anomalies (late check-in, missing check-out). |
| **User Roles Involved** | **Employee** — initiates check-in/check-out. **Manager** — views team attendance records and resolves flagged anomalies. **HR** — configures grace periods and schedule rules; accesses consolidated attendance reports. |
| **Pre-Conditions** | Employee has an active account and is assigned to a work schedule. The system time zone is correctly configured. Network connectivity is available. |
| **Sequential Process Flow** | 1. Employee navigates to the Check-In page on the web portal or mobile app.<br>2. System detects the device's geolocation and classifies the location as "Office" or "Remote".<br>3. Employee taps the Check-In button.<br>4. System records the timestamp, location, and date in the attendance log.<br>5. System compares the check-in time against the employee's scheduled start time.<br>6. If late: system marks the record as "Late" and sends a notification to the employee with a prompt to provide a reason.<br>7. At the end of the workday, employee taps Check-Out.<br>8. System records the check-out time and calculates total hours worked.<br>9. If check-out is missed by 30+ minutes: system sends a reminder notification.<br>10. Manager's dashboard updates immediately with the latest attendance status. |
| **Post-Condition / Output** | An attendance record is created in the database with: EmployeeID, Date, Check-In Time, Check-Out Time, Location (Office/Remote), Status (On Time / Late / Early Leave). The record is visible in real time on the manager's dashboard and included in the next HR attendance report. |

---

## 7. System Failure Prevention (10 marks)

Requirement analysis is the foundation upon which every subsequent phase of system development depends. A poorly executed requirement analysis is consistently cited as one of the primary causes of software project failure — exceeding even technical shortcomings (The Standish Group, 2020). Its role in minimizing design and implementation failures can be evaluated across three key dimensions.

**Preventing Scope Creep:** When requirements are captured ambiguously or incompletely, stakeholders introduce new features during development under the assumption they were "obvious." This uncontrolled expansion — scope creep — is responsible for budget overruns and delayed deliveries in the majority of failed projects. A thorough requirement analysis produces a signed-off requirements specification that serves as a contract between stakeholders and the development team, establishing a clear boundary for what the system will and will not include.

**Reducing Rework Costs:** Correcting a requirement error discovered during the design phase costs roughly five times more than fixing it during requirement analysis. If that same error is only discovered during testing or after deployment, the cost multiplies to fifty or a hundred times (McConnell, 2004). For the Hybrid Work Monitoring System, an ambiguous requirement like "track attendance" could be misinterpreted by developers as simple time logging, when stakeholders actually expected geolocation-based check-in with anomaly detection. Discovering this gap after coding begins would require redesigning the database schema, rewriting the check-in module, and retesting — weeks of wasted effort that could have been avoided with precise requirement specification.

**Aligning Stakeholder Expectations:** Different stakeholders hold different mental models of the system. HR may envision a compliance tool, while managers see a productivity tracker, and employees worry about surveillance. Without structured requirement analysis, these conflicting expectations remain hidden until the system is demonstrated — at which point at least one group is disappointed. Techniques such as interviews, prototyping, and validation sessions surface these conflicts early, allowing the analyst to negotiate a shared understanding before a single line of code is written.

**Conclusion:** Requirement analysis acts as the risk-reduction mechanism of the development lifecycle. For the Hybrid Work Monitoring System, where the system touches sensitive areas of employee privacy, managerial oversight, and organizational policy, precise requirement analysis is not merely beneficial — it is essential to avoid costly rework, missed deadlines, and stakeholder dissatisfaction.

---

### References

McConnell, S. (2004). *Code Complete: A Practical Handbook of Software Construction* (2nd ed.). Microsoft Press.

The Standish Group. (2020). *CHAOS Report 2020: Beyond Infinity*. The Standish Group International, Inc.
