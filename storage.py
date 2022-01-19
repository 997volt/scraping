import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import os


cred = credentials.Certificate('firebase-credentials.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'komper-xyz.appspot.com'
})

bucket = storage.bucket()
blob=bucket.blob('gpus/rtx3060ti/msi_rtx_3060ti_gaming_x_lhr.jpg')
blob.make_public()