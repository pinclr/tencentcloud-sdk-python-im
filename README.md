# tencentcloud-sdk-python-tim

Tencent Cloud Python SDK for TIM (Tencent IM)

## INSTALL

```shell
pip install tencentcloud-sdk-python-im --upgrade 
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
python setup.py bdist_wheel
```

## RELEASE
```shell
twine upload --verbose --repository pypi dist/* 
INFO     Using configuration from /home/robert/.pypirc                                                                    
Uploading distributions to https://upload.pypi.org/legacy/
INFO     dist/tencentcloud_sdk_python_im-0.9.4-py3-none-any.whl (17.3 KB)                                                 
INFO     username set from config file                                                                                    
INFO     password set from config file                                                                                    
INFO     username: __token__                                                                                              
INFO     password: <hidden>                                                                                               
Uploading tencentcloud_sdk_python_im-0.9.4-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 22.1/22.1 kB • 00:00 • 149.6 MB/s
INFO     Response from https://upload.pypi.org/legacy/:                                                                   
         200 OK                                                                                                           

View at:
https://pypi.org/project/tencentcloud-sdk-python-im/0.9.4/
```

![Github Checker](https://github.com/pinclr/tencentcloud-sdk-python-tim/actions/workflows/python-app.yml/badge.svg?branch=main)
[![Pypi](https://img.shields.io/pypi/v/tencentcloud-sdk-python-im.svg)](https://pypi.org/project/tencentcloud-sdk-python-im/)
[![Documentation Status](https://readthedocs.org/projects/tencentcloud-sdk-python-im/badge/?version=latest)](https://tencentcloud-sdk-python-im.readthedocs.io/en/latest/?badge=latest)
[![Downloads](https://pepy.tech/badge/tencentcloud-sdk-python-im)](https://pepy.tech/project/tencentcloud-sdk-python-im)
![GitHub](https://img.shields.io/github/license/pinclr/tencentcloud-sdk-python-tim)
