import { computed, ref, watch } from "vue";
import { messages, type Locale, type MessageTree } from "@/i18n/messages";

const STORAGE_KEY = "taskflow-locale";

function detectLocale(): Locale {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored === "en" || stored === "es") return stored;
  const lang = navigator.language.toLowerCase();
  if (lang.startsWith("es")) return "es";
  return "en";
}

const locale = ref<Locale>(detectLocale());

watch(
  locale,
  (value) => {
    localStorage.setItem(STORAGE_KEY, value);
    document.documentElement.lang = value;
  },
  { immediate: true },
);

export function useLocale() {
  const t = computed<MessageTree>(() => messages[locale.value]);

  function setLocale(next: Locale) {
    locale.value = next;
  }

  return { locale, t, setLocale };
}
