-- BCL1223 Database Fundamentals Continuous Assessment
-- SEGi Student Clubs and Societies Database
-- Student: Chan Jing Yi (SUOL2500321)
-- Oracle Database Free / SQL*Plus compatible. The DDL and DML body can also
-- be used in Oracle Live SQL after omitting the client-only SET/SPOOL commands.

SET ECHO ON
SET FEEDBACK ON
SET HEADING ON
SET PAGESIZE 100
SET LINESIZE 220
SET LONG 20000
SET TRIMSPOOL ON
SET TAB OFF
SET SERVEROUTPUT ON
ALTER SESSION SET NLS_DATE_FORMAT = 'DD-MON-YYYY';

SPOOL /work/20260718_Database_Fundamentals_Assignment_Oracle_Output.txt

PROMPT ================================================================
PROMPT BCL1223 STUDENT CLUBS DATABASE - BUILD AND VERIFICATION
PROMPT ================================================================

-- The drop blocks make the script safely rerunnable in a student schema.
BEGIN EXECUTE IMMEDIATE 'DROP TABLE event_registration CASCADE CONSTRAINTS PURGE';
EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE event CASCADE CONSTRAINTS PURGE';
EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE club_president CASCADE CONSTRAINTS PURGE';
EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE membership CASCADE CONSTRAINTS PURGE';
EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE club CASCADE CONSTRAINTS PURGE';
EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE student CASCADE CONSTRAINTS PURGE';
EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE faculty CASCADE CONSTRAINTS PURGE';
EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE advisor CASCADE CONSTRAINTS PURGE';
EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE venue CASCADE CONSTRAINTS PURGE';
EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE venue_pic CASCADE CONSTRAINTS PURGE';
EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE semester CASCADE CONSTRAINTS PURGE';
EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF; END;
/

PROMPT === TASK 2.1: CREATE TABLES AND CONSTRAINTS ===

CREATE TABLE faculty (
    faculty_id       VARCHAR2(6),
    faculty_name     VARCHAR2(100) NOT NULL,
    CONSTRAINT pk_faculty PRIMARY KEY (faculty_id),
    CONSTRAINT uq_faculty_name UNIQUE (faculty_name)
);

CREATE TABLE advisor (
    advisor_id       VARCHAR2(6),
    advisor_name     VARCHAR2(100) NOT NULL,
    office_room      VARCHAR2(10) NOT NULL,
    office_phone     VARCHAR2(20) NOT NULL,
    CONSTRAINT pk_advisor PRIMARY KEY (advisor_id),
    CONSTRAINT uq_advisor_phone UNIQUE (office_phone)
);

CREATE TABLE venue_pic (
    pic_id           VARCHAR2(6),
    pic_name         VARCHAR2(100) NOT NULL,
    phone_number     VARCHAR2(20) NOT NULL,
    office_room      VARCHAR2(10) NOT NULL,
    CONSTRAINT pk_venue_pic PRIMARY KEY (pic_id),
    CONSTRAINT uq_venue_pic_phone UNIQUE (phone_number)
);

CREATE TABLE semester (
    semester_id      VARCHAR2(8),
    semester_name    VARCHAR2(30) NOT NULL,
    start_date       DATE NOT NULL,
    end_date         DATE NOT NULL,
    CONSTRAINT pk_semester PRIMARY KEY (semester_id),
    CONSTRAINT uq_semester_name UNIQUE (semester_name),
    CONSTRAINT ck_semester_dates CHECK (end_date > start_date)
);

CREATE TABLE student (
    student_id       VARCHAR2(6),
    student_name     VARCHAR2(100) NOT NULL,
    phone_number     VARCHAR2(20) NOT NULL,
    faculty_id       VARCHAR2(6) NOT NULL,
    approval_form    CHAR(1) DEFAULT 'N' NOT NULL,
    scholarship      CHAR(1) DEFAULT 'N' NOT NULL,
    CONSTRAINT pk_student PRIMARY KEY (student_id),
    CONSTRAINT uq_student_phone UNIQUE (phone_number),
    CONSTRAINT fk_student_faculty FOREIGN KEY (faculty_id)
        REFERENCES faculty (faculty_id),
    CONSTRAINT ck_student_id_format CHECK
        (REGEXP_LIKE(student_id, '^[[:alpha:]]{2}[[:digit:]]{4}$', 'c')),
    CONSTRAINT ck_student_approval CHECK (approval_form IN ('Y', 'N')),
    CONSTRAINT ck_student_scholarship CHECK (scholarship IN ('Y', 'N'))
);

CREATE TABLE club (
    club_id          VARCHAR2(6),
    club_name        VARCHAR2(100) NOT NULL,
    advisor_id       VARCHAR2(6) NOT NULL,
    club_notes       VARCHAR2(500),
    CONSTRAINT pk_club PRIMARY KEY (club_id),
    CONSTRAINT uq_club_name UNIQUE (club_name),
    CONSTRAINT fk_club_advisor FOREIGN KEY (advisor_id)
        REFERENCES advisor (advisor_id)
);

CREATE TABLE venue (
    venue_id         VARCHAR2(6),
    venue_name       VARCHAR2(100) NOT NULL,
    venue_type       VARCHAR2(30) NOT NULL,
    capacity         NUMBER(4) NOT NULL,
    pic_id           VARCHAR2(6) NOT NULL,
    CONSTRAINT pk_venue PRIMARY KEY (venue_id),
    CONSTRAINT uq_venue_name UNIQUE (venue_name),
    CONSTRAINT fk_venue_pic FOREIGN KEY (pic_id)
        REFERENCES venue_pic (pic_id),
    CONSTRAINT ck_venue_capacity CHECK (capacity > 0),
    CONSTRAINT ck_venue_type CHECK
        (venue_type IN ('CLASSROOM', 'LABORATORY', 'HALL', 'STUDIO', 'OUTDOOR'))
);

