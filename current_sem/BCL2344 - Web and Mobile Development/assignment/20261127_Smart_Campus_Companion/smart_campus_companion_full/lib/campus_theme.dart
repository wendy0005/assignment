import 'package:material_ui/material_ui.dart';

const navy = Color(0xFF173D57);
const ink = Color(0xFF26384A);
const muted = Color(0xFF4B5B68);
const border = Color(0xFFBBC7D2);
const canvas = Color(0xFFF7F9FC);

final campusTheme = ThemeData(
  colorScheme: ColorScheme.fromSeed(seedColor: navy, primary: navy),
  scaffoldBackgroundColor: canvas,
  appBarTheme: const AppBarTheme(
    backgroundColor: canvas,
    foregroundColor: ink,
    scrolledUnderElevation: 0,
  ),
  outlinedButtonTheme: OutlinedButtonThemeData(
    style: OutlinedButton.styleFrom(
      minimumSize: const Size(0, 48),
      side: const BorderSide(color: border),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
    ),
  ),
);
