-- BCL1223 Database Fundamentals - Setup Script
-- Run via: sqlplus system/OraclePass123@//localhost:1521/XEPDB1 @init.sql

WHENEVER SQLERROR EXIT SQL.SQLCODE

-- Create user/schema
DECLARE
    user_exists NUMBER;
BEGIN
    SELECT COUNT(*) INTO user_exists FROM dba_users WHERE username = 'BCL1223';
    IF user_exists = 1 THEN
        EXECUTE IMMEDIATE 'DROP USER bcl1223 CASCADE';
    END IF;
END;
/

CREATE USER bcl1223 IDENTIFIED BY bcl1223
DEFAULT TABLESPACE USERS
TEMPORARY TABLESPACE TEMP
QUOTA UNLIMITED ON USERS;

GRANT CONNECT, RESOURCE TO bcl1223;
GRANT CREATE VIEW TO bcl1223;
GRANT UNLIMITED TABLESPACE TO bcl1223;

-- Create tables
CREATE TABLE bcl1223.faculty (
    faculty_id       VARCHAR2(6),
    faculty_name     VARCHAR2(100) NOT NULL,
    CONSTRAINT pk_faculty PRIMARY KEY (faculty_id),
    CONSTRAINT uq_faculty_name UNIQUE (faculty_name)
);

CREATE TABLE bcl1223.advisor (
    advisor_id       VARCHAR2(6),
    advisor_name     VARCHAR2(100) NOT NULL,
    office_room      VARCHAR2(10) NOT NULL,
    office_phone     VARCHAR2(20) NOT NULL,
    CONSTRAINT pk_advisor PRIMARY KEY (advisor_id),
    CONSTRAINT uq_advisor_phone UNIQUE (office_phone)
);

CREATE TABLE bcl1223.venue_pic (
    pic_id           VARCHAR2(6),
    pic_name         VARCHAR2(100) NOT NULL,
    phone_number     VARCHAR2(20) NOT NULL,
    office_room      VARCHAR2(10) NOT NULL,
    CONSTRAINT pk_venue_pic PRIMARY KEY (pic_id),
    CONSTRAINT uq_venue_pic_phone UNIQUE (phone_number)
);

CREATE TABLE bcl1223.semester (
    semester_id      VARCHAR2(8),
    semester_name    VARCHAR2(30) NOT NULL,
    start_date       DATE NOT NULL,
    end_date         DATE NOT NULL,
    CONSTRAINT pk_semester PRIMARY KEY (semester_id),
    CONSTRAINT uq_semester_name UNIQUE (semester_name),
    CONSTRAINT ck_semester_dates CHECK (end_date > start_date)
);

CREATE TABLE bcl1223.student (
    student_id       VARCHAR2(6),
    student_name     VARCHAR2(100) NOT NULL,
    phone_number     VARCHAR2(20) NOT NULL,
    faculty_id       VARCHAR2(6) NOT NULL,
    approval_form    CHAR(1) DEFAULT 'N' NOT NULL,
    scholarship      CHAR(1) DEFAULT 'N' NOT NULL,
    CONSTRAINT pk_student PRIMARY KEY (student_id),
    CONSTRAINT uq_student_phone UNIQUE (phone_number),
    CONSTRAINT fk_student_faculty FOREIGN KEY (faculty_id)
        REFERENCES bcl1223.faculty (faculty_id),
    CONSTRAINT ck_student_id_format CHECK
        (REGEXP_LIKE(student_id, '^[[:alpha:]]{2}[[:digit:]]{4}$', 'c')),
    CONSTRAINT ck_student_approval CHECK (approval_form IN ('Y', 'N')),
    CONSTRAINT ck_student_scholarship CHECK (scholarship IN ('Y', 'N'))
);

CREATE TABLE bcl1223.club (
    club_id          VARCHAR2(6),
    club_name        VARCHAR2(100) NOT NULL,
    advisor_id       VARCHAR2(6) NOT NULL,
    club_notes       VARCHAR2(500),
    CONSTRAINT pk_club PRIMARY KEY (club_id),
    CONSTRAINT uq_club_name UNIQUE (club_name),
    CONSTRAINT fk_club_advisor FOREIGN KEY (advisor_id)
        REFERENCES bcl1223.advisor (advisor_id)
);