CREATE TABLE membership (
    club_id          VARCHAR2(6),
    student_id       VARCHAR2(6),
    date_registered  DATE DEFAULT SYSDATE NOT NULL,
    membership_status VARCHAR2(10) DEFAULT 'ACTIVE' NOT NULL,
    CONSTRAINT pk_membership PRIMARY KEY (club_id, student_id),
    CONSTRAINT fk_membership_club FOREIGN KEY (club_id)
        REFERENCES club (club_id) ON DELETE CASCADE,
    CONSTRAINT fk_membership_student FOREIGN KEY (student_id)
        REFERENCES student (student_id) ON DELETE CASCADE,
    CONSTRAINT ck_membership_status CHECK
        (membership_status IN ('ACTIVE', 'INACTIVE'))
);

CREATE TABLE club_president (
    club_id          VARCHAR2(6),
    student_id       VARCHAR2(6) NOT NULL,
    appointment_date DATE NOT NULL,
    CONSTRAINT pk_club_president PRIMARY KEY (club_id),
    CONSTRAINT uq_club_president_pair UNIQUE (club_id, student_id),
    CONSTRAINT fk_president_membership FOREIGN KEY (club_id, student_id)
        REFERENCES membership (club_id, student_id)
);

CREATE TABLE event (
    event_id         VARCHAR2(8),
    club_id          VARCHAR2(6) NOT NULL,
    venue_id         VARCHAR2(6) NOT NULL,
    semester_id      VARCHAR2(8) NOT NULL,
    president_student_id VARCHAR2(6) NOT NULL,
    activity_name    VARCHAR2(150) NOT NULL,
    event_date       DATE NOT NULL,
    CONSTRAINT pk_event PRIMARY KEY (event_id),
    CONSTRAINT uq_event_club_pair UNIQUE (event_id, club_id),
    CONSTRAINT fk_event_club FOREIGN KEY (club_id)
        REFERENCES club (club_id),
    CONSTRAINT fk_event_venue FOREIGN KEY (venue_id)
        REFERENCES venue (venue_id),
    CONSTRAINT fk_event_semester FOREIGN KEY (semester_id)
        REFERENCES semester (semester_id),
    CONSTRAINT fk_event_president FOREIGN KEY (club_id, president_student_id)
        REFERENCES club_president (club_id, student_id)
);

CREATE TABLE event_registration (
    event_id         VARCHAR2(8),
    club_id          VARCHAR2(6),
    student_id       VARCHAR2(6),
    registration_date DATE DEFAULT SYSDATE NOT NULL,
    attendance_status VARCHAR2(10) DEFAULT 'REGISTERED' NOT NULL,
    CONSTRAINT pk_event_registration PRIMARY KEY (event_id, student_id),
    CONSTRAINT fk_registration_event FOREIGN KEY (event_id, club_id)
        REFERENCES event (event_id, club_id) ON DELETE CASCADE,
    CONSTRAINT fk_registration_member FOREIGN KEY (club_id, student_id)
        REFERENCES membership (club_id, student_id),
    CONSTRAINT ck_attendance_status CHECK
        (attendance_status IN ('REGISTERED', 'ATTENDED', 'ABSENT'))
);

-- Foreign-key indexes support joins and parent-row integrity checks.
CREATE INDEX ix_student_faculty ON student (faculty_id);
CREATE INDEX ix_club_advisor ON club (advisor_id);
CREATE INDEX ix_venue_pic ON venue (pic_id);
CREATE INDEX ix_membership_student ON membership (student_id);
CREATE INDEX ix_event_club ON event (club_id);
CREATE INDEX ix_event_venue ON event (venue_id);
CREATE INDEX ix_event_semester ON event (semester_id);
CREATE INDEX ix_registration_member ON event_registration (club_id, student_id);

PROMPT === TASK 2.2: POPULATE TABLES WITH MEANINGFUL DATA ===

INSERT ALL
    INTO faculty VALUES ('F001', 'Faculty of Computing and Innovation')
    INTO faculty VALUES ('F002', 'Faculty of Engineering')
    INTO faculty VALUES ('F003', 'Faculty of Business and Accounting')
    INTO faculty VALUES ('F004', 'Faculty of Communication and Creative Design')
    INTO faculty VALUES ('F005', 'Faculty of Education and Social Sciences')
    INTO faculty VALUES ('F006', 'Faculty of Hospitality and Tourism')
    INTO faculty VALUES ('F007', 'Faculty of Medicine')
    INTO faculty VALUES ('F008', 'Faculty of Dentistry')
    INTO faculty VALUES ('F009', 'Faculty of Pharmacy')
    INTO faculty VALUES ('F010', 'Faculty of Law')
SELECT 1 FROM dual;

INSERT ALL
    INTO advisor VALUES ('A001', 'Dr. Aisha Rahman', 'R2.1', '03-6145-1101')
    INTO advisor VALUES ('A002', 'Mr. Daniel Lee', 'R2.2', '03-6145-1102')
    INTO advisor VALUES ('A003', 'Ms. Nur Izzati', 'R3.1', '03-6145-1103')
    INTO advisor VALUES ('A004', 'Dr. Kelvin Wong', 'R3.2', '03-6145-1104')
    INTO advisor VALUES ('A005', 'Ms. Priya Nair', 'R4.1', '03-6145-1105')
    INTO advisor VALUES ('A006', 'Mr. Hafiz Osman', 'R4.2', '03-6145-1106')
    INTO advisor VALUES ('A007', 'Dr. Siti Hamidah', 'R5.1', '03-6145-1107')
    INTO advisor VALUES ('A008', 'Mr. Marcus Tan', 'R5.2', '03-6145-1108')
    INTO advisor VALUES ('A009', 'Ms. Joanne Lim', 'R6.1', '03-6145-1109')
    INTO advisor VALUES ('A010', 'Dr. Farid Iskandar', 'R6.2', '03-6145-1110')
