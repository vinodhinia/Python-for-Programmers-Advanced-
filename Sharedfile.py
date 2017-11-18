import os
import sys

import django

sys.path.append("./")


from django.conf import settings
settings.configure()

django.setup()
# from basement.types import Residency
import requests
from requests.utils import quote

def authenticate():
    uri_path = '/oauth/token'
    hostname = 'fileittax.sharefile.com'
    client_id = "JY9pWeQTOq094sfkuaY6PfdAdVucTGMK"
    client_secret = "mqwUGGBF5qmLgbQ67kFj17m22op2eki5dPKD6ni4IfoWLAX0"
    username = "hero@fileit.tax"
    password = "%*$*yano^OungM!*cH27"

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'grant_type': 'password', 'client_id': client_id, 'client_secret': client_secret,
              'username': username, 'password': password}

    response = requests.request("POST", 'https://{}{}'.format(hostname, uri_path), headers=headers, data=params)
    token = None
    if response.status_code == 200:
        token = response.json()['access_token']
        print(token)
    else:
        raise Exception('Unable to authenticate')
    return token


def setup_sharefile(token_str, partial_ssn=None, email=None, password=None, first_name=None, last_name=None):
    data3 = {"LastName": last_name, "Password": password, "Email": email, "FirstName": first_name}
    print('Starting Setup {}'.format(data3))
    if not partial_ssn or not first_name or not email or not password or not last_name:
        print('something missing for the fn to run')
        return False

    headers = {
        'authorization': "Bearer " + token_str,
        'cache-control': "no-cache",
    }
    root_folder_path = '/My Files & Folders/Clients'
    url_prefix = 'https://fileittax.sf-api.com/sf/v3/'
    # root_folder_id = getItemIdByPath(headers, root_folder_path, url_prefix)
    root_folder_id = 'foe9344e-8793-4a4a-b793-e67f85b92f69'

    if root_folder_id:
        print('Root ({})"{}"'.format(root_folder_id, root_folder_path))
        folder_name = "{}, {} ({})".format(last_name, first_name, partial_ssn)
        client_folder_id, client_folder_path, status = get_or_create_folder(folder_name, headers, root_folder_id,
                                                                    root_folder_path, url_prefix)
        if client_folder_id:
            sub_folder_name = 'Upload Your Tax Documents Here'
            sub_folder_id, sub_folder_path, sub_folder_status = get_or_create_folder(sub_folder_name, headers, client_folder_id,
                                                                  client_folder_path, url_prefix)
            if sub_folder_id:
                # If we decide to copy the file in - we can uncomment this section
                # checklist_path = '/My Files & Folders/List of required tax documents.pdf'
                # checklist_id = getItemIdByPath(headers, checklist_path, url_prefix)
                # url6 = '{}Items({})/Copy?targetid={}&overwrite=true'.format(url_prefix, checklist_id, sub_folder_id)
                # response6 = requests.request("POST", url6, headers=headers)
                # if response6.status_code == 200:
                #     fixes.append('Copied "{}" to "{}"'.format(checklist_path, sub_folder_name))
                # else:
                #     issues.append('copy_file ', response6.status_code, response6.content)
                client_id, client_url = get_or_create_user(headers, url_prefix, data3)
                if client_id:
                    print('Client ({}) {} {}'.format(client_id, client_url, email))
                    url5 = '{}Items({})/AccessControls'.format(url_prefix, sub_folder_id)
                    response5 = requests.request("GET", url5, headers=headers)
                    addAcl = True
                    if response5.status_code == 200:
                        print('Access Controls Found: {}'.format(len(response5.json().get('value'))))
                        for acl in response5.json().get('value'):
                            aclUserUrl = acl.get('Principal').get('url')
                            response7 = requests.request("GET", aclUserUrl, headers=headers)
                            response7_json = response7.json()
                            userType = response7_json.get('odata.type')
                            if userType == 'ShareFile.Api.Models.AccountUser' or userType == 'ShareFile.Api.Models.User':
                                print('User Access present for {}'.format(response7_json.get('Email')))
                                print(acl)
                                if response7_json.get('Email') == email:
                                    addAcl = False
                            elif userType == 'ShareFile.Api.Models.Group':
                                print('Group Access present for {}'.format(response7_json.get('Name')))
                            else:
                                print('Unknown Access {}'.format(response7_json))
                    else:
                        print('Access Controls {} {}'.format(response5.status_code, response5.content))
                    if addAcl:
                        status = provider_access_to_folder(token_str, url_prefix,sub_folder_id, client_url)
                        if not status:
                            return False
                    else:
                        print('ACL Exists')
                        return True
                else:
                    print('No client id')
                    return False
            else:
                print('No Folder to Upload Docs')
                return False
        else:
            print('No Client Folder Id')
            return False
    else:
        print('No Root Folder Id')
        return False
    return True


def get_or_create_user(headers, url_prefix, data):
    # Retreive the user - Not required as the create is a get_or_create
    # url2 = '{}Users?emailaddress={}'.format(url_prefix, email)
    # response2 = requests.request("GET", url2, headers=headers)
    # if response2.status_code == 200:
    #    client_id = response2.json().get('Id')
    print('get_or_create_user{}'.format(data.get('Email')))
    client_id = None
    client_url = None
    create_client_params = '?pushCreatorDefaultSettings=false&' \
                           'addshared=false&notify=false&ifNecessary=true&addPersonal=true'
    url3 = '{}Users{}'.format(url_prefix, create_client_params)
    print(url3)
    response3 = requests.request("POST", url3, headers=headers, data=data)
    if response3.status_code == 200:
        response3_json = response3.json()
        client_id = response3_json.get('Id')
        client_url = response3_json.get('url')
    else:
        print('get_or_create_user {} {}'.format(response3.status_code, response3.content))
    return client_id, client_url


