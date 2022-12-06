#!/usr/bin/python
"""
Manage resources on Resourcespace through the REST API.
Author: Emily O'Dean
"""

import hashlib
# import urllib3
import parameters
import requests
import json
import urllib.parse


class RSAPI(object):
    def __init__(self, user, private_key):
        self.site_ip = "collections.nbmg.unr.edu/"
        # user name and private key
        # user can only create collection for oneself
        # to create a collection for a user, the user's account name and private key has to be used
        self.user = user
        self.private_key = private_key
        # support API functions
        # get_resource_path, create_collection, delete_collection, delete_resource,
        # create_resource, upload_file, update_field, add_resource_to_collection

    def query(self, function_to_query, parameters):
        """
        :return: the query result
        """
        query = "user=%s&function=%s&%s" % (self.user, function_to_query, parameters)

        # sign = hashlib.sha256(self.private_key+query).hexdigest()
        sign_text = self.private_key + query
        sign = hashlib.sha256(sign_text.encode('utf-8')).hexdigest()
        query_url = "https://collections.nbmg.unr.edu/api/index.php?%s&sign=%s" % (query, sign)

        # print query_url
        try:
            # http = urllib3.PoolManager()
            result = requests.get(query_url, verify=False)
            # result = urllib.urlopen(query_url).read()
        except (IOError, UnicodeDecodeError, requests.exceptions.HTTPError) as err:
            print(err)
        else:
            return result

    def post_resource(self, function_to_post, params):
        """
        :return: the query result
        """
        query = "user=%s&function=%s&%s" % (self.user, function_to_post, params)

        # sign = hashlib.sha256(self.private_key+query).hexdigest()
        signtext = self.private_key + query
        sign = hashlib.sha256(signtext.encode('utf-8')).hexdigest()
        query_url = "https://collections.nbmg.unr.edu/api/?%s&sign=%s" % (query, sign)

        # print query_url
        try:
            result = requests.post(query_url, verify=False)
            # result = urllib.urlopen(query_url).read()
        except (IOError, UnicodeDecodeError, requests.exceptions.HTTPError) as err:
            print(err)
        else:
            return result

    def upload_resource(self, file_path, title, collection_id):
        """
        The original file to be uploaded has to be on the same server where Resourcespace is installed.
        Create a resource, move the file to /filestore, attach it to the resource id, add the resource to the
        collection, update title and date for the uploaded file.
        :param file_path: original file path on the server
        :param title: title of the file
        :param collection_id: id of the collection to be added
        """
        resource_id = self.query("create_resource", parameters.create_resource("4"))
        upload_success = self.query("upload_file", parameters.upload_file(resource_id, file_path))
        if upload_success:
            # add title to the resource
            self.query("update_field", parameters.update_field(resource_id, "8", title))
            # add upload date to the resource
            self.query("update_field", parameters.update_field(resource_id, "12"))
            self.query("add_resource_to_collection", parameters.add_resource_to_collection(resource_id, collection_id))

    def create_resource(self, resource_type, url, metadata, collection_id, lat_lon):
        resource_id = self.query("create_resource", parameters.create_resource(resource_type))

    def get_resource(self, resource_id):
        return self.query("get_resource_data", parameters.get_resource_data(resource_id))

    def get_resource_metadata(self, resource_id):
        return self.query("get_resource_field_data", parameters.get_resource_data(resource_id))

    def update_metadata_field(self, resource_id, field, value):
        return self.query("update_field", parameters.update_field(resource_id, field, value))

    def update_lat_lon(self, resource_id, lat, lon):
        json_string = {"geo_lat": lat, "geo_long": lon}
        json_data = json.dumps(json_string)
        json_data = urllib.parse.quote(json_data)
        return self.query("put_resource_data", parameters.put_resource_data(resource_id, json_data))

    def update_lat(self, resource_id, lat):
        json_string = {
            "geo_lat": lat
        }
        json_data = json.dumps(json_string)
        return self.query("put_resource_data", parameters.put_resource_data(resource_id, json_data))

    def get_resource_folder(self, resource_id, extension):
        """
        :return: the server path to the folder that contains the resource file
        """
        full_path = self.query("get_resource_path", parameters.get_resource_path(resource_id, extension))
        if full_path:
            # escape the double quote in the two ends of the string
            # escape the file name because it is the same as the folder name which is not correct
            folder_path = "".join(full_path.split("\\")[1:-1])
            return folder_path

    def create_collection(self, collection_name):
        collection_id = self.query("create_collection", parameters.create_collection(collection_name))
        return collection_id

    def delete_collection(self, collection_id):
        delete_result = self.query("delete_collection", parameters.delete_collection(collection_id))
        return delete_result

    def delete_resource(self, resource_id):
        """
        Delete the resource. One time query cannot really work.
        Keep query until API return false to make sure the resource is deleted.
        Restrict to 3 iteration of the query.
        """
        for i in range(3):
            delete_result = self.query("delete_resource", parameters.delete_resource(resource_id))
            if not delete_result:
                break

if __name__=="__main__":
    user = ""
    private_key = ""
