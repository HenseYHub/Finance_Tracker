from database import Base, engine, SessionLocal
from models import Expense
from datetime import datetime

# Создание таблиц
def init_db():
    print("⏳ Создание таблиц...")
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы успешно созданы!")

# Добавление примеров расходов
def seed_data():
    print("🌱 Добавление тестовых данных...")
    db = SessionLocal()
    db.add_all([
        Expense(title="Кофе", amount=3.5, category="Еда", date=datetime.utcnow()),
        Expense(title="Метро", amount=1.2, category="Транспорт", date=datetime.utcnow()),
        Expense(title="Фрукты", amount=4.0, category="Еда", date=datetime.utcnow()),
        Expense(title="Книги", amount=10.0, category="Образование", date=datetime.utcnow())
    ])
    db.commit()
    db.close()
    print("✅ Примеры добавлены!")

if __name__ == "__main__":
    init_db()
    seed_data()
