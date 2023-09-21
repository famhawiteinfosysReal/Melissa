## Create Your Own Plugin
We try our best to simplify custom plugin creation.

All you needed is your `<plugin_name>.py` file in the plugins folder `(Melissa/custom_plugins/)`.

Then create a Sub Class that inherited the `plugin.Plugin import from from Melissa import plugin`.
After that give your subclass a class variable named name with the plugin name unless the plugin name will be `"Unnamed"`.

```python
from Melissa import plugin

class ExamplePlugin(plugin.Plugin):
    name = "Example"
```
<!-- -->

For more information about Class you can read about [Python classes](https://docs.python.org/3/tutorial/classes.html)

Be sure to create a [pull request](https://github.com/famhawiteinfosysReal/Melissa/pulls) if you already created a Custom Plugin! We grow together.

Adding a Command Handler To The Plugin
If you are not fan of annotating your code you simply don't need to import anything to register the command,
you just need to create a Coroutine function name that starts with `cmd_[name]` and takes 2 parameters,
self refers to the SubClass you create and ctx refers to ~command.Context.

```python
    async def cmd_example(self, ctx):
        return "My own custom Plugins!"
```
<!-- -->
Then the command for interacting with the bot will be `/example`
and it will respond you message with text the return of that function `My own custom Plugins!`.

Things to Remember!
`~Melissa` Command Handler returns 2 positional arguments:

self The instance of the Sub Plugin Class
`ctx` The instance of `~Melissa.command.Context` that constructed for every command the bot received.
If you want to use or interact with the `~pyrogram.Client` you can use as example below here.
```python
from Melissa import command, plugin

class ExamplePlugin(plugin.Plugin):
    name = "Example Plugin"

    async def cmd_test(self, ctx: command.Context) -> None:
        await self.bot.client.send_message(ctx.chat.id, "Chaw thring...")
        # self.bot == ~Melissa
        # self.bot.client == ~pyrogram.Client
        # This method is must instead of importing the client itself.
```
<!-- -->
*Read more about [plugin attributes & method](https://github.com/famhawiteinfosysReal/Melissa/Guides/attributions.md).
