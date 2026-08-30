Database System - Character Storage and Management
Orah-Lore - Roleplay Game System
"""

import json
import os
from typing import Optional, List, Dict
from models import Character
from datetime import datetime


class CharacterDatabase:
    """SQLite-like character database system"""
    
    def __init__(self, db_path: str = "data/characters.json"):
        """Initialize database"""
        self.db_path = db_path
        self.data_dir = os.path.dirname(db_path)
        
        # Create data directory if it doesn't exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Load or create database
        if not os.path.exists(db_path):
            self._create_db()
        else:
            self._load_db()
    
    def _create_db(self):
        """Create new database file"""
        db_data = {
            'version': '1.0',
            'created_at': datetime.now().isoformat(),
            'characters': {},
            'metadata': {
                'total_characters': 0,
                'total_playtime': 0.0
            }
        }
        self._save_db(db_data)
        print(f"✅ تم إنشاء قاعدة البيانات في {self.db_path}")
    
    def _load_db(self) -> dict:
        """Load database from file"""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ خطأ في تحميل قاعدة البيانات: {e}")
            return None
    
    def _save_db(self, data: dict):
        """Save database to file"""
        try:
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ خطأ في حفظ قاعدة البيانات: {e}")
    
    def save_character(self, character: Character) -> bool:
        """Save a character to database"""
        try:
            db = self._load_db()
            
            # Update character last_played time
            character.last_played = datetime.now().isoformat()
            
            # Save character
            char_id = character.character_id
            db['characters'][char_id] = character.to_dict()
            
            # Update metadata
            db['metadata']['total_characters'] = len(db['characters'])
            db['metadata']['last_save'] = datetime.now().isoformat()
            
            self._save_db(db)
            print(f"✅ تم حفظ الشخصية: {character.identity.full_name}")
            return True
        except Exception as e:
            print(f"❌ خطأ في حفظ الشخصية: {e}")
            return False
    
    def load_character(self, character_id: str) -> Optional[Character]:
        """Load a character from database"""
        try:
            db = self._load_db()
            
            if character_id not in db['characters']:
                print(f"❌ الشخصية برقم {character_id} غير موجودة")
                return None
            
            char_data = db['characters'][character_id]
            character = Character.from_dict(char_data)
            print(f"✅ تم تحميل الشخصية: {character.identity.full_name}")
            return character
        except Exception as e:
            print(f"❌ خطأ في تحميل الشخصية: {e}")
            return None
    
    def delete_character(self, character_id: str) -> bool:
        """Delete a character from database"""
        try:
            db = self._load_db()
            
            if character_id not in db['characters']:
                print(f"❌ الشخصية برقم {character_id} غير موجودة")
                return False
            
            char_name = db['characters'][character_id]['identity']['full_name']
            del db['characters'][character_id]
            
            db['metadata']['total_characters'] = len(db['characters'])
            self._save_db(db)
            
            print(f"✅ تم حذف الشخصية: {char_name}")
            return True
        except Exception as e:
            print(f"❌ خطأ في حذف الشخصية: {e}")
            return False
    
    def get_all_characters(self) -> List[Dict]:
        """Get list of all characters"""
        try:
            db = self._load_db()
            characters = []
            
            for char_id, char_data in db['characters'].items():
                characters.append({
                    'id': char_id,
                    'name': char_data['identity']['full_name'],
                    'age': char_data['appearance']['age'],
                    'created_at': char_data['created_at'],
                    'playtime': char_data['playtime_hours'],
                    'location': char_data['location'],
                    'cash': char_data['cash']
                })
            
            return characters
        except Exception as e:
            print(f"❌ خطأ في الحصول على قائمة الشخصيات: {e}")
            return []
    
    def character_exists(self, character_id: str) -> bool:
        """Check if character exists"""
        db = self._load_db()
        return character_id in db['characters']
    
    def get_character_count(self) -> int:
        """Get total number of characters"""
        db = self._load_db()
        return len(db['characters'])
    
    def search_characters_by_name(self, name: str) -> List[Dict]:
        """Search characters by name"""
        all_chars = self.get_all_characters()
        return [c for c in all_chars if name.lower() in c['name'].lower()]
    
    def export_character(self, character_id: str, export_path: str) -> bool:
        """Export character to a separate file"""
        try:
            character = self.load_character(character_id)
            if not character:
                return False
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(character.to_dict(), f, ensure_ascii=False, indent=2)
            
            print(f"✅ تم تصدير الشخصية إلى: {export_path}")
            return True
        except Exception as e:
            print(f"❌ خطأ في تصدير الشخصية: {e}")
            return False
    
    def import_character(self, import_path: str) -> Optional[Character]:
        """Import character from a file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                char_data = json.load(f)
            
            character = Character.from_dict(char_data)
            self.save_character(character)
            return character
        except Exception as e:
            print(f"❌ خطأ في استيراد الشخصية: {e}")
            return None
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        db = self._load_db()
        all_chars = self.get_all_characters()
        
        total_playtime = sum(c['playtime'] for c in all_chars)
        total_cash = sum(c['cash'] for c in all_chars)
        
        return {
            'total_characters': len(all_chars),
            'total_playtime_hours': total_playtime,
            'total_cash_in_game': total_cash,
            'database_version': db['version'],
            'created_at': db['created_at'],
            'last_save': db['metadata'].get('last_save', 'Unknown')
        }


class SessionManager:
    """Manages player sessions"""
    
    def __init__(self, db: CharacterDatabase):
        """Initialize session manager"""
        self.db = db
        self.current_character: Optional[Character] = None
        self.session_start_time: Optional[datetime] = None
    
    def start_session(self, character_id: str) -> bool:
        """Start a new game session"""
        character = self.db.load_character(character_id)
        
        if not character:
            return False
        
        self.current_character = character
        self.session_start_time = datetime.now()
        print(f"\n🎮 جلسة اللعب بدأت - مرحباً {character.identity.full_name}!")
        return True
    
    def end_session(self) -> bool:
        """End current game session"""
        if not self.current_character:
            print("❌ لا توجد جلسة نشطة")
            return False
        
        if self.session_start_time:
            session_duration = (datetime.now() - self.session_start_time).total_seconds() / 3600
            self.current_character.playtime_hours += session_duration
        
        self.db.save_character(self.current_character)
        
        print(f"\n👋 شكراً على اللعب! تم حفظ الشخصية.")
        print(f"⏱️ وقت اللعب: {self.current_character.playtime_hours:.1f} ساعة")
        
        self.current_character = None
        self.session_start_time = None
        return True
    
    def get_current_character(self) -> Optional[Character]:
        """Get current active character"""
        return self.current_character
