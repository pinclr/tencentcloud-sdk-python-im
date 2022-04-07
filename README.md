# tencentcloud-sdk-python-tim

Tencent Cloud Python SDK for TIM (Tencent IM)

## INSTALL

```shell
$ pip install --upgrade tencentcloud-sdk-python-im
```

## EXAMPLES

```shell
>>> from tencentcloud_im.tcim_client import TCIMClient
>>> client = TCIMClient(sdk_id, sdk_secret, admin_account)
>>>
>>> client.gen_user_sig(user_id)
>>>
>>> client.add_single_user(user_id, nick_name, face_url)
```

### TEST
```shell
pytest
```

## BUILD

```shell
$ python3 -m build
```
