import 'package:material_ui/material_ui.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:smart_campus_companion/main.dart';

void main() {
  testWidgets('weekday selection changes the date and class cards', (
    tester,
  ) async {
    await tester.pumpWidget(const CampusApp());
    expect(find.text('Monday, 26 October'), findsOneWidget);
    expect(find.text('Database Fundamentals'), findsOneWidget);

    await tester.tap(find.text('Tue'));
    await tester.pumpAndSettle();
    expect(find.text('Tuesday, 27 October'), findsOneWidget);
    expect(find.text('Operating Systems'), findsOneWidget);
    expect(find.text('Database Fundamentals'), findsNothing);

    await tester.tap(find.text('Fri'));
    await tester.pumpAndSettle();
    expect(find.text('Friday, 30 October'), findsOneWidget);
    expect(find.text('No classes scheduled for this day.'), findsOneWidget);
  });

  testWidgets('Lab 2 opens and closes without changing the day', (
    tester,
  ) async {
    await tester.pumpWidget(const CampusApp());
    await tester.tap(find.text('Thu'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Find Lab 2 on map'));
    await tester.pumpAndSettle();
    expect(find.text('Campus map'), findsOneWidget);
    expect(find.text('Gate A'), findsOneWidget);

    await tester.tap(find.text('Done'));
    await tester.pumpAndSettle();
    expect(find.text('Campus map'), findsNothing);
    expect(find.text('Thursday, 29 October'), findsOneWidget);
  });

  testWidgets(
    'narrow screen with enlarged text keeps all weekday controls reachable',
    (tester) async {
      tester.view.devicePixelRatio = 1;
      tester.view.physicalSize = const Size(320, 580);
      tester.platformDispatcher.textScaleFactorTestValue = 2;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      addTearDown(tester.platformDispatcher.clearTextScaleFactorTestValue);
      await tester.pumpWidget(const CampusApp());

      final weekdays = find.byWidgetPredicate(
        (widget) =>
            widget is Scrollable && widget.axisDirection == AxisDirection.right,
      );
      await tester.drag(weekdays, const Offset(-520, 0));
      await tester.pumpAndSettle();
      await tester.tap(find.text('Fri'));
      await tester.pumpAndSettle();

      expect(find.text('Friday, 30 October'), findsOneWidget);
      expect(tester.takeException(), isNull);
    },
  );
}
