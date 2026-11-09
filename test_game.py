"""Regression tests. Run: uv run python -m unittest -v"""
import contextlib
import copy
import io
import tempfile
import unittest
from collections import deque
from pathlib import Path
from unittest.mock import patch
import database
from auth import new_player_data, register_or_login
from player import Player
from game import Game
from world_map import MAPS, ENCOUNTERS, NPC_LOCATIONS, BOSS, move_player, show_map
from quest import advance_main_quest
from npc import talk_to_npc
from inventory import use_item
from shop import visit_shop
from combat import fight
from monster import WanderingNoble, EldenLord, Monster
from skill import SKILLS, Skill


def route(player, target):
    """BFS supplies legal movement keys without bypassing walls or portals."""
    start = (player.get('map_name'), player.get('x'), player.get('y'))
    todo = deque([(start, [])])
    seen = {start}
    while todo:
        state, path = todo.popleft()
        if state == target: return path
        for key in 'wasd':
            candidate = Player(new_player_data('Pathfinder'))
            for field, value in zip(('map_name', 'x', 'y'), state): candidate.set(field, value)
            if not move_player(candidate, key): continue
            nxt = (candidate.get('map_name'), candidate.get('x'), candidate.get('y'))
            if nxt not in seen:
                seen.add(nxt)
                todo.append((nxt, path + [key]))
    raise AssertionError(f'Unreachable: {target}')


class GameTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.old_path = database.SAVE_PATH
        database.SAVE_PATH = Path(self.temp.name)/'save.json'
        self.output = contextlib.redirect_stdout(io.StringIO())
        self.output.__enter__()
        database.create_account('tester', 'secret', new_player_data('Test Tarnished'))

    def tearDown(self):
        self.output.__exit__(None, None, None)
        database.SAVE_PATH = self.old_path
        self.temp.cleanup()

    def test_accounts_and_resume(self):
        account = database.find_account('tester')
        self.assertNotIn('password', account)
        self.assertTrue(database.verify_password(account, 'secret'))
        self.assertFalse(database.verify_password(account, 'wrong'))
        with self.assertRaises(ValueError):
            database.create_account('tester', 'new', {})
        data = new_player_data('Test')
        data.update(map_name='Erdtree', x=2, y=5, level=3, xp=17, gold=91,
                    skills=['Heavy Strike', 'Golden Vow'], main_quest=3,
                    side_quests=['Lost Keepsake'], completed_side_quests=['Clear the Road'])
        data['inventory'].append('Moonveil Fragment')
        database.save_player('tester', data)
        self.assertEqual(database.get_player('tester'), data)
        with patch('builtins.input', side_effect=['1', 'tester']), patch('auth.getpass', return_value='secret'):
            loaded = register_or_login()
        restored = Game(loaded).player
        for key, value in data.items(): self.assertEqual(restored.get(key), value)

    def test_maps_reachable_and_return_trip(self):
        p = Player(new_player_data('Test'))
        for name, rows in MAPS.items():
            self.assertTrue(all(len(row) == len(rows[0]) for row in rows))
            goals = list(ENCOUNTERS[name])
            goals += list(NPC_LOCATIONS.values()) if name == 'Limgrave' else [BOSS]
            for x,y in goals: self.assertIsInstance(route(p, (name,x,y)), list)
        for key in route(p, ('Erdtree',2,5)): self.assertTrue(move_player(p,key))
        for key in route(p, ('Limgrave',1,1)): self.assertTrue(move_player(p,key))
        self.assertFalse(move_player(p,'w'))
        self.assertFalse(move_player(p,'banana'))
        show_map(p)

    def test_shop_and_inventory_validation(self):
        p = Player(new_player_data('Test'))
        original = copy.deepcopy(p.data)
        with patch('builtins.input',side_effect=['-1','999','oops','0']): visit_shop(p)
        self.assertEqual(p.data, original)
        for text in ['-1','0','999','oops','']:
            with patch('builtins.input',return_value=text): self.assertFalse(use_item(p))
        p.get('inventory').append('Fire Grease')
        with patch('builtins.input',return_value='4'): self.assertTrue(use_item(p))
        self.assertEqual(p.get('attack_buff'),15)
        p.set('hp',50)
        with patch('builtins.input',return_value='1'): self.assertTrue(use_item(p))
        self.assertEqual(p.get('hp'),85)

    def test_skills_inheritance_cooldowns_and_invalid_index(self):
        self.assertTrue(all(isinstance(s,Skill) for s in SKILLS.values()))
        self.assertIsInstance(EldenLord(),Monster)
        p=Player(new_player_data('Test'))
        enemy=WanderingNoble()
        # Invalid -1 index must not select the last skill. Cooling skill is rejected.
        enemy.hp=60
        with patch('builtins.input',side_effect=['2','0','2','1','2','1','1','1']), patch('combat.random.randint',return_value=100):
            self.assertTrue(fight(p,enemy))
        self.assertEqual(p.get('hp'),86)  # Two valid rounds, no penalty for invalid actions.

    def test_death_recovery_and_intro_map(self):
        g=Game(database.get_player('tester') | {'username':'tester'})
        g.player.take_damage(1000)
        g.recover()
        self.assertFalse(g.player.get('lost'))
        self.assertEqual(g.player.get('hp'),100)
        with patch('builtins.input',return_value='x'): g.run()
        self.assertIn('LIMGRAVE',self.output._new_target.getvalue())
        self.assertEqual(database.get_player('tester')['hp'],100)

    def test_complete_playthrough(self):
        g=Game(database.get_player('tester') | {'username':'tester'})
        p=g.player
        def travel(name,x,y):
            for key in route(p,(name,x,y)):
                self.assertTrue(move_player(p,key))
                g.encounter()
        def battle_input(prompt):
            if prompt.startswith('Enter item'): return str(p.get('inventory').index('Crimson Flask')+1)
            if p.get('hp') <= 55 and 'Crimson Flask' in p.get('inventory'): return '3'
            return '1'
        with patch('builtins.input',side_effect=battle_input), patch('combat.random.randint',return_value=100):
            advance_main_quest(p)
            travel('Limgrave',2,6)
            talk_to_npc(p,'Roderika')
            travel('Limgrave',5,9)
            talk_to_npc(p,'Blaidd')
            for x,y in ENCOUNTERS['Limgrave']: travel('Limgrave',x,y)
            self.assertEqual(len(p.get('completed_side_quests')),2)
            self.assertEqual(p.get('inventory').count('Great Rune Shard'),3)
            travel('Limgrave',2,1)
            advance_main_quest(p)
            self.assertEqual(p.get('main_quest'),2)
            advance_main_quest(p)
            self.assertEqual(p.get('map_name'),'Limgrave')
            travel('Limgrave',5,1)
            # Sell the earned Golden Rune, then buy a sword with earned gold.
            idx=p.get('inventory').index('Golden Rune')+1
            with patch('builtins.input',return_value=str(idx)): use_item(p)
            with patch('builtins.input',side_effect=['4','0']): visit_shop(p)
            self.assertEqual(p.get('equipment'),"Knight's Greatsword")
            travel('Erdtree',2,5)
            p.heal(p.get('max_hp'))
            for x,y in ENCOUNTERS['Erdtree']: travel('Erdtree',x,y)
            travel('Erdtree',2,5)
            p.heal(p.get('max_hp'))
            # Save and rebuild the controller before the final fight.
            g.save()
            g=Game(database.get_player('tester') | {'username':'tester'})
            p=g.player
            travel('Erdtree',*BOSS)
            self.assertTrue(p.get('won'))
            self.assertEqual(p.get('main_quest'),4)
            g.save()
            self.assertTrue(database.get_player('tester')['won'])

if __name__ == '__main__': unittest.main()
