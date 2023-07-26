"""Módulo de gestión de alumnos"""


from apiflask import APIBlueprint, abort
from src.project.auth import login_required
from src.project.models import db, Alumno
from src.project.schemas import AlumnoSchema, AlumnoInSchema

abc_alumnos = APIBlueprint('Gestión de alumnos', __name__)


@abc_alumnos.get("/alumnos")
@abc_alumnos.output(AlumnoSchema(many=True))
def vuelca_base() -> list[Alumno]:
    """Devuelve todos los alumnos"""
    return Alumno.query.all()


@abc_alumnos.get("/<int:cuenta>")
@abc_alumnos.output(AlumnoSchema)
def despliega_alumno(cuenta: int) -> Alumno:
    """Devuelve un alumno al ingresar su cuenta"""
    return Alumno.query.get_or_404(cuenta)


@abc_alumnos.delete("/<int:cuenta>")
@abc_alumnos.output({}, 200)
@login_required
def elimina_alumno(cuenta: int) -> None:
    alumno = Alumno.query.get_or_404(cuenta)
    db.session.delete(alumno)
    db.session.commit()
    return None


@abc_alumnos.post("/<int:cuenta>")
@abc_alumnos.output(AlumnoSchema, status_code=201)
@abc_alumnos.input(AlumnoInSchema)
def crea_alumno(cuenta: int, data: dict) -> Alumno:
    if Alumno.query.filter_by(cuenta=cuenta).first():
        abort(409)
    else:
        data["cuenta"] = cuenta
        alumno = Alumno(**AlumnoSchema().load(data))
        db.session.add(alumno)
        db.session.commit()
        return alumno, 201


@abc_alumnos.put("/<int:cuenta>")
@abc_alumnos.output(AlumnoSchema)
@abc_alumnos.input(AlumnoInSchema)
def sustituye_alumno(cuenta: int, data: dict) -> Alumno:
    alumno = Alumno.query.get_or_404(cuenta)
    db.session.delete(alumno)
    data["cuenta"] = cuenta
    nuevo_alumno = Alumno(**data)
    db.session.add(nuevo_alumno)
    db.session.commit()
    return nuevo_alumno
