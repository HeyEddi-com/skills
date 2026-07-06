import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../providers/users_provider.dart';
import '../widgets/app_shell.dart';

class SettingsScreen extends ConsumerWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final usersAsync = ref.watch(usersProvider);

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
                  Text('Users', style: Theme.of(context).textTheme.titleMedium),
                  const SizedBox(height: 12),
                  usersAsync.when(
                    loading: () => const Center(child: CircularProgressIndicator()),
                    error: (_, __) => const Text('No users available'),
                    data: (users) {
                      if (users.isEmpty) {
                        return const Text('No users yet');
                      }
                      return Column(
                        children: [
                          for (final user in users)
                            ListTile(
                              contentPadding: EdgeInsets.zero,
                              leading: const Icon(Icons.person_outline),
                              title: Text(user.email ?? 'Unknown'),
                              subtitle: Text(user.id ?? ''),
                            ),
                        ],
                      );
                    },
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
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