CREATE TABLE bcl1223.venue (
    venue_id         VARCHAR2(6),
    venue_name       VARCHAR2(100) NOT NULL,
    venue_type       VARCHAR2(30) NOT NULL,
    capacity         NUMBER(4) NOT NULL,
    pic_id           VARCHAR2(6) NOT NULL,
    CONSTRAINT pk_venue PRIMARY KEY (venue_id),
    CONSTRAINT uq_venue_name UNIQUE (venue_name),
    CONSTRAINT fk_venue_pic FOREIGN KEY (pic_id)
        REFERENCES bcl1223.venue_pic (pic_id),
    CONSTRAINT ck_venue_capacity CHECK (capacity > 0),
    CONSTRAINT ck_venue_type CHECK
        (venue_type IN ('CLASSROOM', 'LABORATORY', 'HALL', 'STUDIO', 'OUTDOOR'))
);

CREATE TABLE bcl1223.membership (
    club_id          VARCHAR2(6),
    student_id       VARCHAR2(6),
    date_registered  DATE DEFAULT SYSDATE NOT NULL,
    membership_status VARCHAR2(10) DEFAULT 'ACTIVE' NOT NULL,
    CONSTRAINT pk_membership PRIMARY KEY (club_id, student_id),
    CONSTRAINT fk_membership_club FOREIGN KEY (club_id)
        REFERENCES bcl1223.club (club_id) ON DELETE CASCADE,
    CONSTRAINT fk_membership_student FOREIGN KEY (student_id)
        REFERENCES bcl1223.student (student_id) ON DELETE CASCADE,
    CONSTRAINT ck_membership_status CHECK
        (membership_status IN ('ACTIVE', 'INACTIVE'))
);

CREATE TABLE bcl1223.club_president (
    club_id          VARCHAR2(6),
    student_id       VARCHAR2(6) NOT NULL,
    appointment_date DATE NOT NULL,
    CONSTRAINT pk_club_president PRIMARY KEY (club_id),
    CONSTRAINT uq_club_president_pair UNIQUE (club_id, student_id),
    CONSTRAINT fk_president_membership FOREIGN KEY (club_id, student_id)
        REFERENCES bcl1223.membership (club_id, student_id)
);

CREATE TABLE bcl1223.event (
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
        REFERENCES bcl1223.club (club_id),
    CONSTRAINT fk_event_venue FOREIGN KEY (venue_id)
        REFERENCES bcl1223.venue (venue_id),
    CONSTRAINT fk_event_semester FOREIGN KEY (semester_id)
        REFERENCES bcl1223.semester (semester_id),
    CONSTRAINT fk_event_president FOREIGN KEY (club_id, president_student_id)
        REFERENCES bcl1223.club_president (club_id, student_id)
);

CREATE TABLE bcl1223.event_registration (
    event_id         VARCHAR2(8),
    club_id          VARCHAR2(6),
    student_id       VARCHAR2(6),
    registration_date DATE DEFAULT SYSDATE NOT NULL,
    attendance_status VARCHAR2(10) DEFAULT 'REGISTERED' NOT NULL,
    CONSTRAINT pk_event_registration PRIMARY KEY (event_id, student_id),
    CONSTRAINT fk_registration_event FOREIGN KEY (event_id, club_id)
        REFERENCES bcl1223.event (event_id, club_id) ON DELETE CASCADE,
    CONSTRAINT fk_registration_member FOREIGN KEY (club_id, student_id)
        REFERENCES bcl1223.membership (club_id, student_id),
    CONSTRAINT ck_attendance_status CHECK
        (attendance_status IN ('REGISTERED', 'ATTENDED', 'ABSENT'))
);

CREATE INDEX bcl1223.ix_student_faculty ON bcl1223.student (faculty_id);
CREATE INDEX bcl1223.ix_club_advisor ON bcl1223.club (advisor_id);
CREATE INDEX bcl1223.ix_venue_pic ON bcl1223.venue (pic_id);
CREATE INDEX bcl1223.ix_membership_student ON bcl1223.membership (student_id);
CREATE INDEX bcl1223.ix_event_club ON bcl1223.event (club_id);
CREATE INDEX bcl1223.ix_event_venue ON bcl1223.event (venue_id);
CREATE INDEX bcl1223.ix_event_semester ON bcl1223.event (semester_id);
CREATE INDEX bcl1223.ix_registration_member ON bcl1223.event_registration (club_id, student_id);

