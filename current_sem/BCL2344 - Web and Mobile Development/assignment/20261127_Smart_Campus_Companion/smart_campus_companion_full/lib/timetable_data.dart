class CampusClass {
  const CampusClass(this.time, this.title, this.room, {this.hasLabMap = false});

  final String time;
  final String title;
  final String room;
  final bool hasLabMap;
}

class ScheduleDay {
  const ScheduleDay(this.name, this.date, this.classes);

  final String name;
  final int date;
  final List<CampusClass> classes;

  String get fullDate => '$name, $date October';
}

// The reference wireframe uses an illustrative week, 26–30 October 2026.
const campusWeek = [
  ScheduleDay('Monday', 26, [
    CampusClass(
      '10:00 AM–12:00 PM',
      'Web & Mobile Development',
      'Block B · Lab 2',
      hasLabMap: true,
    ),
    CampusClass('2:00–3:30 PM', 'Database Fundamentals', 'Block A · Room 302'),
  ]),
  ScheduleDay('Tuesday', 27, [
    CampusClass('9:00–11:00 AM', 'Operating Systems', 'Block A · Room 204'),
  ]),
  ScheduleDay('Wednesday', 28, [
    CampusClass(
      '11:00 AM–12:30 PM',
      'Algorithms and Complexity',
      'Block A · Room 302',
    ),
  ]),
  ScheduleDay('Thursday', 29, [
    CampusClass(
      '2:00–4:00 PM',
      'Web & Mobile Development Lab',
      'Block B · Lab 2',
      hasLabMap: true,
    ),
  ]),
  ScheduleDay('Friday', 30, []),
];
