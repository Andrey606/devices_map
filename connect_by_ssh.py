import paramiko 

class SSH():
    client = paramiko.SSHClient()
    sftp = None
    
    def __init__(self, host='192.168.50.18', port=22, username="pi", password='Lfqvyt100gbfcnhjd!', fullFilePath="/home/pi/zina2.0/iot_gw/src/daemons/ZCB/table_lib/table.txt"):
        self.host = host
        self.port = port
        self.USERNAME = username
        self.PASS = password
        self.fullFilePath = fullFilePath
    
    def create_connection(self):
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=host, username=user, password=secret, port=port)
        self.sftp = self.client.open_sftp()

    def get_file(self):
        file = sftp.file(self.fullFilePath,'r')
        return file
    
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

    def close_connection(self):
        self.sftp.close()
        self.client.close()