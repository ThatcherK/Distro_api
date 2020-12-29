from flask.cli import FlaskGroup
from sqlalchemy import text

from app import create_app, db

app = create_app()
cli = FlaskGroup(create_app=create_app)


def drop_all_tables():
    """ drops all tables and sequences from a postgres database"""
    table_sql = """SELECT table_name FROM information_schema.tables
                    WHERE table_schema='public' AND table_type != 'VIEW' AND table_name NOT LIKE 'pg_ts_%%'
                """
    for table in [name for (name, ) in db.engine.execute(text(table_sql))]:
        try:
            db.engine.execute(text('DROP TABLE %s CASCADE' % table))
        except e:
            print(e)
@cli.command("recreate_db")
def recreate_db():
    drop_all_tables()
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    cli()