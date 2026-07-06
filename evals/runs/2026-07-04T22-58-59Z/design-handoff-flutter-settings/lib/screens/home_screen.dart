import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../widgets/app_shell.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return AppShell(
      title: 'Home',
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('TaskFlow Mobile', style: Theme.of(context).textTheme.headlineMedium),
            const SizedBox(height: 16),
            FilledButton(
              onPressed: () => context.go('/settings'),
              child: const Text('Open settings'),
            ),
          ],
        ),
      ),
    );
  }
}
