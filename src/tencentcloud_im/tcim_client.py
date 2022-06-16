# -*- coding: utf8 -*-
# Copyright (c) 2021-2021 Pinclr, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
import random
from datetime import datetime
from typing import List

import requests
from TLSSigAPIv2 import TLSSigAPIv2

TCIM_API_BASE = "https://console.tim.qq.com/v4"


class MyLogger(object):

  @staticmethod
  def get_logger(class_name):
    logging_level = logging.INFO
    my_logger = logging.getLogger(class_name)
    my_logger.setLevel(logging_level)
    handler = logging.StreamHandler()
    handler.setLevel(logging_level)
    formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)d [%(levelname)s]%(message)s')
    handler.setFormatter(formatter)
    my_logger.addHandler(handler)
    return my_logger


logger = MyLogger.get_logger(__name__)


class MessageText(object):
  """
    text message
    """

  def __init__(self, message):
    self.MsgType = "TIMTextElem"
    self.MsgContent = {"Text": message}


class MessageFile(object):
  """
    file message
    """

  def __init__(self, file_url: str, file_size: int, file_name: str):
    self.MsgType = "TIMFileElem"
    self.MsgContent = {
      "Url": file_url,
      "FileSize": file_size,
      "FileName": file_name,
      "Download_Flag": 2
    }


class MessageObj(object):

  def __init__(
    self,
    from_account: str,
    to_account: str,
    text_messages: List[MessageText] = [],
    attachment_messages: List[MessageFile] = [],
    sync_machine: int = 1,
    extra_data: str = ""
  ):
    """
        https://cloud.tencent.com/document/product/269/2282
        消息结构体
        :param from_account:
        :param to_account:
        :param text_messages: 消息结构体
        :param attachment_messages: 附件消息列表
        :param sync_machine: 同步机器
        :param extra_data: 自定义消息
        """
    self.From_Account = from_account
    self.To_Account = to_account
    self.SyncOtherMachine = sync_machine
    self.MsgRandom = random.randint(0, 4294967295)
    self.MsgBody = []
    for text_message in text_messages:
      self.MsgBody.append(text_message.__dict__)

    for attachment_message in attachment_messages:
      self.MsgBody.append(attachment_message.__dict__)

    if extra_data != "":
      self.CloudCustomData = extra_data


class GroupMessageObj(object):

  def __init__(
    self,
    from_account: str,
    send_time: int,
    text_messages: List[MessageText] = [],
    attachment_messages: List[MessageFile] = []
  ):

    self.From_Account = from_account
    self.SendTime = send_time
    self.Random = random.randint(0, 4294967295)
    self.MsgBody = []
    for text_message in text_messages:
      self.MsgBody.append(text_message.__dict__)

    for attachment_message in attachment_messages:
      self.MsgBody.append(attachment_message.__dict__)


class BatchMessageObj(object):

  def __init__(
    self,
    from_account: str,
    to_account: List[str],
    text_messages: List[MessageText] = [],
    attachment_messages: List[MessageFile] = [],
    sync_machine: int = 1
  ):
    self.From_Account = from_account
    self.To_Account = to_account
    self.SyncOtherMachine = sync_machine
    self.MsgRandom = random.randint(0, 4294967295)
    self.MsgBody = []
    for text_message in text_messages:
      self.MsgBody.append(text_message.__dict__)

    for attachment_message in attachment_messages:
      self.MsgBody.append(attachment_message.__dict__)


class FriendObj(object):
  """
    Friend Object
    Attributes
      to_account: target user id
      add_source: user from where
      group_name
      remark

    """

  def __init__(self, to_account, add_source, remark="", group_name=""):
    """
        :param to_account: 目标用户 必填
        :param remark:     备注
        :param add_source  好友来源：web,android ios
        :param group_name: 用户分组
        """
    self.To_Account = to_account
    self.Remark = remark
    self.GroupName = group_name
    self.AddSource = "AddSource_Type_{}".format(add_source)


class SnsItemObj(object):
  """
    SnsItemObj
    Attributes
      tag:
          Group:Array  user group  value: [] 分组信息
          Remark：user remark：    value:str 好友备注
          AddSource：user source   value:str
          AddWording：好友附言  value:str
          AddTime：user time stamp  value:int
    """

  def __init__(self, tag, value):
    self.Tag = tag
    self.Value = value


class UpdateFriendObj(object):
  """

    update user object
    """

  def __init__(self, to_account, sns_items: List[SnsItemObj]):
    self.To_Account = to_account
    SnsItem = []
    for sns_item in sns_items:
      SnsItem.append(sns_item.__dict__)
    self.SnsItem = SnsItem


class GroupMemObj(object):
  """
    群组成员
    """

  def __init__(
    self, user_id: str, role_type: str = "", join_time: int = 0, unread_msg_num: int = 0
  ):
    self.Member_Account = user_id
    if role_type == "Admin":
      self.Role = role_type
    if join_time > 0:
      self.JoinTime = join_time
    if unread_msg_num > 0:
      self.UnreadMsgNum = 0


class GroupAppDefinedData(object):
  """
    群组自定义字段
    """

  def __init__(self, key: str, value: str):
    self.Key = key
    self.Value = value


class GroupAttr(object):

  def __init__(self, key: str, value: str):
    self.key = key
    self.value = value


class GroupObj(object):
  """
    群组结构体
    """

  def __init__(
    self,
    owner_userid: str,
    group_type: str,
    group_name: str,
    introdction: str = "",
    notification: str = "",
    face_url: str = "",
    max_member_count: int = 500,
    mem_list: List[GroupMemObj] = [],
    applicationData: List[GroupAppDefinedData] = [],
    group_id: str = ""
  ):
    """

        :param owner_userid:
        :param group_type:
        :param group_name:
        :param introdction:
        :param notification:
        :param face_url:
        :param max_member_count:
        :param mem_list:
        :param applicationData:
        :param group_id:
        """

    self.Owner_Account = owner_userid
    self.Type = group_type
    self.Name = group_name
    self.MaxMemberCount = max_member_count
    if introdction != "":
      self.Introduction = introdction
    if notification != "":
      self.Notification = notification
    if face_url != "":
      self.FaceUrl = face_url
    if len(mem_list) > 0:
      self.MemberList = []
      for one in mem_list:
        self.MemberList.append(one.__dict__)
    if len(applicationData) > 0:
      self.AppDefinedData = []
      for one in applicationData:
        self.AppDefinedData.append(one.__dict__)
    if group_id != "":
      self.GroupId = group_id


