import os
import cv2
import pickle
templates = {}
for root, subdirs, files in os.walk('templates'):
    print(f"subdirs: {subdirs}")
    for d in subdirs:
        templates[d] = {}
        print(f"d: {d}")
        for r, s, f in os.walk(os.path.join(root,d)):
            print(f"f: {f}")
            for file in f:
                fn, fe = os.path.splitext(file)
                templates[d][fn] = {}
                templates[d][fn]["template"] = cv2.imread(os.path.join(r, file), cv2.IMREAD_GRAYSCALE)
print(f"templates: {templates}")
with open("templates.pickle","wb") as f:
    pickle.dump(templates,f)