SELECT 1 FROM dual;

INSERT ALL
    INTO venue_pic VALUES ('P001', 'Azlan Musa', '012-700-2001', 'G1.1')
    INTO venue_pic VALUES ('P002', 'Mei Ling', '012-700-2002', 'G1.2')
    INTO venue_pic VALUES ('P003', 'Ravi Kumar', '012-700-2003', 'G1.3')
    INTO venue_pic VALUES ('P004', 'Farah Nadia', '012-700-2004', 'G1.4')
    INTO venue_pic VALUES ('P005', 'Jason Chong', '012-700-2005', 'G1.5')
    INTO venue_pic VALUES ('P006', 'Nadia Salleh', '012-700-2006', 'G1.6')
    INTO venue_pic VALUES ('P007', 'Andrew Goh', '012-700-2007', 'G1.7')
    INTO venue_pic VALUES ('P008', 'Kavitha Maniam', '012-700-2008', 'G1.8')
    INTO venue_pic VALUES ('P009', 'Fikri Halim', '012-700-2009', 'G1.9')
    INTO venue_pic VALUES ('P010', 'Elaine Yap', '012-700-2010', 'G1.10')
SELECT 1 FROM dual;

INSERT ALL
    INTO semester VALUES ('S2026M', 'May-Aug 2026', DATE '2026-05-01', DATE '2026-08-31')
    INTO semester VALUES ('S2026S', 'Sep-Dec 2026', DATE '2026-09-01', DATE '2026-12-31')
    INTO semester VALUES ('S2027J', 'Jan-Apr 2027', DATE '2027-01-01', DATE '2027-04-30')
SELECT 1 FROM dual;

INSERT ALL
    INTO student VALUES ('aa1001', 'Adam Abdullah', '012-810-1001', 'F001', 'Y', 'N')
    INTO student VALUES ('bb1002', 'Brenda Balan', '012-810-1002', 'F003', 'Y', 'Y')
    INTO student VALUES ('cc1003', 'Chong Cai Wen', '012-810-1003', 'F002', 'N', 'N')
    INTO student VALUES ('dd1004', 'Devi Krishnan', '012-810-1004', 'F004', 'Y', 'Y')
    INTO student VALUES ('ee1005', 'Ethan Elias', '012-810-1005', 'F005', 'N', 'N')
    INTO student VALUES ('ff1006', 'Farah Faisal', '012-810-1006', 'F006', 'Y', 'N')
    INTO student VALUES ('gg1007', 'Gan Hui Min', '012-810-1007', 'F007', 'Y', 'Y')
    INTO student VALUES ('hh1008', 'Harith Hakim', '012-810-1008', 'F008', 'N', 'N')
    INTO student VALUES ('ii1009', 'Irene Ismail', '012-810-1009', 'F009', 'Y', 'N')
    INTO student VALUES ('jj1010', 'Jason Jamil', '012-810-1010', 'F010', 'Y', 'Y')
    INTO student VALUES ('kk1011', 'Kavitha Kumar', '012-810-1011', 'F001', 'N', 'N')
    INTO student VALUES ('ll1012', 'Lee Li Ann', '012-810-1012', 'F002', 'Y', 'N')
    INTO student VALUES ('mm1013', 'Muhammad Malik', '012-810-1013', 'F003', 'Y', 'Y')
    INTO student VALUES ('nn1014', 'Nur Nabila', '012-810-1014', 'F004', 'N', 'N')
    INTO student VALUES ('oo1015', 'Ong Ooi Wei', '012-810-1015', 'F005', 'Y', 'N')
    INTO student VALUES ('pp1016', 'Pravin Prakash', '012-810-1016', 'F006', 'Y', 'Y')
    INTO student VALUES ('qq1017', 'Qistina Qamar', '012-810-1017', 'F007', 'N', 'N')
    INTO student VALUES ('rr1018', 'Rachel Raj', '012-810-1018', 'F008', 'Y', 'N')
    INTO student VALUES ('ss1019', 'Syafiq Salleh', '012-810-1019', 'F009', 'Y', 'Y')
    INTO student VALUES ('tt1020', 'Tan Tze Wei', '012-810-1020', 'F010', 'N', 'N')
    INTO student VALUES ('uu1021', 'Umair Usman', '012-810-1021', 'F001', 'Y', 'N')
    INTO student VALUES ('vv1022', 'Vanessa Voon', '012-810-1022', 'F002', 'Y', 'Y')
    INTO student VALUES ('ww1023', 'Wong Wai Kit', '012-810-1023', 'F003', 'N', 'N')
    INTO student VALUES ('xx1024', 'Xavier Xian', '012-810-1024', 'F004', 'Y', 'N')
    INTO student VALUES ('yy1025', 'Yasmin Yusof', '012-810-1025', 'F005', 'Y', 'Y')
    INTO student VALUES ('zz1026', 'Zara Zainal', '012-810-1026', 'F006', 'N', 'N')
    INTO student VALUES ('aa1027', 'Amirul Anwar', '012-810-1027', 'F007', 'Y', 'N')
    INTO student VALUES ('bb1028', 'Bella Bahar', '012-810-1028', 'F008', 'Y', 'Y')
    INTO student VALUES ('cc1029', 'Caleb Chan', '012-810-1029', 'F009', 'N', 'N')
    INTO student VALUES ('dd1030', 'Diyana Daud', '012-810-1030', 'F010', 'Y', 'N')
