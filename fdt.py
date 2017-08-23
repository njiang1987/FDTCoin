#coding=utf-8

import json
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# Post 相关的API
def getHTTPHeader():
    headers = {"x-token": auth_token,
               "x-market": "FX",
               "x-language": "CN",
               "x-country": "CN",
               "Accept-Language": "zh-Hans-US;q=1, zh-Hant-US;q=0.9, en-US;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               'Content-Type': 'application/json',
               'Fdt-Did': '391B8D36-B885-4988-B0F9-FF788D339004',
               'Connection': 'keep-alive',
               "User-Agent": "FDTMasterCN/6.3.7.170821001 (iOS: 10.3)"}
    return headers

def getUserPosts(username):
    headers = getHTTPHeader()
    requestURL = 'http://prod.forexmaster.cn/jsocial/post/getUserPostList?limit=100&targetUserId=%s' % username
    response = requests.post(requestURL, headers=headers)
    content = json.loads(response.content)
    return content['data']['list']

def postLikeRequest(postId):
    params = {'moduleKey': 'fdtPost', 'type': 'submit', 'moduleId':  postId}
    str = json.dumps(params)
    headers = getHTTPHeader()
    response = requests.post('http://prod.forexmaster.cn/jsocial/universalLike/post', data=str, headers=headers)
    print '已经赞完帖子(%s) - %d' % (postId, response.status_code)

def doCommentPost(postId):
    params = {'moduleKey': 'fdtPost',
              'moduleId': postId,
              'userNames': [],
              'type': '0',
              'symboleNames': [],
              'comment': '~',
              'userIds': []}
    str = json.dumps(params)
    headers = getHTTPHeader()
    response = requests.post('http://prod.forexmaster.cn/jsocial/universalComment/post', data=str, headers=headers)
    print '已经给他帖子留言(%s) - %d' % (postId, response.status_code)

def doRepostPost(postId):
    params = {'relayPostId': postId, 'originalPostId': postId}
    str = json.dumps(params)
    headers = getHTTPHeader()
    response = requests.post('http://prod.forexmaster.cn/jsocial/post/rePost', data=str, headers=headers)
    print '已经转发帖子(%s) - %d' % (postId, response.status_code)

#发表帖子
def doPost():

    params = {'symbolIds': [],
              'userNames': [],
              'userIds': [],
              'type': '0',
              'msg': '$欧元/谢尔克',
              'symbolNames': []}
    str = json.dumps(params)
    headers = getHTTPHeader()
    response = requests.post('http://prod.forexmaster.cn/jsocial/post/posting', data=str, headers=headers)
    print '已经发布完帖子 - %d' % (response.status_code)

#删除帖子
def doDeletePost(postid):
    params = {'postId': postid}
    str = json.dumps(params)
    headers = getHTTPHeader()
    response = requests.post('http://prod.forexmaster.cn/jsocial/post/delPost', data=str, headers=headers)
    print '已经删除帖子(%s) - %d' % (postid, response.status_code)

#赞某个用户所有的帖子
def doLikeAllPost(username):

    print '开始赞用户: %s 的帖子' % (username)
    posts = getUserPosts(username)

    for post in posts:
        postLikeRequest(post["postId"])

    print '用户: %s 的帖子已经赞完' % (username)

#删除我的所有帖子
def doDeleteAllPost(username):
    posts = getUserPosts(username)

    while len(posts) > 0:
        for post in posts:
            if 'repostid' in post.keys():
                doDeletePost(post['repostid'])
            else:
                doDeletePost(post["postId"])

        posts = getUserPosts(username)

#给帖子留言
def doCommentAllPost(username):

    print '开始给用户帖子留言(%s)' % (username)
    posts = getUserPosts(username)

    for post in posts:
        doCommentPost(post['postId'])

    print '已经给所有的帖子留言完毕'

#转发用户所有帖子
def doRepostAllPost(username):

    print '开始转发用户帖子(%s)' % (username)
    posts = getUserPosts(username)

    for post in posts:
        doRepostPost(post['postId'])

    print '已经转发所有的帖子'

#########################################

POST_ENABLED = 0
LIKE_ENABLED = 0
COMMENT_ENABLED = 0
REPOST_ENABLED = 0
DELETE_ENABLED = 1

auth_token = 'DQO1XOTWSf7VWSs2fhG/i8v8PWPVEO+E3iNJvDvY9tkwleP9CaMJRIG4JuyHOC7j/Qrz9Hoi96QGCESCtGXf4LakDlk/xEa2UzZygdHRSF1dwZiy4QJ+p7TcmGWk9pThdq7IPk7360/ogP1bMmoHGUeqAcL+zUX7t5xeRImu7ho5VC+UjHuotU+ZFjOtwYghMtFBjGqgpfC5iv1aGigR450Wf2MbpjRrO8unW1wUrQlzubN++XEE3yfrEfutqXUVuUF016uaVwj9sGgXg+yEMv5xGkIG0vVkI8NQuzDxvyT5xlQ6tj8OQPixsuXcO9c/WHfdPhgeeyBD1aKQo/SqLg=='
deleteUser = 'mb000000001'


if POST_ENABLED:
    for i in range(1, 100):
        doPost()

# userList = ['mb000000001', 'jn11585852', 'nanjiang', 'fdt_cn_test_15', 'wanghua']
userList = ['mb000000001']

if LIKE_ENABLED:
    for user in userList:
        doLikeAllPost(user)

if COMMENT_ENABLED:
    for user in userList:
        doCommentAllPost(user)

if REPOST_ENABLED:
    for user in userList:
        doRepostAllPost(user)

if DELETE_ENABLED:
    doDeleteAllPost(deleteUser)