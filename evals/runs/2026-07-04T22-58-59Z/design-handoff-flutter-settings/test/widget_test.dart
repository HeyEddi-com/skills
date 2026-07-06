import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:heyeddi_app/app.dart';

void main() {
  testWidgets('app renders home', (tester) async {
    await tester.pumpWidget(const HeyEddiApp());
    await tester.pumpAndSettle();
    expect(find.text('TaskFlow Mobile'), findsOneWidget);
  });
}