SELECT 1 FROM dual;

INSERT ALL
    INTO club VALUES ('C001', 'Information Technology Club', 'A001', 'Practical computing, coding and digital literacy activities.')
    INTO club VALUES ('C002', 'Dance Club', 'A002', 'Cultural and contemporary dance development.')
    INTO club VALUES ('C003', 'Music Club', 'A003', 'Instrumental, vocal and live performance activities.')
    INTO club VALUES ('C004', 'Accounting Club', 'A004', 'Professional accounting and financial literacy activities.')
    INTO club VALUES ('C005', 'Robotics Club', 'A001', 'Robotics design, electronics and autonomous systems.')
    INTO club VALUES ('C006', 'Debate Club', 'A002', 'Competitive debate and public speaking.')
    INTO club VALUES ('C007', 'Entrepreneurship Club', 'A003', 'Student enterprise and business innovation.')
    INTO club VALUES ('C008', 'Photography Club', 'A004', 'Photography technique and visual storytelling.')
    INTO club VALUES ('C009', 'Environmental Club', 'A005', 'Sustainability and environmental awareness.')
    INTO club VALUES ('C010', 'Sports Club', 'A006', 'Recreational sport and student wellbeing.')
    INTO club VALUES ('C011', 'Volunteer Club', 'A007', 'Community service and social responsibility.')
    INTO club VALUES ('C012', 'Drama Club', 'A008', 'Theatre production and performance practice.')
    INTO club VALUES ('C013', 'Cybersecurity Club', 'A001', 'Ethical security awareness and defensive computing.')
    INTO club VALUES ('C014', 'Culinary Club', 'A009', 'Food preparation and hospitality activities.')
    INTO club VALUES ('C015', 'Chess Club', 'A010', 'Strategic board-game practice and competition.')
SELECT 1 FROM dual;

INSERT ALL
    INTO venue VALUES ('V001', 'Computer Lab 1', 'LABORATORY', 40, 'P001')
    INTO venue VALUES ('V002', 'Main Auditorium', 'HALL', 500, 'P002')
    INTO venue VALUES ('V003', 'Dance Studio', 'STUDIO', 80, 'P003')
    INTO venue VALUES ('V004', 'Lecture Hall A', 'HALL', 180, 'P004')
    INTO venue VALUES ('V005', 'Engineering Lab', 'LABORATORY', 50, 'P005')
    INTO venue VALUES ('V006', 'Seminar Room 1', 'CLASSROOM', 45, 'P006')
    INTO venue VALUES ('V007', 'Multipurpose Hall', 'HALL', 250, 'P007')
    INTO venue VALUES ('V008', 'Creative Studio', 'STUDIO', 60, 'P008')
    INTO venue VALUES ('V009', 'Campus Field', 'OUTDOOR', 600, 'P009')
    INTO venue VALUES ('V010', 'Training Kitchen', 'LABORATORY', 35, 'P010')
SELECT 1 FROM dual;

