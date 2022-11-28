#!/usr/bin/python
"""
Form the parameters for the different methods to manage resources on Resourcespace through the REST API
Author: Emily O'Dean
Adapted from Xuenan Pi
"""
import datetime


def get_resource_path(resource_id, extension):
    get_file_path, size, generate = "true", "", "true"
    page, watermarked, alternative = "", "", ""
    parameters = "param1=%s&param2=%s&param3=%s&param4=%s&param5=%s&param6=%s&param7=%s&param8=%s" \
                 % (resource_id, get_file_path, size, generate, extension, page, watermarked, alternative)
    return parameters


def get_resource_data(resource_id):
    parameters = "param1=%s&param2=&param3=&param4=&param5=&param6=" % resource_id
    return parameters


def create_resource(resource_type, url, metadata):
    """
    0: global
    1: photo
    2: document
    3: video
    4: audio
    """
    parameters = "resource_type=%s&url=%s&metadata=%s" % (resource_type, url, metadata)
    return parameters


def upload_file(resource_id, file_path):
    no_exif, revert, autorotate = "1", "", "1"
    parameters = "param1=%s&param2=%s&param3=%s&param4=%s&param5=%s" \
                 % (resource_id, no_exif, revert, autorotate, file_path)
    return parameters


def update_field(resource_id, field_id, value=None):
    """
    8: Title
    12: Date
    """
    if field_id == "12":
        value = datetime.datetime.now().strftime("%Y-%m-%d+%H:%M:%S")
    parameters = "resource=%s&field=%s&value=%s" % (resource_id, field_id, value)
    return parameters


def add_resource_to_collection(resource_id, collection_id):
    parameters = "param1=%s&param2=%s" % (resource_id, collection_id)
    return parameters


def put_resource_data(resource_id, json_data):
    parameters = "resource=%s&data=%s" % (resource_id, json_data)
    return parameters


#def put_resource_data(resource_id):
#    parameters = "resource=%s" % (resource_id)
#    return parameters


def create_collection(collection_name):
    parameters = "param1=%s" % collection_name
    return parameters


def delete_collection(collection_id):
    parameters = "param1=%s" % collection_id
    return parameters


def delete_resource(resource_id):
    parameters = "param1=%s" % resource_id
    return parameters