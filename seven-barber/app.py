import streamlit as st
from datetime import datetime, date
from gc_service import GoogleCalendar

# CONFIGURACIÓN
CREDENTIALS = "credentials.json"
CALENDAR_ID = "mariodanielq.p@gmail.com"   
gc = GoogleCalendar(CREDENTIALS, CALENDAR_ID)

# SERVICIOS
servicios_raw = [
    "Perfil de cejas con guillet y gel de afeitar - 1.00 USD",
    "Afeitado o Perfilación de barba - 3.00 USD",
    "Corte de cabello con maquina - 5.00 USD",
    "Corte de cabello con tijera - 5.00 USD",
    "Diseño freestyle - 7.00 USD",
    "VIP | Corte de cabello a máquina, tijera , perfilado de barba más bebida de cortesía- 8.00 USD",
    "Semi ondulados- 20.00 USD"
]
servicios = [servicio.split(" - ")[0] for servicio in servicios_raw]

# Barberos y horas disponibles
BARBEROS = ['Ariel', 'Josué']
HORAS_DISPONIBLES = [
    '09:00', '10:00', '11:00', '12:00',
    '14:00', '15:00', '16:00', '17:00',
    '18:00', '19:00', '20:00'
]

# INTERFAZ DE STREAMLIT
st.set_page_config(page_title="Reservación", layout="centered")
st.title("💈 Reservas Barbería Seven")

# Datos del formulario
nombre = st.text_input("Nombre del cliente")
barbero = st.selectbox("Selecciona tu barbero", BARBEROS)
fecha = st.date_input("Selecciona la fecha", min_value=date.today())

# Consultar disponibilidad de horas
if fecha:
    horas_ocupadas = gc.get_events_by_date(fecha, barbero)
    horas_libres = [h for h in HORAS_DISPONIBLES if h not in horas_ocupadas]

    if not horas_libres:
        st.warning("No hay horas disponibles para este barbero en la fecha seleccionada")
        st.stop()

    hora = st.selectbox("Selecciona la hora disponible", horas_libres)

# Confirmación de reserva
if st.button("Reservar"):
    if not nombre:
        st.error("Por favor, ingresa tu nombre.")
        st.stop()

    # Validación para no duplicar
    horas_ocupadas = gc.get_events_by_date(fecha, barbero)
    if hora in horas_ocupadas:
        st.error("⛔ Esta hora ya fue reservada. Actualiza la página.")
        st.stop()

    start_dt = f"{fecha}T{hora}:00"
    end_dt = f"{fecha}T{hora}:59"

    gc.create_event(
        title=f"Corte - {barbero}",
        description=f"Cliente: {nombre} | Servicios: {', '.join(servicios)}",
        start_dt=start_dt,
        end_dt=end_dt
    )

    st.success(f"✅ Reserva confirmada para {nombre} con {barbero} a las {hora}")
