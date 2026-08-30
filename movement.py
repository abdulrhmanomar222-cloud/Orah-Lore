Movement System
Orah-Lore - Realistic Life Simulation & Roleplay Game

نظام الحركة والمرونة الأساسية في العالم ثلاثي الأبعاد
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set


class MovementMode(Enum):
    """Movement behavior modes"""
    WALK = "المشي العادي"
    SPRINT = "الركض السريع"
    STEALTH = "التسلل"
    CROUCH = "الانحناء"
    PRONE = "الانطياح"
    FREE_LOOK = "الإلقاء الحر للنظر"


@dataclass
class MovementState:
    """Current movement state for the player"""
    mode: MovementMode = MovementMode.WALK
    direction: Dict[str, bool] = field(default_factory=lambda: {
        "forward": False,
        "backward": False,
        "left": False,
        "right": False,
    })
    sprint_active: bool = False
    jump_active: bool = False
    crouch_active: bool = False
    prone_active: bool = False
    free_look_active: bool = False
    stamina: int = 100
    stress: int = 0
    last_action: str = "الوقوف"
    lean_side: str = "center"
    camera_pitch: float = 0.0


@dataclass
class LanguageProfile:
    """Player language profile for RP servers and multilingual interaction."""
    primary_language: str = "العربية"
    known_languages: Set[str] = field(default_factory=lambda: {"العربية"})
    acquired_methods: Dict[str, str] = field(default_factory=dict)


class LanguageMechanic:
    """Language acquisition and speech rendering logic for RP interactions."""

    def __init__(self, profile: Optional[LanguageProfile] = None):
        self.profile = profile or LanguageProfile()

    def acquire_language(self, language: str, method: str = "training") -> bool:
        """Learn a new language and store how it was acquired."""
        if not language or not language.strip():
            return False

        self.profile.known_languages.add(language)
        self.profile.acquired_methods[language] = method
        return True

    def render_speech(
        self,
        text: str,
        speaker_language: str,
        listener_languages: Optional[Set[str] | List[str]] = None,
    ) -> str:
        """Render speech with language-aware output."""
        listener_languages = listener_languages or {self.profile.primary_language}
        listener_set = set(listener_languages)

        if speaker_language in listener_set:
            return text

        return f"*(يتحدث باللغة {speaker_language})*"