-- Populate data
INSERT ALL
    INTO bcl1223.faculty VALUES ('F001', 'Faculty of Computing and Innovation')
    INTO bcl1223.faculty VALUES ('F002', 'Faculty of Engineering')
    INTO bcl1223.faculty VALUES ('F003', 'Faculty of Business and Accounting')
    INTO bcl1223.faculty VALUES ('F004', 'Faculty of Communication and Creative Design')
    INTO bcl1223.faculty VALUES ('F005', 'Faculty of Education and Social Sciences')
    INTO bcl1223.faculty VALUES ('F006', 'Faculty of Hospitality and Tourism')
    INTO bcl1223.faculty VALUES ('F007', 'Faculty of Medicine')
    INTO bcl1223.faculty VALUES ('F008', 'Faculty of Dentistry')
    INTO bcl1223.faculty VALUES ('F009', 'Faculty of Pharmacy')
    INTO bcl1223.faculty VALUES ('F010', 'Faculty of Law')
SELECT 1 FROM dual;

INSERT ALL
    INTO bcl1223.advisor VALUES ('A001', 'Dr. Aisha Rahman', 'R2.1', '03-6145-1101')
    INTO bcl1223.advisor VALUES ('A002', 'Mr. Daniel Lee', 'R2.2', '03-6145-1102')
    INTO bcl1223.advisor VALUES ('A003', 'Ms. Nur Izzati', 'R3.1', '03-6145-1103')
    INTO bcl1223.advisor VALUES ('A004', 'Dr. Kelvin Wong', 'R3.2', '03-6145-1104')
    INTO bcl1223.advisor VALUES ('A005', 'Ms. Priya Nair', 'R4.1', '03-6145-1105')
    INTO bcl1223.advisor VALUES ('A006', 'Mr. Hafiz Osman', 'R4.2', '03-6145-1106')
    INTO bcl1223.advisor VALUES ('A007', 'Dr. Siti Hamidah', 'R5.1', '03-6145-1107')
    INTO bcl1223.advisor VALUES ('A008', 'Mr. Marcus Tan', 'R5.2', '03-6145-1108')
    INTO bcl1223.advisor VALUES ('A009', 'Ms. Joanne Lim', 'R6.1', '03-6145-1109')
    INTO bcl1223.advisor VALUES ('A010', 'Dr. Farid Iskandar', 'R6.2', '03-6145-1110')
SELECT 1 FROM dual;

INSERT ALL
    INTO bcl1223.venue_pic VALUES ('P001', 'Azlan Musa', '012-700-2001', 'G1.1')
    INTO bcl1223.venue_pic VALUES ('P002', 'Mei Ling', '012-700-2002', 'G1.2')
    INTO bcl1223.venue_pic VALUES ('P003', 'Ravi Kumar', '012-700-2003', 'G1.3')
    INTO bcl1223.venue_pic VALUES ('P004', 'Farah Nadia', '012-700-2004', 'G1.4')
    INTO bcl1223.venue_pic VALUES ('P005', 'Jason Chong', '012-700-2005', 'G1.5')
    INTO bcl1223.venue_pic VALUES ('P006', 'Nadia Salleh', '012-700-2006', 'G1.6')
    INTO bcl1223.venue_pic VALUES ('P007', 'Andrew Goh', '012-700-2007', 'G1.7')
    INTO bcl1223.venue_pic VALUES ('P008', 'Kavitha Maniam', '012-700-2008', 'G1.8')
    INTO bcl1223.venue_pic VALUES ('P009', 'Fikri Halim', '012-700-2009', 'G1.9')
    INTO bcl1223.venue_pic VALUES ('P010', 'Elaine Yap', '012-700-2010', 'G1.10')
SELECT 1 FROM dual;

INSERT ALL
    INTO bcl1223.semester VALUES ('S2026M', 'May-Aug 2026', DATE '2026-05-01', DATE '2026-08-31')
    INTO bcl1223.semester VALUES ('S2026S', 'Sep-Dec 2026', DATE '2026-09-01', DATE '2026-12-31')
    INTO bcl1223.semester VALUES ('S2027J', 'Jan-Apr 2027', DATE '2027-01-01', DATE '2027-04-30')
SELECT 1 FROM dual;

