import streamlit as st
from datetime import date
from gc_service import GoogleCalendar
from streamlit_option_menu import option_menu

# ================= CONFIG =================
CREDENTIALS = "credentials.json"
CALENDAR_ID = "mariodanielq.p@gmail.com"
gc = GoogleCalendar(CREDENTIALS, CALENDAR_ID)

BARBEROS = ['Ariel', 'Josué']
HORAS_DISPONIBLES = [
    '09:00','10:00','11:00','12:00',
    '14:00','15:00','16:00','17:00',
    '18:00','19:00','20:00'
]

servicios = [
    ("Perfil de cejas", "Guillet + gel de afeitar", "$1.00"),
    ("Afeitado / Barba", "Perfilación profesional", "$3.00"),
    ("Corte máquina", "Corte rápido y limpio", "$5.00"),
    ("Corte tijera", "Trabajo detallado", "$5.00"),
    ("Diseño freestyle", "Diseño personalizado", "$7.00"),
    ("VIP", "Corte completo + barba + bebida", "$8.00"),
    ("Semi ondulados", "Ondulado completo", "$20.00")
]

# ================= PAGE =================
st.set_page_config(
    page_title="Barbería Seven",
    page_icon="💈",
    layout="centered"
)

# ================= CSS =================
with open("styles/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ================= HEADER =================
st.image("assets/barberia.jpg")
st.title("Barbería Seven")
st.text("Av. Unidad Nacional | Carabobo | Estación")

# ================= MENU =================
selected = option_menu(
    menu_title=None,
    options=[
        "Portafolio",
        "Servicios",
        "Reservar",
        "Reseñas",
        "Detalles"
    ],
    icons=["image", "scissors", "calendar", "chat", "geo-alt"],
    orientation="horizontal",
)

# ================= PORTAFOLIO =================
if selected == "Portafolio":
    cols = st.columns(2)
    cols[0].image("assets/corte-1-josue.jpg", caption="Degradado profesional")
    cols[1].image("assets/corte-josue-3.jpg", caption="Corte + barba")

# ================= SERVICIOS =================
elif selected == "Servicios":
    st.subheader("Nuestros servicios")

    cols = st.columns(2)
    for i, s in enumerate(servicios):
        with cols[i % 2]:
            st.markdown(
                f"""
                <div class="service-card">
                    <h4>✂️ {s[0]}</h4>
                    <p>{s[1]}</p>
                    <span>{s[2]}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

# ================= RESERVAR =================
elif selected == "Reservar":
    st.subheader("Reserva tu cita")

    nombre = st.text_input("Nombre del cliente")
    barbero = st.selectbox("Selecciona tu barbero", BARBEROS)
    fecha = st.date_input("Selecciona la fecha", min_value=date.today())

    if fecha:
        horas_ocupadas = gc.get_events_by_date(fecha, barbero)
        horas_libres = [h for h in HORAS_DISPONIBLES if h not in horas_ocupadas]

        if horas_libres:
            hora = st.selectbox("Selecciona la hora", horas_libres)
        else:
            st.warning("No hay horas disponibles")
            st.stop()

    if st.button("Reservar"):
        if not nombre:
            st.error("Ingresa tu nombre")
            st.stop()

        start_dt = f"{fecha}T{hora}:00"
        end_dt = f"{fecha}T{hora}:59"

        gc.create_event(
            title=f"Corte - {barbero}",
            description=f"Cliente: {nombre}",
            start_dt=start_dt,
            end_dt=end_dt
        )

        st.success(f"✅ Reserva confirmada para {nombre} con {barbero} a las {hora}")

# ================= RESEÑAS =================
elif selected == "Reseñas":
    st.subheader("Opiniones de clientes")
    st.write("⭐️⭐️⭐️⭐️⭐️ Excelente servicio")
    st.write("⭐️⭐️⭐️⭐️⭐️ Cortes de calidad")
    st.write("⭐️⭐️⭐️⭐️⭐️ Muy recomendado")

# ================= DETALLES =================
elif selected == "Detalles":
    st.image("assets/map.jpg")
    st.markdown(
        "[📍 Ver ubicación en Google Maps](https://www.google.com/maps)"
        "[Desarrollado Monkey Computer &2025](https://www.google.com/maps)"
    )

    st.subheader("Barberos")
    col1, col2 = st.columns(2)
    col1.image("assets/barber1.png", caption="Ariel")
    col2.image("assets/barber2.png", caption="Josué")

    st.subheader("Horario y contacto")
    st.write("🕘 Lunes a Domingo: 09:00 – 20:00")
    st.write("📞 654 789 123")
