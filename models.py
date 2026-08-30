Character Models and Game Entities
 Orah-Lore - Roleplay Game System
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
import uuid


class Gender(Enum):
    """Character gender options"""
    MALE = "ذكر"
    FEMALE = "أنثى"


class EyeColor(Enum):
    """Available eye colors"""
    BROWN = "بني"
    BLUE = "أزرق"
    GREEN = "أخضر"
    HAZEL = "عسلي"
    BLACK = "أسود"


class HairColor(Enum):
    """Available hair colors"""
    BLACK = "أسود"
    BROWN = "بني"
    BLONDE = "أشقر"
    RED = "أحمر"
    GRAY = "رمادي"
    WHITE = "أبيض"


class SkinTone(Enum):
    """Available skin tones"""
    VERY_LIGHT = "فاتح جداً"
    LIGHT = "فاتح"
    MEDIUM = "متوسط"
    DARK = "داكن"
    VERY_DARK = "داكن جداً"


@dataclass
class Appearance:
    """Character physical appearance"""
    gender: Gender
    age: int
    height: int  # cm
    weight: int  # kg
    eye_color: EyeColor
    hair_color: HairColor
    hair_style: str
    skin_tone: SkinTone
    facial_hair: str  # beard/mustache description
    tattoos: List[str] = field(default_factory=list)
    scars: List[str] = field(default_factory=list)
    
    def __str__(self) -> str:
        return f"{self.gender.value}, {self.age} سنة، {self.height}سم، {self.skin_tone.value}"


@dataclass
class Identity:
    """Character identification documents"""
    full_name: str
    first_name: str
    last_name: str
    birth_date: str  # YYYY-MM-DD
    id_number: str  # رقم الهوية
    phone_number: str  # رقم الهاتف
    
    def get_age(self) -> int:
        """Calculate character age from birth date"""
        birth = datetime.strptime(self.birth_date, "%Y-%m-%d")
        today = datetime.now()
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    
    def __str__(self) -> str:
        return f"{self.full_name} | الهوية: {self.id_number} | الهاتف: {self.phone_number}"


@dataclass
class Clothing:
    """Character initial clothing"""
    shirt: str
    pants: str
    shoes: str
    jacket: Optional[str] = None
    hat: Optional[str] = None
    
    def __str__(self) -> str:
        outfit = f"قميص: {self.shirt}, بنطال: {self.pants}, أحذية: {self.shoes}"
        if self.jacket:
            outfit += f", جاكت: {self.jacket}"
        if self.hat:
            outfit += f", قبعة: {self.hat}"
        return outfit


@dataclass
class VitalStats:
    """Character vital statistics"""
    health: int = 100  # Health points (0-100)
    hunger: int = 100  # Hunger level (0-100)
    thirst: int = 100  # Thirst level (0-100)
    energy: int = 100  # Energy/Fatigue (0-100)
    stress: int = 0    # Stress level (0-100)
    
    def is_alive(self) -> bool:
        """Check if character is alive"""
        return self.health > 0