INSERT ALL
    INTO bcl1223.student VALUES ('aa1001', 'Adam Abdullah', '012-810-1001', 'F001', 'Y', 'N')
    INTO bcl1223.student VALUES ('bb1002', 'Brenda Balan', '012-810-1002', 'F003', 'Y', 'Y')
    INTO bcl1223.student VALUES ('cc1003', 'Chong Cai Wen', '012-810-1003', 'F002', 'N', 'N')
    INTO bcl1223.student VALUES ('dd1004', 'Devi Krishnan', '012-810-1004', 'F004', 'Y', 'Y')
    INTO bcl1223.student VALUES ('ee1005', 'Ethan Elias', '012-810-1005', 'F005', 'N', 'N')
    INTO bcl1223.student VALUES ('ff1006', 'Farah Faisal', '012-810-1006', 'F006', 'Y', 'N')
    INTO bcl1223.student VALUES ('gg1007', 'Gan Hui Min', '012-810-1007', 'F007', 'Y', 'Y')
    INTO bcl1223.student VALUES ('hh1008', 'Harith Hakim', '012-810-1008', 'F008', 'N', 'N')
    INTO bcl1223.student VALUES ('ii1009', 'Irene Ismail', '012-810-1009', 'F009', 'Y', 'N')
    INTO bcl1223.student VALUES ('jj1010', 'Jason Jamil', '012-810-1010', 'F010', 'Y', 'Y')
    INTO bcl1223.student VALUES ('kk1011', 'Kavitha Kumar', '012-810-1011', 'F001', 'N', 'N')
    INTO bcl1223.student VALUES ('ll1012', 'Lee Li Ann', '012-810-1012', 'F002', 'Y', 'N')
    INTO bcl1223.student VALUES ('mm1013', 'Muhammad Malik', '012-810-1013', 'F003', 'Y', 'Y')
    INTO bcl1223.student VALUES ('nn1014', 'Nur Nabila', '012-810-1014', 'F004', 'N', 'N')
    INTO bcl1223.student VALUES ('oo1015', 'Ong Ooi Wei', '012-810-1015', 'F005', 'Y', 'N')
    INTO bcl1223.student VALUES ('pp1016', 'Pravin Prakash', '012-810-1016', 'F006', 'Y', 'Y')
    INTO bcl1223.student VALUES ('qq1017', 'Qistina Qamar', '012-810-1017', 'F007', 'N', 'N')
    INTO bcl1223.student VALUES ('rr1018', 'Rachel Raj', '012-810-1018', 'F008', 'Y', 'N')
    INTO bcl1223.student VALUES ('ss1019', 'Syafiq Salleh', '012-810-1019', 'F009', 'Y', 'Y')
    INTO bcl1223.student VALUES ('tt1020', 'Tan Tze Wei', '012-810-1020', 'F010', 'N', 'N')
    INTO bcl1223.student VALUES ('uu1021', 'Umair Usman', '012-810-1021', 'F001', 'Y', 'N')
    INTO bcl1223.student VALUES ('vv1022', 'Vanessa Voon', '012-810-1022', 'F002', 'Y', 'Y')
    INTO bcl1223.student VALUES ('ww1023', 'Wong Wai Kit', '012-810-1023', 'F003', 'N', 'N')
    INTO bcl1223.student VALUES ('xx1024', 'Xavier Xian', '012-810-1024', 'F004', 'Y', 'N')
    INTO bcl1223.student VALUES ('yy1025', 'Yasmin Yusof', '012-810-1025', 'F005', 'Y', 'Y')
    INTO bcl1223.student VALUES ('zz1026', 'Zara Zainal', '012-810-1026', 'F006', 'N', 'N')
    INTO bcl1223.student VALUES ('aa1027', 'Amirul Anwar', '012-810-1027', 'F007', 'Y', 'N')
    INTO bcl1223.student VALUES ('bb1028', 'Bella Bahar', '012-810-1028', 'F008', 'Y', 'Y')
    INTO bcl1223.student VALUES ('cc1029', 'Caleb Chan', '012-810-1029', 'F009', 'N', 'N')
    INTO bcl1223.student VALUES ('dd1030', 'Diyana Daud', '012-810-1030', 'F010', 'Y', 'N')
SELECT 1 FROM dual;

