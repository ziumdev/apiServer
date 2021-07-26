class apiConfig:
    APP_NAME = 'api_interface'
    creator = 'CJM'
    contributor = 'baltop', 'Cuberin', 'ysr'


class DevelopmentConfig(apiConfig):
    serverHost = 'localhost'
    serverPort = 50000

    mrsHost = '192.168.0.103'  # 현재 미사용
    mrsPort = 9201  # 현재 미사용

    ersHost = '192.168.0.102'
    ersPort = 9201  # MRS port : 9102, ERS port : 9202, simulator port : 8888

    mrsClientCd = 'SMT'
    mrsSiteCd = 'PA1'
    sendSystemCd = 'SIM'
    headerTypeCd = '001'
    traceId = '                        '
    location = [{
        'x': '37.76400393860835',
        'y': '126.7839482482826',
        'z': '0'
    }]


class TestConfig(apiConfig):
    serverHost = 'localhost'
    serverPort = 50001

    mrsHost = '211.9.3.50'  # 현재 미사용
    mrsPort = 9201  # 현재 미사용

    ersHost = '211.9.3.50'
    ersPort = 9201  # MRS port : 9102, ERS port : 9202, simulator port : 8888

    mrsClientCd = 'SMT'
    mrsSiteCd = 'PA1'
    sendSystemCd = 'SIM'
    headerTypeCd = '001'
    traceId = '                        '
    location = [{
        'x': '37.761419193645686',
        'y': '126.78460836410522',
        'z': '0'
    }]


class ProductionConfig(apiConfig):
    serverHost = 'localhost'
    serverPort = 50000
    pass


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestConfig,
    prod=ProductionConfig
)
