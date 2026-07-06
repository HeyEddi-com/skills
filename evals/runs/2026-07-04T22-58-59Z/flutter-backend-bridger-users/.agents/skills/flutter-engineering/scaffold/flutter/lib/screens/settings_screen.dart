import 'package:flutter/material.dart';

import '../widgets/app_shell.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return AppShell(
      title: 'Settings',
      child: ListView(
        padding: const EdgeInsets.all(24),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Profile', style: Theme.of(context).textTheme.titleMedium),
                  const SizedBox(height: 12),
                  TextField(
                    decoration: const InputDecoration(labelText: 'Display name'),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: SwitchListTile(
                contentPadding: EdgeInsets.zero,
                title: const Text('Email notifications'),
                value: true,
                onChanged: (_) {},
              ),
            ),
          ),
          const SizedBox(height: 24),
          Align(
            alignment: Alignment.centerRight,
            child: FilledButton(
              onPressed: () {},
              child: const Text('Save changes'),
            ),
          ),
        ],
      ),
    );
  }
}
