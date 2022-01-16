import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import os


cred = credentials.Certificate('firebase-credentials.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'komper-xyz.appspot.com'
})

bucket = storage.bucket()
blob=bucket.blob('gpu.jpg')
blob.make_public()