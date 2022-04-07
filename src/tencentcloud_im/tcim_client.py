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


import random
import requests
import json
from typing import List
from datetime import datetime
from tencentcloud_im.user_sig import TLSSigAPIv2
import logging

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







class FriendObj(object):
  """
  好友结构体
  """

  def __init__(self, to_account,add_source, remark="", group_name="", ):
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
  tag:
  Tag_SNS_IM_Group:Array 好友分组 value: [] 分组信息
  Tag_SNS_IM_Remark：好友备注：    value:str 好友备注
  Tag_SNS_IM_AddSource：好友来源   value:str
  Tag_SNS_IM_AddWording：好友附言  value:str
  Tag_SNS_IM_AddTime：好友时间戳   value:int
  """

  def __init__(self, tag: str, value: str):
    """

    :param tag: 需要更新的字段：
                - Remark
                - Group
    :param value:
    """
    self.Tag = "Tag_SNS_IM_{}".format(tag)
    self.Value = value


class UpdateFriendObj(object):
  """
  更新好友结构体
  """

  def __init__(self, to_account, sns_items:List[SnsItemObj]):
    self.To_Account = to_account
    SnsItem = []
    for sns_item in sns_items:
        SnsItem.append(sns_item.__dict__)
    self.SnsItem = SnsItem


# def Resposne(ActionStatus=None, ErrorInfo=None, ErrorCode=None,
#              FailAccounts=None, ResultItem=None, UserDataItem=None,
#              FriendNum=None, NextStartIndex=None, CompleteFlag=None,
#              Fail_Account=None,ErrorDisplay=None,ResultCode=None):
#   """
#   :param ActionStatus: 请求处理的结果，OK 表示处理成功，FAIL 表示失败
#   :param ErrorInfo:错误信息
#   :param ErrorCode:错误码，0表示成功，非0表示失败
#   :param:ResultItem: 单个帐号的结果对象数组
#   :param FailAccounts:失败账户
#   :param: UserDataItem: 好友信息
#   :param: FriendNum:好友数
#   :param:NextStartIndex:分页接口下一页的起始位置
#   :param: CompleteFlag:分页的结束标识，非0值表示已完成全量拉取
#   :return:
#   """
#   result = {}
#   result["action_status"] = ActionStatus
#   result["error_info"] = ErrorInfo
#   result["err_code"] = ErrorCode
#   result["faile_accounts"] = FailAccounts
#   result["result_item"] = ResultItem
#   result["userdata_item"] = UserDataItem
#   result["friend_num"] = FriendNum
#   result["next_start_index"] = NextStartIndex
#   result["complate_flag"] = CompleteFlag
#   result["faile_account"] = Fail_Account
#   result["err"]
#
#
#   return result







