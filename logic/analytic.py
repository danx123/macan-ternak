# `logic/analytics.py`


from datetime import datetime
import json
from pathlib import Path

class GameAnalytics:
    def __init__(self):
        self.stats_file = Path.home() / '.macan_ternak' / 'analytics.json'
        self.stats = self._load_stats()
    
    def _load_stats(self):
        if self.stats_file.exists():
            with open(self.stats_file) as f:
                return json.load(f)
        return {
            'total_playtime': 0,
            'sessions': [],
            'actions_performed': {'feed': 0, 'clean': 0, 'sleep': 0, 'play': 0},
            'max_level_reached': 1,
            'total_exp_earned': 0
        }
    
    def start_session(self):
        self.session_start = datetime.now()
    
    def end_session(self):
        duration = (datetime.now() - self.session_start).total_seconds()
        self.stats['total_playtime'] += duration
        self.stats['sessions'].append({
            'date': datetime.now().isoformat(),
            'duration': duration
        })
        self._save_stats()
    
    def log_action(self, action_name):
        if action_name in self.stats['actions_performed']:
            self.stats['actions_performed'][action_name] += 1
    
    def update_max_level(self, level):
        self.stats['max_level_reached'] = max(
            self.stats['max_level_reached'], 
            level
        )
    
    def _save_stats(self):
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)