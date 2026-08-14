class ServerConfig {
  final String id;
  final String name;
  final String gameType; // e.g. "Minecraft", "Palworld"
  final String ip;
  final int port;
  final bool isOnline; // For mock status

  const ServerConfig({
    required this.id,
    required this.name,
    required this.gameType,
    required this.ip,
    required this.port,
    this.isOnline = true,
  });
}
