"""
Agent Message Bus
"""

from collections import defaultdict


class MessageBus:

    def __init__(self):

        self.messages = defaultdict(list)

    def send(

        self,

        sender,

        receiver,

        title,

        content,

    ):

        self.messages[receiver].append(

            {

                "sender": sender,

                "title": title,

                "content": content,

            }

        )

    def inbox(

        self,

        receiver,

    ):

        return self.messages.get(

            receiver,

            [],

        )