"""Unit tests for PrimeVue Card slot verification in design-handoff."""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "skills" / "design-handoff" / "scripts"))

from verify_handoff import find_primevue_card_slot_issues  # noqa: E402


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