INSERT ALL
    INTO membership VALUES ('C001', 'aa1001', DATE '2026-05-03', 'ACTIVE')
    INTO membership VALUES ('C001', 'pp1016', DATE '2026-05-04', 'ACTIVE')
    INTO membership VALUES ('C001', 'qq1017', DATE '2026-05-05', 'ACTIVE')
    INTO membership VALUES ('C001', 'rr1018', DATE '2026-05-06', 'ACTIVE')
    INTO membership VALUES ('C002', 'bb1002', DATE '2026-05-03', 'ACTIVE')
    INTO membership VALUES ('C002', 'ss1019', DATE '2026-05-04', 'ACTIVE')
    INTO membership VALUES ('C002', 'tt1020', DATE '2026-05-05', 'ACTIVE')
    INTO membership VALUES ('C002', 'uu1021', DATE '2026-05-06', 'ACTIVE')
    INTO membership VALUES ('C003', 'cc1003', DATE '2026-05-03', 'ACTIVE')
    INTO membership VALUES ('C003', 'vv1022', DATE '2026-05-04', 'ACTIVE')
    INTO membership VALUES ('C003', 'ww1023', DATE '2026-05-05', 'ACTIVE')
    INTO membership VALUES ('C003', 'xx1024', DATE '2026-05-06', 'ACTIVE')
    INTO membership VALUES ('C004', 'dd1004', DATE '2026-05-03', 'ACTIVE')
    INTO membership VALUES ('C004', 'yy1025', DATE '2026-05-04', 'ACTIVE')
    INTO membership VALUES ('C004', 'zz1026', DATE '2026-05-05', 'ACTIVE')
    INTO membership VALUES ('C004', 'aa1027', DATE '2026-05-06', 'ACTIVE')
    INTO membership VALUES ('C005', 'ee1005', DATE '2026-05-03', 'ACTIVE')
    INTO membership VALUES ('C005', 'bb1028', DATE '2026-05-04', 'ACTIVE')
    INTO membership VALUES ('C005', 'cc1029', DATE '2026-05-05', 'ACTIVE')
    INTO membership VALUES ('C005', 'dd1030', DATE '2026-05-06', 'ACTIVE')
    INTO membership VALUES ('C006', 'ff1006', DATE '2026-05-07', 'ACTIVE')
    INTO membership VALUES ('C006', 'aa1001', DATE '2026-05-08', 'ACTIVE')
    INTO membership VALUES ('C006', 'bb1002', DATE '2026-05-09', 'ACTIVE')
    INTO membership VALUES ('C007', 'gg1007', DATE '2026-05-07', 'ACTIVE')
    INTO membership VALUES ('C007', 'cc1003', DATE '2026-05-08', 'ACTIVE')
    INTO membership VALUES ('C007', 'dd1004', DATE '2026-05-09', 'ACTIVE')
    INTO membership VALUES ('C008', 'hh1008', DATE '2026-05-07', 'ACTIVE')
    INTO membership VALUES ('C008', 'ee1005', DATE '2026-05-08', 'ACTIVE')
    INTO membership VALUES ('C008', 'ff1006', DATE '2026-05-09', 'ACTIVE')
    INTO membership VALUES ('C009', 'ii1009', DATE '2026-05-07', 'ACTIVE')
    INTO membership VALUES ('C009', 'gg1007', DATE '2026-05-08', 'ACTIVE')
    INTO membership VALUES ('C009', 'hh1008', DATE '2026-05-09', 'ACTIVE')
    INTO membership VALUES ('C010', 'jj1010', DATE '2026-05-07', 'ACTIVE')
    INTO membership VALUES ('C010', 'ii1009', DATE '2026-05-08', 'ACTIVE')
    INTO membership VALUES ('C010', 'kk1011', DATE '2026-05-09', 'ACTIVE')
    INTO membership VALUES ('C011', 'kk1011', DATE '2026-05-10', 'ACTIVE')
    INTO membership VALUES ('C011', 'll1012', DATE '2026-05-11', 'ACTIVE')
    INTO membership VALUES ('C011', 'mm1013', DATE '2026-05-12', 'ACTIVE')
    INTO membership VALUES ('C012', 'll1012', DATE '2026-05-10', 'ACTIVE')
    INTO membership VALUES ('C012', 'nn1014', DATE '2026-05-11', 'ACTIVE')
    INTO membership VALUES ('C012', 'oo1015', DATE '2026-05-12', 'ACTIVE')
    INTO membership VALUES ('C013', 'mm1013', DATE '2026-05-10', 'ACTIVE')
    INTO membership VALUES ('C013', 'pp1016', DATE '2026-05-11', 'ACTIVE')
    INTO membership VALUES ('C013', 'qq1017', DATE '2026-05-12', 'ACTIVE')
    INTO membership VALUES ('C014', 'nn1014', DATE '2026-05-10', 'ACTIVE')
    INTO membership VALUES ('C014', 'rr1018', DATE '2026-05-11', 'ACTIVE')
    INTO membership VALUES ('C014', 'ss1019', DATE '2026-05-12', 'ACTIVE')
    INTO membership VALUES ('C015', 'oo1015', DATE '2026-05-10', 'ACTIVE')
    INTO membership VALUES ('C015', 'tt1020', DATE '2026-05-11', 'ACTIVE')
    INTO membership VALUES ('C015', 'uu1021', DATE '2026-05-12', 'ACTIVE')
SELECT 1 FROM dual;

INSERT ALL
    INTO club_president VALUES ('C001', 'aa1001', DATE '2026-05-15')
    INTO club_president VALUES ('C002', 'bb1002', DATE '2026-05-15')
    INTO club_president VALUES ('C003', 'cc1003', DATE '2026-05-15')
    INTO club_president VALUES ('C004', 'dd1004', DATE '2026-05-15')
    INTO club_president VALUES ('C005', 'ee1005', DATE '2026-05-15')
    INTO club_president VALUES ('C006', 'ff1006', DATE '2026-05-16')
    INTO club_president VALUES ('C007', 'gg1007', DATE '2026-05-16')
    INTO club_president VALUES ('C008', 'hh1008', DATE '2026-05-16')
    INTO club_president VALUES ('C009', 'ii1009', DATE '2026-05-16')
    INTO club_president VALUES ('C010', 'jj1010', DATE '2026-05-16')
    INTO club_president VALUES ('C011', 'kk1011', DATE '2026-05-17')
    INTO club_president VALUES ('C012', 'll1012', DATE '2026-05-17')
    INTO club_president VALUES ('C013', 'mm1013', DATE '2026-05-17')
    INTO club_president VALUES ('C014', 'nn1014', DATE '2026-05-17')
    INTO club_president VALUES ('C015', 'oo1015', DATE '2026-05-17')
SELECT 1 FROM dual;

