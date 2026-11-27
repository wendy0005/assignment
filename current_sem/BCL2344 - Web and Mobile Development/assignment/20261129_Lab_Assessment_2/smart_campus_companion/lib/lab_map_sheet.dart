import 'package:material_ui/material_ui.dart';

import 'campus_theme.dart';

class LabMapSheet extends StatelessWidget {
  const LabMapSheet({super.key});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      top: false,
      child: SingleChildScrollView(
        padding: const EdgeInsets.fromLTRB(20, 0, 20, 20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              'Campus map',
              style: Theme.of(context).textTheme.titleLarge
                  ?.copyWith(color: ink, fontWeight: FontWeight.w800),
            ),
            const SizedBox(height: 4),
            const Text('Block B · Lab 2', style: TextStyle(color: muted)),
            const SizedBox(height: 14),
            const _CampusMap(),
            const SizedBox(height: 12),
            const Text(
              'From Gate A, head towards Block B. Lab 2 is in that building.',
              style: TextStyle(color: muted),
            ),
            const SizedBox(height: 16),
            FilledButton(
              onPressed: () => Navigator.of(context).pop(),
              style: FilledButton.styleFrom(minimumSize: const Size(0, 48)),
              child: const Text('Done'),
            ),
          ],
        ),
      ),
    );
  }
}

class _CampusMap extends StatelessWidget {
  const _CampusMap();

  @override
  Widget build(BuildContext context) {
    return DecoratedBox(
      decoration: BoxDecoration(
        color: const Color(0xFFDCE5ED),
        border: Border.all(color: border),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text('Illustrative campus map', style: TextStyle(color: ink)),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(
                  child: _mapLabel(
                    'Block B · Lab 2',
                    background: navy,
                    foreground: Colors.white,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(child: _mapLabel('Library')),
              ],
            ),
            const Row(
              children: [
                Expanded(
                  child: Icon(Icons.arrow_upward, size: 24, color: navy),
                ),
                SizedBox(width: 12),
                Expanded(child: SizedBox.shrink()),
              ],
            ),
            Row(
              children: [
                Expanded(child: _mapLabel('Gate A')),
                const SizedBox(width: 12),
                Expanded(child: _mapLabel('Student Centre')),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _mapLabel(
    String label, {
    Color background = const Color(0xFFF7F9FC),
    Color foreground = ink,
  }) {
    return DecoratedBox(
      decoration: BoxDecoration(
        color: background,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 8),
        child: Text(
          label,
          textAlign: TextAlign.center,
          style: TextStyle(color: foreground, fontWeight: FontWeight.w700),
        ),
      ),
    );
  }
}
