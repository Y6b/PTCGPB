import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:app/main.dart';

void main() {
  testWidgets('RCON Manager starts up', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const ProviderScope(child: RconManagerApp()));

    // Verify that our title is present.
    expect(find.text('RCON Manager'), findsOneWidget);
  });
}
