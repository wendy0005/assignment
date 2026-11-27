import 'dart:math' as math;

import 'package:material_ui/material_ui.dart';

import 'campus_theme.dart';
import 'lab_map_sheet.dart';
import 'timetable_data.dart';

class TimetableScreen extends StatefulWidget {
  const TimetableScreen({super.key});

  @override
  State<TimetableScreen> createState() => _TimetableScreenState();
}

class _TimetableScreenState extends State<TimetableScreen> {
  int _selectedDay = 0;

  void _showLabMap() {
    showModalBottomSheet<void>(
      context: context,
      useSafeArea: true,
      isScrollControlled: true,
      showDragHandle: true,
      constraints: const BoxConstraints(maxWidth: 520),
      backgroundColor: Colors.white,
      builder: (context) => const LabMapSheet(),
    );
  }

  @override
  Widget build(BuildContext context) {
    final day = campusWeek[_selectedDay];
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Timetable',
          style: TextStyle(fontWeight: FontWeight.w700),
        ),
        centerTitle: false,
        shape: const Border(bottom: BorderSide(color: border)),
      ),
      body: SafeArea(
        top: false,
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 600),
            child: ListView(
              padding: const EdgeInsets.fromLTRB(18, 22, 18, 24),
              children: [
                Text(
                  'This week',
                  style: Theme.of(context).textTheme.headlineMedium
                      ?.copyWith(color: ink, fontWeight: FontWeight.w800),
                ),
                const SizedBox(height: 3),
                const Text('26–30 October', style: TextStyle(color: muted)),
                const SizedBox(height: 16),
                LayoutBuilder(
                  builder: (context, constraints) {
                    final scaledFont = MediaQuery.textScalerOf(context)
                        .scale(13);
                    final minimumTileWidth = math.max(
                      48.0,
                      scaledFont * 3 + 12,
                    );
                    final availableTileWidth = (constraints.maxWidth - 32) / 5;
                    final tileWidth = math.max(
                      availableTileWidth,
                      minimumTileWidth,
                    );
                    return SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Row(
                        children: [
                          for (final (index, weekday) in campusWeek.indexed)
                            Padding(
                              padding: EdgeInsets.only(
                                right: index == campusWeek.length - 1 ? 0 : 8,
                              ),
                              child: _DayButton(
                                width: tileWidth,
                                day: weekday,
                                selected: index == _selectedDay,
                                onPressed: () =>
                                    setState(() => _selectedDay = index),
                              ),
                            ),
                        ],
                      ),
                    );
                  },
                ),
                const SizedBox(height: 25),
                Semantics(
                  header: true,
                  liveRegion: true,
                  child: Text(
                    day.fullDate,
                    style: Theme.of(context).textTheme.titleMedium
                        ?.copyWith(color: ink, fontWeight: FontWeight.w800),
                  ),
                ),
                const SizedBox(height: 10),
                if (day.classes.isEmpty)
                  const Card(
                    margin: EdgeInsets.zero,
                    color: Colors.white,
                    elevation: 0,
                    child: Padding(
                      padding: EdgeInsets.all(20),
                      child: Text(
                        'No classes scheduled for this day.',
                        style: TextStyle(color: muted),
                      ),
                    ),
                  )
                else
                  for (final (index, lesson) in day.classes.indexed)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 12),
                      child: _ClassCard(
                        lesson: lesson,
                        highlight: index == 0,
                        onFindLab: lesson.hasLabMap ? _showLabMap : null,
                      ),
                    ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _DayButton extends StatelessWidget {
  const _DayButton({
    required this.width,
    required this.day,
    required this.selected,
    required this.onPressed,
  });

  final double width;
  final ScheduleDay day;
  final bool selected;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return Semantics(
      button: true,
      selected: selected,
      label: day.fullDate,
      onTap: onPressed,
      excludeSemantics: true,
      child: SizedBox(
        width: width,
        child: OutlinedButton(
          onPressed: onPressed,
          style: OutlinedButton.styleFrom(
            foregroundColor: selected ? Colors.white : ink,
            backgroundColor: selected ? navy : Colors.white,
            side: BorderSide(color: selected ? navy : border),
            padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 4),
          ),
          child: Column(
            children: [
              Text(
                day.name.substring(0, 3),
                style: const TextStyle(fontSize: 13),
              ),
              const SizedBox(height: 2),
              Text(
                day.date.toString(),
                style: const TextStyle(
                  fontSize: 17,
                  fontWeight: FontWeight.w800,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _ClassCard extends StatelessWidget {
  const _ClassCard({
    required this.lesson,
    required this.highlight,
    this.onFindLab,
  });

  final CampusClass lesson;
  final bool highlight;
  final VoidCallback? onFindLab;

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: EdgeInsets.zero,
      color: Colors.white,
      elevation: 0,
      clipBehavior: Clip.antiAlias,
      shape: RoundedRectangleBorder(
        side: const BorderSide(color: border),
        borderRadius: BorderRadius.circular(12),
      ),
      child: DecoratedBox(
        decoration: BoxDecoration(
          border: highlight
              ? const Border(left: BorderSide(color: navy, width: 4))
              : null,
        ),
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 14, 16, 14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(
                lesson.time,
                style: const TextStyle(
                  color: navy,
                  fontWeight: FontWeight.w700,
                ),
              ),
              const SizedBox(height: 5),
              Text(
                lesson.title,
                style: Theme.of(context).textTheme.titleMedium
                    ?.copyWith(color: ink, fontWeight: FontWeight.w800),
              ),
              const SizedBox(height: 5),
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Icon(Icons.place_outlined, size: 18, color: muted),
                  const SizedBox(width: 5),
                  Expanded(
                    child: Text(
                      lesson.room,
                      style: const TextStyle(color: muted),
                    ),
                  ),
                ],
              ),
              if (onFindLab != null) ...[
                const SizedBox(height: 12),
                OutlinedButton.icon(
                  onPressed: onFindLab,
                  icon: const Icon(Icons.map_outlined, size: 18),
                  label: const Text(
                    'Find Lab 2 on map',
                    textAlign: TextAlign.center,
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
