from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://wordpress:wordpress@localhost:3307/wordpress"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()

def get_post_from_db(post_id: int):
    session = get_session()
    query = text("SELECT ID, post_title, post_content, post_status, post_type FROM wp_posts WHERE ID = :id")
    result = session.execute(query, {"id": post_id}).fetchone()
    session.close()
    return result

def get_comment_from_db(comment_id: int):
    session = get_session()
    query = text("""
        SELECT comment_ID, comment_post_ID, comment_content, comment_author, comment_approved
        FROM wp_comments
        WHERE comment_ID = :id
    """)
    result = session.execute(query, {"id": comment_id}).fetchone()
    session.close()
    return result

