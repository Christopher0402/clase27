from dynamo import crear_tabla, insertar_datos
from s3_upload import exportar_txt

def main():
    print("🚀 Ejecutando...")

    crear_tabla()
    insertar_datos()
    exportar_txt()

    print("🎉 Listo")

if __name__ == "__main__":
    main()
