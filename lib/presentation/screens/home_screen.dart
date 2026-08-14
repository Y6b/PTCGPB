import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../theme/app_theme.dart';
import '../../domain/models/server_config.dart';

// Mock Data
final mockServers = [
  ServerConfig(id: '1', name: 'Survival SMP', gameType: 'Minecraft', ip: '192.168.1.100', port: 25575),
  ServerConfig(id: '2', name: 'Palworld Hub', gameType: 'Palworld', ip: '192.168.1.101', port: 25575),
  ServerConfig(id: '3', name: 'Modded Realm', gameType: 'Minecraft', ip: '192.168.1.102', port: 25575, isOnline: false),
];

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final themeMode = ref.watch(themeModeProvider);
    final isDark = themeMode == ThemeMode.dark ||
        (themeMode == ThemeMode.system && MediaQuery.platformBrightnessOf(context) == Brightness.dark);

    return Scaffold(
      appBar: AppBar(
        title: const Text('My Servers'),
        leading: IconButton(
          icon: const Icon(Icons.logout),
          onPressed: () => context.go('/'),
          tooltip: 'Sign Out',
        ),
        actions: [
          IconButton(
            icon: Icon(isDark ? Icons.light_mode : Icons.dark_mode),
            onPressed: () {
              ref.read(themeModeProvider.notifier).toggleTheme();
            },
            tooltip: 'Toggle Theme',
          ),
        ],
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16.0),
        itemCount: mockServers.length,
        itemBuilder: (context, index) {
          final server = mockServers[index];
          return Card(
            elevation: 2,
            margin: const EdgeInsets.only(bottom: 16),
            child: ListTile(
              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              leading: CircleAvatar(
                backgroundColor: server.gameType == 'Minecraft' ? Colors.green.shade700 : Colors.blue.shade700,
                child: Icon(
                  server.gameType == 'Minecraft' ? Icons.terrain : Icons.pets,
                  color: Colors.white,
                ),
              ),
              title: Text(server.name, style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 4),
                  Text('${server.gameType} • ${server.ip}:${server.port}'),
                  const SizedBox(height: 4),
                  Row(
                    children: [
                      Container(
                        width: 10,
                        height: 10,
                        decoration: BoxDecoration(
                          color: server.isOnline ? Colors.green : Colors.red,
                          shape: BoxShape.circle,
                        ),
                      ),
                      const SizedBox(width: 8),
                      Text(server.isOnline ? 'Online' : 'Offline'),
                    ],
                  ),
                ],
              ),
              trailing: const Icon(Icons.chevron_right),
              onTap: () {
                context.go('/server/${server.id}');
              },
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          // Mock action
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Add server dialog would open here')),
          );
        },
        icon: const Icon(Icons.add),
        label: const Text('Add Server'),
      ),
    );
  }
}
