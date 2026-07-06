
# FastAPI + Dio pattern

```dart
// lib/repositories/users_repository.dart
import '../models/api_models.dart';
import '../services/api_client.dart';

class UsersRepository {
  UsersRepository({ApiClient? client}) : _client = client ?? ApiClient();
  final ApiClient _client;

  Future<List<User>> fetchUsers() async {
    final data = await _client.getJson('/api/users');
    final list = data['items'] as List<dynamic>? ?? [];
    return list.map((e) => User.fromJson(e as Map<String, dynamic>)).toList();
  }
}
```

```dart
// lib/providers/users_provider.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../repositories/users_repository.dart';
import '../models/api_models.dart';

final usersRepositoryProvider = Provider((ref) => UsersRepository());

final usersProvider = FutureProvider<List<User>>((ref) async {
  return ref.watch(usersRepositoryProvider).fetchUsers();
});
```

Attach JWT in `ApiClient` interceptor when auth is required — refresh on 401.
