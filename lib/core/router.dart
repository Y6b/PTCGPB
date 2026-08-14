import 'package:go_router/go_router.dart';
import '../presentation/screens/login_screen.dart';
import '../presentation/screens/home_screen.dart'; // contains mockServers
import '../presentation/screens/server_detail_screen.dart';

final GoRouter appRouter = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const LoginScreen(),
    ),
    GoRoute(
      path: '/dashboard',
      builder: (context, state) => const HomeScreen(),
    ),
    GoRoute(
      path: '/server/:id',
      builder: (context, state) {
        final id = state.pathParameters['id']!;
        // Simple lookup from mock data for wireframe
        final server = mockServers.firstWhere(
          (s) => s.id == id,
          orElse: () => mockServers.first,
        );
        return ServerDetailScreen(serverId: id, server: server);
      },
    ),
  ],
);
