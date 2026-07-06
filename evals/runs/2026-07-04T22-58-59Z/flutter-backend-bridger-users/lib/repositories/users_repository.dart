import 'package:dio/dio.dart';

import '../models/api_models.dart';
import '../services/api_client.dart';

const _demoUsers = [
  User(id: 'demo-1', email: 'demo@example.com'),
];

class UsersRepository {
  UsersRepository({ApiClient? client}) : _client = client ?? ApiClient();

  final ApiClient _client;

  Future<List<User>> fetchUsers() async {
    try {
      final response = await _client.dio.get<List<dynamic>>('/api/users');
      final list = response.data ?? [];
      return list
          .map((e) => User.fromJson(e as Map<String, dynamic>))
          .toList();
    } on DioException {
      return _demoUsers;
    }
  }
}