INSERT ALL
    INTO bcl1223.club VALUES ('C001', 'Information Technology Club', 'A001', 'Practical computing, coding and digital literacy activities.')
    INTO bcl1223.club VALUES ('C002', 'Dance Club', 'A002', 'Cultural and contemporary dance development.')
    INTO bcl1223.club VALUES ('C003', 'Music Club', 'A003', 'Instrumental, vocal and live performance activities.')
    INTO bcl1223.club VALUES ('C004', 'Accounting Club', 'A004', 'Professional accounting and financial literacy activities.')
    INTO bcl1223.club VALUES ('C005', 'Robotics Club', 'A001', 'Robotics design, electronics and autonomous systems.')
    INTO bcl1223.club VALUES ('C006', 'Debate Club', 'A002', 'Competitive debate and public speaking.')
    INTO bcl1223.club VALUES ('C007', 'Entrepreneurship Club', 'A003', 'Student enterprise and business innovation.')
    INTO bcl1223.club VALUES ('C008', 'Photography Club', 'A004', 'Photography technique and visual storytelling.')
    INTO bcl1223.club VALUES ('C009', 'Environmental Club', 'A005', 'Sustainability and environmental awareness.')
    INTO bcl1223.club VALUES ('C010', 'Sports Club', 'A006', 'Recreational sport and student wellbeing.')
    INTO bcl1223.club VALUES ('C011', 'Volunteer Club', 'A007', 'Community service and social responsibility.')
    INTO bcl1223.club VALUES ('C012', 'Drama Club', 'A008', 'Theatre production and performance practice.')
    INTO bcl1223.club VALUES ('C013', 'Cybersecurity Club', 'A001', 'Ethical security awareness and defensive computing.')
    INTO bcl1223.club VALUES ('C014', 'Culinary Club', 'A009', 'Food preparation and hospitality activities.')
    INTO bcl1223.club VALUES ('C015', 'Chess Club', 'A010', 'Strategic board-game practice and competition.')
SELECT 1 FROM dual;

INSERT ALL
    INTO bcl1223.venue VALUES ('V001', 'Computer Lab 1', 'LABORATORY', 40, 'P001')
    INTO bcl1223.venue VALUES ('V002', 'Main Auditorium', 'HALL', 500, 'P002')
    INTO bcl1223.venue VALUES ('V003', 'Dance Studio', 'STUDIO', 80, 'P003')
    INTO bcl1223.venue VALUES ('V004', 'Lecture Hall A', 'HALL', 180, 'P004')
    INTO bcl1223.venue VALUES ('V005', 'Engineering Lab', 'LABORATORY', 50, 'P005')
    INTO bcl1223.venue VALUES ('V006', 'Seminar Room 1', 'CLASSROOM', 45, 'P006')
    INTO bcl1223.venue VALUES ('V007', 'Multipurpose Hall', 'HALL', 250, 'P007')
    INTO bcl1223.venue VALUES ('V008', 'Creative Studio', 'STUDIO', 60, 'P008')
    INTO bcl1223.venue VALUES ('V009', 'Campus Field', 'OUTDOOR', 600, 'P009')
    INTO bcl1223.venue VALUES ('V010', 'Training Kitchen', 'LABORATORY', 35, 'P010')
SELECT 1 FROM dual;

INSERT ALL
    INTO bcl1223.membership VALUES ('C001', 'aa1001', DATE '2026-05-03', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C001', 'pp1016', DATE '2026-05-04', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C001', 'qq1017', DATE '2026-05-05', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C001', 'rr1018', DATE '2026-05-06', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C002', 'bb1002', DATE '2026-05-03', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C002', 'ss1019', DATE '2026-05-04', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C002', 'tt1020', DATE '2026-05-05', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C002', 'uu1021', DATE '2026-05-06', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C003', 'cc1003', DATE '2026-05-03', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C003', 'vv1022', DATE '2026-05-04', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C003', 'ww1023', DATE '2026-05-05', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C003', 'xx1024', DATE '2026-05-06', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C004', 'dd1004', DATE '2026-05-03', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C004', 'yy1025', DATE '2026-05-04', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C004', 'zz1026', DATE '2026-05-05', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C004', 'aa1027', DATE '2026-05-06', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C005', 'ee1005', DATE '2026-05-03', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C005', 'bb1028', DATE '2026-05-04', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C005', 'cc1029', DATE '2026-05-05', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C005', 'dd1030', DATE '2026-05-06', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C006', 'ff1006', DATE '2026-05-07', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C006', 'aa1001', DATE '2026-05-08', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C006', 'bb1002', DATE '2026-05-09', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C007', 'gg1007', DATE '2026-05-07', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C007', 'cc1003', DATE '2026-05-08', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C007', 'dd1004', DATE '2026-05-09', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C008', 'hh1008', DATE '2026-05-07', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C008', 'ee1005', DATE '2026-05-08', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C008', 'ff1006', DATE '2026-05-09', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C009', 'ii1009', DATE '2026-05-07', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C009', 'gg1007', DATE '2026-05-08', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C009', 'hh1008', DATE '2026-05-09', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C010', 'jj1010', DATE '2026-05-07', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C010', 'ii1009', DATE '2026-05-08', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C010', 'kk1011', DATE '2026-05-09', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C011', 'kk1011', DATE '2026-05-10', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C011', 'll1012', DATE '2026-05-11', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C011', 'mm1013', DATE '2026-05-12', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C012', 'll1012', DATE '2026-05-10', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C012', 'nn1014', DATE '2026-05-11', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C012', 'oo1015', DATE '2026-05-12', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C013', 'mm1013', DATE '2026-05-10', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C013', 'pp1016', DATE '2026-05-11', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C013', 'qq1017', DATE '2026-05-12', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C014', 'nn1014', DATE '2026-05-10', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C014', 'rr1018', DATE '2026-05-11', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C014', 'ss1019', DATE '2026-05-12', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C015', 'oo1015', DATE '2026-05-10', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C015', 'tt1020', DATE '2026-05-11', 'ACTIVE')
    INTO bcl1223.membership VALUES ('C015', 'uu1021', DATE '2026-05-12', 'ACTIVE')
