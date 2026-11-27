import 'package:material_ui/material_ui.dart';

import 'campus_theme.dart';
import 'home.dart';

void main() => runApp(const CampusApp());

class CampusApp extends StatelessWidget {
  const CampusApp({super.key});

  @override
  Widget build(BuildContext context) => MaterialApp(
    title: 'Smart Campus Companion',
    debugShowCheckedModeBanner: false,
    theme: campusTheme,
    home: const SignInScreen(),
  );
}
