import boto3
import botocore
import random
from datetime import datetime
from config import REGION, TABLA_NOMBRE

# conexión a DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=REGION)

# =========================
# CREAR TABLA
# =========================
def crear_tabla():
    try:
        tabla = dynamodb.create_table(
            TableName=TABLA_NOMBRE,
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        tabla.wait_until_exists()
        print("✅ Tabla creada")

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("⚠️ La tabla ya existe, continuando...")
        else:
            print("❌ Error al crear tabla:", e)


# =========================
# INSERTAR 50 DATOS
# =========================
def insertar_datos():
    tabla = dynamodb.Table(TABLA_NOMBRE)

    for i in range(50):
        tabla.put_item(
            Item={
                'id': str(i),
                'nombre': f'Cliente_{i}',
                'producto': f'Producto_{random.randint(1,10)}',
                'precio': random.randint(100, 1000),
                'fecha_registro': str(datetime.now()),
                'modificaciones': []
            }
        )

    print("✅ 50 datos insertados")


# =========================
# ACTUALIZAR CLIENTE
# =========================
def actualizar_cliente(id_cliente, nuevo_producto, usuario):
    tabla = dynamodb.Table(TABLA_NOMBRE)

    try:
        response = tabla.get_item(Key={'id': id_cliente})
        item = response.get('Item')

        if not item:
            print("❌ Cliente no encontrado")
            return

        historial = item.get('modificaciones', [])

        cambio = {
            'usuario': usuario,
            'fecha': str(datetime.now()),
            'nuevo_producto': nuevo_producto
        }

        historial.append(cambio)

        tabla.update_item(
            Key={'id': id_cliente},
            UpdateExpression="SET producto = :p, modificaciones = :m",
            ExpressionAttributeValues={
                ':p': nuevo_producto,
                ':m': historial
            }
        )

        print(f"✅ Cliente {id_cliente} actualizado por {usuario}")

    except Exception as e:
        print("❌ Error al actualizar:", e)