SELECT 1 FROM dual;

INSERT ALL
    INTO bcl1223.club_president VALUES ('C001', 'aa1001', DATE '2026-05-15')
    INTO bcl1223.club_president VALUES ('C002', 'bb1002', DATE '2026-05-15')
    INTO bcl1223.club_president VALUES ('C003', 'cc1003', DATE '2026-05-15')
    INTO bcl1223.club_president VALUES ('C004', 'dd1004', DATE '2026-05-15')
    INTO bcl1223.club_president VALUES ('C005', 'ee1005', DATE '2026-05-15')
    INTO bcl1223.club_president VALUES ('C006', 'ff1006', DATE '2026-05-16')
    INTO bcl1223.club_president VALUES ('C007', 'gg1007', DATE '2026-05-16')
    INTO bcl1223.club_president VALUES ('C008', 'hh1008', DATE '2026-05-16')
    INTO bcl1223.club_president VALUES ('C009', 'ii1009', DATE '2026-05-16')
    INTO bcl1223.club_president VALUES ('C010', 'jj1010', DATE '2026-05-16')
    INTO bcl1223.club_president VALUES ('C011', 'kk1011', DATE '2026-05-17')
    INTO bcl1223.club_president VALUES ('C012', 'll1012', DATE '2026-05-17')
    INTO bcl1223.club_president VALUES ('C013', 'mm1013', DATE '2026-05-17')
    INTO bcl1223.club_president VALUES ('C014', 'nn1014', DATE '2026-05-17')
    INTO bcl1223.club_president VALUES ('C015', 'oo1015', DATE '2026-05-17')
SELECT 1 FROM dual;

