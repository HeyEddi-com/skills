// Generated stub from OpenAPI — refine types as needed.
// Source: /home/eddi/Projects/heyeddi/skills/evals/runs/2026-07-04T22-58-59Z/flutter-backend-bridger-users/openapi.json

class User {
  const User({
    required this.id,
    required this.email,
  });

  final String? id;
  final String? email;

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as String?,
      email: json['email'] as String?,
    );
  }
}
