import pickle
import gzip
import json

with gzip.open("./phoenix14t.pami0.dev.annotations_only.gz", 'rb') as f:
    annotations = pickle.load(f)
    resp1 = json.dumps(annotations).replace("\\", "")
print(resp1)
