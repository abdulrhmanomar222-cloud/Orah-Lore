"""
Weapons, cuffs, and security facility system
Orah-Lore - Roleplay Game System

يوفر الأسلحة والكلبشات ومقرات الأمن والاستخبارات حسب القطاعات.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class AgencyType(Enum):
    """Security and intelligence agencies"""
    POLICE = "شرطة"
    MILITARY = "عسكرية"
    FBI = "FBI"
    CIA = "CIA"
    CIVILIAN = "مدني"


@dataclass
class Weapon:
    """Weapon information for law enforcement and intelligence agencies."""
    name: str
    category: AgencyType
    description: str
    fire_mode: str = "Semi-Auto"
    suppressor: bool = False
    magazine_size: int = 17
    ammo_type: str = "9mm"

    def summary(self) -> str:
        return f"{self.name} ({self.category.value}) - {self.description}"


@dataclass
class Cuff:
    """Restrictive restraint equipment used by police or intel units."""
    name: str
    description: str
    agency: AgencyType
    blocked_actions: List[str] = field(default_factory=list)
    lock_type: str = "Double Lock"

    def summary(self) -> str:
        return f"{self.name} | {self.description} | {self.agency.value}"


@dataclass
class Facility:
    """Physical headquarters or covert installation description."""
    name: str
    agency: AgencyType
    description: str
    sections: List[str] = field(default_factory=list)
    security_level: str = "High"

    def full_summary(self) -> str:
        section_text = ", ".join(self.sections) if self.sections else "لا توجد أقسام محددة"
        return f"{self.name} ({self.agency.value}) - {self.description}. الأقسام: {section_text}."


class WeaponsCatalog:
    """Structured catalog of weapons by sector."""

    @staticmethod
    def police_weapons() -> List[Weapon]:
        return [
            Weapon(
                name="Glock 17",
                category=AgencyType.POLICE,
                description="مسدس خدمي خفيف مع ارتداد منخفض للدوريات",
                fire_mode="Semi-Auto",
                magazine_size=17,
                ammo_type="9mm",
            ),
            Weapon(
                name="Pump-Action Shotgun",
                category=AgencyType.POLICE,
                description="بندقية كاسرة مثبتة داخل السيارة لإيقاف التهديدات القريبة",
                fire_mode="Pump",
                magazine_size=8,
                ammo_type="12 Gauge",
            ),
            Weapon(
                name="M4A1 Patrol Rifle",
                category=AgencyType.POLICE,
                description="بندقية هجومية تستخدم في البلاغات الكبرى وإطلاق النار الثقيل",
                fire_mode="Selective",
                magazine_size=30,
                ammo_type="5.56mm",
            ),
        ]

    @staticmethod
    def fbi_weapons() -> List[Weapon]:
        return [
            Weapon(
                name="FN 509",
                category=AgencyType.FBI,
                description="مسدس معدّل بدقة عالية مع منظار ليزر ومخزن ضخم",
                fire_mode="Semi-Auto",
                magazine_size=24,
                ammo_type="9mm",
            ),
            Weapon(
                name="MP5",
                category=AgencyType.FBI,
                description="رشاش قريب للعمليات الميدانية والمداهمات",
                fire_mode="Auto",
                magazine_size=30,
                ammo_type="9mm",
            ),
            Weapon(
                name="M24",
                category=AgencyType.FBI,
                description="بندقية قنص متوسطة تستخدم في إنقاذ الرهائن وحماية الشخصيات الهامة",
                fire_mode="Bolt-Action",
                magazine_size=5,
                ammo_type="7.62mm",
            ),
        ]

    @staticmethod
    def cia_weapons() -> List[Weapon]:
        return [
            Weapon(
                name="HK MP7 Suppressed",
                category=AgencyType.CIA,
                description="سلاح مكتوم مدمج لعمليات استخباراتية سرية",
                fire_mode="Auto",
                suppressor=True,
                magazine_size=30,
                ammo_type="4.6mm",
            ),
            Weapon(
                name="SIG P365",
                category=AgencyType.CIA,
                description="مسدس صغير مخفي تحت الملابس المدنية",
                fire_mode="Semi-Auto",
                magazine_size=12,
                ammo_type="9mm",
            ),
        ]

    @staticmethod
    def default_cuffs() -> List[Cuff]:
        return [
            Cuff(
                name="Standard Steel Handcuffs",
                description="قيود فولاذية ثقيلة مع نظام قفل مزدوج",
                agency=AgencyType.POLICE,
                blocked_actions=["open_inventory", "use_phone", "run"],
                lock_type="Double Lock",
            ),
            Cuff(
                name="Heavy-Duty Hinged Cuffs",
                description="قيود حديدية مفصلية تمنع حركة المعصم كلياً",
                agency=AgencyType.FBI,
                blocked_actions=["move_tactically", "unlock", "run"],
                lock_type="Hinged",
            ),
            Cuff(
                name="Tactical Zip Ties & Covert Cuffs",
                description="قيود بلاستيكية أو مرنة خفيفة للعمليات السرية",
                agency=AgencyType.CIA,
                blocked_actions=["signal", "escape", "use_tools"],
                lock_type="Covert",
            ),
        ]

    @staticmethod
    def default_facilities() -> List[Facility]:
        return [
            Facility(
                name="Police Headquarters",
                agency=AgencyType.POLICE,
                description="مركز الشرطة الرئيسي في وسط المدينة",
                sections=["بهو الاستقبال", "غرف التحقيق", "التوقيف المؤقت", "غرفة الأدلة"],
                security_level="High",
            ),
            Facility(
                name="FBI Regional Headquarters",
                agency=AgencyType.FBI,
                description="مقر المنطقة الفيدرالي يتضمن مركز عمليات ومختبر للطب الشرعي",
                sections=["War Room", "المختبر الجنائي", "مهبط المروحيات", "كراج السيارات"],
                security_level="Maximum",
            ),
            Facility(
                name="CIA Black Site",
                agency=AgencyType.CIA,
                description="منشأة سرية تحت الأرض مموهة بشكل كامل",
                sections=["الأبواب المخفية", "المقر السفلي", "أنفاق الهروب", "غرف التشفير"],
                security_level="Top Secret",
            ),
        ]
