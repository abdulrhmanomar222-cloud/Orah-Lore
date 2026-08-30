"""
Orah-Lore - Realistic Life Simulation & Roleplay Game
Vercel Serverless Web Entry Point
"""

import os
import sys

# إضافة المسار الحالي
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    try:
        # هنا يتم استدعاء منطق اللعبة
        return jsonify(
            {
                "status": "success",
                "message": "Orah-Lore Game Server is Running!",
                "game": "لعبة الحياة الواقعية - محاكي حياة واقعي وتقمص أدوار",
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# هذا المتغير هو ما يبحث عنه Vercel لتشغيل التطبيق
app = app

if __name__ == "__main__":
    app.run(debug=True)
