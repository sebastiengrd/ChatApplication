from MessageField import MessageField
from Message import Message

class MessageFactory():
    @staticmethod
    def createMessage(messageFields: list[MessageField]):
        return Message(messageFields)

    @staticmethod
    def createMessageToClients(userFrom, message):
        fromField = MessageFactory.createMessageField("from", userFrom)
        messageField = MessageFactory.createMessageField("message", message)
        message = MessageFactory.createMessage([fromField, messageField])
        return message
    @staticmethod
    def createMessageField(name, value):
        return MessageField(name, value)

    @staticmethod
    def parseMessage(data):
        message = MessageFactory.createMessage([])
        for field in data:
            message.addField(MessageFactory.createMessageField(field, data[field]))


        return MessageFactory.createMessage([MessageFactory.createMessageField("username", username)])

    @staticmethod
    def createMessageWithUsers(users):
        return MessageFactory.createMessage([MessageFactory.createMessageField("users", users)])
    