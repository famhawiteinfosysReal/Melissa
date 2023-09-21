Plugin
class
Anjani.
Plugin
Every Custom Plugin takes two class variables named name and helpable. Define this variable on the plugin class.

Attributes
name (str) - This variable is to give your plugin name (Mandatory variable).
helpable (bool, optional) - Define this variable and set it to True if the plugin has a helper(documentation) to the /help command.
If this True you need to add the helper string on the Localized String File with {name}-help and {name}-button as the keys.
bot (~anjani.Anjani) - The Anjani instance.
comment (str, optional) - The comment of the plugin.
disabled (bool, optional) - Define this to True if you want to disable the plugin.
log (~logging.Logger) - Python Logging Module, the plugin's logger.
Method
Plugin.get_text

Parse the string with the user language setting. Return English string in case other language doesn't have the string requested. alias Plugin.text.

Parameters:

chat_id (int) - Id of the sender if in PM's or chat_id to fetch the user language setting.
name (str) - String name(key) to parse.
*args (any, Optional) - One or more values that should be formatted and inserted in the string. The value should be in order based on the language string placeholder.
noformat (bool, Optional) - If exist and True, the text returned will not be formatted (if you don't want to insert any value to the placeholders). Default to False.
**kwargs (any, Optional) - One or more keyword values that should be formatted and inserted in the string. Based on the keyword placeholder on the language strings.
The plugin variable will be like below.

from anjani_bot import plugin

class ExamplePlugin(plugin.Plugin):
     comment = "This is an example plugin"  # Optional
     name = "Example"
     helpable = True  # You don't need to add this variable, if you don't want to create plugin-help.
Based on the name variable the keys you need to put on the Localized strings file e.g; en.yaml is

example-button: Example
example-help: |
    An "odds and ends" plugin for small, simple commands which don't really fit anywhere.

    **Commands:**
    /<some commands> : <usage>
For other text localization you can read Tranlation Plugin.

Commands
For creating a commands handler go to this page

Listener Methods
Listener is a methods that automatically called when we got an update either from Telegram or ~Anjani itself.
~Anjani register 4 handlers into Pyrogram to interact with Telegram update:

~CallbackQueryHandler
on_callback_query
~InlineQueryHandler
on_inline_query
~MessageHandler
on_message
on_chat_action
on_chat_migrate
~ChatMemberUpdatedHandler
on_chat_member_update
Meanwhile ~Anjani itself have 5 handlers to interact with plugins:

on_load
on_start
on_started This one use 2 parameters the instance of the class self and start_time: int
on_stop
on_stopped
NOTE: All name of the listeners function must follow the above otherwise it will not be called.

We are trying our best to cover all listener documentation, you can ask us in issues or go to our support group. Here is an example of what Custom Plugin we created ExamplePlugin be sure to experiment on it!

On Load Listener
This Coroutine function is called when the plugin loaded on the startup. This method only takes the class instance. You can use this to load the database collection on the plugin. This method is mainly used to fetch any MongoDB Database collection or just initialized some config.

from typing import Optional

from anjani import plugin, util


class ExamplePlugin(plugin.Plugin):

    db: util.db.AsyncCollection
    token: Optional[str]

    async def on_load(self) -> None:
        self.db = self.bot.db.get_collection("example")
        self.token = self.bot.config.get("example_token")
On Callback Query Listener
This Coroutine function is used for detecting user that clicked the button. This method takes 2 parameters instance of the class and the ~pyrogram.types.CallbackQuery object.

Parameters:

query (~pyrogram.types.CallbackQuery) - CallbackQuery object
from anjani import plugin


class ExamplePlugin(plugin.Plugin):

    async def on_callback_query(self, query: CallbackQuery) -> None:
        self.log.info("Button clicked: %s", query.data)
        await query.answer("You clicked the button!")
On Chat Action Listener
This Coroutine function is used for detecting user that either joined group/chat or left. This method takes 2 parameters instance of the class and the ~pyrogram.types.Message object. This handler is filtered only for this 2 purpose.

Parameters:

message (~pyrogram.types.Message) - Message object
from anjani import plugin


class ExamplePlugin(plugin.Plugin):

    async def on_chat_action(self, message: Message) -> None:
        if message.new_chat_members:
            for new_member in message.new_chat_members:
                self.log.info("New member joined: %s", new_member.first_name)
        else:
            left_member = message.left_chat_member
            self.log.info("A member just left chat: %s", left_member.first_name)
On Chat Migrate Listener
This Coroutine function is used for migrating chats - when a chat is upgraded to a supergroup, the ID changes, so it is necessary to migrate it in the DB. This method takes 2 parameters instance of the class and the ~pyrogram.types.Message object. This handler is filtered only for migrating purpose.

Parameters:

message (~pyrogram.types.Message) - Message object
# self.db is from ~on_load above example
from anjani import plugin


class ExamplePlugin(plugin.Plugin):

    async def on_chat_migrate(self, message: Message) -> None:
        self.log.info("Migrating chat...")
        new_chat = message.chat.id
        old_chat = message.migrate_from_chat_id

        await self.db.update_one(
            {"chat_id": old_chat},
            {"$set": {"chat_id": new_chat}},
        )
It is recommended that you follow what we wrote here, but you can try out different way if you know what you are doing.

On Chat Member Updated Listener
This Coroutine function is used for detecting a chat member update eg: Promoted or demoted admins. This method takes 2 parameters. The instance of the class and ~pyrogram.types.ChatMemberUpdated object.

Parameters:

update (~pyrogram.types.ChatMemberUpdated) - ChatMemberUpdated object
from anjani import plugin


class ExamplePlugin(plugin.Plugin):

    async def on_chat_action(self, update: ChatMemberUpdated) -> None:
        await self.bot.client.send_message(update.chat.id, "There is an updated chat member")
On Message Listener
This Coroutine function is used to listen all incoming/outgoing message into the bot. This method takes 2 parameters instance of the class and the ~pyrogram.types.Message object.

Parameters:

message (~pyrogram.types.Message) - Message object
# self.db is from ~on_load above example
from anjani import plugin


class ExamplePlugin(plugin.Plugin):

    async def on_message(self, message: Message) -> None:
        self.log.info(f"Received message: {message.text}")
        await self.db.update_one(
            {"_id": message.id}, {"$set": {"text": message.text}}, upsert=True
        )
Plugin Backup Listener
This Coroutine function called when an admin of a chat executing /backup commands. This function must return a Dict take a look of what we wrote below and be sure to follow it. But again if you know what you are doing you can experiment on it.

Parameters:

chat_id (int) - Chat id of the backup requested.
# self.db is from ~on_load above example
from typing import Any, MutableMapping

from anjani import plugin


class ExamplePlugin(plugin.Plugin):

    async def on_plugin_backup(self, chat_id: int) -> MutableMapping[str, Any]:
        """Dispatched when /backup command is Called"""
        self.log.info("Backing up data plugin: %s", self.name)
        data = await self.db.find_one({"chat_id": chat_id}, {"_id": False})
        if not data:
            return {}

        return {self.name: data}
Plugin Restore Listener
This Coroutine function called when an admin of a chat executing /restore commands.

Parameters:

chat_id (int) - Chat id of the restore target.
data (Dict) - The data you got from file after executing /backup command.
# self.db is from ~on_load above example
from anjani import plugin


class ExamplePlugin(plugin.Plugin):

    async def on_plugin_restore(self, chat_id: int, data: MutableMapping[str, Any]) -> None:
        """Dispatched when /restore command is Called"""
        self.log.info("Restoring data plugin: %s", self.name)
        await self.db.update_one({"chat_id": chat_id},
                                 {"$set": data[self.name]},
                                 upsert=True)
Command and Listener Filters
For using filters into command or listener you can go to this page.