class MovementController:
    """Handles walking, sprinting, crouch, stealth, tactical actions and hybrid visuals."""

    def __init__(self):
        self.state = MovementState()

    def handle_key(self, key: str) -> MovementState:
        """Process keyboard presses for movement controls."""
        key_name = key.strip().lower()

        if key_name in {"w", "forward"}:
            self.state.direction["forward"] = True
            self.state.last_action = "التقدم للأمام"
            self._update_mode_from_activity()
            return self.state

        if key_name in {"s", "backward"}:
            self.state.direction["backward"] = True
            self.state.last_action = "التراجع للخلف"
            self._update_mode_from_activity()
            return self.state

        if key_name in {"a", "left"}:
            self.state.direction["left"] = True
            self.state.last_action = "التحرك إلى اليسار"
            self._update_mode_from_activity()
            return self.state

        if key_name in {"d", "right"}:
            self.state.direction["right"] = True
            self.state.last_action = "التحرك إلى اليمين"
            self._update_mode_from_activity()
            return self.state

        if key_name in {"shift", "leftshift"}:
            self.state.sprint_active = True
            self.state.mode = MovementMode.SPRINT
            self.state.last_action = "الركض السريع"
            self.state.stamina = max(0, self.state.stamina - 5)
            self.state.stress = min(100, self.state.stress + 4)
            return self.state

        if key_name in {"c", "ctrl", "leftctrl"}:
            self.state.mode = MovementMode.CROUCH
            self.state.crouch_active = True
            self.state.prone_active = False
            self.state.last_action = "المشي البطيء / الانحناء"
            return self.state

        if key_name == "space":
            self.state.jump_active = True
            self.state.last_action = "القفز / تجاوز العائق"
            return self.state

        if key_name == "alt":
            self.state.free_look_active = True
            self.state.mode = MovementMode.FREE_LOOK
            self.state.last_action = "التطلع الحر"
            return self.state

        if key_name in {"q", "e"}:
            self.lean("left" if key_name == "q" else "right")
            return self.state

        return self.state

    def release_key(self, key: str) -> MovementState:
        """Reset movement flags when a key is released."""
        key_name = key.strip().lower()

        if key_name in {"w", "forward"}:
            self.state.direction["forward"] = False
        elif key_name in {"s", "backward"}:
            self.state.direction["backward"] = False
        elif key_name in {"a", "left"}:
            self.state.direction["left"] = False
        elif key_name in {"d", "right"}:
            self.state.direction["right"] = False
        elif key_name in {"shift", "leftshift"}:
            self.state.sprint_active = False
            self.state.mode = MovementMode.WALK
            self.state.stamina = min(100, self.state.stamina + 8)
            self.state.stress = max(0, self.state.stress - 3)
        elif key_name in {"space"}:
            self.state.jump_active = False
        elif key_name in {"alt"}:
            self.state.free_look_active = False
            self.state.mode = MovementMode.WALK
        elif key_name in {"c", "ctrl", "leftctrl"}:
            self.state.crouch_active = False
            self.state.mode = MovementMode.WALK

        if not any(self.state.direction.values()) and not self.state.sprint_active:
            self.state.last_action = "الوقوف"

        return self.state

    def _update_mode_from_activity(self):
        """Adjust mode based on movement actions."""
        if self.state.sprint_active:
            self.state.mode = MovementMode.SPRINT
        elif self.state.crouch_active:
            self.state.mode = MovementMode.CROUCH
        elif self.state.prone_active:
            self.state.mode = MovementMode.PRONE
        elif self.state.free_look_active:
            self.state.mode = MovementMode.FREE_LOOK
        else:
            self.state.mode = MovementMode.WALK

    def slide(self, terrain: str = "ground") -> Dict[str, object]:
        """Sliding mechanic: quick crouch while sprinting."""
        if not self.state.sprint_active:
            return {
                "action": "slide",
                "distance_meters": 0.0,
                "terrain": terrain,
                "message": "يجب أن تكون في حالة ركض سريع لتفعيل الانزلاق"
            }

        terrain_factor = {
            "mountain": 1.8,
            "ground": 1.0,
            "wet": 0.8,
            "road": 0.7,
        }.get(terrain.lower(), 1.0)

        distance = round(3.0 * terrain_factor + 2.0, 2)
        self.state.crouch_active = True
        self.state.mode = MovementMode.CROUCH
        self.state.stamina = max(0, self.state.stamina - 30)
        self.state.last_action = "الانزلاق التكتيكي"

        return {
            "action": "slide",
            "distance_meters": distance,
            "terrain": terrain,
            "stamina_cost": 30,
            "message": "تم تنفيذ الانزلاق التكتيكي"
        }

    def lean(self, side: str) -> str:
        """Lean left/right to peek around cover while crouched."""
        side = side.strip().lower()
        if side not in {"left", "right", "center"}:
            side = "center"

        self.state.lean_side = side
        self.state.last_action = f"الميلان التكتيكي إلى {side}"
        return side

    def tactical_roll(self, direction: str = "forward") -> Dict[str, object]:
        """Roll and dodge while firing or moving."""
        distance = 3.5 if direction.lower() in {"forward", "right", "left", "backward"} else 2.0
        self.state.jump_active = True
        self.state.mode = MovementMode.WALK
        self.state.last_action = "الدحرجة التكتيكية"

        return {
            "action": "tactical_roll",
            "direction": direction,
            "distance_meters": round(distance, 2),
            "message": "تم تنفيذ الشقلبة التكتيكية وعودة الوضع إلى التصويب"
        }

    def get_control_guide(self) -> List[str]:
        """Return user-friendly movement instructions."""
        return [
            "W: التحرك إلى الأمام",
            "S: التحرك إلى الخلف",
            "A: التحرك إلى اليسار",
            "D: التحرك إلى اليمين",
            "Shift: الركض السريع / يستهلك الطاقة والإجهاد",
            "C أو Ctrl: المشي البطيء / الهدوء / التخفي",
            "Space: القفز أو تجاوز العقبات",
            "Alt: التطلع الحر مع الاحتفاظ باتجاه المشي",
            "Ctrl + movement: الانحناء والتسلل",
            "Shift + A/D/S/W + Space: الانطياح/الانقضاض الأرضي",
            "Ctrl أثناء الركض: الانزلاق التكتيكي لمسافة 3-6 أمتار",
            "Q / E: الميلان التكتيكي لرؤية ما خلف الجدار",
            "Right Click + W/A/S/D + Space: الشقلبة 360 درجة للدفع بعيداً عن الخطر",
        ]

    def get_hybrid_render_summary(self) -> str:
        """Return hybrid 3D/2D render description for the game world."""
        return (
            "العالم ثلاثية الأبعاد بالكامل: الشخصيات والمباني والمركبات والبيئة تُرسم ككائنات ثلاثية الأبعاد مع ظل، إضاءة، "
            "واحتكاك فيزيائي. أما واجهات المستخدم والهواتف والخريطة المصغرة وHUD فتُعرض كواجهة ثنائية الأبعاد واضحة، "
            "لتسهيل التعامل والقراءة. كما تُستخدم المؤثرات الجزيئية وبيلبواردينغ ثنائي الأبعاد لإضفاء عمق بصري على الدخان والنار والمياه."
        )

    def get_status_summary(self) -> str:
        """Return a human-readable movement summary."""
        return (
            f"الوضع: {self.state.mode.value} | "
            f"الركض: {'نشط' if self.state.sprint_active else 'متوقف'} | "
            f"القفز: {'نشط' if self.state.jump_active else 'غير نشط'} | "
            f"التطلع الحر: {'نشط' if self.state.free_look_active else 'غير نشط'} | "
            f"الميلان: {self.state.lean_side} | "
            f"الشدة: {self.state.stamina}%"
        )
