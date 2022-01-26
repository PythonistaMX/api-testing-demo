from apiflask import APIFlask
from project.models import db, Alumno, User
from project.blueprints import abc_alumnos
from project.auth.blueprints import auth_bp
from sqlalchemy import engine, inspect

def create_app():
    app = APIFlask(__name__)
    app.config.from_pyfile("settings.py")
    db.init_app(app)  
    @app.before_first_request
    def crea_bases():
        inspector = inspect(db.engine)
        if not inspector.has_table('alumno'):
            db.create_all()
            # Crea y llena la base de alumno.
            with open(app.config['PATH'] + "/../data/alumnos.txt", "rt") as f:
                alumnos = eval(f.read())
                for alumno in alumnos:
                    if Alumno.query.filter_by(cuenta=alumno["cuenta"]).first():
                        continue
                    else:
                        db.session.add(Alumno(**alumno))
                db.session.commit()
            if not User.query.filter_by(username="admin"):
                user = User(username='admin', email='example@example.com',password='admin', active=True)
                db.session.add(user)
                db.session.commit() 
    app.register_blueprint(abc_alumnos, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)