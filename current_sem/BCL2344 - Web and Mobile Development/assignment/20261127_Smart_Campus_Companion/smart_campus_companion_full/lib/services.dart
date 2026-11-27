import 'package:material_ui/material_ui.dart';

import 'campus_map.dart';
import 'campus_session.dart';
import 'campus_ui.dart';

class Facility {
  const Facility(
    this.title,
    this.subtitle,
    this.category,
    this.hours,
    this.place,
    this.icon,
  );

  final String title;
  final String subtitle;
  final String category;
  final String hours;
  final CampusPlace place;
  final IconData icon;

  bool get hasStudyRooms => place == CampusPlace.library;
}

const campusFacilities = [
  Facility(
    'Campus Library',
    'Study rooms · Level 2',
    'Study',
    '8:00 AM–10:00 PM',
    CampusPlace.library,
    Icons.local_library_outlined,
  ),
  Facility(
    'Student Support',
    'Advice and appointments',
    'Support',
    '9:00 AM–5:00 PM',
    CampusPlace.support,
    Icons.support_agent,
  ),
  Facility(
    'IT Help Desk',
    'Campus access and Wi-Fi',
    'Support',
    '9:00 AM–5:00 PM',
    CampusPlace.support,
    Icons.devices_outlined,
  ),
];

class ServicesScreen extends StatefulWidget {
  const ServicesScreen({
    required this.session,
    required this.onDone,
    super.key,
  });

  final CampusSession session;
  final VoidCallback onDone;

  @override
  State<ServicesScreen> createState() => _ServicesScreenState();
}

class _ServicesScreenState extends State<ServicesScreen> {
  String _query = '';
  String _category = 'All';

  @override
  Widget build(BuildContext context) {
    final matches = campusFacilities.where(
      (facility) =>
          (_category == 'All' || facility.category == _category) &&
          '${facility.title} ${facility.subtitle}'.toLowerCase().contains(
            _query.trim().toLowerCase(),
          ),
    );
    return CampusPage(
      title: 'Facilities & services',
      children: [
        const SectionHeading('Campus services'),
        TextField(
          onChanged: (query) => setState(() => _query = query),
          decoration: const InputDecoration(
            prefixIcon: Icon(Icons.search),
            labelText: 'Search services',
            hintText: 'Try study rooms',
            border: OutlineInputBorder(),
          ),
        ),
        CampusChoices(
          labels: const ['All', 'Study', 'Support'],
          selected: _category,
          onSelect: (category) => setState(() => _category = category),
        ),
        if (matches.isEmpty) const Text('No services match your filters.'),
        for (final facility in matches)
          CampusCard(
            title: facility.title,
            subtitle: facility.subtitle,
            icon: facility.icon,
            onTap: () => openScreen(
              context,
              FacilityScreen(
                facility: facility,
                session: widget.session,
                onDone: widget.onDone,
              ),
            ),
          ),
      ],
    );
  }
}

class FacilityScreen extends StatelessWidget {
  const FacilityScreen({
    required this.facility,
    required this.session,
    required this.onDone,
    super.key,
  });

  final Facility facility;
  final CampusSession session;
  final VoidCallback onDone;

  @override
  Widget build(BuildContext context) => CampusPage(
    title: 'Facility details',
    children: [
      SectionHeading(
        facility.title,
        subtitle: facility.hasStudyRooms
            ? 'North block · Level 2 study rooms'
            : facility.subtitle,
      ),
      CampusCard(
        title: 'Open today',
        subtitle: facility.hours,
        icon: Icons.schedule,
      ),
      if (facility.hasStudyRooms) ...[
        const CampusCard(
          title: 'Study Room L2-04',
          subtitle: '4 seats · 1 hour per reservation',
          icon: Icons.meeting_room_outlined,
        ),
        CampusAction(
          'Book a study room',
          () => openScreen(
            context,
            BookRoomScreen(session: session, onDone: onDone),
          ),
        ),
      ],
      CampusAction(
        'View on map',
        () => openScreen(context, CampusMapScreen(initial: facility.place)),
        secondary: true,
      ),
    ],
  );
}

