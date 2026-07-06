import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/api_models.dart';
import '../repositories/users_repository.dart';

final usersRepositoryProvider = Provider((ref) => UsersRepository());

final usersProvider = FutureProvider<List<User>>((ref) async {
  return ref.watch(usersRepositoryProvider).fetchUsers();
});
