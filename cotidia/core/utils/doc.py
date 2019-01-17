import os
import json

from django.conf import settings
from rest_framework.response import Response


class Doc:
    def __init__(self, file_name=None, title=None):

        if file_name:
            self.file_path = os.path.join(
                settings.PROJECT_DIR, "../../docs/api/{0}".format(file_name)
            )

            self.file_handle = open(self.file_path, "w")
            self.file_handle.write("# {0}\n" "\n".format(title))

    def __get_section_content(self, content):

        if isinstance(content.get("response"), Response):
            return self.__get_section_content_new(content)
        else:
            return self.__get_section_content_old(content)

    def __get_section_content_old(self, content):

        content["payload"] = json.dumps(content.get("payload"), indent=4)
        content["response"] = json.dumps(content.get("response"), indent=4)

        return self.__format_section_content(content)

    def __get_section_content_new(self, content):

        content["payload"] = json.dumps(content.get("payload"), indent=4)
        content["status_code"] = content.get("response").status_code
        content["response"] = json.dumps(content.get("response").data, indent=4)

        return self.__format_section_content(content)

    def __format_section_content(self, content):

        description = ""
        payload = "None."
        response = ""

        if content.get("description", ""):
            description = ("\n" "{0}\n").format(content.get("description"))

        payload_json = content.get("payload")

        if payload_json and payload_json != "{}" and payload_json != "null":
            payload = ("```json\n" "{0}\n" "```").format(payload_json)

        if content.get("status_code"):
            response = "A `{0}` HTTP status on successful execution".format(
                content.get("status_code")
            )

        response_json = content.get("response")

        if response_json and response_json != "{}" and response_json != "null":
            response += (
                "{0} JSON body representing the response:\n\n" "```json\n" "{1}\n" "```"
            ).format(" and a" if response else "A", response_json)
        else:
            response += " and no body content."

        return (
            "## {0}\n"
            "\n"
            "    [{1}] {2}{3}\n"
            "{4}"
            "\n"
            "### Payload\n"
            "\n"
            "{5}\n"
            "\n"
            "### Response\n"
            "\n"
            "{6}\n".format(
                content.get("title"),
                content.get("http_method"),
                settings.SITE_URL,
                content.get("url"),
                description,
                payload,
                response,
            )
        )

    def write_section(self, content):
        section = self.__get_section_content(content)

        self.file_handle = open(self.file_path, "a")
        self.file_handle.write(section)

    def display_section(self, content):
        section = self.__get_section_content(content)

        print(section)

    def close(self):
        if hasattr(self, "file_handle"):
            self.file_handle.close()
