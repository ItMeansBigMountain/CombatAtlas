import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "newsletter_batch_upload.py"
spec = importlib.util.spec_from_file_location("newsletter_batch_upload", MODULE_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def stoic_source():
    return {
        "from": "Daily Stoic <info@dailystoic.com>",
        "subject": "You Can’t Stop Here",
        "snippet": "Marcus Aurelius kept returning to Epictetus.",
        "body": (
            "When Junius Rusticus handed the future emperor of Rome a book, it came with an implication. "
            "A true philosopher could not be satisfied just getting the gist of something. "
            "Marcus Aurelius went over Epictetus again and again until it seeped into his soul. "
            "Meditations repeats the same ideas on anger, difficult people, death, and duty—not because "
            "Marcus had mastered them, but because he had not. Epictetus taught that true freedom comes "
            "from recognizing what lies beyond our control and focusing only on what is up to us."
        ),
    }


class RetentionScriptTests(unittest.TestCase):
    def test_stoic_script_opens_with_specific_tension_and_has_a_payoff(self):
        narration = module.build_script(stoic_source())["narration"]
        first_sentence = narration.split(".", 1)[0]
        self.assertIn("Marcus Aurelius", first_sentence)
        self.assertTrue(any(word in first_sentence.lower() for word in ("failed", "couldn't", "wasn't", "never")))
        self.assertIn("not because", narration.lower())
        self.assertIn("but because", narration.lower())

    def test_script_removes_pipeline_boilerplate_and_fake_transitions(self):
        narration = module.build_script(stoic_source())["narration"].lower()
        banned = (
            "this one lands quietly", "the reason it works is simple", "then the email",
            "what makes it hit harder", "by the end", "the point is not loud",
            "this newsletter", "this email", "the receipt", "the signal",
        )
        self.assertFalse(any(phrase in narration for phrase in banned))

    def test_scene_duration_guard_rejects_silence_or_corrupt_tts(self):
        self.assertTrue(module.scene_audio_too_long("A short sentence with only a few words.", 77.0))
        self.assertFalse(module.scene_audio_too_long("A short sentence with only a few words.", 5.0))

    def test_retention_beats_are_short_specific_and_not_generic_labels(self):
        script = module.build_script(stoic_source())
        self.assertGreaterEqual(len(script["beats"]), 5)
        self.assertLessEqual(len(script["beats"]), 8)
        self.assertTrue(all(len(spoken.split()) <= 35 for _, spoken in script["beats"]))
        generic = {"YOU MISSED THIS", "NOT THE HEADLINE", "WATCH THE SHIFT", "THE REAL SIGNAL", "FOLLOW THE MONEY", "THE RECEIPT", "WHY IT MATTERS", "YOUR MOVE"}
        self.assertFalse(any(caption in generic for caption, _ in script["beats"]))


if __name__ == "__main__":
    unittest.main()
