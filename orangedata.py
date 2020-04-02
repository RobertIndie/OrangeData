from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import json
import hashlib
import binascii

# 证书数据库可由证书信任链维护，这里不进行演示
certDatabase = {}


class Factory:

    def __init__(self, name):
        self.name = name
        keyPair = RSA.generate(1024)
        self.keyPair = keyPair
        self.pubKey = keyPair.publickey()
        self._privateKey = keyPair  # 将公钥放进证书数据库中，供其他人调用。
        certDatabase[name] = self.pubKey

    def Process(self, orange, processName, data):
        # 组建数据区块
        b = Block()
        b.prevBlock = orange.identity
        b.processName = processName
        b.factoryName = self.name
        b.data = data

        # 获取前一区块的加密数据
        prevEncryptedStr = b.prevBlock[256:]
        prevEncryptedBytes = binascii.unhexlify(prevEncryptedStr)

        # 生成待加密的数据
        blockJson = json.dumps(b.__dict__).encode('utf-8')
        #blockBytes = bytes(blockJson, encoding='utf-8')
        data = prevEncryptedBytes + blockJson
        sha256hash = hashlib.sha256(data).digest()  # 利用哈希算法对数据进行压缩

        # 加密数据
        encryptor = PKCS1_OAEP.new(self.keyPair)
        encrypted = encryptor.encrypt(sha256hash)
        encryptedStr = ''.join(format(x, '02x') for x in encrypted)

        # 更新标识
        orange.identity = prevEncryptedStr + encryptedStr
        orange.blockData.append(b)
        return orange


def Validate(pubKey, identity, block):
    # 解析标识
    prevEncryptedStr = identity[:256]
    encryptedStr = identity[256:]

    # 解密数据
    encryptedBytes = binascii.unhexlify(encryptedStr)
    decryptor = PKCS1_OAEP.new(pubKey)
    decryptedSHA256Hash = decryptor.decrypt(encryptedBytes)

    # 生成校验数据
    prevEncryptedBytes = binascii.unhexlify(prevEncryptedStr)
    blockJson = json.dumps(block.__dict__).encode('utf-8')
    #blockBytes = bytes(blockJson, encoding='utf-8')
    data = prevEncryptedBytes + blockJson
    sha256hash = hashlib.sha256(data).digest()

    result = sha256hash == decryptedSHA256Hash
    return result


class Block:
    def __init__(self):
        self.prevBlock = ""
        self.processName = ""
        self.factoryName = ""
        self.data = ""


class Orange:
    def __init__(self):
        self.blockData = []
        self.identity = "0"*512


factoires = {}

factoires["种子工厂"] = Factory('种子工厂')
factoires["种植场"] = Factory("种植场")
factoires["食品加工厂"] = Factory("食品加工厂")
factoires["超市"] = Factory("超市")

orange = Orange()

orange = factoires["种子工厂"].Process(orange, "种子", "第一天，采集了一个种子，质量为优。；出售种子。")
orange = factoires["种植场"].Process(
    orange, "种植", "第二天，从种子工厂获取了种子；第三天，将种子种在优质土壤上，生长状况良好。；第四十天，出售。")
orange = factoires["食品加工厂"].Process(orange, "食品加工", "加工了一下")
orange = factoires["超市"].Process(orange, "超市", "出售")

i = len(orange.blockData) - 1
identity = orange.identity
while i >= 0 :
	block = orange.blockData[i]
	pubKey = certDatabase[block.factoryName]
	print(Validate(pubKey,identity,block))
	identity = block.prevBlock
	i = i - 1