-- Each club has one event in each of the three modelled semesters.
INSERT ALL
    INTO event VALUES ('E001', 'C001', 'V001', 'S2026M', 'aa1001', 'Python Coding Clinic', DATE '2026-06-06')
    INTO event VALUES ('E002', 'C002', 'V003', 'S2026M', 'bb1002', 'Cultural Dance Workshop', DATE '2026-06-07')
    INTO event VALUES ('E003', 'C003', 'V002', 'S2026M', 'cc1003', 'Campus Music Showcase', DATE '2026-06-13')
    INTO event VALUES ('E004', 'C004', 'V004', 'S2026M', 'dd1004', 'Budgeting Challenge', DATE '2026-06-14')
    INTO event VALUES ('E005', 'C005', 'V005', 'S2026M', 'ee1005', 'Line-Following Robot Lab', DATE '2026-06-20')
    INTO event VALUES ('E006', 'C006', 'V006', 'S2026M', 'ff1006', 'Interfaculty Debate', DATE '2026-06-21')
    INTO event VALUES ('E007', 'C007', 'V004', 'S2026M', 'gg1007', 'Student Startup Pitch', DATE '2026-06-27')
    INTO event VALUES ('E008', 'C008', 'V008', 'S2026M', 'hh1008', 'Portrait Photography Lab', DATE '2026-06-28')
    INTO event VALUES ('E009', 'C009', 'V009', 'S2026M', 'ii1009', 'Campus Recycling Drive', DATE '2026-07-04')
    INTO event VALUES ('E010', 'C010', 'V009', 'S2026M', 'jj1010', 'Interclub Sports Day', DATE '2026-07-05')
    INTO event VALUES ('E011', 'C011', 'V007', 'S2026M', 'kk1011', 'Community Care Packing', DATE '2026-07-11')
    INTO event VALUES ('E012', 'C012', 'V002', 'S2026M', 'll1012', 'One-Act Play Festival', DATE '2026-07-12')
    INTO event VALUES ('E013', 'C013', 'V001', 'S2026M', 'mm1013', 'Phishing Defence Workshop', DATE '2026-07-18')
    INTO event VALUES ('E014', 'C014', 'V010', 'S2026M', 'nn1014', 'Malaysian Cuisine Workshop', DATE '2026-07-19')
    INTO event VALUES ('E015', 'C015', 'V006', 'S2026M', 'oo1015', 'Rapid Chess Tournament', DATE '2026-07-25')
    INTO event VALUES ('E016', 'C001', 'V001', 'S2026S', 'aa1001', 'Web Application Hackathon', DATE '2026-09-12')
    INTO event VALUES ('E017', 'C002', 'V003', 'S2026S', 'bb1002', 'Contemporary Dance Clinic', DATE '2026-09-19')
    INTO event VALUES ('E018', 'C003', 'V002', 'S2026S', 'cc1003', 'Acoustic Night', DATE '2026-09-26')
    INTO event VALUES ('E019', 'C004', 'V004', 'S2026S', 'dd1004', 'Tax Literacy Seminar', DATE '2026-10-03')
    INTO event VALUES ('E020', 'C005', 'V005', 'S2026S', 'ee1005', 'Drone Navigation Challenge', DATE '2026-10-10')
    INTO event VALUES ('E021', 'C006', 'V006', 'S2026S', 'ff1006', 'Public Speaking Bootcamp', DATE '2026-10-17')
    INTO event VALUES ('E022', 'C007', 'V004', 'S2026S', 'gg1007', 'Social Enterprise Forum', DATE '2026-10-24')
    INTO event VALUES ('E023', 'C008', 'V008', 'S2026S', 'hh1008', 'Night Photography Walk', DATE '2026-10-31')
    INTO event VALUES ('E024', 'C009', 'V009', 'S2026S', 'ii1009', 'Tree Planting Day', DATE '2026-11-07')
    INTO event VALUES ('E025', 'C010', 'V009', 'S2026S', 'jj1010', 'Wellness Fun Run', DATE '2026-11-14')
    INTO event VALUES ('E026', 'C011', 'V007', 'S2026S', 'kk1011', 'Food Bank Collection', DATE '2026-11-21')
    INTO event VALUES ('E027', 'C012', 'V002', 'S2026S', 'll1012', 'Stagecraft Workshop', DATE '2026-11-28')
    INTO event VALUES ('E028', 'C013', 'V001', 'S2026S', 'mm1013', 'Capture-the-Flag Practice', DATE '2026-12-05')
    INTO event VALUES ('E029', 'C014', 'V010', 'S2026S', 'nn1014', 'Healthy Baking Lab', DATE '2026-12-12')
    INTO event VALUES ('E030', 'C015', 'V006', 'S2026S', 'oo1015', 'Team Chess League', DATE '2026-12-19')
    INTO event VALUES ('E031', 'C001', 'V001', 'S2027J', 'aa1001', 'Database Design Sprint', DATE '2027-01-16')
    INTO event VALUES ('E032', 'C002', 'V003', 'S2027J', 'bb1002', 'Traditional Dance Exchange', DATE '2027-01-23')
    INTO event VALUES ('E033', 'C003', 'V002', 'S2027J', 'cc1003', 'Battle of the Bands', DATE '2027-01-30')
    INTO event VALUES ('E034', 'C004', 'V004', 'S2027J', 'dd1004', 'Investment Case Competition', DATE '2027-02-06')
    INTO event VALUES ('E035', 'C005', 'V005', 'S2027J', 'ee1005', 'Robotics Open Day', DATE '2027-02-13')
    INTO event VALUES ('E036', 'C006', 'V006', 'S2027J', 'ff1006', 'Policy Debate Finals', DATE '2027-02-20')
    INTO event VALUES ('E037', 'C007', 'V004', 'S2027J', 'gg1007', 'Business Model Workshop', DATE '2027-02-27')
    INTO event VALUES ('E038', 'C008', 'V008', 'S2027J', 'hh1008', 'Documentary Photo Exhibition', DATE '2027-03-06')
    INTO event VALUES ('E039', 'C009', 'V009', 'S2027J', 'ii1009', 'Earth Hour Campaign', DATE '2027-03-13')
    INTO event VALUES ('E040', 'C010', 'V009', 'S2027J', 'jj1010', 'Campus Badminton Open', DATE '2027-03-20')
    INTO event VALUES ('E041', 'C011', 'V007', 'S2027J', 'kk1011', 'Volunteer Leadership Forum', DATE '2027-03-27')
    INTO event VALUES ('E042', 'C012', 'V002', 'S2027J', 'll1012', 'Student Theatre Premiere', DATE '2027-04-03')
    INTO event VALUES ('E043', 'C013', 'V001', 'S2027J', 'mm1013', 'Secure Coding Clinic', DATE '2027-04-10')
    INTO event VALUES ('E044', 'C014', 'V010', 'S2027J', 'nn1014', 'Sustainable Cooking Challenge', DATE '2027-04-17')
    INTO event VALUES ('E045', 'C015', 'V006', 'S2027J', 'oo1015', 'Intercollege Chess Cup', DATE '2027-04-24')
