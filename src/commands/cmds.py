"""
Decorators for automatically adding commands to the commands list.
"""


from typing import Any, Callable, Union, Optional
from enum import Enum

import discord

from commands_list import commands


class ReplyType(Enum):
    """
    ANYREPLY means that the result for the command should be a direct reply to the message.

    PRIVATEREPLY also means that the result should be a reply to the message,
    but only if the command was called through direct messages.

    PRIVATE means that the result for the command should be sent through DMs,
    instead of a reply.
    Used in get_reply_command.
    """
    ANYREPLY = 0
    PRIVATEREPLY = 1
    PRIVATE = 2


def get_args(command_call: str) -> list:
    """
    Gets the arguments passed to the command in that call
    """
    return command_call.split()[1:]


class Command:
    """Class for holding commands' functions+additional data."""
    def __init__(self,
                 func: Callable[[discord.Message, Union[str, list], Any], tuple],
                 reply_type: ReplyType,
                 parameter_types: Optional[list] = None):
        """
        Keyword Arguments:
        func: Callable               -- Wrapped with self.wrap().
        reply_type: ReplyType        -- ReplyType for this command.
        parameter_types: list        -- List of types for the command parameters.
                                        If [], it is assumed that there is only one string parameter,
                                        and all arguments passed to the command should be concatenated into it.
        """

        self.reply_type: ReplyType = reply_type
        self.parameter_types: list[type] = parameter_types
        self.run: Callable = self.wrap(func)

    def wrap(self,
             func: Callable[[discord.Message, Union[str, list], Any], tuple]
             ) -> Callable[[discord.Message], tuple]:
        """
        Decorates func, so that it can be called only with only one argument, a discord.Message.
        This function adds the command parameters as an argument, and adds an AIOHTTP ClientSession in **kwargs
        It also adds some exceptions: 
            - If a command with ReplyType PRIVATEREPLY gets called from somewhere other than a private channel.
            - If the arguments provided from a command call aren't consistent with self.parameter_types
        
        Keyword Arguments:
        func: Callable -- Function to be decorated. Should have 3 parameters, a discord.Message, a list, and **kwargs.
        """

        def wrapper(message: discord.Message, session) -> tuple:
            """
            session:
            For asynchronous HTTP requests using AIOHTTP.
            An AIOHTTP ClientSession. 
            Used in **kwargs.
            """

            #
            # Parameters and arguments
            #
            
            # Check if the arguments are consistent with the parameters
            if self.parameter_types:
                # Get the arguments
                arguments: list = get_args(message.content)

                # Length
                if len(self.parameter_types) > len(arguments):
                    raise Exception(f'''Not enough arguments
{func.__name__} requires {len(self.parameter_types)} arguments: {str(self.parameter_types)}''')

                # Types
                for index, parameter_type in enumerate(self.parameter_types):
                    try:
                        arguments[index] = parameter_type(arguments[index])
                    except Exception:
                        raise Exception(f"""Wrong type argument
{func.__name__}'s argument number {index} is {self.parameter_types[index]}""")
            # If self.parameter_types is [], join the arguments into a string
            else:
                arguments: list[str] = message.content.split(' ', 1)
                arguments: Optional[str] = arguments[1] if len(arguments) > 1 else None

            #
            # PRIVATEREPLY exception
            #

            if self.reply_type == ReplyType.PRIVATEREPLY and message.channel.type != discord.ChannelType.private:
                raise Exception('You should only use this command in private messages')

            #
            # Run the function
            #

            return func(message, arguments, aiohttp_session=session)

        return wrapper

    def get_reply_function(self, message: discord.Message) -> Callable:
        """
        Returns the function that should be called for replying with the command results.

        Keyword Arguments:
        message: discord.Message -- Message the function should be in relation to.
        """

        match: dict = {
            ReplyType.ANYREPLY: message.reply,
            ReplyType.PRIVATEREPLY: message.reply,
            ReplyType.PRIVATE: message.author.send
        }

        return match[self.reply_type]
        

#
# Decorator
#


def cmd(reply_type: ReplyType = ReplyType.ANYREPLY,
        parameter_types: Optional[list] = None
        ) -> Callable[[Callable], Callable]:
    """
    Decorator for commands.
    Takes arguments.
    """

    def decorator(func: Callable) -> Callable:
        """Decorator"""
        # Create a Command object for the func
        com: Command = Command(func, reply_type, parameter_types)

        # Add the object to the commands list
        commands[func.__name__] = com

        # Return the decoraded func
        # (Note that the class decoraded it, not this function)
        return com.run

    return decorator
