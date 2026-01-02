import sys
import os

# إضافة مجلد DevMido إلى مسار البحث عن الملفات
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'DevMido')))

from bot import run_bot

if __name__ == "__main__":
    run_bot()
