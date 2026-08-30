Character Creation System - Interactive Character Builder
Orah-Lore - Roleplay Game System
"""

from models import (
    Character, Identity, Appearance, Clothing, VitalStats,
    Gender, EyeColor, HairColor, SkinTone
)
from datetime import datetime, timedelta
import random
from typing import Tuple
import os


class CharacterCreator:
    """Interactive character creation system"""
    
    # Appearance options
    HAIR_STYLES = {
        'ذكر': ['قصير', 'متوسط', 'طويل', 'أفرو', 'صلع', 'موهوك'],
        'أنثى': ['طويل', 'قصير', 'شعر مموج', 'ضفائر', 'ذيل حصان', 'بوب']
    }
    
    FACIAL_HAIR_OPTIONS = {
        'ذكر': ['لا يوجد', 'لحية خفيفة', 'لحية كثيفة', 'شارب', 'لحية وشارب'],
        'أنثى': ['لا يوجد']
    }
    
    CLOTHING_PRESETS = {
        'casual': {
            'shirt': ['قميص أبيض', 'تي شيرت أسود', 'قميص أزرق', 'بولو'],
            'pants': ['جينز أزرق', 'تراك سوداء', 'تراك رمادية', 'بنطال رسمي'],
            'shoes': ['أحذية رياضية', 'حذاء عادي', 'أحذية كاجوال', 'صندل']
        },
        'formal': {
            'shirt': ['قميص أبيض', 'قميص أسود', 'قميص رمادي'],
            'pants': ['بنطال أسود', 'بنطال رمادي', 'بنطال بني'],
            'shoes': ['حذاء جلدي', 'حذاء رسمي']
        },
        'street': {
            'shirt': ['تي شيرت', 'هوديز', 'قميص هيب هوب'],
            'pants': ['جينز ممزق', 'تراك', 'بنطال رياضي'],
            'shoes': ['حذاء رياضي', 'حذاء شارع']
        }
    }
    
    def __init__(self):
        """Initialize character creator"""
        self.character = None
        self.current_gender = None
    
    def clear_screen(self):
        """Clear console screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self, title: str):
        """Print formatted header"""
        print("\n" + "="*60)
        print(f"  🎮 {title}")
        print("="*60 + "\n")
    
    def print_menu(self, options: dict, title: str = ""):
        """Print formatted menu"""
        if title:
            print(f"\n📋 {title}")
            print("-" * 50)
        for key, value in options.items():
            if isinstance(value, tuple):
                print(f"  {key}) {value[0]}")
            else:
                print(f"  {key}) {value}")
        print()
    
    def get_input(self, prompt: str, valid_options=None) -> str:
        """Get validated user input"""
        while True:
            try:
                user_input = input(f"➤ {prompt}: ").strip()
                
                if valid_options and user_input not in valid_options:
                    print(f"❌ خيار غير صحيح. الخيارات الصحيحة: {', '.join(valid_options)}")
                    continue
                
                return user_input
            except KeyboardInterrupt:
                print("\n⚠️  تم إيقاف العملية.")
                return None
    
    def create_character(self) -> Character:
        """Main character creation flow"""
        self.clear_screen()
        self.print_header("نظام إنشاء الشخصية")
        
        print("""
مرحباً بك في لعبة الحياة الواقعية! 🌆
سيتم إنشاء شخصيتك الافتراضية خطوة بخطوة.

دعونا نبدأ بمعلومات أساسية...
        """)
        
        # Step 1: Gender selection
        self.character = Character()
        self._create_identity()
        
        # Step 2: Appearance
        self._create_appearance()
        
        # Step 3: Clothing
        self._create_clothing()
        
        # Step 4: Review
        self._review_character()
        
        return self.character
    
    def _create_identity(self):
        """Create character identity"""
        self.clear_screen()
        self.print_header("الخطوة 1: الهوية والمعلومات الشخصية")
        
        # Gender
        gender_options = {'1': ('ذكر', Gender.MALE), '2': ('أنثى', Gender.FEMALE)}
        self.print_menu({k: v[0] for k, v in gender_options.items()}, "اختر الجنس")
        
        gender_choice = self.get_input("الجنس (1/2)", valid_options=['1', '2'])
        if gender_choice is None:
            return
        
        self.current_gender = gender_options[gender_choice][1]
        
        # Name
        first_name = self.get_input("الاسم الأول")
        if first_name is None:
            return
        last_name = self.get_input("الاسم الأخير")
        if last_name is None:
            return
        full_name = f"{first_name} {last_name}"
        
        # Birth date
        print("\n📅 تاريخ الميلاد (الصيغة: السنة-الشهر-اليوم)")
        while True:
            birth_date = self.get_input("تاريخ الميلاد (مثال: 1995-05-15)")
            if birth_date is None:
                return
            try:
                datetime.strptime(birth_date, "%Y-%m-%d")
                age = self._calculate_age(birth_date)
                if age < 18 or age > 100:
                    print("❌ العمر يجب أن يكون بين 18 و 100 سنة")
                    continue
                break
            except ValueError:
                print("❌ صيغة التاريخ غير صحيحة. استخدم YYYY-MM-DD")
        
        # ID Number
        id_number = self.get_input("رقم الهوية (مثال: 1234567890)")
        if id_number is None:
            return
        
        # Phone number
        phone_number = self.get_input("رقم الهاتف (مثال: 0501234567)")
        if phone_number is None:
            return
        
        # Create identity
        self.character.identity = Identity(
            full_name=full_name,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            id_number=id_number,
            phone_number=phone_number
        )
        
        print("\n✅ تم حفظ المعلومات الشخصية بنجاح!")
    
    def _create_appearance(self):
        """Create character appearance"""
        self.clear_screen()
        self.print_header("الخطوة 2: المظهر الخارجي")
        
        age = self.character.identity.get_age()
        
        # Height
        print("📏 الطول (بالسنتيمتر، من 150 إلى 200)")
        while True:
            height_str = self.get_input("الطول")
            if height_str is None:
                return
            try:
                height = int(height_str)
                if 150 <= height <= 200:
                    break
                print("❌ الطول يجب أن يكون بين 150 و 200 سم")
            except ValueError:
                print("❌ أدخل رقماً صحيحاً")
        
        # Weight
        print("\n⚖️ الوزن (بالكيلوجرام، من 40 إلى 150)")
        while True:
            weight_str = self.get_input("الوزن")
            if weight_str is None:
                return
            try:
                weight = int(weight_str)
                if 40 <= weight <= 150:
                    break
                print("❌ الوزن يجب أن يكون بين 40 و 150 كجم")
            except ValueError:
                print("❌ أدخل رقماً صحيحاً")
        
        # Eye color
        print("\n👁️ لون العيون")
        eye_colors = {str(i): (e.value, e) for i, e in enumerate(EyeColor, 1)}
        self.print_menu({k: v[0] for k, v in eye_colors.items()})
        eye_choice = self.get_input("اختر لون العيون", valid_options=list(eye_colors.keys()))
        if eye_choice is None:
            return
        eye_color = eye_colors[eye_choice][1]
        
        # Hair color
        print("\n💇 لون الشعر")
        hair_colors = {str(i): (h.value, h) for i, h in enumerate(HairColor, 1)}
        self.print_menu({k: v[0] for k, v in hair_colors.items()})
        hair_choice = self.get_input("اختر لون الشعر", valid_options=list(hair_colors.keys()))
        if hair_choice is None:
            return
        hair_color = hair_colors[hair_choice][1]
        
        # Hair style
        print("\n💇‍♂️ تسريحة الشعر")
        gender_key = 'ذكر' if self.current_gender == Gender.MALE else 'أنثى'
        hair_styles = {str(i): s for i, s in enumerate(self.HAIR_STYLES[gender_key], 1)}
        self.print_menu(hair_styles)
        style_choice = self.get_input("اختر التسريحة", valid_options=list(hair_styles.keys()))
        if style_choice is None:
            return
        hair_style = hair_styles[style_choice]
        
        # Skin tone
        print("\n🎨 لون البشرة")
        skin_tones = {str(i): (s.value, s) for i, s in enumerate(SkinTone, 1)}
        self.print_menu({k: v[0] for k, v in skin_tones.items()})
        skin_choice = self.get_input("اختر لون البشرة", valid_options=list(skin_tones.keys()))
        if skin_choice is None:
            return
        skin_tone = skin_tones[skin_choice][1]
        
        # Facial hair
        facial_hair_options = self.FACIAL_HAIR_OPTIONS[gender_key]
        if len(facial_hair_options) > 1:
            print("\n🧔 شعر الوجه")
            facial_options = {str(i): f for i, f in enumerate(facial_hair_options, 1)}
            self.print_menu(facial_options)
            facial_choice = self.get_input("اختر شعر الوجه", valid_options=list(facial_options.keys()))
            if facial_choice is None:
                return
            facial_hair = facial_options[facial_choice]
        else:
            facial_hair = facial_hair_options[0]
        
        # Create appearance
        self.character.appearance = Appearance(
            gender=self.current_gender,
            age=age,
            height=height,
            weight=weight,
            eye_color=eye_color,
            hair_color=hair_color,
            hair_style=hair_style,
            skin_tone=skin_tone,
            facial_hair=facial_hair
        )
        
        print("\n✅ تم حفظ المظهر الخارجي بنجاح!")
    
    def _create_clothing(self):
        """Create character initial clothing"""
        self.clear_screen()
        self.print_header("الخطوة 3: الملابس الأولية")
        
        print("اختر نمط ملابسك الأولي:")
        clothing_styles = {'1': ('كاجوال', 'casual'), '2': ('رسمي', 'formal'), '3': ('شارع', 'street')}
        self.print_menu({k: v[0] for k, v in clothing_styles.items()})
        
        style_choice = self.get_input("اختر النمط (1/2/3)", valid_options=['1', '2', '3'])
        if style_choice is None:
            return
        
        style_key = clothing_styles[style_choice][1]
        preset = self.CLOTHING_PRESETS[style_key]
        
        # Shirt
        print("\n👕 الأعلى")
        shirts = {str(i): s for i, s in enumerate(preset['shirt'], 1)}
        self.print_menu(shirts)
        shirt_choice = self.get_input("اختر الأعلى", valid_options=list(shirts.keys()))
        if shirt_choice is None:
            return
        shirt = shirts[shirt_choice]
        
        # Pants
        print("\n👖 السفلى")
        pants = {str(i): p for i, p in enumerate(preset['pants'], 1)}
        self.print_menu(pants)
        pants_choice = self.get_input("اختر السفلى", valid_options=list(pants.keys()))
        if pants_choice is None:
            return
        pants_item = pants[pants_choice]
        
        # Shoes
        print("\n👟 الأحذية")
        shoes = {str(i): s for i, s in enumerate(preset['shoes'], 1)}
        self.print_menu(shoes)
        shoes_choice = self.get_input("اختر الأحذية", valid_options=list(shoes.keys()))
        if shoes_choice is None:
            return
        shoes_item = shoes[shoes_choice]
        
        # Create clothing
        self.character.clothing = Clothing(
            shirt=shirt,
            pants=pants_item,
            shoes=shoes_item
        )
        
        print("\n✅ تم حفظ الملابس بنجاح!")
    
    def _review_character(self):
        """Review and confirm character"""
        self.clear_screen()
        self.print_header("الخطوة 4: مراجعة الشخصية")
        
        # Set random starting money
        self.character.cash = random.uniform(5000, 10000)
        
        print(self.character.get_full_info())
        
        confirm = self.get_input("\nهل تريد قبول هذه الشخصية؟ (نعم/لا)", valid_options=['نعم', 'لا'])
        
        if confirm == 'نعم':
            print("\n✅ تم إنشاء الشخصية بنجاح! مرحباً بك في اللعبة! 🎉")
            return True
        else:
            print("\n🔄 دعونا نحاول مجدداً...")
            return self.create_character()
    
    @staticmethod
    def _calculate_age(birth_date: str) -> int:
        """Calculate age from birth date"""
        birth = datetime.strptime(birth_date, "%Y-%m-%d")
        today = datetime.now()
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))


def start_character_creation() -> Character:
    """Start the character creation process"""
    creator = CharacterCreator()
    return creator.create_character()