def getItemIdByPath(headers, item_path, url_prefix):
    if ' ' in item_path:
        item_path = quote(item_path, safe='')
    url1 = '{}Items/ByPath?path={}'.format(url_prefix, item_path)
    response1 = requests.request("GET", url1, headers=headers)
    item_id = None
    if response1.status_code == 200:
        item_id = response1.json().get('Id')
    else:
        print('getItemIdByPath {} {}'.format(response1.status_code, response1.content))
    return item_id


def get_or_create_folder(folder_name, headers, parent_folder_id, parent_path, url_prefix):
    folder_path = '{}/{}'.format(parent_path, folder_name)
    folder_id = getItemIdByPath(headers, folder_path, url_prefix)
    if folder_id:
        print('SubFolder  Exists {} "{}"'.format(folder_id, folder_name))
        return folder_id, folder_path, 0
    else:
        url2 = '{}Items({})/Folder?overwrite=false&passthrough=false'.format(url_prefix, parent_folder_id)
        data2 = {"Name": "{}".format(folder_name)}
        response2 = requests.request("POST", url2, headers=headers, data=data2)
        if response2.status_code == 200:
            folder_id = response2.json().get('Id')
            print('Subfolder Created {} "{}"'.format(folder_id, folder_name))
            return folder_id, folder_path, 1
        else:
            print(' get_or_create_folder {} {}'.format(response2.status_code, response2.content))
    return None, None, -1


def provider_access_to_folder(token, url_prefix, folder_id, user_url):
    temp_header = {'content-type': 'application/json', 'cache-control': 'no-cache',
                    'authorization': 'Bearer ' + token}
    # client_id = 'e80b5ae392ed-44ee-8340-5ea49d50ee71'
    # client_url = 'https://fileittax.sf-api.com/sf/v3/Users(e80b5ae3-92ed-44ee-8340-5ea49d50ee71)'

    url7 = '{}Items({})/AccessControls?recursive=true'.format(url_prefix, folder_id)
    data7 = '{  "Principal":{"url":"' + user_url + '"}, "CanUpload":true, "CanDownload":true, "CanView":true, "CanDelete":false, "NotifyOnUpload":true, "CanManagePermissions":false}'
    response7 = requests.request("POST", url7, headers=temp_header, data=data7)
    if response7.status_code == 200:
        print('Succesfully created acl')
        return True
    else:
        print(' provide_access_to_folder {} {}'.format(response7.status_code, response7.content))
        return False


def update_crm_task(task, format='xml'):
    from django.conf import settings
    authtoken = settings.CRM_AUTHKEY
    update_URL = 'https://crm.zoho.com/crm/private/{}/{}/updateRecords'.format(format, "Tasks")

    xml_data = '<Tasks>' \
               '<row no="1">' \
               '<FL val="Subject">Send Registration Email</FL><FL val="Status">Completed</FL></row></Tasks>'
    params = {'authtoken': authtoken, 'scope': 'crmapi', 'id': task.activityId, 'xmlData': xml_data}

    r = requests.post(update_URL, data=params)

    if r.status_code == requests.codes.ok and r.text.__contains__("successfully"):
        return 1
    else:
        return -1


# def runner():
#     from crm.models import CrmTasks, CrmClients
#     from basement.types import TaskStatus
#     from crm.services import sync
#     from basement.utils.datetime import nowDatetimeStr
#     from emails.utils import sendEmail
#
#     token_str = authenticate()
#     results = {}
#     sync('clients')
#     sync('tasks')
#     for task in CrmTasks.objects.filter(subject='ShareFile Portal', status=TaskStatus.NS):
#
#         client = CrmClients.objects.filter(email=task.email).first()
#         segment = client.segmentType if client else None
#         residency = client.residencyStatus if client else None
#         if not client:
#             print('Skipping {} as client record not found'.format(task.email))
#             continue
#             print('Starting {}'.format(task.email))
#         status = setup_sharefile(
#             token_str=token_str, partial_ssn=task.last4ssn, email=task.email,
#             password=task.tempPassword, last_name=task.lastName, first_name=task.firstName)
#         results[task.email] = {'status': status}
#         print('Ended {}:{}'.format(task.email, status))
#         if status:
#
#             cSubject = 'File It.tax Account Activation'
#             cFromEmail = 'File It.tax <vip.support@fileit.tax>'
#             cToEmail = [task.email]
#             cBcc = ['avinash@fileit.tax', 'vip.support@fileit.tax']
#             emailbody = emailBodyBuilder(task.firstName,
#                                          task.tempPassword,
#                                          segment,
#                                          residency,
#                                          task.email)
#             sendEmail(cBcc, cFromEmail, cSubject, cToEmail, emailbody, 'ShareFileAccountCreated')
#             update_crm_task(task)
#
#     import csv
#     nIss = 0
#     filename = '/tmp/sharefile_fixes_{}.csv'.format(nowDatetimeStr())
#     with open(filename, 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#         for k in results.keys():
#             val = results[k]
#             status = val['status']
#             if not status:
#                 nIss += 1
#             writer.writerow([k, status])
#     if nIss > 0:
#         fromEmail = 'it@fileit.tax'
#         # toEmail = ['it@fileit.tax']
#         # bcc = ['avinash@fileit.tax']
#         toEmail = ['it@fileit.tax']
#         bcc = []
#         sendEmail(bcc, fromEmail, 'FAIL:ShareFile Account Creation Status{}'.format(nowDatetimeStr()), toEmail, 'Check the attachment', 'ShareFileAccountCreationStatus', filename)
#
#

def runner():
    token_str = authenticate()
    results = {}
    sync('clients')
    sync('tasks')



runner()


