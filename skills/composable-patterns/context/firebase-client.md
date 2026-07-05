
# Firebase client composable pattern

```ts
// useFirestoreCollection.ts — rules-aware reads
import { collection, onSnapshot, query, where } from "firebase/firestore";
import { useFirebase } from "./useFirebase";

export function useFirestoreCollection<T>(name: string, ownerId: string) {
  const { db, user } = useFirebase();
  const items = ref<T[]>([]);
  watchEffect((onCleanup) => {
    if (!user.value) return;
    const q = query(collection(db, name), where("ownerId", "==", ownerId));
    const unsub = onSnapshot(q, (snap) => {
      items.value = snap.docs.map((d) => ({ id: d.id, ...d.data() }) as T);
    });
    onCleanup(unsub);
  });
  return { items };
}
```
