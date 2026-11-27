import 'package:material_ui/material_ui.dart';

import 'campus_session.dart';
import 'campus_ui.dart';

class CampusEvent {
  const CampusEvent(
    this.name,
    this.host,
    this.date,
    this.time,
    this.location,
    this.description,
    this.cost,
  );

  final String name;
  final String host;
  final String date;
  final String time;
  final String location;
  final String description;
  final int cost;

  bool get free => cost == 0;
  String get price => free ? 'Free' : 'RM$cost.00';
}

const campusEvents = [
  CampusEvent(
    'Campus Design Jam',
    'Workshop · Student Design Club',
    'Thursday, 29 October',
    '4:00–6:00 PM',
    'Innovation Lab · North block',
    'Sketch, prototype and test an idea with other students. Materials included.',
    10,
  ),
  CampusEvent(
    'Study Skills Clinic',
    'Student Support',
    'Friday, 30 October',
    '1:00–2:00 PM',
    'Student Centre',
    'Try practical techniques for planning revision, taking notes and preparing for assessments.',
    0,
  ),
];

class EventsScreen extends StatefulWidget {
  const EventsScreen({required this.session, required this.onDone, super.key});

  final CampusSession session;
  final VoidCallback onDone;

  @override
  State<EventsScreen> createState() => _EventsScreenState();
}

class _EventsScreenState extends State<EventsScreen> {
  String _filter = 'Upcoming';

  @override
  Widget build(BuildContext context) => CampusPage(
    title: 'Campus events',
    children: [
      const SectionHeading('What’s on', subtitle: '26 October–1 November'),
      CampusChoices(
        labels: const ['Upcoming', 'Free'],
        selected: _filter,
        onSelect: (filter) => setState(() => _filter = filter),
      ),
      for (final event in campusEvents)
        if (_filter != 'Free' || event.free)
          CampusCard(
            title: event.name,
            subtitle: '${event.date} · ${event.price}\n${event.location}',
            icon: Icons.event_outlined,
            children: [
              CampusAction(
                'View event',
                () => openScreen(
                  context,
                  EventDetails(
                    event: event,
                    session: widget.session,
                    onDone: widget.onDone,
                  ),
                ),
                secondary: true,
              ),
            ],
          ),
    ],
  );
}

class EventDetails extends StatelessWidget {
  const EventDetails({
    required this.event,
    required this.session,
    required this.onDone,
    super.key,
  });

  final CampusEvent event;
  final CampusSession session;
  final VoidCallback onDone;

  @override
  Widget build(BuildContext context) => ListenableBuilder(
    listenable: session,
    builder: (context, _) {
      final reference = session.ticketFor(event.name);
      return CampusPage(
        title: 'Event details',
        children: [
          SectionHeading(event.name, subtitle: event.host),
          CampusCard(
            title: event.date,
            subtitle: event.time,
            icon: Icons.schedule,
          ),
          CampusCard(title: event.location, icon: Icons.place_outlined),
          CampusCard(
            title: 'About the workshop',
            children: [Text(event.description)],
          ),
          if (reference == null)
            CampusAction(
              'Get ticket · ${event.price}',
              () => openScreen(
                context,
                TicketCheckout(event: event, session: session, onDone: onDone),
              ),
            )
          else
            CampusAction(
              'View ticket',
              () => openScreen(
                context,
                TicketConfirmed(
                  event: event,
                  reference: reference,
                  onDone: onDone,
                ),
              ),
            ),
        ],
      );
    },
  );
}

enum _BankResult { approved, declined, pending }

class TicketCheckout extends StatefulWidget {
  const TicketCheckout({
    required this.event,
    required this.session,
    required this.onDone,
    super.key,
  });

  final CampusEvent event;
  final CampusSession session;
  final VoidCallback onDone;

  @override
  State<TicketCheckout> createState() => _TicketCheckoutState();
}

