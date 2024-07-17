import os
def get_val(d,key,default):
    if key in d:
        return d[key]
    return default


def rm_recursive(path):
    if not os.path.exists(path):
        return
    
    if os.path.isdir(path):
        for file in os.listdir(path):
            rm_recursive(os.path.join(path,file))
        os.rmdir(path)
    else:
        os.remove(path)