const _bookingDates = [
  'Wednesday, 28 October',
  'Thursday, 29 October',
  'Friday, 30 October',
];
const _dailySlots = [
  ['2:00 PM', '3:00 PM', '4:00 PM'],
  ['10:00 AM', '11:00 AM', '2:00 PM'],
  ['1:00 PM', '2:00 PM', '4:00 PM'],
];
const _room = 'Study Room L2-04';

String _bookingTime(String start) {
  final split = start.split(':');
  final firstHour = int.parse(split.first);
  final nextHour = firstHour % 12 + 1;
  final period = start.split(' ').last;
  final nextPeriod = firstHour == 11 ? (period == 'AM' ? 'PM' : 'AM') : period;
  return '$start–$nextHour:00 $nextPeriod';
}

class BookRoomScreen extends StatefulWidget {
  const BookRoomScreen({
    required this.session,
    required this.onDone,
    super.key,
  });

  final CampusSession session;
  final VoidCallback onDone;

  @override
  State<BookRoomScreen> createState() => _BookRoomScreenState();
}

class _BookRoomScreenState extends State<BookRoomScreen> {
  int _date = 0;
  String? _time;
  String? _conflict;

  void _confirm() {
    final time = _time;
    if (time == null) return;
    final date = _bookingDates[_date];
    final reference = widget.session.reserve(date, time);
    if (reference == null) {
      setState(() {
        _conflict = time;
        _time = null;
      });
      return;
    }
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(
        builder: (_) => ReservationScreen(
          reference: reference,
          date: date,
          time: time,
          onDone: widget.onDone,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final date = _bookingDates[_date];
    final time = _time;
    final showConflict = _conflict != null && time == null;
    return CampusPage(
      title: 'Book a study room',
      children: [
        const SectionHeading(
          _room,
          subtitle: 'Campus Library · Up to 4 students',
        ),
        InputDecorator(
          decoration: const InputDecoration(
            labelText: 'Date',
            border: OutlineInputBorder(),
          ),
          child: DropdownButtonHideUnderline(
            child: DropdownButton<int>(
              isExpanded: true,
              value: _date,
              items: [
                for (final (index, date) in _bookingDates.indexed)
                  DropdownMenuItem(value: index, child: Text(date)),
              ],
              onChanged: (index) => setState(() {
                _date = index!;
                _time = null;
                _conflict = null;
              }),
            ),
          ),
        ),
        Text(
          showConflict ? 'Choose another time' : 'Choose a time',
          style: Theme.of(context).textTheme.titleMedium,
        ),
        Wrap(
          spacing: 8,
          runSpacing: 4,
          children: [
            for (final slot in _dailySlots[_date])
              ChoiceChip(
                label: Text(
                  slot == _conflict || widget.session.reserved(date, slot)
                      ? '$slot · Taken'
                      : slot,
                ),
                selected: time == slot,
                onSelected:
                    slot == _conflict || widget.session.reserved(date, slot)
                    ? null
                    : (_) => setState(() => _time = slot),
              ),
          ],
        ),
        if (showConflict)
          CampusCard(
            title: '$_conflict is no longer available',
            subtitle: 'Choose a new time to continue.',
            icon: Icons.info_outline,
          ),
        if (time != null)
          CampusCard(
            title: 'Your booking',
            subtitle: '$date · ${_bookingTime(time)}\n$_room',
          ),
        const Text('1 hour · 1 room · No fee'),
        CampusAction('Confirm reservation', time == null ? null : _confirm),
      ],
    );
  }
}

class ReservationScreen extends StatelessWidget {
  const ReservationScreen({
    required this.reference,
    required this.date,
    required this.time,
    required this.onDone,
    super.key,
  });

  final String reference;
  final String date;
  final String time;
  final VoidCallback onDone;

  @override
  Widget build(BuildContext context) => CampusPage(
    title: 'Reservation',
    children: [
      SectionHeading(
        'Room reserved',
        subtitle: 'Booking reference: $reference',
      ),
      CampusCard(
        title: _room,
        subtitle: '$date · ${_bookingTime(time)}\nCampus Library · Level 2',
        icon: Icons.check_circle_outline,
        children: const [Text('Present your student ID at check-in.')],
      ),
      CampusAction(
        'Get directions',
        () =>
            openScreen(context, const RoutePreview(place: CampusPlace.library)),
      ),
      CampusAction('Done', onDone, secondary: true),
    ],
  );
}
