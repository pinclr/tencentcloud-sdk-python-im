# tencentcloud-sdk-python-tim
Tencent Cloud Python SDK for TIM (Tencent IM)


### 接口列表
目前封装了以下接口
- add_single_user #创建用户 
- batch_add_users #批量创建用户
- del_user  #删除用户
- search_user  #查询用户
- abolition_user_sig #废除usersig
- check_user_online  #检查用户是否在线
- add_friend       # 添加好友
- delete_friends #删除好友
- update_friend   #更新遨游
- add_group       #新增分组
- delete_group    #删除分组
- get_group       #获取分组

### 使用方法
```python
sdk_id = 23344
key = "xxx"
admin = "xxcvc"

client = TimClient(sdk_id,key,admin)

resp = client.add_single_user(user_id="df",username="xxx",face_url="xx")
if resp == None:
    print("网络问题"）
else:
    if resp.get("action_status") == "OK":
        print("OK")
    else:
       print("失败")







```