class TCIMClient(object):
  """
    Tecent Im Rest API Client

    Attributes
      sdk_id: im sdk id
      key:IM im sdk secret key
      admin: im sdk admin user id
      tencent_url: tencent im rest url
      expire_time: user sig expire time(seconds)


    """

  def __init__(self, sdk_id, key, admin, tencent_url=TCIM_API_BASE, expire_time=60 * 5):
    """
        :param sdk_id: IM SDK ID
        :param key:    IM SDK SECRET KEY
        :param admin:  ADMIN
        :param tencent_url: tencent rest url
        :param expire_time:   expire time
        """
    self.sdk_id = sdk_id
    self.key = key
    self.admin = admin
    self.tecent_url = tencent_url
    self.expire_time = expire_time
    self.next_time = datetime.now()
    self.user_sig = None

  def get_user_sig(self, user_id: str, expire_time: int = 180 * 86400):
    """
        generate user sig
        :param user_id: user id
        :param expire_time: expire time
        :return: user_sig
        """

    api = TLSSigAPIv2(self.sdk_id, self.key)
    sig = api.gen_sig(user_id, expire_time)
    return sig

  def _gen_query(self):
    """
    generate rest url
    """
    current_time = datetime.now()

    # 计算时间：如果大于登陆5分钟，则重新生成user_sig
    if self.user_sig == None or (current_time - self.next_time).seconds >= self.expire_time:
      self.user_sig = self.get_user_sig(self.admin, self.expire_time)
      self.next_time = current_time

    querys = {}
    querys["sdkappid"] = self.sdk_id
    querys["identifier"] = self.admin
    querys["usersig"] = self.user_sig
    querys["random"] = random.randint(0, 4294967295)
    querys["contenttype"] = "json"
    return querys

  def add_single_user(self, user_id: str, nick_name: str, face_url: str):
    """
        add user to im server
        https://cloud.tencent.com/document/product/269/1608
        :param user_id
        :param nick_name:
        :param face_url:
        :return: response
        response.content:
        {
            "ActionStatus":"OK",  # if "OK" means success else "Fail" means fail
            "ErrorInfo":"",
            "ErrorCode":0
        }
        """
    rest_url = "{}/im_open_login_svc/account_import".format(self.tecent_url)

    data = {}
    try:
      data["UserID"] = user_id
      data["Nick"] = nick_name
      data["FaceUrl"] = face_url
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("add user failed:{}".format(e))
      return None

  def batch_add_users(self, user_ids: List[str]):
    """
        batch add users to im server
        https://cloud.tencent.com/document/product/269/4919
        :param user_ids:  list of user_ids eg: ["user0","user1"]
        :return:response
        response.content
        {
            "ActionStatus": "OK", #if "OK" means success else "Fail" means fail
            "ErrorCode": 0,
            "ErrorInfo": "",
            "FailAccounts": [   // List of accounts that failed to be imported to im server
                "test3",
                "test4"
            ]
        }
        """
    try:
      rest_url = "{}/im_open_login_svc/multiaccount_import".format(self.tecent_url)
      data = {}
      data["Accounts"] = user_ids
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("batch add user failed:{}".format(e))
      return None

  def del_user(self, user_ids: List[str]):
    """
          delete user in im server
          https://cloud.tencent.com/document/product/269/36443
          :param user_ids: list of user_ids eg: ["user0","user1"]
          :return:response
          response.content
          {
              "ActionStatus": "OK",
              "ErrorCode": 0,
              "ErrorInfo": "",
              "ResultItem": [
                  {
                      "ResultCode": 0,   # if "0" means success  else  means fail
                      "ResultInfo": "",  # error info
                      "UserID": "UserID_1"
                  },
                  {
                      "ResultCode": 70107,
                      "ResultInfo": "Err_TLS_PT_Open_Login_Account_Not_Exist",
                      "UserID": "UserID_2"
                  }
              ]
          }
        """
    rest_url = "{}/im_open_login_svc/account_delete".format(self.tecent_url)
    data = {}
    DeleteItem = []
    try:
      for user_id in user_ids:
        tmp_map = {}
        tmp_map["UserID"] = user_id
        DeleteItem.append(tmp_map)

      data["DeleteItem"] = DeleteItem
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:

      logger.error("delete user failed:{}".format(e))
      return None

  def search_user(self, user_ids: List[str]):
    """
          search user
          https://cloud.tencent.com/document/product/269/38417
          :param user_ids: list of user_ids eg: ["user0","user1"]
          :return: response
          response.content
          {
              "ActionStatus": "OK",
              "ErrorCode": 0,
              "ErrorInfo": "",
              "ResultItem": [
                  {
                      "UserID": "UserID_1",
                      "ResultCode": 0,     # if "0" means success  else  means fail
                      "ResultInfo": "",
                      "AccountStatus": "Imported"  # "Import" means this user_id is in im server
                  },
                  {
                      "UserID": "UserID_2",
                      "ResultCode": 0,
                      "ResultInfo": "",
                      "AccountStatus": "NotImported"  # "NotImported" means this user_id is not in im server
                  }
              ]
          }
        """
    rest_url = "{}/im_open_login_svc/account_check".format(self.tecent_url)
    data = {}
    CheckItem = []
    try:
      for user_id in user_ids:
        tmp_map = {}
        tmp_map["UserID"] = user_id
        CheckItem.append(tmp_map)

      data["CheckItem"] = CheckItem
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))

    except Exception as e:
      logger.error("search user failed:{}".format(e))
      return None

  def abolition_user_sig(self, user_id):
    """
        login status of invalid account
        https://cloud.tencent.com/document/product/269/3853
        :param user_id:
        :return: response
        response.content
        {
            "ActionStatus":"OK",
            "ErrorInfo":"",
            "ErrorCode":0
        }

        """
    rest_url = "{}/im_open_login_svc/kick".format(self.tecent_url)
    data = {}
    data["UserID"] = user_id
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("abolish user sig failed:{} ".format(e))
      return None

  def check_user_online(self, user_ids: List[str]):
    """
        check user status
        https://cloud.tencent.com/document/product/269/2566
        :param user_ids:list of user_ids eg: ["user0","user1"]
        :return:response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0,
            "QueryResult": [
                {
                    "To_Account": "id1",
                    "Status": "Online",
                    "Detail": [
                        {
                            "Platform": "iPhone",
                            "Status": "PushOnline"
                        },
                        {
                            "Platform": "Web",
                            "Status": "Online"
                        }
                    ]
                },
                {
                    "To_Account": "id2",
                    "Status": "Offline",
                }
            ],
            "ErrorList": [
                {
                    "To_Account": "id4",
                    "ErrorCode": 70107
                }
            ]
            }

        """
    rest_url = "{}/openim/query_online_status".format(self.tecent_url)
    data = {}
    try:
      data["IsNeedDetail"] = 1
      data["To_Account"] = user_ids
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("check user status failed:{}".format(e))
      return None

  def add_friend(self, from_account: str, friends: List[FriendObj]):
    """
        add friend
        https://cloud.tencent.com/document/product/269/1643
        :param from_account: 需要添加好友的账户
        :param friends: need to be added  [FriendObj]
        :return: response
        response.content
        {
            "ResultItem":
            [
                {
                    "To_Account":"id1",
                    "ResultCode":0,
                    "ResultInfo":""
                },
                {
                    "To_Account":"id2",
                    "ResultCode":30006,
                    "ResultInfo":"Err_SNS_FriendAdd_Unpack_Profile_Data_Fail"
                },
                {
                    "To_Account":"id3",
                    "ResultCode":30002,
                    "ResultInfo":"Err_SNS_FriendAdd_SdkAppId_Illegal"
                }
            ],
            "Fail_Account":["id2","id3"],
            "ActionStatus":"OK",
            "ErrorCode":0,
            "ErrorInfo":"",
            "ErrorDisplay":""
        }

        """
    rest_url = "{}/sns/friend_add".format(self.tecent_url)
    data = {}
    data["From_Account"] = from_account
    AddFriendItem = []
    try:
      for friend in friends:
        AddFriendItem.append(friend.__dict__)
      data["AddFriendItem"] = AddFriendItem
      data["AddType"] = "Add_Type_Both"
      data["ForceAddFlags"] = 1
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("add friend failed:{}".format(e))
      return None

  def delete_friends(
    self, from_account: str, to_accounts: List[str], delete_type="Delete_Type_Both"
  ):
    """
        delete friends
        https://cloud.tencent.com/document/product/269/1644
        :param from_account
        :param to_accounts: list of user ids
        :param delete_type: Delete_Type_Both or Delete_Type_Single
        :return: response
        response.content
        {
            "ResultItem":
            [
                {
                    "To_Account":"id1",
                    "ResultCode":0,
                    "ResultInfo":""
                },
                {
                    "To_Account":"id2",
                    "ResultCode":0,
                    "ResultInfo":""
                },
                {
                    "To_Account":"id3",
                    "ResultCode":0,
                    "ResultInfo":""
                }
            ],
            "ActionStatus":"OK",
            "ErrorCode":0,
            "ErrorInfo":"0",
            "ErrorDisplay":""
        }

        """
    rest_url = "{}/sns/friend_delete".format(self.tecent_url)
    data = {}
    try:
      data["From_Account"] = from_account
      data["To_Account"] = to_accounts
      data["DeleteType"] = delete_type
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("delete user failed:{}".format(e))
      return None

  def update_friend(self, from_account: str, update_objs: List[UpdateFriendObj]):
    """
        update friend  relational link data
        https://cloud.tencent.com/document/product/269/12525
        :param from_account:
        :param update_objs: list[UpdateFriendObj]
        :return: response
        response.content
        {
            "ResultItem":
            [
                {
                    "To_Account":"id1",
                    "ResultCode":0,
                    "ResultInfo":""
                },
                {
                    "To_Account":"id2",
                    "ResultCode":30011,
                    "ResultInfo":"Err_SNS_FriendUpdate_Group_Num_Exceed_Threshold"
                },
                {
                    "To_Account":"id3",
                    "ResultCode":30002,
                    "ResultInfo":"Err_SNS_FriendImport_SdkAppId_Illegal"
                }
            ],
            "Fail_Account":["id2","id3"],
            "ActionStatus":"OK",
            "ErrorCode":0,
            "ErrorInfo":"",
            "ErrorDisplay":""
        }
        """

    rest_url = "{}/sns/friend_update".format(self.tecent_url)
    data = {}
    try:
      updateItems = []
      for update_obj in update_objs:
        updateItems.append(update_obj.__dict__)
      data["From_Account"] = from_account
      data["UpdateItem"] = updateItems
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("update freind failed:{}".format(e))
      return None

  def get_target_friends(self, from_account: str, to_accounts: List[str], tags: List[str]):
    """
        get target friends
        https://cloud.tencent.com/document/product/269/8609
        :param from_account:
        :param to_accounts: user ids list
        :param tags: tags list
        :return:response
        response.content
                {
            "InfoItem": [
                {
                    "To_Account": "UserID_2",
                    "SnsProfileItem": [
                        {
                            "Tag": "Tag_SNS_IM_Remark",
                            "Value": "remark_2"
                        },
                        {
                            "Tag": "Tag_SNS_IM_Group",
                            "Value": ["group1","group2"]
                        },
                        {
                            "Tag": "Tag_Profile_IM_Nick",
                            "Value": "nick_2"
                        },
                        {
                            "Tag": "Tag_SNS_Custom_Test",
                            "Value": "custom_sns_2"
                        },
                        {
                            "Tag": "Tag_Profile_Custom_Test",
                            "Value": "custom_profile_2"
                        }
                    ],
                    "ResultCode": 0,
                    "ResultInfo": ""
                }
            ],
            "ActionStatus": "OK",
            "ErrorCode": 0,
            "ErrorInfo": "",
            "ErrorDisplay": ""
        }
        """
    rest_url = "{}/sns/friend_get_list".format(self.tecent_url)
    data = {}
    try:
      data["From_Account"] = from_account
      data["To_Account"] = to_accounts
      data["TagList"] = tags
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("get target friends failed:{}".format(e))
      return None

  def get_friends(self, from_account: str, start_index: int = 0):
    """
        get friends
        https://cloud.tencent.com/document/product/269/1647
        :param from_account
        :param:start_index: start index from next_start_index in response
        :return:response
        response.content
            {
            "UserDataItem": [
                {
                    "To_Account": "id1",
                    "ValueItem": [
                        {
                            "Tag": "Tag_SNS_IM_AddSource",
                            "Value": "AddSource_Type_Android"
                        },
                        {
                            "Tag": "Tag_SNS_IM_Remark",
                            "Value": "Remark1"
                        },
                        {
                            "Tag": "Tag_SNS_IM_Group",
                            "Value":["Group1","Group2"]
                        },
                        {
                            "Tag": "Tag_SNS_IM_AddTime",
                            "Value": 1563867420
                        },
                        {
                            "Tag": "Tag_SNS_Custom_Test",
                            "Value": "CustomData1"
                        }
                    ]
                },
                {
                    "To_Account": "id2",
                    "ValueItem": [
                        {
                            "Tag": "Tag_SNS_IM_AddSource",
                            "Value": "AddSource_Type_IOS"
                        },
                        {
                            "Tag": "Tag_SNS_IM_Group",
                            "Value":["Group1"]
                        },
                        {
                            "Tag": "Tag_SNS_IM_AddTime",
                            "Value": 1563867425
                        }
                    ]
                }
            ],
            "StandardSequence": 88,
            "CustomSequence": 46,
            "FriendNum": 20,
            "CompleteFlag": 1,
            "NextStartIndex": 0,
            "ActionStatus": "OK",
            "ErrorCode": 0,
            "ErrorInfo": "",
            "ErrorDisplay": ""
        }
        """

    rest_url = "{}/sns/friend_get".format(self.tecent_url)
    data = {}
    try:
      data["From_Account"] = from_account
      data["StartIndex"] = start_index
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("get user failed:{}".format(e))
      return None

  def add_sns_group(self, from_account: str, groups: List[str], to_accounts: List[str]):
    """
        add group

        https://cloud.tencent.com/document/product/269/10107
        :param from_account  :
        :param groups        ：list of groups
        :param to_accounts   ：add user id to groups
        :return:response
        response.content
        {
            "ResultItem":
            [
                {
                    "To_Account": "id1",
                    "ResultCode": 0,
                    "ResultInfo": ""
                },
                {
                    "To_Account": "id2",
                    "ResultCode": 32216,
                    "ResultInfo": "Err_SNS_GroupAdd_ToTinyId_Not_Friend"
                },
                {
                    "To_Account": "id3",
                    "ResultCode": 30002,
                    "ResultInfo": "ERR_SDKAPPID_ILLEGAL"
                }
            ],
            "Fail_Account":["id2","id3"],
            "CurrentSequence": 3,
            "ActionStatus": "OK",
            "ErrorCode": 0,
            "ErrorInfo": "",
            "ErrorDisplay": ""
        }

        """

    rest_url = "{}/sns/group_add".format(self.tecent_url)
    data = {}
    try:
      data["From_Account"] = from_account
      data["GroupName"] = groups
      data["To_Account"] = to_accounts
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("add group failed:{}".format(e))
      return None

  def delete_sns_group(self, from_account: str, groups: List[str]):
    """
        delete group
        https://cloud.tencent.com/document/product/269/10108
        :param: from_account:
        :param  groups: list of group names
        :return:response
        response.content
        {
            "CurrentSequence": 4,
            "ActionStatus":"OK",
            "ErrorCode":0,
            "ErrorInfo":"0",
            "ErrorDisplay":""
        }
        """
    try:
      rest_url = "{}/sns/group_delete".format(self.tecent_url)
      data = {}
      data["From_Account"] = from_account
      data["GroupName"] = groups
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))

    except Exception as e:
      logger.error("delete group failed:{}".format(e))
      return None

  def get_sns_group(
    self,
    from_account: str,
    groups: List[str] = [],
    need_friend_flag: str = "Need_Friend_Type_Yes"
  ):
    """
        get grounds
        https://cloud.tencent.com/document/product/269/54763
        :param from_account:
        :param: groups: list of group names
        :param: need_friend_flag: "Need_Friend_Type_Yes"
        :return: response
        response.content
        {
            "ResultItem": [
                {
                    "GroupName": "group1",
                    "FriendNumber": 1,
                    "To_Account": ["friend1"]
                }
            ],
            "CurrentSequence": 2,
            "ActionStatus": "OK",
            "ErrorCode": 0,
            "ErrorInfo": "",
            "ErrorDisplay": ""
        }

        """
    rest_url = "{}/sns/group_get".format(self.tecent_url)
    data = {}
    try:
      data["From_Account"] = from_account
      if len(groups) > 0:
        data["GroupName"] = groups
      data["NeedFriend"] = need_friend_flag
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("get group failed:{}".format(e))
      return None

  def send_message(self, messgeObj: MessageObj):
    """
        send message
        https://cloud.tencent.com/document/product/269/2282
        :return: response
        response.content
        {
          "ActionStatus": "OK",
          "ErrorInfo": "",
          "ErrorCode": 0,
          "MsgTime": 1572870301,
          "MsgKey": "89541_2574206_1572870301"
        }
        """
    rest_url = "{}/openim/sendmsg".format(self.tecent_url)
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(messgeObj.__dict__))
    except Exception as e:
      logger.error("send message faield:{}".format(e))
      return None

  def batch_send_message(self, batchMessageObj: BatchMessageObj):
    """
      batch send message
      https://cloud.tencent.com/document/product/269/2282
      :return: response
      response.content
        {
          "ActionStatus": "OK",
          "ErrorInfo": "",
          "ErrorCode": 0,
          "MsgTime": 1572870301,
          "MsgKey": "89541_2574206_1572870301"
        }
      """
    rest_url = "{}/openim/batchsendmsg".format(self.tecent_url)
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(batchMessageObj.__dict__))
    except Exception as e:
      logger.error("batch send message faield:{}".format(e))
      return None

  def import_message_to_im(self, messgeObj: MessageObj, timestamp: int, sync_from_old: int = 1):
    """
        import history message to im server
        https://cloud.tencent.com/document/product/269/2568
        :return: response
        response.content
        {
            "ActionStatus" : "OK",
            "ErrorInfo" : "",
            "ErrorCode" : 0
        }

        """
    rest_url = "{}/openim/importmsg".format(self.tecent_url)
    data = messgeObj.__dict__
    data["MsgTimeStamp"] = timestamp
    data["SyncFromOldSystem"] = sync_from_old

    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("import message failed:{}".format(e))
      return None

  def get_message_list(
    self,
    from_account: str,
    to_account: str,
    max_count: int,
    from_timestamp: int,
    to_timestamp: int,
    last_message_key: str = ""
  ):
    """
        get message
        https://cloud.tencent.com/document/product/269/42794
        :param from_account:
        :param to_account:
        :param max_count: number of messages
        :param from_timestamp: from timestamp
        :param to_timestamp:  from timestamp
        :param last_message_key: if you want get next message you should transfer it(from LastMsgKey)
        :return: response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0,
            "Complete": 1,
            "MsgCnt": 1,
            "LastMsgTime": 1584669680,
            "LastMsgKey": "549396494_2578554_1584669680",
            "MsgList": [
                {
                    "From_Account": "user1",
                    "To_Account": "user2",
                    "MsgSeq": 549396494,
                    "MsgRandom": 2578554,
                    "MsgTimeStamp": 1584669680,
                    "MsgFlagBits": 0,
                    "MsgKey": "549396494_2578554_1584669680",
                    "MsgBody": [
                        {
                            "MsgType": "TIMTextElem",
                            "MsgContent": {
                                "Text": "1"
                            }
                        }
                    ],
                    "CloudCustomData": "your cloud custom data"
                }
            ]
        }
        """
    rest_url = "{}/openim/admin_getroammsg".format(self.tecent_url)
    data = {}
    data["From_Account"] = from_account
    data["To_Account"] = to_account
    data["MaxCnt"] = max_count
    data["MinTime"] = from_timestamp
    data["MaxTime"] = to_timestamp
    if last_message_key != "":
      data["LastMsgKey"] = last_message_key
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("get message failed:{}".format(e))
      return None

  def draw_message(self, from_account: str, to_account: str, msg_key: str):
    """
        draw message
        https://cloud.tencent.com/document/product/269/38980

        :param from_account:
        :param to_account:
        :param msg_key:
        :return: resposne
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0
        }
        """
    rest_url = "{}/openim/admin_msgwithdraw".format(self.tecent_url)
    data = {}
    data["From_Account"] = from_account
    data["To_Account"] = to_account
    data["MsgKey"] = msg_key
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("draw message failed:{}".format(e))
      return None

  def set_user_message_read(self, from_account: str, to_account: str, read_timestamp: int = 0):
    """
        set user message read
        https://cloud.tencent.com/document/product/269/50349
        :param from_account: user id for message read
        :param to_account:
        :param read_timestamp: read message before read_timestamp if message_read_timestamp we will set current time
        :return: response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0
        }
        """
    rest_url = "{}/openim/admin_set_msg_read".format(self.tecent_url)
    data = {}
    data["Report_Account"] = from_account
    data["Peer_Account"] = to_account
    if read_timestamp != 0:
      data["MsgReadTime"] = read_timestamp
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("set  message read failed:{}".format(e))
      return None

  def get_unread_num(self, from_account: str, to_accounts: List[str] = []):
    """
        get unread message num
        https://cloud.tencent.com/document/product/269/56043
        :param from_account:
        :param to_accounts:
        :return: response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0,
            "C2CUnreadMsgNumList": [
                {
                    "Peer_Account": "dramon2",
                    "C2CUnreadMsgNum": 12
                },
                {
                    "Peer_Account": "teacher",
                    "C2CUnreadMsgNum": 12
                }
            ]
        }
        """
    rest_url = "{}/openim/get_c2c_unread_msg_num".format(self.tecent_url)
    data = {}
    data["To_Account"] = from_account
    if len(to_accounts) > 0:
      data["Peer_Account"] = to_accounts
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("set  message read failed:{}".format(e))
      return None

  def get_group(self, limit_nm: int = 1000, next_num: int = 0, group_type: str = ""):
    """
        get group
        https://cloud.tencent.com/document/product/269/1614
        :param limit_nm: max number one request you get
        :param next_num: next page
        :param group_type: you can choice Public（公开群），Private（即 Work，好友工作群），ChatRoom（即 Meeting，会议群），AVChatRoom（音视频聊天室），
        BChatRoom（在线成员广播大群）和社群（Community）
        :return:response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0,
            "TotalCount": 2,
            "GroupIdList": [
                {
                    "GroupId": "@TGS#2J4SZEAEL"
                },
                {
                    "GroupId": "@TGS#2C5SZEAEF"
                }
            ],
            "Next": 4454685361
        }
        """
    rest_url = "{}/group_open_http_svc/get_appid_group_list".format(self.tecent_url)

    data = {}
    data["Limit"] = limit_nm
    data["Next"] = next_num
    data["GroupType"] = group_type
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("set  message read failed:{}".format(e))
      return None

  def create_group(self, groupObj: GroupObj):
    """
        create group
        https://cloud.tencent.com/document/product/269/1615
        :return: response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0,
            "GroupId": "@TGS#2J4SZEAEL"
        }
        """
    rest_url = "{}/group_open_http_svc/create_group".format(self.tecent_url)
    data = groupObj.__dict__
    group_type = data.get("Type")
    if group_type not in ["Public", "Private", "ChatRoom", "AVChatRoom", "Community"]:
      logger.error("group type only choice Public,Private,ChatRoom,AVChatRoom,Community")
      return None
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("group create failed:{}".format(e))
      return None

  def get_group_detail(
    self,
    group_id_list: List[str],
    baseInfoFilter: List[str] = [],
    memInfoFilter: List[str] = [],
    appDefineDataFilterGroup: List[str] = [],
    appDefineDataFilterMem: List[str] = []
  ):
    """
        https://cloud.tencent.com/document/product/269/1616
        :param group_id_list:
        :return:response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "", // 这里的 ErrorInfo 无意义，需要判断每个群组的 ErrorInfo
            "ErrorCode": 0, // 这里的 ErrorCode 无意义，需要判断每个群组的 ErrorCode
            "GroupInfo": [ // 返回结果为群组信息数组，为简单起见这里仅列出一个群
                {
                    "GroupId": "@TGS#2J4SZEAEL",
                    "ErrorCode": 0, // 针对该群组的返回结果
                    "ErrorInfo": "" , // 针对该群组的返回结果
                    "Type": "Public", // 群组类型
                    "Name": "MyFirstGroup", // 群组名称
                    "Appid":1400001001,//即时通信应用的 SDKAppID
                    "Introduction": "TestGroup", // 群组简介
                    "Notification": "TestGroup", // 群组通知
                    "FaceUrl": "http://this.is.face.url", // 群组头像
                    "Owner_Account": "leckie", // 群主 ID
                    "CreateTime": 1426976500, // 群组创建时间（UTC 时间）
                    "LastInfoTime": 1426976500, // 最后群资料变更时间（UTC 时间）
                    "LastMsgTime": 1426976600, // 群内最后一条消息的时间（UTC 时间）
                    "NextMsgSeq": 1234,
                    "MemberNum": 2, // 当前群成员数量
                    "MaxMemberNum": 50, // 最大群成员数量
                    "ApplyJoinOption": "FreeAccess", // 申请加群处理方式
                    "ShutUpAllMember": "On", // 群全员禁言状态
                    "AppDefinedData": [ // 群组维度的自定义字段
                        {
                            "Key": "GroupTestData1", // 自定义字段的key
                            "Value": "xxxx" // 自定义字段的值
                        },
                        {
                            "Key": "GroupTestData2",
                            "Value": "abc\u0000\u0001" // 自定义字段支持二进制数据
                        }
                    ],
                    "MemberList": [ // 群成员列表
                        {
                            "Member_Account": "leckie", // 成员 ID
                            "Role": "Owner", // 群内角色
                            "JoinTime": 1425976500, // 入群时间（UTC 时间）
                            "MsgSeq": 1233,
                            "MsgFlag": "AcceptAndNotify", // 消息屏蔽选项
                            "LastSendMsgTime": 1425976500, // 最后发言时间（UTC 时间）
                            "ShutUpUntil": 1431069882, // 禁言截止时间（UTC 时间）
                            "AppMemberDefinedData": [ // 群成员自定义字段
                                {
                                     "Key": "MemberDefined1",
                                     "Value": "ModifyDefined1"
                                },
                                {
                                     "Key": "MemberDefined2",
                                     "Value": "ModifyDefined2"
                                }
                            ]
                        },
                        {
                            "Member_Account": "peter",
                            "Role": "Member",
                            "JoinTime": 1425976500, // 入群时间
                            "MsgSeq": 1233,
                            "MsgFlag": "AcceptAndNotify",
                            "LastSendMsgTime": 1425976500, // 最后一次发消息的时间
                            "ShutUpUntil": 0, // 0表示未被禁言，否则为禁言的截止时间
                            "AppMemberDefinedData":[ // 群成员自定义字段
                                {
                                    "Key": "MemberDefined1",
                                    "Value": "ModifyDefined1"
                                },
                                {
                                    "Key":"MemberDefined2",
                                    "Value":"ModifyDefined2"
                                }
                             ]
                        }
                    ]
                }
            ]
        }
        """
    rest_url = "{}/group_open_http_svc/get_group_info".format(self.tecent_url)

    data = {}
    data["GroupIdList"] = group_id_list
    responseFilter = {}
    if len(baseInfoFilter) > 0:
      responseFilter["GroupBaseInfoFilter"] = baseInfoFilter

    if len(memInfoFilter) > 0:
      responseFilter["MemberInfoFilter"] = memInfoFilter

    if len(appDefineDataFilterGroup) > 0:
      responseFilter["AppDefinedDataFilter_Group"] = appDefineDataFilterGroup

    if len(appDefineDataFilterMem) > 0:
      responseFilter["AppDefinedDataFilter_GroupMember"] = appDefineDataFilterMem

    if len(responseFilter) > 0:
      data["ResponseFilter"] = responseFilter

    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("get group info failed:{}".format(e))
      return None

  def get_group_mem_info_detail(
    self,
    group_id: str,
    limit_count: int = 100,
    offset: int = 0,
    memInfoFilter: List[str] = [],
    memRoleFilter: List[str] = [],
    next: str = "",
    appDefineDataFilterMem: List[str] = []
  ):
    """
        https://cloud.tencent.com/document/product/269/1617
        :param group_id:
        :param limit_count:
        :param offset:
        :return: response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0,
            "Next": "144115265295492787", // 仅社群会返回该字段
            "MemberNum": 2, // 本群组的群成员总数
            "MemberList": [ // 群成员列表
                {
                    "Member_Account": "bob",
                    "Role": "Owner",
                    "JoinTime": 1425976500, // 入群时间
                    "MsgSeq": 1233,
                    "MsgFlag": "AcceptAndNotify",
                    "LastSendMsgTime": 1425976500, // 最后一次发消息的时间
                    "ShutUpUntil": 1431069882, // 禁言截至时间（秒数）
                    "AppMemberDefinedData": [ //群成员自定义字段
                        {
                           "Key": "MemberDefined1",
                           "Value": "ModifyDefined1"
                        },
                        {
                            "Key": "MemberDefined2",
                            "Value": "ModifyDefined2"
                        }
                     ]
                },
                {
                    "Member_Account": "peter",
                    "Role": "Member ",
                    "JoinTime": 1425976500,
                    "MsgSeq": 1233,
                    "MsgFlag": "AcceptAndNotify",
                    "LastSendMsgTime": 1425976500,
                    "ShutUpUntil": 0, // 0表示未被禁言，否则为禁言的截止时间
                    "AppMemberDefinedData": [ // 群成员自定义字段
                        {
                           "Key": "MemberDefined1",
                           "Value": "ModifyDefined1"
                        },
                        {
                            "Key": "MemberDefined2",
                            "Value": "ModifyDefined2"
                        }
                     ]
                }
            ]
        }
        """
    rest_url = "{}/group_open_http_svc/get_group_member_info".format(self.tecent_url)

    data = {}
    data["GroupId"] = group_id
    data["Limit"] = limit_count
    data["Offset"] = offset
    if len(memInfoFilter) > 0:
      data["MemberInfoFilter"] = memInfoFilter

    if len(memRoleFilter) > 0:
      data["MemberRoleFilter"] = memRoleFilter

    if len(appDefineDataFilterMem) > 0:
      data["AppDefinedDataFilter_GroupMember"] = appDefineDataFilterMem

    if next != "":
      data["Next"] = next

    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("get group member info failed:{}".format(e))
      return None

  def update_group_baseinfo(
    self,
    group_id: str,
    group_name: str = "",
    introduction: str = "",
    notification: str = "",
    face_url: str = "",
    max_member_num: int = 0,
    appJoinOption: str = "",
    shutUpFlag: str = "",
    appDefineData: List[GroupAppDefinedData] = []
  ):
    """
        https://cloud.tencent.com/document/product/269/1620
        :param group_id:
        :param group_name:
        :param introduction:
        :param notification:
        :param face_url:
        :param max_member_num:
        :param appJoinOption:
        :param shutUpFlag:
        :return: response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0
        }
        """
    rest_url = "{}/group_open_http_svc/modify_group_base_info".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    if group_name != "":
      data["Name"] = group_name
    if introduction:
      data["Introduction"] = introduction
    if notification:
      data["Notification"] = notification
    if face_url:
      data["FaceUrl"] = face_url
    if max_member_num > 0:
      data["MaxMemberNum"] = max_member_num
    if appJoinOption != "":
      data["ApplyJoinOption"] = appJoinOption
    if shutUpFlag == "On" or shutUpFlag == "Off":
      data["ShutUpAllMember"] = shutUpFlag

    if len(appDefineData) > 0:
      data["AppDefinedData"] = [i.__dict__ for i in appDefineData]

    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("update group info failed:{}".format(e))
      return None

  def add_group_member(self, group_id: str, mem_list: List[GroupMemObj], silence: int = 1):
    """
        https://cloud.tencent.com/document/product/269/1621
        :param group_id:
        :param mem_list:
        :param silence:
        :return:
        """
    rest_url = "{}/group_open_http_svc/add_group_member".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    data["Silence"] = silence
    data["MemberList"] = [i.__dict__ for i in mem_list]
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("add mem to group info failed:{}".format(e))
      return None

  def delete_group_mem(self, group_id: str, mem_list: List[str], silence: int = 1):
    """
        https://cloud.tencent.com/document/product/269/1622
        :param group_id:
        :param mem_list:
        :param silence:
        :return:response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0
        }
        """
    rest_url = "{}/group_open_http_svc/delete_group_member".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    data["Silence"] = silence
    data["MemberToDel_Account"] = mem_list
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("add mem to group info failed:{}".format(e))
      return None

  def update_group_mem_info(
    self,
    group_id: str,
    mem_id: str,
    role_type: str = "",
    namecard: str = "",
    appMemDefineData: List[GroupAppDefinedData] = [],
    shutUpTime: int = 0
  ):
    """
        https://cloud.tencent.com/document/product/269/1623
        :param group_id:
        :param mem_id:
        :param role_type:
        :param namecard:
        :param appMemDefineData:
        :param shutUpTime:
        :return:
        """
    rest_url = "{}/group_open_http_svc/modify_group_member_info".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    data["Member_Account"] = mem_id
    if role_type == "Member" or role_type == "Admin":
      data["Role"] = role_type
    if namecard != "":
      data["NameCard"] = namecard
    if shutUpTime > 0:
      data["ShutUpTime"] = shutUpTime

    if len(appMemDefineData) > 0:
      data["AppMemberDefinedData"] = [i.__dict__ for i in appMemDefineData]

    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("update mem to group info failed:{}".format(e))
      return None

  def delete_group(self, group_id: str):
    """
        https://cloud.tencent.com/document/product/269/1624
        :param group_id:
        :return:
        """
    rest_url = "{}/group_open_http_svc/destroy_group".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("update mem to group info failed:{}".format(e))
      return None

  def get_joined_groups(
    self,
    user_id: str,
    limit_count: int = 0,
    offset: int = 0,
    group_type: str = "",
    baseInfoFilter: List[str] = [],
    selfInfoFilter: List[str] = []
  ):
    """
        https://cloud.tencent.com/document/product/269/1625
        :param user_id:
        :param limt_count:
        :param offset:
        :param group_type:
        :param baseInfoFilter:
        :param selfInfoFilter:
        :return:response
        reponse.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0,
            "TotalCount": 1, // 不论 Limit 和 Offset 如何设置，该值总是满足条件的群组总数
            "GroupIdList": [
                {
                    "ApplyJoinOption": "DisableApply",
                    "CreateTime": 1585718204,
                    "FaceUrl": "",
                    "GroupId": "@TGS#16UMONKGG",
                    "Introduction": "",
                    "LastInfoTime": 1588148506,
                    "LastMsgTime": 0,
                    "MaxMemberNum": 200,
                    "MemberNum": 1,
                    "Name": "d",
                    "NextMsgSeq": 2,
                    "Notification": "",
                    "Owner_Account": "",
                    "SelfInfo": {
                        "JoinTime": 1588148506,
                        "MsgFlag": "AcceptAndNotify",
                        "Role": "Member",
                        "MsgSeq": 1
                    },
                    "ShutUpAllMember": "Off",
                    "Type": "Private"
                }
            ]
        }
        """
    rest_url = "{}/group_open_http_svc/get_joined_group_list".format(self.tecent_url)
    data = {}
    data["Member_Account"] = user_id
    if limit_count > 0:
      data["Limit"] = limit_count
    if offset > 0:
      data["Offset"] = offset

    if group_type != "":
      data["GroupType"] = group_type

    responseFilter = {}
    if len(baseInfoFilter) > 0:
      responseFilter["GroupBaseInfoFilter"] = baseInfoFilter

    if len(selfInfoFilter) > 0:
      responseFilter["SelfInfoFilter"] = selfInfoFilter

    if len(responseFilter) > 0:
      data["ResponseFilter"] = responseFilter
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("update mem to group info failed:{}".format(e))
      return None

  def get_mem_role_in_group(self, group_id: str, user_ids: List[str]):
    """
        https://cloud.tencent.com/document/product/269/1626
        :param group_id:
        :param user_ids:
        :return:response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0,
            "UserIdList": [ // 结果
                {
                    "Member_Account": "leckie",
                    "Role": "Owner" // 成员角色：Owner/Admin/Member/NotMember
                },
                {
                    "Member_Account": "peter",
                    "Role": "Member"
                },
                {
                    "Member_Account": "wesley",
                    "Role": "NotMember"
                }
            ]
        }
        """
    rest_url = "{}/group_open_http_svc/get_role_in_group".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    data["User_Account"] = user_ids
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("get mem role in group failed:{}".format(e))
      return None

  def forbid_send_msg(self, group_id: str, user_ids: List[str], shutUpTime: int):
    """
        https://cloud.tencent.com/document/product/269/1627
        :param group_id:
        :param user_ids:
        :param shutUpTime: if shutUpTime =0  cancel shutup
        :return:response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0
        }
        """
    rest_url = "{}/group_open_http_svc/forbid_send_msg".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    data["Members_Account"] = user_ids
    data["ShutUpTime"] = shutUpTime
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("get mem role in group failed:{}".format(e))
      return None

  def get_group_shutup_list(self, group_id: str):
    """
        https://cloud.tencent.com/document/product/269/2925
        :param group_id:
        :return:response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorCode": 0,
            "GroupId": "@TGS#2FZNNRAEU",
            "ShuttedUinList": [ // 群组中被禁言的用户列表
                {
                    "Member_Account": "tommy", // 用户 ID
                    "ShuttedUntil": 1458115189 // 禁言到的时间（使用 UTC 时间，即世界协调时间）
                },
                {
                    "Member_Account": "peter",
                    "ShuttedUntil": 1458115189
                }
            ]
        }
        """
    rest_url = "{}/group_open_http_svc/get_group_shutted_uin".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("get mem role in group failed:{}".format(e))
      return None

  def send_group_message(
    self,
    group_id: str,
    messageText: List[MessageText] = [],
    attchements: List[MessageFile] = [],
    to_accounts: List[str] = [],
    from_account: str = "",
    msgPriority: str = "",
  ):
    """
        https://cloud.tencent.com/document/product/269/1629
        :param group_id:
        :param messageText:
        :param attchements:
        :param to_accounts:
        :param from_account:
        :param msgPriority:
        :return:response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0,
            "MsgTime": 1497249503,
            "MsgSeq": 1
        }
        """
    rest_url = "{}/group_open_http_svc/send_group_msg".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    data["Random"] = random.randint(0, 4294967295)
    if len(to_accounts) > 0:
      data["To_Account"] = to_accounts

    if from_account != "":
      data["From_Account"] = from_account

    if msgPriority == "High" or msgPriority == "Low":
      data["MsgPriority"] = msgPriority

    messageBody = []
    if len(messageText) > 0:
      messageBody.extend([i.__dict__ for i in messageText])

    if len(attchements) > 0:
      messageBody.extend([i.__dict__ for i in attchements])

    if len(messageBody) > 0:
      data["MsgBody"] = messageBody

    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("send message in group failed:{}".format(e))
      return None

  def send_system_message_in_group(self, group_id: str, content: str, to_accounts: List[str] = []):
    """
        https://cloud.tencent.com/document/product/269/1630
        :param group_id:
        :param content:
        :param to_accounts:
        :return:response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0
        }
        """

    rest_url = "{}/group_open_http_svc/send_group_system_notification".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    data["Content"] = content

    if len(to_accounts) > 0:
      data["ToMembers_Account"] = to_accounts

    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("send message in group failed:{}".format(e))
      return None

  def change_group_owner(self, group_id: str, new_owner_id: str):
    """
        https://cloud.tencent.com/document/product/269/1633
        :param group_id:
        :param new_owner_id:
        :return: response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0
        }
        """
    rest_url = "{}/group_open_http_svc/change_group_owner".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    data["NewOwner_Account"] = new_owner_id

    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("change group owner failed:{}".format(e))
      return None

  def recall_group_message(self, group_id: str, msg_ids: List[str]):
    """
        https://cloud.tencent.com/document/product/269/12341
        :param group_id:
        :param msg_ids:
        :return:response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0,
            "RecallRetList":[
                {
                    "MsgSeq":100,
                    "RetCode":10030
                },
                {
                    "MsgSeq":101,
                    "RetCode":0
                }
            ]
        }
        """
    rest_url = "{}/group_open_http_svc/group_msg_recall".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    msgs = []
    for i in msg_ids:
      tmp_map = {}
      tmp_map["MsgSeq"] = i
      msgs.append(tmp_map)

    data["MsgSeqList"] = msgs

    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("recall group message failed:{}".format(e))
      return None

  def import_message_to_group(
    self, group_id: str, recent_contract_flag: int = 1, messages: List[GroupMessageObj] = []
  ):
    """
        https://cloud.tencent.com/document/product/269/1635
        :param group_id:
        :param recent_contract_flag:
        :param messages:
        :return:response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0,
            "ImportMsgResult": [
                {
                    "MsgSeq": 1,
                    "MsgTime": 1620808101,
                    "Result": 0
                },
                {
                    "MsgSeq": 2,
                    "MsgTime": 1620892821,
                    "Result": 0
                },
            ]
        }
        """
    rest_url = "{}/group_open_http_svc/import_group_msg".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    data["RecentContactFlag"] = recent_contract_flag
    if len(messages) > 0:
      data["MsgList"] = [i.__dict__ for i in messages]
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("import group message failed:{}".format(e))
      return None

  def import_group_members(self, group_id: str, mem_list: List[GroupMemObj] = []):
    """
        https://cloud.tencent.com/document/product/269/1636
        :param group_id:
        :param mem_list:
        :return:response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0,
            "MemberList": [
            {
                 "Member_Account": "tommy",
                 "Result": 1 // 导入结果：0表示失败；1表示成功；2表示已经是群成员
            },
            {
                 "Member_Account": "jared",
                 "Result": 1
            }]
        }
        """
    rest_url = "{}/group_open_http_svc/import_group_member".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    if len(mem_list) > 0:
      data["MemberList"] = [i.__dict__ for i in mem_list]
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("import group message failed:{}".format(e))
      return None

  def set_group_unread_msg_num(self, group_id: str, mem_id: str, unread_num: int):
    """
        https://cloud.tencent.com/document/product/269/1637
        :param group_id:
        :param mem_id:
        :param unread_num:
        :return: response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0
        }
        """
    rest_url = "{}/group_open_http_svc/set_unread_msg_num".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    data["Member_Account"] = mem_id
    data["UnreadMsgNum"] = unread_num
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("import group message failed:{}".format(e))
      return None

  def delete_group_msg_by_sender(self, group_id: str, send_account: str):
    """
        https://cloud.tencent.com/document/product/269/2359
        :param group_id:
        :param send_account:
        :return:
        """
    rest_url = "{}/group_open_http_svc/delete_group_msg_by_sender".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    data["Sender_Account"] = send_account
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("delete mesg in group  failed:{}".format(e))
      return None

  def get_msg_in_group(
    self, group_id: str, msg_num: int, with_recalled_msg: int = 1, msg_seq: int = 0
  ):
    """
        https://cloud.tencent.com/document/product/269/2738
        :param group_id:
        :param msg_num:
        :param with_recalled_msg:
        :param msg_seq:
        :return:response
        response.content
                {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0,
            "GroupId": "@TGS#15ERQPAER",
            "IsFinished": 1,
            "RspMsgList": [
                {
                    "From_Account": "144115197276518801",
                    "IsPlaceMsg": 0,
                    "MsgBody": [
                        {
                            "MsgContent": {
                                "Data": "\b\u0001\u0010\u0006\u001A\u0006猫瞳",
                                "Desc": "MIF",
                                "Ext": ""
                            },
                            "MsgType": "TIMCustomElem"
                        },
                        {
                            "MsgContent": {
                                "Data": "",
                                "Index": 15
                            },
                            "MsgType": "TIMFaceElem"
                        }
                    ],
                    "MsgPriority": 1,
                    "MsgRandom": 51083293,
                    "MsgSeq": 7803321,
                    "MsgTimeStamp": 1458721802
                },
                {
                    "From_Account": "144115198339527735",
                    "IsPlaceMsg": 0,
                    "MsgBody": [
                        {
                            "MsgContent": {
                                "Data": "\b\u0001\u0010\u0006\u001A\u000F西瓜妹妹。",
                                "Desc": "MIF",
                                "Ext": ""
                            },
                            "MsgType": "TIMCustomElem"
                        },
                        {
                            "MsgContent": {
                                "Text": "报上来"
                            },
                            "MsgType": "TIMTextElem"
                        }
                    ],
                    "MsgPriority": 1,
                    "MsgRandom": 235168582,
                    "MsgSeq": 7803320,
                    "MsgTimeStamp": 1458721797
                }
            ]
        }

        """
    rest_url = "{}/group_open_http_svc/group_msg_get_simple".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    data["ReqMsgNumber"] = msg_num
    data["WithRecalledMsg"] = with_recalled_msg
    if msg_seq > 0:
      data["ReqMsgSeq"] = msg_seq
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("get msg in group  failed:{}".format(e))
      return None

  def get_online_member_num(self, group_id: str):
    """
        https://cloud.tencent.com/document/product/269/49180
        :param group_id:
        :return:response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0,
            "OnlineMemberNum":1000 //在线人数
        }
        """
    rest_url = "{}/group_open_http_svc/get_online_member_num".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("get mem number in online group failed:{}".format(e))
      return None

  def get_group_attr(self, group_id: str):
    """
        https://cloud.tencent.com/document/product/269/67012
        :param group_id:
        :return:response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0,
            "GroupAttrAry": [
                {
                    "key": "attr_key1",
                    "value": "attr_val1"
                },
                {
                    "key": "attr_key2",
                    "value": "attr_val2"
                }
            ]
        }
        """
    rest_url = "{}/group_open_attr_http_svc/get_group_attr".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("get group attr failed:{}".format(e))
      return None

  def update_group_attr(self, group_id: str, attr_list: List[GroupAttr]):
    """
        https://cloud.tencent.com/document/product/269/67010
        :param group_id:
        :param attr_list:
        :return:response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0
        }
        """
    rest_url = "{}/group_open_http_svc/modify_group_attr".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    data["GroupAttr"] = [i.__dict__ for i in attr_list]
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("update group attrfailed:{}".format(e))
      return None

  def clean_group_attr(self, group_id: str):
    """
        https://cloud.tencent.com/document/product/269/67009
        :param group_id:
        :return:response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0
        }
        """
    rest_url = "{}/group_open_http_svc/clear_group_attr".format(self.tecent_url)
    data = {}
    data["GroupId"] = group_id
    try:
      query = self._gen_query()
      return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
      logger.error("update group attrfailed:{}".format(e))
      return None


if __name__ == "__main__":
  pass

  pass
