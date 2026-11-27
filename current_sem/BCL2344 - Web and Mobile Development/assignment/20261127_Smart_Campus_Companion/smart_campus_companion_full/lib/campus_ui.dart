import 'package:material_ui/material_ui.dart';

import 'campus_theme.dart';

Future<T?> openScreen<T>(BuildContext context, Widget screen) =>
    Navigator.of(context).push<T>(MaterialPageRoute(builder: (_) => screen));

class CampusPage extends StatelessWidget {
  const CampusPage({
    required this.title,
    required this.children,
    this.actions = const [],
    super.key,
  });

  final String title;
  final List<Widget> children;
  final List<Widget> actions;

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(
      title: Text(title, style: const TextStyle(fontWeight: FontWeight.w700)),
      shape: const Border(bottom: BorderSide(color: border)),
      actions: actions,
    ),
    body: SafeArea(
      top: false,
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 600),
          child: ListView(
            padding: const EdgeInsets.fromLTRB(18, 22, 18, 24),
            children: [
              for (final child in children)
                Padding(
                  padding: const EdgeInsets.only(bottom: 14),
                  child: child,
                ),
            ],
          ),
        ),
      ),
    ),
  );
}

class SectionHeading extends StatelessWidget {
  const SectionHeading(this.title, {this.subtitle, super.key});

  final String title;
  final String? subtitle;

  @override
  Widget build(BuildContext context) => Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Semantics(
        header: true,
        child: Text(
          title,
          style: Theme.of(context).textTheme.headlineMedium
              ?.copyWith(color: ink, fontWeight: FontWeight.w800),
        ),
      ),
      if (subtitle != null) ...[
        const SizedBox(height: 4),
        Text(subtitle!, style: const TextStyle(color: muted)),
      ],
    ],
  );
}

class CampusCard extends StatelessWidget {
  const CampusCard({
    required this.title,
    this.subtitle,
    this.icon,
    this.children = const [],
    this.onTap,
    super.key,
  });

  final String title;
  final String? subtitle;
  final IconData? icon;
  final List<Widget> children;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) => Card(
    margin: EdgeInsets.zero,
    elevation: 0,
    color: Colors.white,
    clipBehavior: Clip.antiAlias,
    shape: RoundedRectangleBorder(
      side: const BorderSide(color: border),
      borderRadius: BorderRadius.circular(12),
    ),
    child: InkWell(
      onTap: onTap,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (icon != null) ...[
                  Icon(icon, color: navy),
                  const SizedBox(width: 12),
                ],
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        title,
                        style: const TextStyle(
                          color: ink,
                          fontWeight: FontWeight.w800,
                          fontSize: 16,
                        ),
                      ),
                      if (subtitle != null) ...[
                        const SizedBox(height: 4),
                        Text(subtitle!, style: const TextStyle(color: muted)),
                      ],
                    ],
                  ),
                ),
                if (onTap != null) const Icon(Icons.chevron_right, color: navy),
              ],
            ),
            for (final child in children)
              Padding(padding: const EdgeInsets.only(top: 12), child: child),
          ],
        ),
      ),
    ),
  );
}

class CampusAction extends StatelessWidget {
  const CampusAction(
    this.label,
    this.onPressed, {
    this.secondary = false,
    super.key,
  });

  final String label;
  final VoidCallback? onPressed;
  final bool secondary;

  @override
  Widget build(BuildContext context) => secondary
      ? OutlinedButton(onPressed: onPressed, child: Text(label))
      : FilledButton(
          onPressed: onPressed,
          style: FilledButton.styleFrom(minimumSize: const Size(0, 48)),
          child: Text(label),
        );
}

class CampusChoices extends StatelessWidget {
  const CampusChoices({
    required this.labels,
    required this.selected,
    required this.onSelect,
    super.key,
  });

  final List<String> labels;
  final String selected;
  final ValueChanged<String> onSelect;

  @override
  Widget build(BuildContext context) => Wrap(
    spacing: 8,
    runSpacing: 4,
    children: [
      for (final label in labels)
        ChoiceChip(
          label: Text(label),
          selected: label == selected,
          onSelected: (_) => onSelect(label),
        ),
    ],
  );
}
