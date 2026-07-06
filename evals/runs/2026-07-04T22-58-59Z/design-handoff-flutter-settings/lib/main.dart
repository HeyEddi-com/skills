import 'package:flutter/material.dart';

import 'app.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  // HeyEddiApp wires theme: AppTheme.light, darkTheme: AppTheme.dark on MaterialApp.router
  runApp(const HeyEddiApp());
}
