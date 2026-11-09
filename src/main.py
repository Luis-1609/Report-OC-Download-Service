import os
import logging
# pyrefly: ignore [missing-import]
from playwright.sync_api import Playwright, sync_playwright, expect



# CONSTANTES NECESARIAS PARA CENTURIA_EXPORT.PY
import tempfile
from pathlib import Path

logger = logging.getLogger("ReportOCDownloadService")

# Código para capturar valores del .env
def cargar_env(ruta_env=".env"):
    if os.path.exists(ruta_env):
        with open(ruta_env, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                # Ignorar líneas vacías y comentarios
                if linea and not linea.startswith("#"):
                    if "=" in linea:
                        clave, valor = linea.split("=", 1)
                        # Limpiar espacios y comillas
                        clave = clave.strip()
                        valor = valor.strip().strip('"').strip("'")
                        os.environ[clave] = valor

# Cargamos el archivo .env que está en el mismo directorio
cargar_env()

USUARIO = os.getenv("TEST_USERNAME")
PASSWORD = os.getenv("TEST_PASSWORD")
#SHEET_CONSULTA = os.getenv("SPREADSHEET_ID")

#WORKSHEET_NAME = os.getenv("WORKSHEET_NAME")


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
            headless=False,
            slow_mo=100, # Da tiempo a que las animaciones y menús de Centuria abran correctamente
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="es-PE", # Configuración cultural peruana para asegurar el formato de fechas y números
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    page.goto("https://centuria.pucp.edu.pe/")

    ## LOGIN
    page.locator("span").nth(1).click()
    page.locator("span").nth(3).click()
    page.get_by_role("textbox", name="Ingrese su usuario").click()
    page.get_by_role("textbox", name="Ingrese su usuario").fill(USUARIO)
    page.get_by_role("textbox", name="Ingrese su contraseña aquí").click()
    page.get_by_role("textbox", name="Ingrese su contraseña aquí").fill(PASSWORD)
    page.get_by_role("button", name="INGRESAR").click()

    ## Acaba el Login 
    #PUCP_PO_CONSULTA_IMPORTES_PEDI
    ## NAVEGACIÓN
    logger.info("Haciendo clic en 'Menú Principal : Menú Bú'...")
    page.get_by_text("Menú Principal : Menú Bú").click(force=True)
    page.locator("#PT_REPORTING_TOOLS > .pthnavrightarrow").click()
    page.locator("#PT_QUERY > .pthnavrightarrow").click()
    page.locator("#crefli_PT_QUERY_VIEWER_GBL").click() #acá se navega al visor de consultas, de donde sale el reporte
    ##

    ## En el visor de consultas
    page.locator("iframe[name=\"TargetContent\"]").content_frame.locator("#QRY_VIEWERS_WRK_QRYSEARCHTEXT254").fill("PUCP_PO_CONSULTA_IMPORTES_PEDI")
    page.locator("iframe[name=\"TargetContent\"]").content_frame.get_by_role("button", name="Buscar").click()
    with page.expect_popup() as page1_info:
        page.locator("iframe[name=\"TargetContent\"]").content_frame.get_by_role("link", name="Excel", exact=True).click()
    
    ## Se abre la pestaña nueva
    page1 = page1_info.value
    page1.get_by_role("textbox", name="Unidad de Negocio Compras:").fill("PO001")
    page1.get_by_role("textbox", name="Fecha Inicial:").fill("01/11/2026") # LA FECHA INICIO Y FIN DEBEN SER VARIABLES AUTOCALCULABLES
    page1.get_by_role("textbox", name="Fecha Final:").fill("08/11/2026")   # LA FECHA INICIO Y FIN DEBEN SER VARIABLES AUTOCALCULABLES

    

    page.wait_for_timeout(5000)
    return 1

with sync_playwright() as playwright:
    run(playwright)