class _TicketCheckoutState extends State<TicketCheckout> {
  Future<void> _pay() async {
    final event = widget.event;
    final session = widget.session;
    if (event.free) {
      _confirm();
      return;
    }
    final result = await showDialog<_BankResult>(
      context: context,
      builder: (dialog) => AlertDialog(
        title: const Text('Simulated online banking'),
        content: const Text('Choose a demo bank response.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialog, _BankResult.pending),
            child: const Text('Keep pending'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(dialog, _BankResult.declined),
            child: const Text('Decline'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(dialog, _BankResult.approved),
            child: const Text('Approve'),
          ),
        ],
      ),
    );
    if (!mounted || result == null) return;
    setState(
      () => session.setPending(event.name, result == _BankResult.pending),
    );
    switch (result) {
      case _BankResult.approved:
        _confirm();
      case _BankResult.declined:
        final backToEvent = await openScreen<bool>(
          context,
          PaymentIncomplete(event: event),
        );
        if (mounted && backToEvent == true) Navigator.pop(context);
      case _BankResult.pending:
        break;
    }
  }

  void _confirm() {
    final reference = widget.session.issueTicket(widget.event.name);
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(
        builder: (_) => TicketConfirmed(
          event: widget.event,
          reference: reference,
          onDone: widget.onDone,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final event = widget.event;
    final pending = widget.session.isPending(event.name);
    return CampusPage(
      title: 'Ticket checkout',
      children: [
        SectionHeading(
          'Review your ticket',
          subtitle: '${event.name} · ${event.date}',
        ),
        CampusCard(
          title: '1 student ticket',
          subtitle: event.price,
          children: [
            const Text('Fees · RM0.00'),
            const Divider(height: 1),
            Text(
              'Total · ${event.free ? 'RM0.00' : event.price}',
              style: const TextStyle(fontWeight: FontWeight.w700),
            ),
          ],
        ),
        if (!event.free)
          const CampusCard(
            title: 'Payment method',
            subtitle: 'Online banking · Demo',
            icon: Icons.account_balance_outlined,
          ),
        if (pending) ...[
          const CampusCard(
            title: 'Payment pending',
            subtitle: 'A new payment is locked while the bank is processing this one.',
            icon: Icons.hourglass_top,
          ),
          CampusAction('Check payment status', _pay),
        ] else
          CampusAction(
            event.free ? 'Confirm free ticket' : 'Pay ${event.price}',
            _pay,
          ),
        CampusAction(
          'Cancel and return to event',
          () => Navigator.pop(context),
          secondary: true,
        ),
      ],
    );
  }
}

class PaymentIncomplete extends StatelessWidget {
  const PaymentIncomplete({required this.event, super.key});

  final CampusEvent event;

  @override
  Widget build(BuildContext context) => CampusPage(
    title: 'Payment status',
    children: [
      const SectionHeading(
        'Payment incomplete',
        subtitle:
            'The simulated bank declined the payment. No ticket was issued.',
      ),
      CampusCard(
        title: event.name,
        subtitle: '1 student ticket · ${event.price}',
        icon: Icons.info_outline,
      ),
      CampusAction('Return to checkout', () => Navigator.pop(context, false)),
      CampusAction(
        'Back to event',
        () => Navigator.pop(context, true),
        secondary: true,
      ),
    ],
  );
}

class TicketConfirmed extends StatelessWidget {
  const TicketConfirmed({
    required this.event,
    required this.reference,
    required this.onDone,
    super.key,
  });

  final CampusEvent event;
  final String reference;
  final VoidCallback onDone;

  @override
  Widget build(BuildContext context) => CampusPage(
    title: 'Your ticket',
    children: [
      SectionHeading(
        'Ticket confirmed',
        subtitle: event.free
            ? 'Free student ticket'
            : 'Demo payment approved · ${event.price}',
      ),
      CampusCard(
        title: event.name,
        subtitle: '${event.date} · ${event.time}\n${event.location}',
        icon: Icons.confirmation_number_outlined,
        children: [
          Text(
            'Ticket reference: $reference',
            style: const TextStyle(fontWeight: FontWeight.w700),
          ),
          const Text('Show the ticket reference at entry.'),
        ],
      ),
      CampusAction('Back to events', onDone),
    ],
  );
}