@dataclass
class Character:
    """Main Character class representing a player"""
    character_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    identity: Identity = None
    appearance: Appearance = None
    clothing: Clothing = None
    vital_stats: VitalStats = field(default_factory=VitalStats)
    
    # Economic data
    cash: float = 7500.0  # Starting money (between 5000-10000)
    bank_balance: float = 0.0
    
    # Location
    location: str = "مطار العاصمة الدولي"  # Starting location
    
    # Game progression
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_played: str = field(default_factory=lambda: datetime.now().isoformat())
    playtime_hours: float = 0.0
    
    # Inventory
    inventory: Dict[str, int] = field(default_factory=dict)
    
    # Status flags
    is_alive: bool = True
    is_wanted: bool = False
    wanted_level: int = 0
    
    # Relationships
    friends: List[str] = field(default_factory=list)
    enemies: List[str] = field(default_factory=list)
    
    # Skills/Experience
    skills: Dict[str, int] = field(default_factory=dict)  # skill_name: experience_points
    
    # Reputation
    reputation_score: int = 50  # Neutral (0-100, 50 = neutral)
    crimes_committed: int = 0
    arrests: int = 0
    
    def get_full_info(self) -> str:
        """Get comprehensive character information"""
        info = f"""
╔════════════════════════════════════════════════════════════╗
║                   معلومات الشخصية الكاملة                      ║
╚════════════════════════════════════════════════════════════╝

📋 الهوية:
   {self.identity}

🎭 المظهر:
   {self.appearance}

👕 الملابس:
   {self.clothing}

💰 المالية:
   النقود: {self.cash:,.2f} $
   الحساب البنكي: {self.bank_balance:,.2f} $

📍 الموقع الحالي:
   {self.location}

❤️ المؤشرات الحيوية:
   الصحة: {self.vital_stats.health}/100
   الجوع: {self.vital_stats.hunger}/100
   العطش: {self.vital_stats.thirst}/100
   الطاقة: {self.vital_stats.energy}/100
   الإجهاد: {self.vital_stats.stress}/100

⏱️ وقت اللعب:
   {self.playtime_hours:.1f} ساعة

📊 السمعة:
   نقاط السمعة: {self.reputation_score}/100
   الجرائم المرتكبة: {self.crimes_committed}
   الاعتقالات: {self.arrests}

🆔 معرف الشخصية:
   {self.character_id}
"""
        return info
    
    def to_dict(self) -> dict:
        """Convert character to dictionary for storage"""
        return {
            'character_id': self.character_id,
            'identity': {
                'full_name': self.identity.full_name,
                'first_name': self.identity.first_name,
                'last_name': self.identity.last_name,
                'birth_date': self.identity.birth_date,
                'id_number': self.identity.id_number,
                'phone_number': self.identity.phone_number,
            },
            'appearance': {
                'gender': self.appearance.gender.value,
                'age': self.appearance.age,
                'height': self.appearance.height,
                'weight': self.appearance.weight,
                'eye_color': self.appearance.eye_color.value,
                'hair_color': self.appearance.hair_color.value,
                'hair_style': self.appearance.hair_style,
                'skin_tone': self.appearance.skin_tone.value,
                'facial_hair': self.appearance.facial_hair,
                'tattoos': self.appearance.tattoos,
                'scars': self.appearance.scars,
            },
            'clothing': {
                'shirt': self.clothing.shirt,
                'pants': self.clothing.pants,
                'shoes': self.clothing.shoes,
                'jacket': self.clothing.jacket,
                'hat': self.clothing.hat,
            },
            'vital_stats': {
                'health': self.vital_stats.health,
                'hunger': self.vital_stats.hunger,
                'thirst': self.vital_stats.thirst,
                'energy': self.vital_stats.energy,
                'stress': self.vital_stats.stress,
            },
            'cash': self.cash,
            'bank_balance': self.bank_balance,
            'location': self.location,
            'created_at': self.created_at,
            'last_played': self.last_played,
            'playtime_hours': self.playtime_hours,
            'is_alive': self.is_alive,
            'is_wanted': self.is_wanted,
            'wanted_level': self.wanted_level,
            'reputation_score': self.reputation_score,
            'crimes_committed': self.crimes_committed,
            'arrests': self.arrests,
            'inventory': self.inventory,
            'friends': self.friends,
            'enemies': self.enemies,
            'skills': self.skills,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Character':
        """Create character from dictionary"""
        identity = Identity(
            full_name=data['identity']['full_name'],
            first_name=data['identity']['first_name'],
            last_name=data['identity']['last_name'],
            birth_date=data['identity']['birth_date'],
            id_number=data['identity']['id_number'],
            phone_number=data['identity']['phone_number'],
        )
        
        appearance = Appearance(
            gender=Gender(data['appearance']['gender']),
            age=data['appearance']['age'],
            height=data['appearance']['height'],
            weight=data['appearance']['weight'],
            eye_color=EyeColor(data['appearance']['eye_color']),
            hair_color=HairColor(data['appearance']['hair_color']),
            hair_style=data['appearance']['hair_style'],
            skin_tone=SkinTone(data['appearance']['skin_tone']),
            facial_hair=data['appearance']['facial_hair'],
            tattoos=data['appearance'].get('tattoos', []),
            scars=data['appearance'].get('scars', []),
        )
        
        clothing = Clothing(
            shirt=data['clothing']['shirt'],
            pants=data['clothing']['pants'],
            shoes=data['clothing']['shoes'],
            jacket=data['clothing'].get('jacket'),
            hat=data['clothing'].get('hat'),
        )
        
        vital_stats = VitalStats(**data['vital_stats'])
        
        char = cls(
            character_id=data['character_id'],
            identity=identity,
            appearance=appearance,
            clothing=clothing,
            vital_stats=vital_stats,
            cash=data['cash'],
            bank_balance=data['bank_balance'],
            location=data['location'],
            created_at=data['created_at'],
            last_played=data['last_played'],
            playtime_hours=data['playtime_hours'],
            is_alive=data['is_alive'],
            is_wanted=data['is_wanted'],
            wanted_level=data['wanted_level'],
            reputation_score=data['reputation_score'],
            crimes_committed=data['crimes_committed'],
            arrests=data['arrests'],
            inventory=data.get('inventory', {}),
            friends=data.get('friends', []),
            enemies=data.get('enemies', []),
            skills=data.get('skills', {}),
        )
        
        return char
