"""Unit tests for PrimeVue Card slot verification in heyeddi-handoff."""
from __future__ import annotations

from _skill_loader import load_skill_script

_vh = load_skill_script("heyeddi-handoff", "verify_handoff")
find_primevue_card_slot_issues = _vh.find_primevue_card_slot_issues


GOOD_CARD = """
<Card class="settings__card">
  <template #title>Profile</template>
  <template #subtitle>Hint</template>
  <template #content>
    <div class="settings__fields">
      <InputText v-model="name" />
    </div>
  </template>
</Card>
"""

BAD_CARD = """
<Card class="settings__card">
  <template #title>Profile</template>
  <template #subtitle>Hint</template>
  <div class="settings__fields">
    <InputText v-model="name" />
  </div>
</Card>
"""

TITLE_ONLY_CARD = """
<Card>
  <template #title>Profile</template>
  <template #subtitle>Hint</template>
</Card>
"""


def test_good_card_has_no_issues() -> None:
    assert find_primevue_card_slot_issues(GOOD_CARD) == []


def test_bad_card_without_content_slot() -> None:
    issues = find_primevue_card_slot_issues(BAD_CARD, source="SettingsView.vue")
    assert len(issues) == 1
    assert "template #content" in issues[0]["message"]


def test_title_only_card_is_ok() -> None:
    assert find_primevue_card_slot_issues(TITLE_ONLY_CARD) == []
