import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../domain/models/server_config.dart';

class ServerDetailScreen extends ConsumerStatefulWidget {
  final String serverId;
  final ServerConfig server;

  const ServerDetailScreen({
    super.key,
    required this.serverId,
    required this.server,
  });

  @override
  ConsumerState<ServerDetailScreen> createState() => _ServerDetailScreenState();
}

class _ServerDetailScreenState extends ConsumerState<ServerDetailScreen> {
  final TextEditingController _commandController = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  // Mock console logs
  final List<String> _consoleLogs = [
    '[INFO] RCON Connection Established.',
    '[INFO] Authenticated successfully.',
    '[INFO] Server version: 1.20.4',
    '[INFO] 3 players currently online.',
  ];

  @override
  void dispose() {
    _commandController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  void _sendCommand(String cmd) {
    if (cmd.isEmpty) return;
    setState(() {
      _consoleLogs.add('> $cmd');
      _consoleLogs.add('[Mock Response] Command executed: $cmd');
    });
    _commandController.clear();

    // Auto-scroll to bottom
    Future.delayed(const Duration(milliseconds: 100), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 200),
          curve: Curves.easeOut,
        );
      }
    });
  }

  Widget _buildActionButtons() {
    if (widget.server.gameType == 'Minecraft') {
      return Wrap(
        spacing: 8.0,
        runSpacing: 8.0,
        children: [
          ActionChip(
            label: const Text('Kick Player'),
            avatar: const Icon(Icons.person_remove, size: 16),
            onPressed: () => _sendCommand('kick <player>'),
          ),
          ActionChip(
            label: const Text('Ban Player'),
            avatar: const Icon(Icons.block, size: 16),
            onPressed: () => _sendCommand('ban <player>'),
          ),
          ActionChip(
            label: const Text('Time Set Day'),
            avatar: const Icon(Icons.wb_sunny, size: 16),
            onPressed: () => _sendCommand('time set day'),
          ),
          ActionChip(
            label: const Text('Weather Clear'),
            avatar: const Icon(Icons.cloud_off, size: 16),
            onPressed: () => _sendCommand('weather clear'),
          ),
          ActionChip(
            label: const Text('Save-All'),
            avatar: const Icon(Icons.save, size: 16),
            onPressed: () => _sendCommand('save-all'),
          ),
        ],
      );
    } else if (widget.server.gameType == 'Palworld') {
      return Wrap(
        spacing: 8.0,
        runSpacing: 8.0,
        children: [
          ActionChip(
            label: const Text('Broadcast'),
            avatar: const Icon(Icons.campaign, size: 16),
            onPressed: () => _sendCommand('Broadcast <message>'),
          ),
          ActionChip(
            label: const Text('Save'),
            avatar: const Icon(Icons.save, size: 16),
            onPressed: () => _sendCommand('Save'),
          ),
          ActionChip(
            label: const Text('Show Players'),
            avatar: const Icon(Icons.people, size: 16),
            onPressed: () => _sendCommand('ShowPlayers'),
          ),
          ActionChip(
            label: const Text('Kick Player'),
            avatar: const Icon(Icons.person_remove, size: 16),
            onPressed: () => _sendCommand('KickPlayer <steamid>'),
          ),
          ActionChip(
            label: const Text('Ban Player'),
            avatar: const Icon(Icons.block, size: 16),
            onPressed: () => _sendCommand('BanPlayer <steamid>'),
          ),
          ActionChip(
            label: const Text('Shutdown'),
            avatar: const Icon(Icons.power_settings_new, size: 16),
            onPressed: () => _sendCommand('Shutdown 10 <message>'),
          ),
        ],
      );
    }
    return const SizedBox.shrink();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.server.name),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/dashboard'),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Server Info Header
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Row(
                  children: [
                    Icon(
                      widget.server.gameType == 'Minecraft' ? Icons.terrain : Icons.pets,
                      size: 40,
                      color: Theme.of(context).colorScheme.primary,
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            widget.server.name,
                            style: Theme.of(context).textTheme.titleLarge,
                          ),
                          Text('${widget.server.gameType} • ${widget.server.ip}:${widget.server.port}'),
                        ],
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      decoration: BoxDecoration(
                        color: widget.server.isOnline ? Colors.green.shade100 : Colors.red.shade100,
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Text(
                        widget.server.isOnline ? 'ONLINE' : 'OFFLINE',
                        style: TextStyle(
                          color: widget.server.isOnline ? Colors.green.shade800 : Colors.red.shade800,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Quick Actions
            Text('Quick Actions', style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 8),
            _buildActionButtons(),
            const SizedBox(height: 16),

            // Console Terminal
            Text('RCON Console', style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 8),
            Expanded(
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.black87,
                  borderRadius: BorderRadius.circular(8),
                ),
                padding: const EdgeInsets.all(8.0),
                child: ListView.builder(
                  controller: _scrollController,
                  itemCount: _consoleLogs.length,
                  itemBuilder: (context, index) {
                    final log = _consoleLogs[index];
                    final isCommand = log.startsWith('>');
                    return Padding(
                      padding: const EdgeInsets.symmetric(vertical: 2.0),
                      child: Text(
                        log,
                        style: TextStyle(
                          color: isCommand ? Colors.yellow : Colors.greenAccent,
                          fontFamily: 'monospace',
                          fontSize: 14,
                        ),
                      ),
                    );
                  },
                ),
              ),
            ),
            const SizedBox(height: 8),

            // Custom Command Input
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _commandController,
                    decoration: const InputDecoration(
                      hintText: 'Enter custom RCON command...',
                      border: OutlineInputBorder(),
                      contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                    ),
                    onSubmitted: _sendCommand,
                  ),
                ),
                const SizedBox(width: 8),
                IconButton.filled(
                  icon: const Icon(Icons.send),
                  onPressed: () => _sendCommand(_commandController.text),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
