import 'package:material_ui/material_ui.dart';

import 'campus_map.dart';
import 'campus_session.dart';
import 'campus_theme.dart';
import 'campus_ui.dart';
import 'events.dart';
import 'services.dart';
import 'timetable_screen.dart';

class SignInScreen extends StatefulWidget {
  const SignInScreen({super.key});

  @override
  State<SignInScreen> createState() => _SignInScreenState();
}

class _SignInScreenState extends State<SignInScreen> {
  final _form = GlobalKey<FormState>();
  final _email = TextEditingController();
  final _password = TextEditingController();
  bool _showPassword = false;

  @override
  void dispose() {
    _email.dispose();
    _password.dispose();
    super.dispose();
  }

  void _signIn() {
    if (!_form.currentState!.validate()) return;
    final session = CampusSession(_email.text.trim().toLowerCase());
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(builder: (_) => CampusHome(session: session)),
    );
  }

  @override
  Widget build(BuildContext context) => CampusPage(
    title: 'Sign in',
    children: [
      const Padding(
        padding: EdgeInsets.only(top: 10, bottom: 10),
        child: SectionHeading(
          'Smart Campus Companion',
          subtitle: 'Sign in with your student account.',
        ),
      ),
      Form(
        key: _form,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextFormField(
              controller: _email,
              keyboardType: TextInputType.emailAddress,
              textInputAction: TextInputAction.next,
              decoration: const InputDecoration(
                labelText: 'University email',
                hintText: 'student@university.edu',
                prefixIcon: Icon(Icons.mail_outline),
                border: OutlineInputBorder(),
              ),
              validator: (value) =>
                  RegExp(r'^[a-zA-Z0-9][^\s@]*@[^\s@]+\.[^\s@]+$')
                      .hasMatch(value!.trim())
                  ? null
                  : 'Enter a valid email address.',
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _password,
              obscureText: !_showPassword,
              textInputAction: TextInputAction.done,
              onFieldSubmitted: (_) => _signIn(),
              decoration: InputDecoration(
                labelText: 'Password',
                prefixIcon: const Icon(Icons.lock_outline),
                border: const OutlineInputBorder(),
                suffixIcon: IconButton(
                  icon: Icon(
                    _showPassword ? Icons.visibility_off : Icons.visibility,
                  ),
                  tooltip: _showPassword ? 'Hide password' : 'Show password',
                  onPressed: () =>
                      setState(() => _showPassword = !_showPassword),
                ),
              ),
              validator: (value) => value!.trim().length >= 6
                  ? null
                  : 'Enter at least six characters.',
            ),
            Align(
              alignment: Alignment.centerRight,
              child: TextButton(
                onPressed: () => showDialog<void>(
                  context: context,
                  builder: (dialog) => AlertDialog(
                    title: const Text('Account recovery'),
                    content: const Text(
                      'Use your university’s account recovery service to reset a real password. To explore this demo, use the sample account below.',
                    ),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(dialog),
                        child: const Text('OK'),
                      ),
                    ],
                  ),
                ),
                child: const Text('Forgot password?'),
              ),
            ),
            CampusAction('Sign in', _signIn),
            const SizedBox(height: 8),
            CampusAction('Use demo account', () {
              _email.text = 'aina@university.edu';
              _password.text = 'campus-demo';
            }, secondary: true),
            const SizedBox(height: 12),
            const Text(
              'Demo sign-in uses local validation. Use sample details.',
              style: TextStyle(color: muted),
            ),
          ],
        ),
      ),
    ],
  );
}

class CampusHome extends StatefulWidget {
  const CampusHome({required this.session, super.key});

  final CampusSession session;

  @override
  State<CampusHome> createState() => _CampusHomeState();
}

class _CampusHomeState extends State<CampusHome> {
  int _tab = 0;

  @override
  void dispose() {
    widget.session.dispose();
    super.dispose();
  }

  void _select(int index) => setState(() => _tab = index);

  void _showTab(int index) {
    Navigator.of(context).popUntil((route) => route.isFirst);
    _select(index);
  }

  @override
  Widget build(BuildContext context) {
    final session = widget.session;
    return Scaffold(
      body: IndexedStack(
        index: _tab,
        children: [
          _Today(session: session, onTab: _showTab),
          const CampusMapScreen(),
          ServicesScreen(session: session, onDone: () => _showTab(2)),
          EventsScreen(session: session, onDone: () => _showTab(3)),
        ],
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _tab,
        onDestinationSelected: _select,
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.today_outlined),
            label: 'Today',
          ),
          NavigationDestination(icon: Icon(Icons.map_outlined), label: 'Map'),
          NavigationDestination(
            icon: Icon(Icons.school_outlined),
            label: 'Services',
          ),
          NavigationDestination(
            icon: Icon(Icons.event_outlined),
            label: 'Events',
          ),
        ],
      ),
    );
  }
}

class _Today extends StatelessWidget {
  const _Today({required this.session, required this.onTab});

  final CampusSession session;
  final ValueChanged<int> onTab;