INSERT ALL
    INTO bcl1223.event VALUES ('E001', 'C001', 'V001', 'S2026M', 'aa1001', 'Python Coding Clinic', DATE '2026-06-06')
    INTO bcl1223.event VALUES ('E002', 'C002', 'V003', 'S2026M', 'bb1002', 'Cultural Dance Workshop', DATE '2026-06-07')
    INTO bcl1223.event VALUES ('E003', 'C003', 'V002', 'S2026M', 'cc1003', 'Campus Music Showcase', DATE '2026-06-13')
    INTO bcl1223.event VALUES ('E004', 'C004', 'V004', 'S2026M', 'dd1004', 'Budgeting Challenge', DATE '2026-06-14')
    INTO bcl1223.event VALUES ('E005', 'C005', 'V005', 'S2026M', 'ee1005', 'Line-Following Robot Lab', DATE '2026-06-20')
    INTO bcl1223.event VALUES ('E006', 'C006', 'V006', 'S2026M', 'ff1006', 'Interfaculty Debate', DATE '2026-06-21')
    INTO bcl1223.event VALUES ('E007', 'C007', 'V004', 'S2026M', 'gg1007', 'Student Startup Pitch', DATE '2026-06-27')
    INTO bcl1223.event VALUES ('E008', 'C008', 'V008', 'S2026M', 'hh1008', 'Portrait Photography Lab', DATE '2026-06-28')
    INTO bcl1223.event VALUES ('E009', 'C009', 'V009', 'S2026M', 'ii1009', 'Campus Recycling Drive', DATE '2026-07-04')
    INTO bcl1223.event VALUES ('E010', 'C010', 'V009', 'S2026M', 'jj1010', 'Interclub Sports Day', DATE '2026-07-05')
    INTO bcl1223.event VALUES ('E011', 'C011', 'V007', 'S2026M', 'kk1011', 'Community Care Packing', DATE '2026-07-11')
    INTO bcl1223.event VALUES ('E012', 'C012', 'V002', 'S2026M', 'll1012', 'One-Act Play Festival', DATE '2026-07-12')
    INTO bcl1223.event VALUES ('E013', 'C013', 'V001', 'S2026M', 'mm1013', 'Phishing Defence Workshop', DATE '2026-07-18')
    INTO bcl1223.event VALUES ('E014', 'C014', 'V010', 'S2026M', 'nn1014', 'Malaysian Cuisine Workshop', DATE '2026-07-19')
    INTO bcl1223.event VALUES ('E015', 'C015', 'V006', 'S2026M', 'oo1015', 'Rapid Chess Tournament', DATE '2026-07-25')
    INTO bcl1223.event VALUES ('E016', 'C001', 'V001', 'S2026S', 'aa1001', 'Web Application Hackathon', DATE '2026-09-12')
    INTO bcl1223.event VALUES ('E017', 'C002', 'V003', 'S2026S', 'bb1002', 'Contemporary Dance Clinic', DATE '2026-09-19')
    INTO bcl1223.event VALUES ('E018', 'C003', 'V002', 'S2026S', 'cc1003', 'Acoustic Night', DATE '2026-09-26')
    INTO bcl1223.event VALUES ('E019', 'C004', 'V004', 'S2026S', 'dd1004', 'Tax Literacy Seminar', DATE '2026-10-03')
    INTO bcl1223.event VALUES ('E020', 'C005', 'V005', 'S2026S', 'ee1005', 'Drone Navigation Challenge', DATE '2026-10-10')
    INTO bcl1223.event VALUES ('E021', 'C006', 'V006', 'S2026S', 'ff1006', 'Public Speaking Bootcamp', DATE '2026-10-17')
    INTO bcl1223.event VALUES ('E022', 'C007', 'V004', 'S2026S', 'gg1007', 'Social Enterprise Forum', DATE '2026-10-24')
    INTO bcl1223.event VALUES ('E023', 'C008', 'V008', 'S2026S', 'hh1008', 'Night Photography Walk', DATE '2026-10-31')
    INTO bcl1223.event VALUES ('E024', 'C009', 'V009', 'S2026S', 'ii1009', 'Tree Planting Day', DATE '2026-11-07')
    INTO bcl1223.event VALUES ('E025', 'C010', 'V009', 'S2026S', 'jj1010', 'Wellness Fun Run', DATE '2026-11-14')
    INTO bcl1223.event VALUES ('E026', 'C011', 'V007', 'S2026S', 'kk1011', 'Food Bank Collection', DATE '2026-11-21')
    INTO bcl1223.event VALUES ('E027', 'C012', 'V002', 'S2026S', 'll1012', 'Stagecraft Workshop', DATE '2026-11-28')
    INTO bcl1223.event VALUES ('E028', 'C013', 'V001', 'S2026S', 'mm1013', 'Capture-the-Flag Practice', DATE '2026-12-05')
    INTO bcl1223.event VALUES ('E029', 'C014', 'V010', 'S2026S', 'nn1014', 'Healthy Baking Lab', DATE '2026-12-12')
    INTO bcl1223.event VALUES ('E030', 'C015', 'V006', 'S2026S', 'oo1015', 'Team Chess League', DATE '2026-12-19')
    INTO bcl1223.event VALUES ('E031', 'C001', 'V001', 'S2027J', 'aa1001', 'Database Design Sprint', DATE '2027-01-16')
    INTO bcl1223.event VALUES ('E032', 'C002', 'V003', 'S2027J', 'bb1002', 'Traditional Dance Exchange', DATE '2027-01-23')
    INTO bcl1223.event VALUES ('E033', 'C003', 'V002', 'S2027J', 'cc1003', 'Battle of the Bands', DATE '2027-01-30')
    INTO bcl1223.event VALUES ('E034', 'C004', 'V004', 'S2027J', 'dd1004', 'Investment Case Competition', DATE '2027-02-06')
    INTO bcl1223.event VALUES ('E035', 'C005', 'V005', 'S2027J', 'ee1005', 'Robotics Open Day', DATE '2027-02-13')
    INTO bcl1223.event VALUES ('E036', 'C006', 'V006', 'S2027J', 'ff1006', 'Policy Debate Finals', DATE '2027-02-20')
    INTO bcl1223.event VALUES ('E037', 'C007', 'V004', 'S2027J', 'gg1007', 'Business Model Workshop', DATE '2027-02-27')
    INTO bcl1223.event VALUES ('E038', 'C008', 'V008', 'S2027J', 'hh1008', 'Documentary Photo Exhibition', DATE '2027-03-06')
    INTO bcl1223.event VALUES ('E039', 'C009', 'V009', 'S2027J', 'ii1009', 'Earth Hour Campaign', DATE '2027-03-13')
    INTO bcl1223.event VALUES ('E040', 'C010', 'V009', 'S2027J', 'jj1010', 'Campus Badminton Open', DATE '2027-03-20')
    INTO bcl1223.event VALUES ('E041', 'C011', 'V007', 'S2027J', 'kk1011', 'Volunteer Leadership Forum', DATE '2027-03-27')
    INTO bcl1223.event VALUES ('E042', 'C012', 'V002', 'S2027J', 'll1012', 'Student Theatre Premiere', DATE '2027-04-03')
    INTO bcl1223.event VALUES ('E043', 'C013', 'V001', 'S2027J', 'mm1013', 'Secure Coding Clinic', DATE '2027-04-10')
    INTO bcl1223.event VALUES ('E044', 'C014', 'V010', 'S2027J', 'nn1014', 'Sustainable Cooking Challenge', DATE '2027-04-17')
    INTO bcl1223.event VALUES ('E045', 'C015', 'V006', 'S2027J', 'oo1015', 'Intercollege Chess Cup', DATE '2027-04-24')
