"""
Game UI System - Main Menu and Character Selection
Orah Lore - Roleplay Game System
"""

import os
from typing import Optional
from models import Character
from character_creator import start_character_creation
from database import CharacterDatabase, SessionManager
from movement import MovementController


class GameUI:
    """Main game user interface"""
    
    def __init__(self):
        """Initialize game UI"""
        self.db = CharacterDatabase("data/characters.json")
        self.session = SessionManager(self.db)
        self.movement = MovementController()
    
    def clear_screen(self):
        """Clear console screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_banner(self):
        """Print game banner"""
        banner = """
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║          🌆  لعبة الحياة الواقعية - 3D LAND BOT  🌆                      ║
║                                                                           ║
║              Realistic Life Simulation & Roleplay Game                    ║
║                                                                           ║
║                    مرحباً بك في عالم جديد ومثير!                         ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def print_menu(self, options: dict, title: str = ""):
        """Print formatted menu"""
        if title:
            print(f"\n{'='*60}")
            print(f"  {title}")
            print(f"{'='*60}\n")
        
        for key, value in options.items():
            print(f"  {key}) {value}")
        print()
    
    def get_input(self, prompt: str = "اختر", valid_options=None) -> Optional[str]:
        """Get validated user input"""
        while True:
            try:
                user_input = input(f"➤ {prompt}: ").strip()
                
                if not user_input:
                    print("❌ الرجاء إدخال قيمة")
                    continue
                
                if valid_options and user_input not in valid_options:
                    print(f"❌ خيار غير صحيح")
                    continue
                
                return user_input
            except KeyboardInterrupt:
                print("\n⚠️  تم إيقاف العملية.")
                return None
            except Exception as e:
                print(f"❌ خطأ: {e}")
                continue
    
    def main_menu(self):
        """Main menu loop"""
        while True:
            self.clear_screen()
            self.print_banner()
            
            char_count = self.db.get_character_count()
            print(f"\n📊 عدد الشخصيات: {char_count}\n")
            
            menu_options = {
                '1': 'إنشاء شخصية جديدة 🆕',
                '2': 'اختيار شخصية والبدء 🎮',
                '3': 'عرض الشخصيات 👥',
                '4': 'إحصائيات اللعبة 📈',
                '5': 'عرض أوامر الحركة 🕹️',
                '6': 'الخروج من اللعبة 🚪'
            }
            
            self.print_menu(menu_options, "القائمة الرئيسية")
            
            choice = self.get_input("خيارك", valid_options=list(menu_options.keys()))
            
            if choice == '1':
                self._create_new_character()
            elif choice == '2':
                self._select_and_play_character()
            elif choice == '3':
                self._view_all_characters()
            elif choice == '4':
                self._show_statistics()
            elif choice == '5':
                self._show_movement_controls()
            elif choice == '6':
                self._exit_game()
                break
    
    def _create_new_character(self):
        """Create new character"""
        print("\n" + "="*60)
        print("  🆕 إنشاء شخصية جديدة")
        print("="*60)
        
        character = start_character_creation()
        
        if character:
            if self.db.save_character(character):
                print("\n✅ تم حفظ الشخصية بنجاح!")
                print(f"🆔 معرف الشخصية: {character.character_id}")
                input("\nاضغط Enter للعودة للقائمة الرئيسية...")
            else:
                print("\n❌ حدث خطأ في حفظ الشخصية")
                input("\nاضغط Enter للعودة...")
    
    def _select_and_play_character(self):
        """Select and start playing with a character"""
        characters = self.db.get_all_characters()
        
        if not characters:
            print("\n❌ لا توجد شخصيات. الرجاء إنشاء شخصية أولاً.")
            input("\nاضغط Enter للعودة...")
            return
        
        self.clear_screen()
        print("\n" + "="*60)
        print("  🎮 اختر شخصيتك")
        print("="*60 + "\n")
        
        # Display characters
        options = {}
        for i, char in enumerate(characters, 1):
            options[str(i)] = f"{char['name']} (العمر: {char['age']}) - وقت اللعب: {char['playtime']:.1f} ساعة"
        
        options[str(len(characters) + 1)] = "العودة للقائمة الرئيسية"
        
        for key, value in options.items():
            print(f"  {key}) {value}")
        print()
        
        choice = self.get_input("اختيارك", valid_options=list(options.keys()))
        
        if choice == str(len(characters) + 1):
            return
        
        selected_char = characters[int(choice) - 1]
        self._start_game(selected_char['id'])
    
    def _start_game(self, character_id: str):
        """Start game with selected character"""
        if self.session.start_session(character_id):
            self._game_loop()
        else:
            print("\n❌ فشل في تحميل الشخصية")
            input("\nاضغط Enter للعودة...")
    
    def _game_loop(self):
        """Main game loop"""
        character = self.session.get_current_character()
        
        while character:
            self.clear_screen()
            
            # Display character info
            print("\n" + "="*60)
            print(f"  👤 {character.identity.full_name}")
            print("="*60)
            
            # Vital stats bar
            print(f"\n💚 الصحة: [{self._get_bar(character.vital_stats.health)}] {character.vital_stats.health}%")
            print(f"🍗 الجوع: [{self._get_bar(character.vital_stats.hunger)}] {character.vital_stats.hunger}%")
            print(f"💧 العطش: [{self._get_bar(character.vital_stats.thirst)}] {character.vital_stats.thirst}%")
            print(f"⚡ الطاقة: [{self._get_bar(character.vital_stats.energy)}] {character.vital_stats.energy}%")
            
            # Location and money
            print(f"\n📍 الموقع: {character.location}")
            print(f"💰 النقود: {character.cash:,.2f} $ | 🏦 البنك: {character.bank_balance:,.2f} $")
            
            # Game options
            print("\n" + "-"*60)
            game_menu = {
                '1': 'عرض معلومات الشخصية 📋',
                '2': 'إدارة الحقيبة 🎒',
                '3': 'الذهاب إلى مكان 📍',
                '4': 'العودة للقائمة الرئيسية 🏠',
                '5': 'الخروج من اللعبة 🚪'
            }
            
            self.print_menu(game_menu, "خيارات اللعبة")
            
            choice = self.get_input("اختيارك", valid_options=list(game_menu.keys()))
            
            if choice == '1':
                self._show_character_info()
            elif choice == '2':
                self._manage_inventory()
            elif choice == '3':
                self._travel()
            elif choice == '4':
                self.session.end_session()
                break
            elif choice == '5':
                self._exit_game()
                break
            
            character = self.session.get_current_character()
    
    def _show_character_info(self):
        """Display detailed character information"""
        character = self.session.get_current_character()
        self.clear_screen()
        print(character.get_full_info())
        input("\nاضغط Enter للعودة...")
    
    def _manage_inventory(self):
        """Manage character inventory"""
        character = self.session.get_current_character()
        
        self.clear_screen()
        print("\n" + "="*60)
        print("  🎒 إدارة الحقيبة")
        print("="*60 + "\n")
        
        if not character.inventory:
            print("❌ الحقيبة فارغة")
        else:
            print("محتويات الحقيبة:")
            total_items = 0
            for item, count in character.inventory.items():
                print(f"  • {item}: {count}")
                total_items += count
            print(f"\nإجمالي الأغراض: {total_items}")
        
        input("\nاضغط Enter للعودة...")
    
    def _travel(self):
        """Travel to different locations"""
        character = self.session.get_current_character()
        
        self.clear_screen()
        print("\n" + "="*60)
        print("  📍 الأماكن المتاحة")
        print("="*60 + "\n")
        
        locations = {
            '1': 'مطار العاصمة الدولي',
            '2': 'وسط المدينة (المركز التجاري)',
            '3': 'الميناء التجاري',
            '4': 'الأحياء القديمة',
            '5': 'حي التلال الفارهة',
            '6': 'بلدة الصحراء',
            '7': 'العودة للقائمة السابقة'
        }
        
        self.print_menu(locations)
        
        choice = self.get_input("اختر الموقع", valid_options=list(locations.keys()))
        
        if choice != '7':
            character.location = locations[choice]
            print(f"\n✈️ يتم الانتقال إلى {locations[choice]}...")
            input("اضغط Enter للمتابعة...")
    
    def _view_all_characters(self):
        """View all characters in database"""
        characters = self.db.get_all_characters()
        
        self.clear_screen()
        print("\n" + "="*60)
        print("  👥 قائمة جميع الشخصيات")
        print("="*60 + "\n")
        
        if not characters:
            print("❌ لا توجد شخصيات حالياً")
        else:
            print(f"{'الاسم':<20} {'العمر':<6} {'وقت اللعب':<12} {'المال':<12}")
            print("-" * 60)
            
            for char in characters:
                print(f"{char['name']:<20} {char['age']:<6} {char['playtime']:<12.1f} ${char['cash']:<12,.2f}")
        
        input("\nاضغط Enter للعودة...")
    
    def _show_statistics(self):
        """Show game statistics"""
        stats = self.db.get_statistics()
        
        self.clear_screen()
        print("\n" + "="*60)
        print("  📈 إحصائيات اللعبة")
        print("="*60 + "\n")
        
        print(f"عدد الشخصيات: {stats['total_characters']}")
        print(f"إجمالي وقت اللعب: {stats['total_playtime_hours']:.1f} ساعة")
        print(f"إجمالي المال في اللعبة: ${stats['total_cash_in_game']:,.2f}")
        print(f"إصدار قاعدة البيانات: {stats['database_version']}")
        print(f"تاريخ الإنشاء: {stats['created_at']}")
        print(f"آخر حفظ: {stats['last_save']}")
        
        input("\nاضغط Enter للعودة...")

    def _show_movement_controls(self):
        """Display movement controls and hybrid world model."""
        self.clear_screen()
        print("\n" + "="*70)
        print("  🕹️ أزرار الحركة والمشي الميداني")
        print("="*70 + "\n")

        for item in self.movement.get_control_guide():
            print(f"  • {item}")

        print("\n  🌍 العرض الهجين:")
        print(f"  {self.movement.get_hybrid_render_summary()}")
        print(f"\n  📌 الحالة الحالية: {self.movement.get_status_summary()}")

        input("\nاضغط Enter للعودة...")
    
    def _exit_game(self):
        """Exit game"""
        self.clear_screen()
        print("\n" + "="*60)
        print("  شكراً على اللعب! 👋")
        print("="*60)
        print("\n  نتمنى أن تكون قد استمتعت باللعبة")
        print("  إلى اللقاء قريباً! 🎮\n")
    
    @staticmethod
    def _get_bar(percentage: int, length: int = 20) -> str:
        """Create a percentage bar"""
        filled = int(length * percentage / 100)
        bar = '█' * filled + '░' * (length - filled)
        return bar


def run_game():
    """Run the game"""
    ui = GameUI()
    ui.main_menu()


if __name__ == "__main__":
    run_game()