  @override
  Widget build(BuildContext context) => ListenableBuilder(
    listenable: session,
    builder: (context, _) => CampusPage(
      title: 'Campus Companion',
      actions: [
        IconButton(
          tooltip: 'Profile',
          icon: const Icon(Icons.account_circle_outlined),
          onPressed: () => openScreen(context, ProfileScreen(session: session)),
        ),
        IconButton(
          tooltip: 'Alerts',
          icon: Badge(
            isLabelVisible: session.libraryUnread,
            child: const Icon(Icons.notifications_outlined),
          ),
          onPressed: () =>
              openScreen(context, AlertsScreen(session: session, onTab: onTab)),
        ),
      ],
      children: [
        SectionHeading(
          'Good morning, ${session.firstName}',
          subtitle: 'Monday, 26 October',
        ),
        CampusCard(
          title: 'Web & Mobile Development',
          subtitle: 'Next class · 10:00 AM\nBlock B · Lab 2',
          icon: Icons.schedule,
          children: [
            CampusAction(
              'View timetable',
              () => openScreen(context, const TimetableScreen()),
            ),
          ],
        ),
        Text('Campus shortcuts', style: Theme.of(context).textTheme.titleLarge),
        CampusCard(
          title: 'Find a building',
          subtitle: 'Browse the campus map',
          icon: Icons.map_outlined,
          onTap: () => onTab(1),
        ),
        CampusCard(
          title: 'Book a study room',
          subtitle: 'Library and other services',
          icon: Icons.meeting_room_outlined,
          onTap: () => onTab(2),
        ),
        CampusCard(
          title: 'Library hours changed',
          subtitle: session.libraryUnread
              ? 'Unread announcement'
              : 'Announcement',
          icon: Icons.campaign_outlined,
          onTap: () => openLibraryNotice(context, session, onTab),
        ),
      ],
    ),
  );
}

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({required this.session, super.key});

  final CampusSession session;

  @override
  Widget build(BuildContext context) => ListenableBuilder(
    listenable: session,
    builder: (context, _) => CampusPage(
      title: 'Profile',
      children: [
        SectionHeading(
          session.fullName,
          subtitle: 'Undergraduate student · Kota Damansara campus',
        ),
        CampusCard(
          title: 'Account',
          icon: Icons.person_outline,
          children: [Text('University email\n${session.email}')],
        ),
        CampusCard(
          title: 'Notifications',
          children: [
            SwitchListTile(
              contentPadding: EdgeInsets.zero,
              title: const Text('Event reminders'),
              subtitle: Text(session.reminders ? 'On' : 'Off'),
              value: session.reminders,
              onChanged: session.setReminders,
            ),
          ],
        ),
        CampusAction(
          'Sign out',
          () => Navigator.of(context).pushAndRemoveUntil(
            MaterialPageRoute(builder: (_) => const SignInScreen()),
            (_) => false,
          ),
          secondary: true,
        ),
      ],
    ),
  );
}

void openLibraryNotice(
  BuildContext context,
  CampusSession session,
  ValueChanged<int> onTab,
) {
  session.readLibraryNotice();
  openScreen(
    context,
    CampusPage(
      title: 'Announcement',
      children: [
        const SectionHeading(
          'Library hours changed',
          subtitle: 'Campus Library · 26 October, 8:30 AM',
        ),
        const Text(
          'Extended study hours begin today. The main library will stay open later through Friday, 30 October.',
        ),
        const CampusCard(
          title: 'Temporary hours',
          subtitle: 'Mon–Fri · 8:00 AM–10:00 PM',
          icon: Icons.schedule,
        ),
        Builder(
          builder: (context) => CampusAction(
            'View Campus Library',
            () => openScreen(
              context,
              FacilityScreen(
                facility: campusFacilities.first,
                session: session,
                onDone: () => onTab(2),
              ),
            ),
          ),
        ),
      ],
    ),
  );
}

class AlertsScreen extends StatefulWidget {
  const AlertsScreen({required this.session, required this.onTab, super.key});

  final CampusSession session;
  final ValueChanged<int> onTab;

  @override
  State<AlertsScreen> createState() => _AlertsScreenState();
}

class _AlertsScreenState extends State<AlertsScreen> {
  String _filter = 'All';

  @override
  Widget build(BuildContext context) {
    final session = widget.session;
    final onTab = widget.onTab;
    return ListenableBuilder(
      listenable: session,
      builder: (context, _) => CampusPage(
        title: 'Alerts',
        children: [
          SectionHeading(
            'Campus inbox',
            subtitle: session.libraryUnread
                ? '1 unread item'
                : '0 unread items',
          ),
          CampusChoices(
            labels: const ['All', 'Unread'],
            selected: _filter,
            onSelect: (filter) => setState(() => _filter = filter),
          ),
          if (_filter == 'All' || session.libraryUnread)
            CampusCard(
              title: 'Library hours changed',
              subtitle: session.libraryUnread
                  ? 'Unread · Announcement'
                  : 'Announcement',
              icon: Icons.campaign_outlined,
              onTap: () => openLibraryNotice(context, session, onTab),
            ),
          if (_filter == 'All') ...[
            if (session.reminders)
              CampusCard(
                title: 'Reminder · Design Jam',
                subtitle: 'Event starts on 29 October',
                icon: Icons.event_outlined,
                onTap: () => openScreen(
                  context,
                  EventDetails(
                    event: campusEvents.first,
                    session: session,
                    onDone: () => onTab(3),
                  ),
                ),
              ),
            CampusCard(
              title: 'Wi-Fi maintenance',
              subtitle: 'Service notice · 22 October',
              icon: Icons.wifi,
              onTap: () => openScreen(
                context,
                const CampusPage(
                  title: 'Announcement',
                  children: [
                    SectionHeading(
                      'Wi-Fi maintenance',
                      subtitle: 'IT Help Desk · 22 October',
                    ),
                    Text(
                      'Campus Wi-Fi maintenance has been completed. Contact the IT Help Desk if you cannot connect.',
                    ),
                  ],
                ),
              ),
            ),
          ] else if (!session.libraryUnread)
            const Text('You’re all caught up.'),
        ],
      ),
    );
  }
}
