<template>
  <div class="home">
    <section class="home__hero">
      <p class="home__eyebrow">{{ t.brand.name }}</p>
      <h1 class="home__headline">{{ t.home.heroHeadline }}</h1>
      <p class="home__sub">{{ t.home.heroSub }}</p>
      <div class="home__actions">
        <RouterLink to="/login">
          <Button :label="t.home.ctaPrimary" size="large" />
        </RouterLink>
        <a class="home__secondary" href="#features">{{ t.home.ctaSecondary }}</a>
      </div>
    </section>

    <section id="features" class="home__features" :aria-label="t.brand.features">
      <article v-for="feature in features" :key="feature.title" class="home__feature-card">
        <span class="home__feature-icon" aria-hidden="true">{{ feature.icon }}</span>
        <h2 class="home__feature-title">{{ feature.title }}</h2>
        <p class="home__feature-body">{{ feature.body }}</p>
      </article>
    </section>

    <section class="home__proof">
      <p>{{ t.home.proof }}</p>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import Button from "primevue/button";
import { useLocale } from "@/composables/useLocale";

const { t } = useLocale();

const features = computed(() => [
  { icon: "◎", title: t.value.home.feature1Title, body: t.value.home.feature1Body },
  { icon: "⚑", title: t.value.home.feature2Title, body: t.value.home.feature2Body },
  { icon: "◫", title: t.value.home.feature3Title, body: t.value.home.feature3Body },
]);
</script>

<style scoped>
.home {
  background: var(--hero-glow);
}

.home__hero {
  max-width: var(--content-max);
  margin: 0 auto;
  padding: var(--size-8) var(--size-4) var(--size-7);
  text-align: center;
}

.home__eyebrow {
  margin: 0 0 var(--size-3);
  font-size: var(--font-size-1);
  font-weight: var(--font-weight-6);
  color: var(--brand);
  letter-spacing: var(--font-letterspacing-1);
  text-transform: uppercase;
}

.home__headline {
  margin: 0 0 var(--size-4);
  font-family: var(--font-display);
  font-size: var(--text-display);
  font-weight: var(--font-weight-8);
  line-height: var(--font-lineheight-0);
  letter-spacing: var(--font-letterspacing-0);
  max-width: 18ch;
  margin-inline: auto;
}

.home__sub {
  margin: 0 auto var(--size-6);
  max-width: 42rem;
  color: var(--text-2);
  font-size: var(--font-size-2);
}

.home__actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--size-3);
}

.home__secondary {
  color: var(--text-2);
  font-size: var(--font-size-1);
}

.home__features {
  max-width: var(--content-max);
  margin: 0 auto;
  padding: 0 var(--size-4) var(--size-7);
  display: grid;
  gap: var(--size-4);
  grid-template-columns: 1fr;
}

.home__feature-card {
  background: var(--surface-2);
  border: 1px solid var(--border-1);
  border-radius: var(--radius-card);
  padding: var(--size-5);
  box-shadow: 0 1px 2px light-dark(rgb(0 0 0 / 0.04), rgb(0 0 0 / 0.2));
}

.home__feature-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: var(--size-7);
  height: var(--size-7);
  border-radius: var(--radius-round);
  background: var(--brand-subtle);
  color: var(--brand);
  font-size: var(--font-size-3);
  margin-bottom: var(--size-3);
}

.home__feature-title {
  margin: 0 0 var(--size-2);
  font-size: var(--font-size-3);
  font-weight: var(--font-weight-7);
}

.home__feature-body {
  margin: 0;
  color: var(--text-2);
}

.home__proof {
  max-width: var(--content-max);
  margin: 0 auto;
  padding: 0 var(--size-4) var(--size-8);
  text-align: center;
}

.home__proof p {
  margin: 0;
  padding: var(--size-4) var(--size-5);
  border-radius: var(--radius-card);
  border: 1px solid var(--border-1);
  background: light-dark(var(--surface-0), var(--surface-2));
  color: var(--text-2);
}

@media (min-width: 768px) {
  .home__features {
    grid-template-columns: repeat(3, 1fr);
  }

  .home__actions {
    flex-direction: row;
    justify-content: center;
  }
}
</style>
