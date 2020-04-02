from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii
import json

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
        # 构建数据区块
        b = Block()
        b.prevBlock = orange.identity
        b.processName = processName
        b.factoryName = self.name
        b.data = data

        # 获取前一区块的标识
        prevSignedStr = b.prevBlock[256:]
        prevSignedBytes = binascii.unhexlify(prevSignedStr)

        # 生成待签名的数据
        blockJson = json.dumps(b.__dict__).encode('utf-8')
        data = prevSignedBytes + blockJson

        # 数据签名
        hashData = SHA256.new(data)  # 哈希压缩数据
        signer = PKCS115_SigScheme(self.keyPair)
        signature = signer.sign(hashData)

        signatureStr = ''.join(format(x, '02x') for x in signature)

        # 更新标识并添加数据区块
        orange.identity = prevSignedStr + signatureStr
        orange.blockData.append(b)
        return orange


def Validate(pubKey, identity, block):
    # 解析标识
    prevSignedStr = identity[:256]
    signedStr = identity[256:]

    signedBytes = binascii.unhexlify(signedStr)

    # 生成校验数据
    signedBytes = binascii.unhexlify(prevSignedStr)
    blockJson = json.dumps(block.__dict__).encode('utf-8')
    data = signedBytes + blockJson
    hashData = SHA256.new(data)
    verifier = PKCS115_SigScheme(pubKey)

    # 进行校验
    result = False
    try:
        verifier.verify(hashData, signedBytes)
        result = True
    except:
        result = False
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

orange = factoires["种子工厂"].Process(orange, "种子", "第1天，采集了一个种子，质量为优；第2天，出售种子。")
orange = factoires["种植场"].Process(
    orange, "种植", "第2天，从种子工厂获取了种子；第3天，将种子种在优质土壤上，生长状况良好。；第365天，生长良好，采集香橙；第366天，出售香橙。")
orange = factoires["食品加工厂"].Process(
    orange, "食品加工", "第366天，购买香橙；第368天，加工香橙，更香了；第369天，出售。")
orange = factoires["超市"].Process(orange, "超市", "第369天，采购香橙。")

# 用户在超市购买香橙时，拿到了orange的数据，现在开始校验
# 校验过程仅用到了证书数据库
i = len(orange.blockData) - 1
identity = orange.identity
while i >= 0:
    # 套娃校验
    block = orange.blockData[i]
    pubKey = certDatabase[block.factoryName]
    print(Validate(pubKey, identity, block))
    identity = block.prevBlock
    i = i - 1
