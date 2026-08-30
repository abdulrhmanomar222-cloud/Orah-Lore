Orah-Lore - Realistic Life Simulation & Roleplay Game
Main Entry Point

لعبة الحياة الواقعية - محاكي حياة واقعي وتقمص أدوار
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui import run_game


def main():
    """Main entry point"""
    try:
        run_game()
    except KeyboardInterrupt:
        print("\n\n⚠️  تم إيقاف البرنامج بواسطة المستخدم.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ حدث خطأ: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
