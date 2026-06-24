"""
=====================================================================
 Flujo de Caja Proyectado
 ConfiguroWeb · 2026 · Python real en el navegador (PyScript)
=====================================================================
"""
from pyscript import document, window
from js import localStorage
import json
import math

APP_CLAVE = "python_flujo_caja_proyectado_datos"
VERSION = "1.0.0"


# =====================================================================
#  Lógica de negocio
# =====================================================================
class Calculadora:
    """Modelo de cálculo de Flujo de Caja Proyectado."""

    def __init__(self, ingresos, egresos, meses):
        self.ingresos = float(ingresos)
        self.egresos = float(egresos)
        self.meses = float(meses)

    def calcular(self):
        """Ejecuta el cálculo principal y devuelve un dict de resultados."""

        flujo = self.ingresos - self.egresos
        proyectado = flujo * self.meses
        return {"flujo": flujo, "proyectado": proyectado}


    def diagnostico(self, resultados):
        """Texto explicativo del resultado."""

        if resultados["flujo"] < 0:
            return "❌ Flujo negativo. Estás perdiendo dinero cada mes."
        return "✅ Flujo positivo. Acumulas caja."



# =====================================================================
#  Formateadores
# =====================================================================
def fmt_moneda(v):
    if v is None:
        return "—"
    if math.isinf(v):
        return "∞"
    return f"${v:,.0f}"

def fmt_num(v):
    if v is None:
        return "—"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}"

def fmt_pct(v):
    if v is None:
        return "—"
    return f"{v:.1f}%"


# =====================================================================
#  Persistencia localStorage
# =====================================================================
def cargar_guardado():
    try:
        raw = localStorage.getItem(APP_CLAVE)
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None

def guardar_ls(datos):
    try:
        localStorage.setItem(APP_CLAVE, json.dumps(datos))
        return True
    except Exception:
        return False


# =====================================================================
#  UI helpers
# =====================================================================
def input_float(eid):
    el = document.querySelector(f"#{eid}")
    if not el or not el.value:
        return 0.0
    try:
        return float(el.value)
    except (ValueError, TypeError):
        return 0.0

def mostrar(html, clase=""):
    caja = document.querySelector("#resultado")
    caja.innerHTML = html
    caja.classList.remove("hidden", "is-error", "is-success")
    if clase:
        caja.classList.add(clase)


# =====================================================================
#  Handlers
# =====================================================================
def calcular_handler(event=None):
    """Lee inputs, instancia, calcula y muestra."""

    c = Calculadora(input_float("ingresos"), input_float("egresos"), input_float("meses"))
    r = c.calcular()
    html = f"""
      <div class="result-value">💵 Flujo mensual: {fmt_moneda(r["flujo"])}</div>
      <p class="result-detail">Proyección {int(c.meses)} meses: {fmt_moneda(r["proyectado"])}</p>
      <p class="result-detail">{c.diagnostico(r)}</p>
    """
    mostrar(html, clase="is-success")



def guardar_datos(event=None):
    datos = {
            "ingresos": input_float("ingresos"),
            "egresos": input_float("egresos"),
            "meses": input_float("meses"),
        "version": VERSION,
    }
    ok = guardar_ls(datos)
    if ok:
        mostrar("💾 Datos guardados en este navegador.", clase="is-success")
    else:
        mostrar("❌ No se pudieron guardar los datos.", clase="is-error")


def cargar_al_inicio():
    datos = cargar_guardado()
    if not datos:
        return
    try:
            if "ingresos" in datos:
                document.querySelector("#ingresos").value = datos["ingresos"]
            if "egresos" in datos:
                document.querySelector("#egresos").value = datos["egresos"]
            if "meses" in datos:
                document.querySelector("#meses").value = datos["meses"]
        aviso = document.querySelector("#resultado")
        aviso.innerHTML = "📂 Datos cargados. Pulsa <em>Calcular</em>."
        aviso.classList.remove("hidden")
    except Exception:
        pass


def inicializar():
    cargar_al_inicio()
    window.dispatchEvent(window.Event.new("py:ready"))

inicializar()