SELECT 1 FROM dual;

INSERT ALL
    INTO bcl1223.event_registration VALUES ('E001', 'C001', 'aa1001', DATE '2026-05-20', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E001', 'C001', 'pp1016', DATE '2026-05-21', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E002', 'C002', 'bb1002', DATE '2026-05-20', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E002', 'C002', 'ss1019', DATE '2026-05-21', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E003', 'C003', 'cc1003', DATE '2026-05-20', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E003', 'C003', 'vv1022', DATE '2026-05-21', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E004', 'C004', 'dd1004', DATE '2026-05-20', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E004', 'C004', 'yy1025', DATE '2026-05-21', 'ABSENT')
    INTO bcl1223.event_registration VALUES ('E005', 'C005', 'ee1005', DATE '2026-05-20', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E005', 'C005', 'bb1028', DATE '2026-05-21', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E006', 'C006', 'ff1006', DATE '2026-05-22', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E006', 'C006', 'aa1001', DATE '2026-05-23', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E007', 'C007', 'gg1007', DATE '2026-05-22', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E007', 'C007', 'cc1003', DATE '2026-05-23', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E008', 'C008', 'hh1008', DATE '2026-05-22', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E008', 'C008', 'ee1005', DATE '2026-05-23', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E009', 'C009', 'ii1009', DATE '2026-05-22', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E009', 'C009', 'gg1007', DATE '2026-05-23', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E010', 'C010', 'jj1010', DATE '2026-05-22', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E010', 'C010', 'ii1009', DATE '2026-05-23', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E011', 'C011', 'kk1011', DATE '2026-05-24', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E011', 'C011', 'll1012', DATE '2026-05-25', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E012', 'C012', 'll1012', DATE '2026-05-24', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E012', 'C012', 'nn1014', DATE '2026-05-25', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E013', 'C013', 'mm1013', DATE '2026-05-24', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E013', 'C013', 'pp1016', DATE '2026-05-25', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E014', 'C014', 'nn1014', DATE '2026-05-24', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E014', 'C014', 'rr1018', DATE '2026-05-25', 'ATTENDED')
    INTO bcl1223.event_registration VALUES ('E015', 'C015', 'oo1015', DATE '2026-05-24', 'REGISTERED')
    INTO bcl1223.event_registration VALUES ('E015', 'C015', 'tt1020', DATE '2026-05-25', 'REGISTERED')
SELECT 1 FROM dual;

COMMIT;

EXIT;
