from dynamo import crear_tabla, insertar_datos
from s3_upload import exportar_txt
import boto3

def main():
    print("🚀 Ejecutando...")

    # 1. Asegura que la tabla exista
    crear_tabla()

    # 2. Datos actualizados con el campo 'precio' para evitar el KeyError
    nuevo_cliente = {
        'id': '102',
        'nombre': 'Christopher Soto - Prueba 2',
        'estado': 'Activo',
        'comentario': 'Segunda modificación exitosa',
        'precio': 600  # <--- Agregamos esto para que s3_upload.py no falle
    }

    # 3. Conexión e inserción en DynamoDB
    # Usamos la región us-east-2 que es la que tienes configurada
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    tabla = dynamodb.Table('Clientes')
    
    print(f"📝 Insertando registro: {nuevo_cliente['nombre']}...")
    
    try:
        tabla.put_item(Item=nuevo_cliente)
        print("✅ Registro insertado en DynamoDB.")
    except Exception as e:
        print(f"❌ Error al insertar en DynamoDB: {e}")

    # 4. Exportamos el reporte a S3
    # Ahora esta función sí encontrará el campo 'precio' y funcionará
    print("📤 Exportando reporte a S3...")
    exportar_txt()

    print("🎉 Proceso completado exitosamente.")

if __name__ == "__main__":
    main()
