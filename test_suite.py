#!/usr/bin/env python3
"""
Test Suite - مجموعة اختبارات النظام
Orah-Lore - Character Creation System Tests
"""

import sys
import os
from datetime import datetime, timedelta
from models import (
    Character, Identity, Appearance, Clothing, VitalStats,
    Gender, EyeColor, HairColor, SkinTone
)
from character_creator import CharacterCreator
from database import CharacterDatabase, SessionManager
from movement import MovementController, MovementMode, LanguageMechanic, LanguageProfile
from weapons import Weapon, Cuff, Facility, AgencyType

def print_test_header(title):
    """طباعة رأس الاختبار"""
    print(f"\n{'='*70}")
    print(f"🧪 {title}")
    print(f"{'='*70}\n")

def test_models():
    """اختبار نماذج البيانات"""
    print_test_header("اختبار نماذج البيانات - Models Test")
    
    try:
        # إنشاء هوية
        identity = Identity(
            full_name="محمد أحمد",
            first_name="محمد",
            last_name="أحمد",
            birth_date="1995-05-15",
            id_number="1234567890",
            phone_number="0501234567"
        )
        print(f"✅ هوية تم إنشاؤها بنجاح")
        print(f"   الاسم: {identity.full_name}")
        print(f"   العمر: {identity.get_age()} سنة")
        
        # إنشاء مظهر
        appearance = Appearance(
            gender=Gender.MALE,
            age=28,
            height=170,
            weight=75,
            eye_color=EyeColor.BROWN,
            hair_color=HairColor.BLACK,
            hair_style="قصير",
            skin_tone=SkinTone.MEDIUM,
            facial_hair="شارب خفيف"
        )
        print(f"✅ مظهر تم إنشاؤه بنجاح")
        print(f"   الجنس: {appearance.gender.value}")
        print(f"   الطول: {appearance.height} سم")
        print(f"   الوزن: {appearance.weight} كجم")
        
        # إنشاء ملابس
        clothing = Clothing(
            shirt="قميص أبيض",
            pants="جينز أزرق",
            shoes="حذاء رياضي"
        )
        print(f"✅ ملابس تم إنشاؤها بنجاح")
        print(f"   الأعلى: {clothing.shirt}")
        print(f"   السفلى: {clothing.pants}")
        
        # إنشاء مؤشرات حيوية
        vital_stats = VitalStats()
        print(f"✅ مؤشرات حيوية تم إنشاؤها بنجاح")
        print(f"   الصحة: {vital_stats.health}%")
        print(f"   الجوع: {vital_stats.hunger}%")
        
        # إنشاء شخصية كاملة
        character = Character(
            identity=identity,
            appearance=appearance,
            clothing=clothing,
            vital_stats=vital_stats,
            cash=7500.50
        )
        print(f"✅ شخصية كاملة تم إنشاؤها بنجاح")
        print(f"   المعرف: {character.character_id}")
        print(f"   الأموال: ${character.cash}")
        
        # اختبار التحويل إلى dict
        char_dict = character.to_dict()
        print(f"✅ تحويل إلى dict بنجاح")
        print(f"   عدد المفاتيح: {len(char_dict)}")
        
        # اختبار التحويل من dict
        character2 = Character.from_dict(char_dict)
        print(f"✅ تحويل من dict بنجاح")
        print(f"   الأموال (المسترجعة): ${character2.cash}")
        
        print(f"\n✨ جميع اختبارات النماذج نجحت!")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار النماذج: {e}")
        return False

