def create_config(data):
    serv  = {}
    if data is None:
        return None
    serv['encrypted'] = do_parse(data[0])
    serv['pollinterval'] = do_parse(data[1])
    det = do_parse(data[2])
    q = det.split(' ')
    serv['proto']  = q[0]
    serv['uname']  = q[1]
    serv['pswd']   = q[2]
    serv['server'] = q[3]
    serv['port']   = q[4]
    serv['mbox']   = q[5]
    serv['con']    = None
    return serv

def do_parse(data):
    if data is None:
        return None
    return data.__getitem__(1)
    
