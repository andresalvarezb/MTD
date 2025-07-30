import subprocess
import requests
import json

OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "codellama:7b-instruct"

def obtener_diff():
    return subprocess.check_output(["git", "diff", "--cached"]).decode("utf-8")

def generar_mensaje_commit(diff):
    prompt = f"""
Genera un mensaje de commit en español bien redactado basado en este diff de Git.

El mensaje debe tener:
1. Un título claro (50 caracteres o menos, en presente).
2. Un cuerpo con detalles sobre los cambios, línea por línea.

Diff:
{diff}
    """.strip()

    response = requests.post(
        OLLAMA_API,
        json={"model": MODEL_NAME, "prompt": prompt, "stream": False}
    )

    if response.status_code == 200:
        return response.json()["response"].strip()
    else:
        raise Exception(f"Error de Ollama: {response.text}")

def hacer_commit(mensaje):
    titulo = mensaje.splitlines()[0]
    cuerpo = "\n".join(mensaje.splitlines()[1:])
    subprocess.run(["git", "commit", "-m", titulo, "-m", cuerpo])

if __name__ == "__main__":
    diff = obtener_diff()
    if not diff.strip():
        print("⚠️ No hay cambios para commitear.")
        exit(0)

    mensaje = generar_mensaje_commit(diff)
    print("\n📋 Mensaje sugerido:\n")
    print(mensaje)
    
    confirmar = input("\n¿Quieres hacer el commit con este mensaje? (s/n): ")
    if confirmar.lower() == "s":
        hacer_commit(mensaje)
    else:
        print("❌ Commit cancelado.")