def test_database():
    """اختبار قاعدة البيانات"""
    print_test_header("اختبار قاعدة البيانات - Database Test")
    
    try:
        db = CharacterDatabase()
        print(f"✅ قاعدة البيانات تم فتحها بنجاح")
        
        # إنشاء شخصية اختبار
        identity = Identity(
            full_name="شخصية اختبار",
            first_name="اختبار",
            last_name="شخصية",
            birth_date="2000-01-01",
            id_number="9999999999",
            phone_number="0509999999"
        )
        
        character = Character(
            identity=identity,
            appearance=Appearance(
                gender=Gender.FEMALE,
                age=20,
                height=165,
                weight=60,
                eye_color=EyeColor.GREEN,
                hair_color=HairColor.BLONDE,
                hair_style="طويل",
                skin_tone=SkinTone.LIGHT,
                facial_hair="لا يوجد"
            ),
            clothing=Clothing(
                shirt="فستان",
                pants="جينز",
                shoes="حذاء"
            ),
            cash=5000
        )
        print(f"✅ شخصية اختبار تم إنشاؤها")
        
        # حفظ الشخصية
        char_id = character.character_id
        db.save_character(character)
        print(f"✅ شخصية تم حفظها في قاعدة البيانات")
        
        # التحقق من وجود الشخصية
        exists = db.character_exists(char_id)
        print(f"✅ التحقق من وجود الشخصية: {exists}")
        
        # تحميل الشخصية
        loaded_char = db.load_character(char_id)
        print(f"✅ شخصية تم تحميلها من قاعدة البيانات")
        print(f"   الاسم: {loaded_char.identity.full_name}")
        print(f"   الأموال: ${loaded_char.cash}")
        
        # عدد الشخصيات
        count = db.get_character_count()
        print(f"✅ عدد الشخصيات: {count}")
        
        # الحصول على إحصائيات
        stats = db.get_statistics()
        print(f"✅ إحصائيات قاعدة البيانات:")
        print(f"   إجمالي الشخصيات: {stats['total_characters']}")
        print(f"   إصدار قاعدة البيانات: {stats['database_version']}")
        
        # حذف الشخصية (تنظيف)
        db.delete_character(char_id)
        print(f"✅ شخصية الاختبار تم حذفها")
        
        print(f"\n✨ جميع اختبارات قاعدة البيانات نجحت!")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار قاعدة البيانات: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_session_manager():
    """اختبار مدير الجلسات"""
    print_test_header("اختبار مدير الجلسات - Session Manager Test")
    
    try:
        db = CharacterDatabase()
        session_mgr = SessionManager(db)
        print(f"✅ مدير الجلسات تم إنشاؤه بنجاح")
        
        # إنشاء شخصية اختبار
        character = Character(
            identity=Identity(
                full_name="اختبار جلسة",
                first_name="جلسة",
                last_name="اختبار",
                birth_date="2000-01-01",
                id_number="8888888888",
                phone_number="0508888888"
            ),
            appearance=Appearance(
                gender=Gender.MALE,
                age=25,
                height=175,
                weight=80,
                eye_color=EyeColor.BLUE,
                hair_color=HairColor.BROWN,
                hair_style="متوسط",
                skin_tone=SkinTone.MEDIUM,
                facial_hair="شارب"
            ),
            clothing=Clothing(
                shirt="قميص أزرق",
                pants="جينز أسود",
                shoes="حذاء رياضي"
            ),
            cash=10000
        )
        
        char_id = character.character_id
        saved = db.save_character(character)
        if not saved:
            raise Exception("Failed to save test character")
        print(f"✅ شخصية الجلسة تم حفظها")
        
        # بدء جلسة
        started = session_mgr.start_session(char_id)
        if not started:
            raise Exception("Failed to start session")
        
        current = session_mgr.get_current_character()
        if current is None:
            raise Exception("Current character is None after start_session")
        print(f"✅ جلسة بدأت")
        print(f"   الشخصية الحالية: {current.identity.full_name}")
        
        # محاكاة اللعب
        current.cash -= 500
        print(f"✅ محاكاة اللعب (إنفاق 500 دولار)")
        
        # نهاية الجلسة
        session_mgr.end_session()
        print(f"✅ جلسة انتهت")
        
        # تحميل الشخصية والتحقق من الحفظ
        saved_char = db.load_character(char_id)
        print(f"✅ التحقق من الحفظ:")
        print(f"   الأموال بعد الجلسة: ${saved_char.cash}")
        
        # تنظيف
        db.delete_character(char_id)
        print(f"✅ شخصية الاختبار تم حذفها")
        
        print(f"\n✨ جميع اختبارات مدير الجلسات نجحت!")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار مدير الجلسات: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_movement_system():
    """اختبار نظام الحركة والتفاعل"""
    print_test_header("اختبار نظام الحركة - Movement System Test")

    try:
        controller = MovementController()
        print("✅ تم إنشاء نظام الحركة بنجاح")

        controller.handle_key('W')
        controller.handle_key('Shift')
        controller.handle_key('C')
        controller.handle_key('Space')

        print(f"✅ الوضع الحالي: {controller.state.mode.value}")
        print(f"✅ قدرة الركض: {controller.state.sprint_active}")
        print(f"✅ حالة القفز: {controller.state.jump_active}")

        guide = controller.get_control_guide()
        if len(guide) < 6:
            raise Exception("Movement guide is unexpectedly short")
        print(f"✅ دليل التحكم تم إنشاؤه بنجاح ({len(guide)} عناصر)")

        hybrid_summary = controller.get_hybrid_render_summary()
        if 'ثلاثية الأبعاد' not in hybrid_summary or 'ثنائية الأبعاد' not in hybrid_summary:
            raise Exception("Hybrid render summary missing 3D/2D descriptors")
        print("✅ ملخص العرض الهجين متاح")

        print(f"\n✨ جميع اختبارات نظام الحركة نجحت!")
        return True
    except Exception as e:
        print(f"❌ خطأ في اختبار نظام الحركة: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_advanced_movement_and_languages():
    """اختبار الحركات التكتيكية المتقدمة واللغات"""
    print_test_header("اختبار الحركات التكتيكية واللغات - Advanced Movement & Languages Test")

    try:
        controller = MovementController()
        controller.state.sprint_active = True
        controller.state.stamina = 100
        controller.state.crouch_active = True
        slide = controller.slide(terrain="mountain")
        print(f"✅ الانزلاق تم بنجاح: {slide['distance_meters']} متر")

        controller.lean("right")
        print(f"✅ الميلان الجانبي: {controller.state.lean_side}")

        roll = controller.tactical_roll("forward")
        print(f"✅ الشقلبة: {roll['action']} / {roll['distance_meters']} متر")

        profile = LanguageProfile(primary_language="العربية")
        profile.known_languages = {"العربية", "الإسبانية"}
        mechanic = LanguageMechanic(profile)
        mechanic.acquire_language("الإسبانية", method="training")
        spoken = mechanic.render_speech("Hola amigo", speaker_language="الإسبانية", listener_languages={"العربية"})
        print(f"✅ ترجمة الكلام: {spoken}")

        print(f"\n✨ جميع اختبارات الحركات واللغات نجحت!")
        return True
    except Exception as e:
        print(f"❌ خطأ في اختبار الحركات واللغات: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_weapons_and_facilities():
    """اختبار الأسلحة والمقرات الأمنية والاستخباراتية"""
    print_test_header("اختبار الأسلحة والمقرات - Weapons & Facilities Test")

    try:
        weapon = Weapon(
            name="AR-15",
            category=AgencyType.MILITARY,
            description="بندقية هجومية للشرطة والدوريات",
            fire_mode="Semi-Auto",
            suppressor=False,
        )
        cuff = Cuff(
            name="Standard Steel Handcuffs",
            description="قيود فولاذية مع قفل مزدوج",
            blocked_actions=["open_inventory", "use_phone", "run"],
            agency=AgencyType.POLICE,
        )
        facility = Facility(
            name="Police Headquarters",
            agency=AgencyType.POLICE,
            description="مركز الشرطة الرئيسي في وسط المدينة",
            sections=["بهو الاستقبال", "غرف التحقيق", "التوقيف المؤقت"],
        )

        print(f"✅ السلاح: {weapon.name} / {weapon.category.value}")
        print(f"✅ الكلبشة: {cuff.name} / {len(cuff.blocked_actions)} قيود")
        print(f"✅ المقر: {facility.name} / {len(facility.sections)} أقسام")
        print(f"✅ تفاصيل المقر: {facility.full_summary()}")
        print(f"\n✨ جميع اختبارات الأسلحة والمقرات نجحت!")
        return True
    except Exception as e:
        print(f"❌ خطأ في اختبار الأسلحة والمقرات: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """تشغيل جميع الاختبارات"""
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                  🧪 3D Land Bot - Test Suite 🧪                           ║
║                                                                            ║
║               مجموعة اختبارات نظام إنشاء الشخصيات                          ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    results = {
        "Models": test_models(),
        "Database": test_database(),
        "Sessions": test_session_manager(),
        "Movement": test_movement_system(),
        "Advanced": test_advanced_movement_and_languages(),
        "Weapons": test_weapons_and_facilities()
    }
    
    # الخلاصة
    print("\n" + "="*70)
    print("📊 ملخص الاختبارات - Test Summary")
    print("="*70 + "\n")
    
    for test_name, result in results.items():
        status = "✅ نجح" if result else "❌ فشل"
        print(f"{test_name:20} {status}")
    
    total = sum(results.values())
    print(f"\n✨ النتيجة النهائية: {total}/{len(results)} اختبارات نجحت")
    
    if total == len(results):
        print("\n🎉 جميع الاختبارات نجحت! اللعبة جاهزة للتشغيل!\n")
        return 0
    else:
        print(f"\n⚠️  بعض الاختبارات فشلت. يرجى التحقق من الأخطاء أعلاه.\n")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
