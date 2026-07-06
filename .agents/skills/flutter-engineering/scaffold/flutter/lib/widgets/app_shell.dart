import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class AppShell extends StatelessWidget {
  const AppShell({super.key, required this.title, required this.child});

  final String title;
  final Widget child;

  @override
  Widget build(BuildContext context) {
    final location = GoRouterState.of(context).uri.path;
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      drawer: NavigationDrawer(
        selectedIndex: location == '/settings' ? 1 : 0,
        onDestinationSelected: (index) {
          Navigator.pop(context);
          context.go(index == 1 ? '/settings' : '/');
        },
        children: const [
          NavigationDrawerDestination(
            icon: Icon(Icons.home_outlined),
            selectedIcon: Icon(Icons.home),
            label: Text('Home'),
          ),
          NavigationDrawerDestination(
            icon: Icon(Icons.settings_outlined),
            selectedIcon: Icon(Icons.settings),
            label: Text('Settings'),
          ),
        ],
      ),
      body: child,
    );
  }
}
