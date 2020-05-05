import json
import boto3
import base64
import urllib.parse

def lambda_handler(event, context):
    # TODO implement
    print(event) 
    
    # UPLOADされたデータのファイル名称を取得する
    key = event['Records'][0]['s3']['object']['key']
    key = urllib.parse.unquote(key) #%decode実施
    print(key) #print関数の標準出力がCloudwatch Logsに出力される

    # S3のbucket情報の取得
    s3=boto3.resource('s3')
    bucket=s3.Bucket('recognitonsample')


    # S3に置いたファイルをRekognitionに認識させる
    rekognition=boto3.client('rekognition')
    res = rekognition.detect_labels(
      Image={"S3Object": {"Bucket": 'recognitonsample', "Name": key}})


    # Rekognitionの認識結果を表示する
    print("Detected labels for " + key)
    #print()
    for label in res["Labels"]:
        print("Label: " + label["Name"])
        print("Confidence: " + str(label["Confidence"]))
        #print("Instances:")
        for instance in label["Instances"]:
            print("  Bounding box")
            print("    Top: " + str(instance["BoundingBox"]["Top"]))
            print("    Left: " + str(instance["BoundingBox"]["Left"]))
            print("    Width: " + str(instance["BoundingBox"]["Width"]))
            print("    Height: " + str(instance["BoundingBox"]["Height"]))
            print("  Confidence: " + str(instance["Confidence"]))
            print()
    
            print("Parents:")
            for parent in label["Parents"]:
                print("   " + parent["Name"])
            print("----------")
            print()
            

    return(label)

