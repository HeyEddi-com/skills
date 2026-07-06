
# Firebase client pattern

```dart
// lib/repositories/firestore_users_repository.dart
import 'package:cloud_firestore/cloud_firestore.dart';

class FirestoreUsersRepository {
  FirestoreUsersRepository({FirebaseFirestore? firestore})
      : _firestore = firestore ?? FirebaseFirestore.instance;

  final FirebaseFirestore _firestore;

  Stream<List<Map<String, dynamic>>> watchUsers() {
    return _firestore.collection('users').snapshots().map(
          (snap) => snap.docs.map((d) => {...d.data(), 'id': d.id}).toList(),
        );
  }
}
```

Use emulators in debug:

```dart
await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
FirebaseFirestore.instance.useFirestoreEmulator('127.0.0.1', 8080);
```
