"""Synthetic observation tests, not a native Stonescript parser/render test."""
from pathlib import Path
import re
from types import SimpleNamespace
import tempfile
import unittest

from stonescript_policy_harness import Foe, load_module

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "scripts/rocky/main.txt"


class PerfectedTraceTests(unittest.TestCase):
    def setUp(self):
        self.main = MAIN.read_text()
        fields = "\n".join(line for line in self.main.splitlines() if line.startswith("var rayTrace"))
        observe = self.main.split("func ObservePerfectedTrace(", 1)[1].split("func DrawPerfectedTrace()", 1)[0]
        self.native = dict(foe=Foe(), totaltime=0)
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "trace.txt"
            source.write_text(fields + "\nfunc ObservePerfectedTrace(" + observe)
            self.trace = load_module(source, self.native)
        self.globals = type(self.trace).ObservePerfectedTrace.__globals__

    def frame(self, state=32, elapsed=0, total=100, target="dysangelos phase3", rocky=True):
        foe = Foe(target)
        foe.state, foe.time = state, elapsed
        self.globals.update(foe=foe, totaltime=total)
        self.trace.ObservePerfectedTrace(rocky)

    def test_live_state_time_and_last_transition_hold(self):
        self.frame(state=32, elapsed=12)
        self.assertTrue(self.trace.rayTraceActive)
        self.assertEqual(str(self.trace.rayTraceTransition), "entry 32:12 @100")
        self.frame(state=32, elapsed=13, total=101)
        self.assertEqual(self.trace.rayTraceTime, 13)
        self.assertEqual(str(self.trace.rayTraceTransition), "entry 32:12 @100")
        self.frame(state=115, elapsed=0, total=102)
        self.assertEqual(str(self.trace.rayTraceTransition), "prev 32:13 -> 115:0 @102")
        self.frame(state=115, elapsed=61, total=163)
        self.assertEqual(self.trace.rayTraceTime, 61)
        self.assertEqual(str(self.trace.rayTraceTransition), "prev 32:13 -> 115:0 @102")
        self.frame(state=2, elapsed=0, total=164)
        self.assertTrue(self.trace.rayTraceAfter115)
        self.assertEqual(str(self.trace.rayTraceTransition), "prev 115:61 -> 2:0 @164")
        self.frame(state=32, elapsed=0, total=165)
        self.assertFalse(self.trace.rayTraceAfter115)

    def test_timer_restart_same_state_is_observed_without_attack_assumptions(self):
        self.frame(state=115, elapsed=20)
        self.frame(state=115, elapsed=0, total=101)
        self.assertEqual(str(self.trace.rayTraceTransition), "prev 115:20 -> 115:0 @101")

    def test_only_perfected_in_rocky_context_and_reentry_resets_history(self):
        for target, rocky in [("acronian_scout", True), ("dysangelos phase1", True),
                              ("dysangelos phase2", True), ("", True),
                              ("other_foe phase3", True), ("dysangelos phase3", False)]:
            self.frame(state=115, elapsed=10)
            self.frame(target=target, rocky=rocky)
            self.assertFalse(self.trace.rayTraceActive)
            self.frame(state=32, elapsed=5, total=200)
            self.assertEqual(str(self.trace.rayTraceTransition), "entry 32:5 @200")
            self.assertFalse(self.trace.rayTraceAfter115)
        self.frame(target="dysangelos_perfected", state=115)
        self.assertTrue(self.trace.rayTraceActive)

    def test_observer_has_no_equipment_ability_or_gameplay_writes(self):
        observer = self.main.split("func ObservePerfectedTrace(", 1)[1].split("func DrawRockyCandidate()", 1)[0]
        self.assertNotRegex(observer, r"(?m)^\s*(?:equip\w* |activate |loadout |brew |disable |enable )")
        code_only = "\n".join(line for line in observer.splitlines() if not line.lstrip().startswith(">"))
        self.assertNotRegex(code_only, r"(?:gear|rocky|combat|equipment|metrics|item)\.")
        for line in observer.splitlines():
            if re.match(r"^  [A-Za-z]\w* =", line):
                self.assertTrue(line.strip().startswith("rayTrace"), line)
        self.assertNotIn("item.GetCount", observer)
        self.assertNotIn("item.GetCooldown", observer)

    def test_diagnostics_gate_scope_and_top_rows(self):
        tail = self.main.split("metrics.Observe()", 1)[1]
        self.assertRegex(tail, r'\?config.showDiagnostics & rockyConfig.showDiagnostics\s+ObservePerfectedTrace\(string.Equals\(locations.handler, "rocky"\) & loc.stars = rockyConfig.targetStars & rockyConfig.enabled\)\s+DrawRockyCandidate\(\)\s+DrawPerfectedTrace\(\)\s+:\s+rayTraceActive = false')
        draw = self.main.split("func DrawPerfectedTrace()", 1)[1].split("func DrawRockyCandidate()", 1)[0]
        self.assertIn('?!rayTraceActive', draw)
        self.assertIn('0,0,#red,R15 P3 *115*', draw)
        self.assertIn('0,0,#yellow,R15 P3 AFTER 115', draw)
        self.assertIn('0,1,#white,Last:', draw)
        self.assertIn('@rayTraceState@', draw)
        self.assertIn('@rayTraceTime@', draw)
        self.assertNotRegex(draw, r'foe.time\s*[<>]')


if __name__ == "__main__":
    unittest.main()