class TCIMClient(object):
  def __init__(self, sdk_id, key, admin, tencent_url=TCIM_API_BASE, expire_time=60 * 5):
    """

    :param sdk_id: sdk_id
    :param key:    key
    :param admin:  管理员账户
    :param tencent_url:  腾讯URL
    :param expire_time:  过期时间
    """
    self.sdk_id = sdk_id
    self.key = key
    self.admin = admin
    self.tecent_url = tencent_url
    self.expire_time = expire_time
    self.next_time = datetime.now()
    self.user_sig = None

  def get_user_sig(self, user_id: str, expire_time: str):
    """
    生成user_sig
    :param user_id: 用户user_id,
    :param expire_time: 过期时间：单位为秒
    :return:
    """
    api = TLSSigAPIv2(self.sdk_id, self.key)
    sig = api.genUserSig(user_id, expire_time)
    return sig

  def _gen_query(self):
    """
    生成后端操作的rest url
    :param sdk_id:
    :param admin:
    :param user_sig:
    :return:
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
    创建用户
    :param user_id
    :param nick_name:
    :param face_url:
    :return:
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



  def batch_add_users(self, user_ids:List[str]):

    """
    批量增加用户:单词最多100个
    :param user_ids: user_ids 列表["a","b","c"]
    :return:
    """
    if len(user_ids) == 0:
      return

    try:
        rest_url = "{}/v4/im_open_login_svc/multiaccount_import".format(self.tecent_url)
        data = {}
        data["Accounts"] = user_ids
        query = self._gen_query()
        return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
        logger.error("batch add user failed:{}".format(e))
        return None


  def del_user(self, user_ids:List[str]):

    """
    删除用户
    :param user_ids: user_ids 列表["a","b","c"]
    :return:
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

  def search_user(self, user_ids:List[str]):

    """
    查询账户
    :param user_ids: user_ids 列表["a","b","c"]
    :return:
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
    废除某个账号的user_sig,可以让该账号直接登陆失败
    :param user_id:
    :return:
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


  def check_user_online(self, user_ids:List[str]):
    """
    检查账户是否在线状态
    :param user_ids:user_ids 列表["a","b","c"]
    :return:
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


  def add_friend(self, from_account: str, friends:List[FriendObj]):
    """
    添加好友
    :param from_account: 需要添加好友的账户
    :param friends: 需要添加哪些好友
    :return:
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


  def delete_friends(self, from_account: str, to_accounts: List[str], delete_type="Delete_Type_Both"):
    """
    删除好友
    :param from_account: 需要删除好友的账户
    :param to_accounts:需要删除好友
    :param delete_type: 删除类型：Delete_Type_Both：双向删除， Delete_Type_Single:单向删除
    :return:
    """
    rest_url = "{}/v4/sns/friend_delete".format(self.tecent_url)
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


  def update_friend(self, from_account: str, update_objs:List[UpdateFriendObj]):
    """
    更新好友
    :param from_account:
    :return:
    """

    rest_url = "{}/v4/sns/friend_update".format(self.tecent_url)
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


  def get_friends(self, from_account: str, start_index: int = 0):

    """
    拉取全部好友
    :param from_account:指定要拉取好友数据的用户的 UserID
    :param:start_index:分页的起始位置,后面该参数继承Response中的next_start_index
    :return:
    """

    rest_url = "{}/v4/sns/friend_get".format(self.tecent_url)
    data = {}
    try:
        data["From_Account"] = from_account
        data["StartIndex"] = start_index
        query = self._gen_query()
        return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
        logger.error("get user failed:{}".format(e))
        return None



  def add_group(self, from_account: str, groups:List[str], to_accounts:List[str]):
    """
    添加分组
    :param from_account  :需要为该 UserID 添加新分组
    :param groups        ：新增分组列表
    :param to_accounts   ：需要加入新增分组的好友的 UserID 列表
    :return:
    """

    rest_url = "{}/v4/sns/group_add".format(self.tecent_url)
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



  def delete_group(self, from_account: str, groups:List[str]):
    """
    删除分组
    :param: from_account:需要删除该 UserID 的分组
    :param  groups: 要删除的分组列表
    :return:
    """

    try:
        rest_url = "{}/v4/sns/group_delete".format(self.tecent_url)
        data = {}
        data["From_Account"] = from_account
        data["GroupName"] = groups
        query = self._gen_query()
        return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
        logger.error("delete group failed:{}".format(e))
        return None



  def get_group(self, from_account: str, groups:List[str]=[],
                need_friend_flag:str = "Need_Friend_Type_Yes"):
    """
    拉取分组
    :param from_account:指定要拉取分组的用户的 UserID
    :param: groups: 需要获取的分组，默认为空则是全部获取
    :param: need_friend_flag: 获取分组好友
    :return:
    """

    rest_url = "{}/v4/sns/group_get".format(self.tecent_url)
    data = {}
    try:
        data["From_Account"] = from_account
        if len(groups) >0:
            data["GroupName"] = groups
        data["NeedFriend"] = need_friend_flag
        query = self._gen_query()
        return requests.post(rest_url, params=query, data=json.dumps(data))
    except Exception as e:
        logger.error("get group failed:{}".format(e))
        return None


if __name__ == "__main__":
  pass