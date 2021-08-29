lmsHost = '211.9.2.61'
port = 53306
dbUserId = 'ese'
dbUserPw = 'eselms'
db = 'watchall_2x'

lmsColumns = {
    'objName': '장비명',
    'objDefineId': '장비종류',
    'IP': 'IP',
    'eventLevel': '이벤트등급',
    'eventMessage': '이벤트 메시지',
    'eventCondition': '이벤트판단조건',
    'eventCheckDatetime': '이벤트발생시각'
}

eventLevel = {
    'IF': '00',  # Info
    'MN': '10',  # Minor
    'MJ': '20',  # Major
    'CT': '30',  # Critical
    'DN': '40',  # Down
}

interval = 1000