SELECT 1 FROM dual;

-- Two valid member registrations for each May-Aug 2026 event.
INSERT ALL
    INTO event_registration VALUES ('E001', 'C001', 'aa1001', DATE '2026-05-20', 'ATTENDED')
    INTO event_registration VALUES ('E001', 'C001', 'pp1016', DATE '2026-05-21', 'ATTENDED')
    INTO event_registration VALUES ('E002', 'C002', 'bb1002', DATE '2026-05-20', 'ATTENDED')
    INTO event_registration VALUES ('E002', 'C002', 'ss1019', DATE '2026-05-21', 'ATTENDED')
    INTO event_registration VALUES ('E003', 'C003', 'cc1003', DATE '2026-05-20', 'ATTENDED')
    INTO event_registration VALUES ('E003', 'C003', 'vv1022', DATE '2026-05-21', 'ATTENDED')
    INTO event_registration VALUES ('E004', 'C004', 'dd1004', DATE '2026-05-20', 'ATTENDED')
    INTO event_registration VALUES ('E004', 'C004', 'yy1025', DATE '2026-05-21', 'ABSENT')
    INTO event_registration VALUES ('E005', 'C005', 'ee1005', DATE '2026-05-20', 'ATTENDED')
    INTO event_registration VALUES ('E005', 'C005', 'bb1028', DATE '2026-05-21', 'ATTENDED')
    INTO event_registration VALUES ('E006', 'C006', 'ff1006', DATE '2026-05-22', 'ATTENDED')
    INTO event_registration VALUES ('E006', 'C006', 'aa1001', DATE '2026-05-23', 'ATTENDED')
    INTO event_registration VALUES ('E007', 'C007', 'gg1007', DATE '2026-05-22', 'ATTENDED')
    INTO event_registration VALUES ('E007', 'C007', 'cc1003', DATE '2026-05-23', 'ATTENDED')
    INTO event_registration VALUES ('E008', 'C008', 'hh1008', DATE '2026-05-22', 'ATTENDED')
    INTO event_registration VALUES ('E008', 'C008', 'ee1005', DATE '2026-05-23', 'ATTENDED')
    INTO event_registration VALUES ('E009', 'C009', 'ii1009', DATE '2026-05-22', 'ATTENDED')
    INTO event_registration VALUES ('E009', 'C009', 'gg1007', DATE '2026-05-23', 'ATTENDED')
    INTO event_registration VALUES ('E010', 'C010', 'jj1010', DATE '2026-05-22', 'ATTENDED')
    INTO event_registration VALUES ('E010', 'C010', 'ii1009', DATE '2026-05-23', 'ATTENDED')
    INTO event_registration VALUES ('E011', 'C011', 'kk1011', DATE '2026-05-24', 'ATTENDED')
    INTO event_registration VALUES ('E011', 'C011', 'll1012', DATE '2026-05-25', 'ATTENDED')
    INTO event_registration VALUES ('E012', 'C012', 'll1012', DATE '2026-05-24', 'ATTENDED')
    INTO event_registration VALUES ('E012', 'C012', 'nn1014', DATE '2026-05-25', 'ATTENDED')
    INTO event_registration VALUES ('E013', 'C013', 'mm1013', DATE '2026-05-24', 'ATTENDED')
    INTO event_registration VALUES ('E013', 'C013', 'pp1016', DATE '2026-05-25', 'ATTENDED')
    INTO event_registration VALUES ('E014', 'C014', 'nn1014', DATE '2026-05-24', 'ATTENDED')
    INTO event_registration VALUES ('E014', 'C014', 'rr1018', DATE '2026-05-25', 'ATTENDED')
    INTO event_registration VALUES ('E015', 'C015', 'oo1015', DATE '2026-05-24', 'REGISTERED')
    INTO event_registration VALUES ('E015', 'C015', 'tt1020', DATE '2026-05-25', 'REGISTERED')
SELECT 1 FROM dual;

COMMIT;

PROMPT === DATABASE VERSION ===
SELECT banner_full FROM v$version WHERE banner_full LIKE 'Oracle%Database%';

PROMPT === TABLE ROW COUNTS ===
COLUMN table_name FORMAT A24
COLUMN row_count FORMAT 9999
SELECT 'FACULTY' table_name, COUNT(*) row_count FROM faculty UNION ALL
SELECT 'ADVISOR', COUNT(*) FROM advisor UNION ALL
SELECT 'VENUE_PIC', COUNT(*) FROM venue_pic UNION ALL
SELECT 'SEMESTER', COUNT(*) FROM semester UNION ALL
SELECT 'STUDENT', COUNT(*) FROM student UNION ALL
SELECT 'CLUB', COUNT(*) FROM club UNION ALL
SELECT 'VENUE', COUNT(*) FROM venue UNION ALL
SELECT 'MEMBERSHIP', COUNT(*) FROM membership UNION ALL
SELECT 'CLUB_PRESIDENT', COUNT(*) FROM club_president UNION ALL
SELECT 'EVENT', COUNT(*) FROM event UNION ALL
SELECT 'EVENT_REGISTRATION', COUNT(*) FROM event_registration;

PROMPT === INTEGRITY AUDIT: EXPECT ZERO INVALID EVENT REGISTRATIONS ===
SELECT COUNT(*) AS invalid_event_registrations
FROM event_registration er
LEFT JOIN membership m
  ON m.club_id = er.club_id AND m.student_id = er.student_id
WHERE m.student_id IS NULL;

