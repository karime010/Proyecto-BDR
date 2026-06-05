import flet as ft
import mysql.connector
import bcrypt
import os


# =========================
# CONEXIÓN MYSQL
# =========================
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="escuela"
)
cursor = conn.cursor()


# =========================
# APP PRINCIPAL
# =========================
def main(page: ft.Page):

    page.title = "Sistema CRUD Alumnos"
    page.bgcolor = ft.Colors.BLUE_GREY_50

    # =========================
    # VARIABLES
    # =========================
    login_user = ft.TextField(label="Usuario")
    login_pass = ft.TextField(label="Contraseña", password=True)

    matricula = ft.TextField(label="Matrícula")
    ap_pat = ft.TextField(label="Apellido Paterno")
    ap_mat = ft.TextField(label="Apellido Materno")
    nombres = ft.TextField(label="Nombres")
    curp = ft.TextField(label="CURP")
    especialidad = ft.TextField(label="Especialidad")
    telefono = ft.TextField(label="Teléfono")
    ciudad = ft.TextField(label="Ciudad")
    estado = ft.TextField(label="Estado")
    disciplinas = ft.TextField(label="Disciplinas")

    foto_path = ft.Text("Sin foto")

    mensaje = ft.Text()

    # =========================
    # LOGIN
    # =========================
    def login(e):
        cursor.execute("SELECT password FROM usuarios WHERE usuario=%s", (login_user.value,))
        user = cursor.fetchone()

        if not user:
            mensaje.value = "Usuario no existe"
            page.update()
            return

        if bcrypt.checkpw(login_pass.value.encode(), user[0].encode()):
            page.clean()
            page.add(crud_view())
        else:
            mensaje.value = "Contraseña incorrecta"
            page.update()

    # =========================
    # REGISTRAR ALUMNO
    # =========================
    def guardar(e):
        if not matricula.value:
            mensaje.value = "Matrícula obligatoria"
            page.update()
            return

        sql = """
        INSERT INTO alumnos VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            matricula.value,
            ap_pat.value,
            ap_mat.value,
            nombres.value,
            curp.value.upper(),
            especialidad.value,
            telefono.value,
            ciudad.value,
            estado.value,
            disciplinas.value,
            foto_path.value
        )

        cursor.execute(sql, values)
        conn.commit()

        mensaje.value = "Alumno guardado"
        page.update()
        consultar(None)

    # =========================
    # CONSULTAR
    # =========================
    def consultar(e):
        lista.controls.clear()

        cursor.execute("SELECT matricula, nombres, ap_paterno FROM alumnos")
        for m, n, ap in cursor.fetchall():
            lista.controls.append(
                ft.ListTile(
                    title=ft.Text(m),
                    subtitle=ft.Text(f"{n} {ap}")
                )
            )
        page.update()

    # =========================
    # ELIMINAR
    # =========================
    def eliminar(e):
        cursor.execute("DELETE FROM alumnos WHERE matricula=%s", (matricula.value,))
        conn.commit()
        mensaje.value = "Eliminado"
        page.update()
        consultar(None)

    # =========================
    # SUBIR FOTO (SIMPLIFICADO)
    # =========================
    def subir_foto(e):
        if e.files:
            file = e.files[0]
            ruta = f"uploads/{file.name}"
            os.makedirs("uploads", exist_ok=True)
            with open(ruta, "wb") as f:
                f.write(file.read())
            foto_path.value = ruta
            page.update()

    file_picker = ft.FilePicker(on_result=subir_foto)
    page.overlay.append(file_picker)

    # =========================
    # LISTA
    # =========================
    lista = ft.Column(scroll=ft.ScrollMode.AUTO)

    # =========================
    # VISTA CRUD
    # =========================
    def crud_view():
        return ft.Column([
            ft.Text("CRUD ALUMNOS", size=25, weight="bold"),

            matricula,
            ap_pat,
            ap_mat,
            nombres,
            curp,
            especialidad,
            telefono,
            ciudad,
            estado,
            disciplinas,

            ft.ElevatedButton("Subir foto", on_click=lambda _: file_picker.pick_files()),
            foto_path,

            ft.Row([
                ft.ElevatedButton("Guardar", on_click=guardar),
                ft.ElevatedButton("Consultar", on_click=consultar),
                ft.ElevatedButton("Eliminar", on_click=eliminar),
            ]),

            mensaje,
            lista
        ])

    # =========================
    # LOGIN UI
    # =========================
    page.add(
        ft.Column([
            ft.Text("LOGIN", size=30),
            login_user,
            login_pass,
            ft.ElevatedButton("Entrar", on_click=login),
            mensaje
        ])
    )


ft.app(target=main)