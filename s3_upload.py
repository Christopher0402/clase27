import boto3
from config import REGION, TABLA_NOMBRE, BUCKET

dynamodb = boto3.resource('dynamodb', region_name=REGION)
s3 = boto3.client('s3', region_name=REGION)

def exportar_txt():
    tabla = dynamodb.Table(TABLA_NOMBRE)
    response = tabla.scan()

    datos = ""
    for item in response['Items']:
        if item['precio'] > 500:
            datos += str(item) + "\n"

    with open("reporte.txt", "w") as f:
        f.write(datos)

    s3.upload_file("reporte.txt", BUCKET, "reporte.txt")

    print("☁️ Archivo subido a S3")