PROMPT === DATE AUDIT: EXPECT ZERO EVENTS OUTSIDE THEIR SEMESTER ===
SELECT COUNT(*) AS events_outside_semester
FROM event e
JOIN semester s ON s.semester_id = e.semester_id
WHERE e.event_date < s.start_date OR e.event_date > s.end_date;

PROMPT === COVERAGE AUDIT: EXPECT THREE EVENTS PER CLUB ===
SELECT c.club_id, c.club_name, COUNT(e.event_id) AS event_count
FROM club c
LEFT JOIN event e ON e.club_id = c.club_id
GROUP BY c.club_id, c.club_name
ORDER BY c.club_id;

PROMPT === CONSTRAINT REJECTION TESTS: EACH LINE SHOULD REPORT PASS ===
DECLARE
    PROCEDURE expect_rejection(p_test_name VARCHAR2, p_sql VARCHAR2) IS
    BEGIN
        SAVEPOINT before_rejection_test;
        EXECUTE IMMEDIATE p_sql;
        DBMS_OUTPUT.PUT_LINE('FAIL - ' || p_test_name || ' was accepted');
        ROLLBACK TO before_rejection_test;
    EXCEPTION
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('PASS - ' || p_test_name || ' rejected (' || SQLCODE || ')');
            ROLLBACK TO before_rejection_test;
    END;
BEGIN
    expect_rejection(
        'malformed student ID',
        q'[INSERT INTO student VALUES ('BAD123', 'Invalid ID', '012-999-0001', 'F001', 'Y', 'N')]'
    );
    expect_rejection(
        'invalid approval status',
        q'[INSERT INTO student VALUES ('ab9998', 'Invalid Status', '012-999-0002', 'F001', 'X', 'N')]'
    );
    expect_rejection(
        'duplicate club membership',
        q'[INSERT INTO membership VALUES ('C001', 'aa1001', DATE '2026-06-01', 'ACTIVE')]'
    );
    expect_rejection(
        'club with missing advisor',
        q'[INSERT INTO club VALUES ('C999', 'Invalid Club', 'A999', 'Must fail')]'
    );
    expect_rejection(
        'president who is not a member of the club',
        q'[UPDATE club_president SET student_id = 'bb1002' WHERE club_id = 'C001']'
    );
    expect_rejection(
        'event registration by a non-member',
        q'[INSERT INTO event_registration VALUES ('E001', 'C001', 'bb1002', DATE '2026-05-28', 'REGISTERED')]'
    );
END;
/

PROMPT ================================================================
PROMPT TASK 3.1 - STUDENT PHONE LIST, ORDERED BY NAME
PROMPT ================================================================
COLUMN student_id FORMAT A10
COLUMN student_name FORMAT A24
COLUMN phone_number FORMAT A16
SELECT DISTINCT s.student_id, s.student_name, s.phone_number
FROM student s
JOIN membership m ON m.student_id = s.student_id
ORDER BY s.student_name;

PROMPT ================================================================
PROMPT TASK 3.2 - ADVISORS RESPONSIBLE FOR MORE THAN ONE CLUB
PROMPT ================================================================
COLUMN advisor_name FORMAT A24
COLUMN assigned_clubs FORMAT A100
SELECT a.advisor_id,
       a.advisor_name,
       COUNT(c.club_id) AS number_of_clubs,
       LISTAGG(c.club_name, '; ') WITHIN GROUP (ORDER BY c.club_name) AS assigned_clubs
FROM advisor a
JOIN club c ON c.advisor_id = a.advisor_id
GROUP BY a.advisor_id, a.advisor_name
HAVING COUNT(c.club_id) > 1
ORDER BY a.advisor_name;

PROMPT ================================================================
PROMPT TASK 3.3 - STUDENTS MISSING THE FACULTY APPROVAL FORM
PROMPT ================================================================
COLUMN missing_form FORMAT A28
SELECT s.student_id,
       s.student_name,
       s.phone_number,
       'Faculty Approval Form' AS missing_form
FROM student s
WHERE s.approval_form = 'N'
  AND EXISTS (SELECT 1 FROM membership m WHERE m.student_id = s.student_id)
ORDER BY s.student_name;

PROMPT ================================================================
PROMPT TASK 3.4 - ADVISORS, CLUBS, EVENTS AND EVENT DATES
PROMPT ================================================================
COLUMN club_name FORMAT A30
COLUMN activity_name FORMAT A34
COLUMN semester_name FORMAT A16
SELECT a.advisor_name,
       c.club_name,
       e.activity_name,
       s.semester_name,
       TO_CHAR(e.event_date, 'DD-MON-YYYY') AS event_date
FROM advisor a
JOIN club c ON c.advisor_id = a.advisor_id
JOIN event e ON e.club_id = c.club_id
JOIN semester s ON s.semester_id = e.semester_id
ORDER BY a.advisor_name, e.event_date, c.club_name;

PROMPT ================================================================
PROMPT TASK 3.5 - NUMBER OF EVENTS PER ADVISOR AND SEMESTER (PIVOT)
PROMPT ================================================================
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

PROMPT ================================================================
PROMPT TASK 3.6 - CLUBS AND STUDENTS ASSIGNED TO THEM
PROMPT ================================================================
SELECT c.club_name,
       s.student_id,
       s.student_name,
       TO_CHAR(m.date_registered, 'DD-MON-YYYY') AS date_registered
FROM club c
JOIN membership m ON m.club_id = c.club_id
JOIN student s ON s.student_id = m.student_id
WHERE m.membership_status = 'ACTIVE'
ORDER BY c.club_name, s.student_name;

PROMPT === END OF VERIFIED ASSIGNMENT SCRIPT ===
SPOOL OFF
