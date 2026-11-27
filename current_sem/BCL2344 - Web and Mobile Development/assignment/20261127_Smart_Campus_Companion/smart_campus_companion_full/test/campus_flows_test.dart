import 'package:flutter_test/flutter_test.dart';
import 'package:material_ui/material_ui.dart';
import 'package:smart_campus_companion/main.dart';

Future<void> tap(WidgetTester tester, String label) async {
  final target = find.text(label);
  await tester.ensureVisible(target);
  await tester.tap(target);
  await tester.pumpAndSettle();
}

Future<void> openDemo(WidgetTester tester) async {
  await tester.pumpWidget(const CampusApp());
  await tester.pumpAndSettle();
  await tap(tester, 'Use demo account');
  await tester.tap(find.widgetWithText(FilledButton, 'Sign in'));
  await tester.pumpAndSettle();
  expect(find.text('Good morning, Aina'), findsOneWidget);
}

void main() {
  testWidgets(
    'sign in validates fields and profile sign out clears the session',
    (tester) async {
      await tester.pumpWidget(const CampusApp());
      await tester.tap(find.widgetWithText(FilledButton, 'Sign in'));
      await tester.pumpAndSettle();
      expect(find.text('Enter a valid email address.'), findsOneWidget);
      await openDemo(tester);
      await tester.tap(find.byTooltip('Profile'));
      await tester.pumpAndSettle();
      expect(find.text('Aina Rahman'), findsOneWidget);
      await tap(tester, 'Event reminders');
      expect(find.text('Off'), findsOneWidget);
      await tap(tester, 'Sign out');
      expect(find.text('Use demo account'), findsOneWidget);
    },
  );

  testWidgets('timetable links to Lab 2 and can show a step-free route', (
    tester,
  ) async {
    await openDemo(tester);
    await tap(tester, 'View timetable');
    await tap(tester, 'Find Lab 2 on map');
    expect(find.text('Block B · Lab 2'), findsOneWidget);
    await tap(tester, 'Get directions');
    expect(find.text('3 min · 210 m'), findsOneWidget);
    await tap(tester, 'Step-free');
    expect(find.text('4 min · 300 m'), findsOneWidget);
    expect(find.textContaining('Use the ramp'), findsOneWidget);
  });

  testWidgets(
    'reading an unread notice updates the inbox and links to the facility',
    (tester) async {
      await openDemo(tester);
      await tester.tap(find.byTooltip('Alerts'));
      await tester.pumpAndSettle();
      await tap(tester, 'Unread');
      await tap(tester, 'Library hours changed');
      await tap(tester, 'View Campus Library');
      expect(find.text('Facility details'), findsOneWidget);
      await tester.pageBack();
      await tester.pumpAndSettle();
      await tester.pageBack();
      await tester.pumpAndSettle();
      expect(find.text('0 unread items'), findsOneWidget);
    },
  );

  testWidgets(
    'booking conflict keeps the date and recovers with another time',
    (tester) async {
      await openDemo(tester);
      await tap(tester, 'Services');
      await tap(tester, 'Campus Library');
      await tap(tester, 'Book a study room');
      await tap(tester, '2:00 PM');
      await tap(tester, 'Confirm reservation');
      expect(find.text('2:00 PM is no longer available'), findsOneWidget);
      expect(find.text('Wednesday, 28 October'), findsOneWidget);
      expect(
        tester
            .widget<FilledButton>(
              find.widgetWithText(FilledButton, 'Confirm reservation'),
            )
            .onPressed,
        isNull,
      );
      await tap(tester, '3:00 PM');
      await tester.scrollUntilVisible(find.text('Confirm reservation'), 100);
      await tap(tester, 'Confirm reservation');
      expect(find.text('Booking reference: LIB-2841'), findsOneWidget);
      await tap(tester, 'Done');
      expect(find.text('Campus services'), findsOneWidget);
    },
  );

  testWidgets(
    'payment decline can retry, pending prevents duplicates, approval issues one ticket',
    (tester) async {
      await openDemo(tester);
      await tap(tester, 'Events');
      final paidEvent = find.widgetWithText(OutlinedButton, 'View event').first;
      await tester.ensureVisible(paidEvent);
      await tester.tap(paidEvent);
      await tester.pumpAndSettle();
      await tap(tester, 'Get ticket · RM10.00');
      await tap(tester, 'Pay RM10.00');
      await tap(tester, 'Decline');
      expect(find.text('Payment incomplete'), findsOneWidget);
      await tap(tester, 'Return to checkout');
      await tap(tester, 'Pay RM10.00');
      await tap(tester, 'Keep pending');
      expect(find.text('Pay RM10.00'), findsNothing);
      await tap(tester, 'Check payment status');
      await tap(tester, 'Approve');
      expect(find.text('Ticket reference: EVT-2916'), findsOneWidget);
      await tap(tester, 'Back to events');
      await tester.tap(paidEvent);
      await tester.pumpAndSettle();
      await tap(tester, 'View ticket');
      expect(find.text('Ticket reference: EVT-2916'), findsOneWidget);
    },
  );
}
