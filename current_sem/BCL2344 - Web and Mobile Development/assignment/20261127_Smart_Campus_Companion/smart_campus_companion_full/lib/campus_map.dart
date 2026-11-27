import 'package:material_ui/material_ui.dart';

import 'campus_theme.dart';
import 'campus_ui.dart';

enum CampusPlace {
  library('Campus Library', 'North block · Level 2', 'Library', 280),
  lab('Block B · Lab 2', 'Block B · Level 1', 'Block B', 210),
  support(
    'Student Centre',
    'Student Support and IT Help Desk',
    'Student Centre',
    160,
  );

  const CampusPlace(
    this.title,
    this.description,
    this.pin,
    this.walkingDistance,
  );

  final String title;
  final String description;
  final String pin;
  final int walkingDistance;

  int get walkingMinutes => (walkingDistance / 75).ceil();
}

class CampusMapScreen extends StatefulWidget {
  const CampusMapScreen({this.initial = CampusPlace.library, super.key});

  final CampusPlace initial;

  @override
  State<CampusMapScreen> createState() => _CampusMapScreenState();
}

class _CampusMapScreenState extends State<CampusMapScreen> {
  late CampusPlace _selected = widget.initial;
  String _query = '';

  @override
  Widget build(BuildContext context) {
    final matches = CampusPlace.values.where(
      (place) => '${place.title} ${place.description}'.toLowerCase().contains(
        _query.trim().toLowerCase(),
      ),
    );
    return CampusPage(
      title: 'Campus map',
      children: [
        const SectionHeading('Find a place'),
        TextField(
          onChanged: (value) => setState(() => _query = value),
          decoration: const InputDecoration(
            labelText: 'Search campus',
            hintText: 'Try Lab 2 or Library',
            prefixIcon: Icon(Icons.search),
            border: OutlineInputBorder(),
          ),
        ),
        if (_query.trim().isNotEmpty)
          if (matches.isEmpty)
            const Text('No places match your search.')
          else
            Wrap(
              spacing: 8,
              children: [
                for (final place in matches)
                  ActionChip(
                    label: Text(place.title),
                    onPressed: () => setState(() => _selected = place),
                  ),
              ],
            ),
        CampusSchematic(
          selected: _selected,
          onSelect: (place) => setState(() => _selected = place),
        ),
        CampusCard(
          title: _selected.title,
          subtitle: '${_selected.walkingMinutes} min walk from Gate A',
          icon: Icons.place_outlined,
          children: [
            CampusAction(
              'Get directions',
              () => openScreen(context, RoutePreview(place: _selected)),
            ),
          ],
        ),
      ],
    );
  }
}

class CampusSchematic extends StatelessWidget {
  const CampusSchematic({
    required this.selected,
    this.onSelect,
    this.stepFree,
    super.key,
  });

  final CampusPlace selected;
  final ValueChanged<CampusPlace>? onSelect;
  final bool? stepFree;

  Widget _pin(CampusPlace place) {
    final selected = place == this.selected;
    return Semantics(
      selected: selected,
      child: InkWell(
        onTap: onSelect == null ? null : () => onSelect!(place),
        borderRadius: BorderRadius.circular(8),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 10),
          constraints: const BoxConstraints(minHeight: 48),
          decoration: BoxDecoration(
            color: selected ? navy : const Color(0xFFF7F9FC),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Text(
            place.pin,
            textAlign: TextAlign.center,
            style: TextStyle(
              color: selected ? Colors.white : ink,
              fontWeight: FontWeight.w700,
            ),
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.all(14),
    decoration: BoxDecoration(
      color: const Color(0xFFDCE5ED),
      borderRadius: BorderRadius.circular(12),
      border: Border.all(color: border),
    ),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const Text('Illustrative campus map', style: TextStyle(color: muted)),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(child: _pin(CampusPlace.lab)),
            const SizedBox(width: 12),
            Expanded(child: _pin(CampusPlace.library)),
          ],
        ),
        Padding(
          padding: const EdgeInsets.symmetric(vertical: 8),
          child: Icon(
            stepFree == null
                ? Icons.horizontal_rule
                : stepFree!
                ? Icons.accessible_forward
                : Icons.north_east,
            color: navy,
          ),
        ),
        Row(
          children: [
            const Expanded(
              child: Text(
                'Gate A',
                textAlign: TextAlign.center,
                style: TextStyle(color: navy, fontWeight: FontWeight.w700),
              ),
            ),
            const SizedBox(width: 12),
            Expanded(child: _pin(CampusPlace.support)),
          ],
        ),
      ],
    ),
  );
}

class RoutePreview extends StatefulWidget {
  const RoutePreview({required this.place, super.key});

  final CampusPlace place;

  @override
  State<RoutePreview> createState() => _RoutePreviewState();
}

class _RoutePreviewState extends State<RoutePreview> {
  bool _stepFree = false;

  @override
  Widget build(BuildContext context) {
    final place = widget.place;
    final distance = place.walkingDistance + (_stepFree ? 90 : 0);
    final directions = [
      'Enter from Gate A.',
      _stepFree
          ? 'Use the ramp next to the central walkway.'
          : 'Follow the central walkway.',
      _stepFree
          ? 'Follow the accessible entrance signs for ${place.pin}.'
          : 'Follow the signs for ${place.pin}.',
    ];
    return CampusPage(
      title: 'Route preview',
      children: [
        SectionHeading('To ${place.title}', subtitle: 'From Gate A'),
        CampusSchematic(selected: place, stepFree: _stepFree),
        CampusChoices(
          labels: const ['Standard', 'Step-free'],
          selected: _stepFree ? 'Step-free' : 'Standard',
          onSelect: (option) =>
              setState(() => _stepFree = option == 'Step-free'),
        ),
        CampusCard(
          title: '${(distance / 75).ceil()} min · $distance m',
          children: [
            for (final (index, direction) in directions.indexed)
              Text('${index + 1}. $direction'),
          ],
        ),
      ],
    );
  }
}
