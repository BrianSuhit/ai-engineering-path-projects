# Paquetes a instalar en tu entorno virtual:
# uv add mcp fastmcp

# Importamos FastMCP, el framework que maneja toda la red y el protocolo por nosotros
from mcp.server.fastmcp import FastMCP

# 1. Inicializamos el Servidor MCP dándole un nombre descriptivo
mcp = FastMCP(name="Servidor-Comedor-UNICEN")

# 2. La magia: Este decorador envuelve la función y la expone como una Herramienta MCP.
# Cualquier IA que se conecte a este servidor podrá ver el nombre, la descripción y los parámetros.
@mcp.tool()
def consultar_menu_comedor(dia: str) -> str:
    """Consulta el plato principal del comedor universitario para un día de la semana."""

    # Limpiamos el texto que nos envíe la IA para evitar errores
    dia_limpio = dia.lower().strip()
 
    # Usar un diccionario es más escalable y limpio que múltiples if/elif
    menu = {
        "lunes": "Menú del Lunes: Milanesa con puré.",
        "martes": "Menú del Martes: Fideos con tuco."
    }
 
    # Buscamos el día en el diccionario y devolvemos el menú o un mensaje por defecto
    return menu.get(dia_limpio, "Menú no disponible para ese día. Revisa la web oficial.")

# 3. El punto de entrada del script
if __name__ == "__main__":
    print("🚀 Arrancando el Servidor MCP local...")
    # mcp.run() inicia el servidor y lo deja escuchando conexiones a través de Stdio
    mcp.run()