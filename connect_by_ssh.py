import paramiko 

# HOST
host = '192.168.50.18'
user = 'pi'
secret = 'Lfqvyt100gbfcnhjd!'
port = 22
fullFilePath = "/home/pi/zina2.0/iot_gw/src/daemons/ZCB/table_lib/table.txt"


def get_file():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)
    
    sftp = client.open_sftp()
    fileObject = sftp.file(fullFilePath,'r')
    
    ret = parse_file(fileObject)

    sftp.close()
    client.close()

    return ret


def parse_file(file):
    ret = []

    for i, line in enumerate(file):
        if(line[0] != '0'):
            continue
        arr = line.replace(' ', '').replace('\n', '').split('|')
        arr.pop()
        arr.pop(0)
        ret.append(arr)
        
    return ret

def inArray(var, array):
    for arr1 in array:
        if var in arr1:
            return True
    
    return False