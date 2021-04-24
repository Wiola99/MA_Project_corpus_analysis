import os
import xml.etree.ElementTree as ET
import re
import json
from datetime import datetime

BASE_PATH = '../../Corpus_WUSv7paula/WUSv7paula'

result = {'list': []}


def parse_chat(chat_name):
    print(chat_name)
    # Add chat to the result list
    result['list'].append(chat_name)

    # Create the result object
    result[chat_name] = {
        'total_token': 0,
        'emoji_list': [],
        'lang': 'undefined'
    }

    # Read meta multiFeat xml fil
    meta_tree = ET.parse(
        BASE_PATH + '/' + chat_name + '/' + chat_name + '.meta_multiFeat.xml')
    meta_root = meta_tree.getroot()
    lang = meta_root[1][0][0].attrib['value']
    if lang:
        result[chat_name]['lang'] = lang

    # Read message multiFeat xml file
    tree = ET.parse(
        BASE_PATH + '/' + chat_name + '/' + chat_name + '.msg_multiFeat.xml')
    root = tree.getroot()
    multi_feat_list = root[1]
    for multi_feat in multi_feat_list:
        # print(multi_feat.attrib)
        feat = {}
        for feat_item in multi_feat:
            feat[feat_item.attrib['name']] = feat_item.attrib['value']

        message = feat['msg.msg']
        if message.find('redactedQ') > -1 \
                or message.find('mediaQ') > -1 \
                or message.find('systemQ') > -1 \
                or message.find('encryptedQ') > -1:
            continue

        # Parse and add number of tokens for this line
        tokens_number = int(feat['msg.msg_tokens'])
        if type(tokens_number) == int or type(tokens_number) == float:
            result[chat_name]['total_token'] += tokens_number

        # Extract emoji in message
        regex = r"(emojiQ[A-z]+)"
        matches = re.finditer(regex, message, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            result[chat_name]['emoji_list'].append(match.group())

    return result


# parse_chat('chat8')
chat_directory = os.listdir(BASE_PATH)
for item in chat_directory:
    if item.find('chat') > -1:
        parse_chat(item)


# Write result in json file
now = datetime.now()
timestamp = datetime.timestamp(now)
with open('data1.json', 'w') as outfile:
    json.dump(result, outfile)


