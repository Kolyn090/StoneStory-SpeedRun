"""R16 actual-source sequence tests with fake natives; no gameplay success claim."""
from pathlib import Path
import tempfile
import unittest
import test_rocky_candidate as baseline
from stonescript_policy_harness import Text, load_module

ROOT=Path(__file__).resolve().parents[1]

class R16Tests(unittest.TestCase):
    frame=baseline.PolicyTests.frame
    def setUp(self):
        baseline.PolicyTests.setUp(self)
        self.profile.dualWieldEnabled=True
        self.native['ai'].walking=True
        self.options=load_module(ROOT/'scripts/rocky_r16/config/Experiments.txt',self.native)
        self.actions=load_module(ROOT/'scripts/rocky_r16/combat/Experiments.txt',self.native)
        self.handler.experiment=self.actions
        self.items.counts.update({'cultist mask':1,'quarterstaff DashStaff':1})
        self.items.cooldowns.update(mask=0,quarterstaff=0)
        self.items.specific_ready.update(mask=True,quarterstaff=True)
        # Gear stub keeps ordinary requests separate from native protected commands.
        self.native['foe'].distance=5
        self.native['foe'].id=Text('acronian_scout')
        self.actions.Prepare(self.options)

    def step(self, target='acronian_scout', total=1, distance=5, **kwargs):
        # Existing helper creates native foe; assign distance before Tick via a wrapper.
        original=self.handler.Tick
        def tick(*args):
            foe=type(self.handler).Tick.__globals__['foe']
            foe.distance=distance
            type(self.actions).TryCombat.__globals__.update(foe=foe,hp=kwargs.get('player_hp',100),totaltime=total)
            return original(*args)
        self.handler.Tick=tick
        try:return self.frame(target,total=total,**kwargs)
        finally:self.handler.Tick=original

    def enable(self, name):
        setattr(self.options,name+'Enabled',True)
        self.actions.Prepare(self.options)

    def test_disabled_equivalence_normal_recovery_armor_and_phase_trace(self):
        base_handler=(ROOT/'scripts/rocky/locations/RockyPlateau.txt').read_text()
        # Remove only the explicitly optional hook to reconstruct the baseline policy.
        base_handler=base_handler.replace('// Optional R16 object; null keeps R15 behavior and ownership unchanged.\nvar experiment = null\n','')
        hook='  ?Type(experiment) = "object"\n    ?experiment.TryCombat(gear, equipment, bearerRecoveryActive, physicalOnly, phase)\n      attacks.ResetCycle()\n      strategy = experiment.status\n      return\n'
        self.assertIn(hook,base_handler)
        base_handler=base_handler.replace(hook,'')
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'base.txt';path.write_text(base_handler)
            original=load_module(path,self.native)
            self.assertFalse(self.options.maskEnabled)
            self.assertFalse(self.options.dashEnabled)
            for target,hp,armor,total in [('acronian_scout',100,0,1),('dysangelos phase1',40,0,2),
                                         ('dysangelos phase1',85,0,3),('dysangelos phase2 fire',100,9,4),
                                         ('dysangelos phase3',100,0,5),('',100,0,6)]:
                self.step(target,total=total,player_hp=hp,armor=armor)
                observed=(list(self.gear.calls),self.gear.lastShield,str(self.handler.phase),str(self.handler.strategy))
                for func in vars(type(original)).values():
                    if hasattr(func,'__globals__'):
                        func.__globals__.update(type(self.handler).Tick.__globals__)
                # Do not overwrite generated self bindings: globals contain only natives.
                self.gear.calls.clear()
                original.Tick(self.gear,self.settings,self.equipment,self.profile,self.combat,self.attacks)
                self.assertEqual(observed,(list(self.gear.calls),self.gear.lastShield,str(original.phase),str(original.strategy)))
        self.assertEqual(self.items.equips,[])
        self.assertEqual(self.items.activations,[])

    def test_mask_arm_activate_once_and_restore(self):
        self.enable('mask')
        self.step(total=1)
        self.assertEqual(self.items.equips,[('both','cultist mask')])
        self.assertEqual(self.gear.calls,[])
        self.assertEqual(self.items.activations,[])
        self.items.right.id=Text('cultist mask')
        # Fake item string supports the documented item.right criteria test.
        self.items.right=Text('cultist mask')
        self.items.right.id=Text('cultist mask');self.items.right.state=0
        self.step(total=2)
        self.assertEqual(self.items.activations,['R'])
        self.assertEqual(self.gear.calls,[])
        self.step(total=3)
        self.assertEqual(self.gear.calls,['fire sword'])
        self.assertIn('restored',self.actions.status)
        self.step(total=700)
        self.assertEqual(self.items.activations,['R'])

    def test_mask_cooldown_does_not_change_equipment(self):
        self.enable('mask');self.items.cooldowns['mask']=20
        self.step()
        self.assertEqual(self.items.equips,[])
        self.assertEqual(self.gear.calls,['fire sword'])

    def test_unknown_cooldown_requires_equipped_specific_eligibility(self):
        self.enable('mask');self.items.cooldowns['mask']=-1
        self.items.specific_ready['mask']=False
        self.step(total=1);self.step(total=7)
        self.assertEqual(self.items.activations,[])
        self.assertEqual(self.gear.calls,['fire sword'])
        self.assertIn('timeout',self.actions.status)
        self.step(total=1000)
        self.assertEqual(self.actions.maskAttempts,1)

    def test_mask_retry_is_bounded_and_interval_gated(self):
        self.enable('mask');self.options.maskMaxAttempts=2
        self.step(total=1);self.step(total=7)
        self.step(total=600);self.assertEqual(self.actions.maskAttempts,1)
        self.step(total=601);self.assertEqual(self.actions.maskAttempts,2)
        self.step(total=607);self.step(total=1300)
        self.assertEqual(self.actions.maskAttempts,2)

    def test_mask_never_claims_effect_active_or_queries_invented_uid(self):
        self.enable('mask');self.step()
        source=(ROOT/'scripts/rocky_r16/combat/Experiments.txt').read_text()
        self.assertNotIn('GetCount("debuff_',source)
        self.assertNotIn('feeble_active',source)

    def test_dash_arm_activate_and_restore(self):
        self.enable('dash');self.step(total=1,distance=22)
        self.assertEqual(self.items.equips,[('both','quarterstaff DashStaff')])
        self.items.right=Text('quarterstaff');self.items.right.id=Text('quarterstaff');self.items.right.state=0
        self.step(total=2,distance=22)
        self.assertEqual(self.items.activations,['R'])
        self.step(total=3,distance=5)
        self.assertEqual(self.gear.calls,['fire sword'])
        self.step(total=200,distance=22)
        self.assertEqual(self.actions.dashAttempts,1)

    def test_dash_distance_cooldown_and_walking_guards(self):
        self.enable('dash')
        for distance in (0,5,17,29,47):
            self.step(distance=distance)
            self.assertEqual(self.items.equips,[])
        self.items.cooldowns['quarterstaff']=2
        self.step(distance=22);self.assertEqual(self.items.equips,[])
        self.items.cooldowns['quarterstaff']=0;self.native['ai'].walking=False
        self.step(distance=22);self.assertEqual(self.items.equips,[])

    def test_recovery_armor_immunity_and_bosses_preempt_experiments(self):
        self.enable('mask');self.options.dashEnabled=True;self.actions.Prepare(self.options)
        for target, hp, armor in [('acronian_scout',60,0),('acronian_scout',100,10),
                                  ('acronian_scout immune_to_physical',100,0),
                                  ('dysangelos phase1',100,0),('dysangelos phase2',100,0),('dysangelos phase3',100,0)]:
            self.step(target,player_hp=hp,armor=armor)
            self.assertEqual(self.items.activations,[])
            self.assertEqual(self.items.equips,[])

    def test_protected_ray_interrupts_experiment_without_stale_restore(self):
        self.enable('mask');self.step(total=1)
        self.step('dysangelos phase3',total=2,foe_state=115,foe_time=23)
        self.assertEqual(self.gear.calls,['mind stone'])
        self.assertEqual(self.items.activations,[])
        self.step('',total=3)
        self.assertEqual(self.gear.calls,['mind stone'])
        self.step('dysangelos phase3',total=33,foe_state=116)
        self.assertNotEqual(self.gear.calls,['cultist mask'])
        self.assertEqual(self.actions.action,'none')

    def test_low_hp_cancels_active_mask_for_vigor(self):
        self.enable('mask');self.step(total=1)
        self.step(total=2,player_hp=50)
        self.assertEqual(self.gear.calls,['fire sword'])
        self.assertEqual(self.gear.lastShield,'vigor sword dL -big +21')
        self.assertEqual(self.actions.action,'none')
        self.assertEqual(self.items.activations,[])

    def test_target_change_and_lost_target_do_not_activate(self):
        self.enable('mask');self.step(total=1)
        self.step('dysangelos phase2 fire',total=2)
        self.assertEqual(self.gear.calls,['aether sword'])
        self.assertEqual(self.items.activations,[])
        self.assertEqual(self.actions.action,'none')

    def test_missing_and_ambiguous_selector_never_falls_back(self):
        for count in (0,2):
            self.options.maskEnabled=self.options.dashEnabled=True
            self.items.counts['cultist mask']=count;self.items.counts['quarterstaff DashStaff']=count
            self.actions.Prepare(self.options)
            self.step(total=1);self.step(total=2,distance=22)
            self.assertEqual(self.items.equips,[])
            self.assertEqual(self.items.activations,[])

    def test_preparation_only_inventory_queries_and_reset(self):
        self.enable('mask');before=len(self.items.queries)
        for total in range(1,20):self.step(total=total)
        self.assertEqual(len(self.items.queries),before)
        self.actions.Reset();self.assertEqual(self.actions.maskAttempts,0)

    def test_active_sequence_resets_aac_and_no_ordinary_pair_is_sent(self):
        self.enable('mask');self.items.left.state=self.items.right.state=3
        self.step(total=1)
        self.assertEqual(self.gear.calls,[])
        self.assertEqual(self.attacks.status,'protected/reset')
        self.assertEqual(len(self.items.equips),1)


    def test_r16_package_has_no_r15_replacement_payload(self):
        import importlib.util
        import sys
        sys.path.insert(0,str(ROOT/'tools'))
        try:
            import prepare_r16_candidate as package
            with tempfile.TemporaryDirectory() as folder:
                import shutil
                root=Path(folder);shutil.copytree(ROOT/'scripts',root/'scripts')
                target=package.prepare(root)
                payload=[p.relative_to(target).as_posix() for p in target.rglob('*.txt')]
                self.assertEqual(len(payload),4)
                self.assertTrue(all(p.startswith('SpeedRunRockyR16/') for p in payload))
                self.assertEqual(package.prepare(root),target)
        finally:sys.path.pop(0)

    def test_global_activation_disable_aborts_without_rearming_loop(self):
        self.enable('mask');self.step(total=1)
        self.items.abilities_enabled=False
        self.step(total=2)
        self.assertEqual(self.items.activations,[])
        self.assertEqual(self.gear.calls,['fire sword'])
        self.items.abilities_enabled=True
        prior=len(self.items.equips)
        self.step(total=3)
        self.assertEqual(len(self.items.equips),prior)
        self.assertEqual(self.actions.maskAttempts,1)
    def test_selector_refresh_does_not_reset_attempt_budget(self):
        self.enable('mask');self.step(total=1)
        self.assertEqual(self.actions.maskAttempts,1)
        self.actions.Prepare(self.options)
        self.step('dysangelos phase1',total=2)
        self.assertEqual(self.actions.maskAttempts,1)
        self.assertEqual(self.items.activations,[])
if __name__=='__main__':unittest.main()
