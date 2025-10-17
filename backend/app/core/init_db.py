from sqlalchemy.orm import Session
from app.core.database import engine, Base, SessionLocal
from app.core.security import hash_password
from app.models import User, Chat, Message, Transcript, GenderEnum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db() -> None:
    try:
        from app.models import User, Chat, Message, Transcript

        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")

    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def create_admin_user(db: Session, email: str, password: str, name: str = "Admin") -> User:
    try:
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            logger.info(f"Admin user with email {email} already exists")
            return existing_user

        hashed_password = hash_password(password)
        admin_user = User(
            name=name,
            email=email,
            hashed_password=hashed_password,
            is_admin=True
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        logger.info(f"Admin user created successfully with email: {email}")
        return admin_user

    except Exception as e:
        logger.error(f"Error creating admin user: {e}")
        db.rollback()
        raise


def seed_initial_data(db: Session) -> None:
    try:
        logger.info("Seeding initial data...")

        create_admin_user(
            db=db,
            email="howchromium@gmail.com",
            password="admin123",
            name="System Admin"
        )

        logger.info("Initial data seeded successfully!")

    except Exception as e:
        logger.error(f"Error seeding initial data: {e}")
        raise


def main(seed_data: bool = True):
    logger.info("Starting database initialization...")

    init_db()

    if seed_data:
        db = SessionLocal()
        try:
            seed_initial_data(db)
        except Exception as e:
            logger.warning(f"Failed to seed initial data: {e}")
            logger.info("Continuing without seeding data...")
        finally:
            db.close()

    logger.info("Database initialization completed!")


if __name__ == "__main__":
    import sys
    seed = "--no-seed" not in sys.argv
    main(seed_data=seed)
