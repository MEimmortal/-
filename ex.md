# A basic walkthrough guide on subclassing HelpCommand
This guide will walkthrough the ways to create a custom help command by subclassing HelpCommand.

## Table Content
- [Brief explanation of subclassing](#brief)
- [Why subclassing is better](#why)
- [Getting started](#start)
  - [Types of HelpCommand class](#start1)
  - [Embed MinimalHelpCommand](#start2)
- [HelpCommand](#helping)
  - [Basic method to override](#helping1)
  - [Useful Attributes](#helping2)
  - [help command](#helping_guide1)
  - [help \<argument>](#helping_guide2)
  - [Command Attributes](#command_attrs)
  - [Error handling for HelpCommand](#error_handling) 
  - [Setting Cog for HelpCommand](#cog)
- [Paginated Help Command](#paginate_help)
  - [Pagination for 1.7.x](#paginate_help_1_7)
  - [Pagination for 2.x](#paginate_help_2)
  - [ListPageSource class](#list_page_source)
  - [Integrating classes of pagination](#help_pagination_intergrate)
- [The end](#the_end)


## <a name="brief"></a> Brief explanation of subclassing
In simple terms, a subclass is a way to inherit a class behaviour/attributes from another class. Here's how you would subclass
a class in Python.
```py
class A:
    def __init__(self, attribute1):
        self.attribute1 = attribute1

    def method1(self):
        print("method 1")

    def method2(self):
        print("method 2")


class B(A):
    def __init__(self, attribute1, attribute2):
        super().__init__(attribute1) # This calls A().__init__ magic method.
        self.attribute2 = attribute2

    def method1(self): # Overrides A().method1
        print("Hi")
```
Given the example, the variable `instance_a` contains the instance of class `A`. As expected, the output will be this.
```py
>>> instance_a = A(1)
>>> instance_a.attribute1
1
>>> instance_a.method1()
"method 1"
```
How about `B` class? `instance_b` contains the instance of class `B`, it inherits attributes/methods from class `A`. Meaning
it will have everything that class `A` have, but with an additional attribute/methods.
```py
>>> instance_b = B(1, 2)
>>> instance_b.attribute1
1
>>> instance_b.attribute2
2
>>> instance_b.method1()
"Hi"
>>> instance_b.method2()
"method 2"
```
Make sure to look and practice more into subclassing classes to understand fully on what it is before diving into subclassing 
HelpCommand.

## <a name="why"></a> Why subclassing HelpCommand is better
Firstly, let me show you the wrong way of creating a help command.

#### One of the most incorrect ways of to create a help command.

```python
bot = commands.Bot(command_prefix="uwu ", help_command=None)

# OR
bot.help_command = None

# OR
bot.remove_command("help")

@bot.command()
async def help(ctx):
    ...
```
This is directly from YouTube, which are known to have bad tutorials for 
discord.py.

### Why are these bad?
#### 1. Command handling specifically for HelpCommand
Missing out on command handling that are specifically for HelpCommand. 

For instance, say my prefix is `!`. Command handling such as

`!help`

`!help <command>`

`!help <group>`

`!help <cog>`

For a HelpCommand, all of these are handled in the background, including showing 
appropriate error when `command`/`group`/`cog` are an invalid argument that were
given. You can also show custom error when an invalid argument are given.

For people who remove the HelpCommand? There is no handling, you have to do it yourself.


For example
##### Bad way
```py
bot = commands.Bot(command_prefix="!", help_command=None)

@bot.command()
async def help(ctx, argument=None):
    # !help
    if argument is None:
        await ctx.send("This is help")
    
    elif argument in bot.all_commands:
        command = bot.get_command(argument)
        if isinstance(command, commands.Group):
            # !help <group>
           await ctx.send("This is help group")
        else:
            # !help <command>
           await ctx.send("This is help command")
    elif argument in bot.cogs:
        # !help <cog>
        cog = bot.get_cog(argument)
        await ctx.send("This is help cog")
    else:
       await ctx.send("Invalid command or cog")

```
This is an ok implementation and all, but you have to handle more than this.
I'm only simplifying the code.

Now for the subclassed HelpCommand code.
#### Good way 
```py
bot = commands.Bot(command_prefix="!")

class MyHelp(commands.HelpCommand):
   # !help
    async def send_bot_help(self, mapping):
        await self.context.send("This is help")
       
   # !help <command>
    async def send_command_help(self, command):
        await self.context.send("This is help command")
      
   # !help <group>
    async def send_group_help(self, group):
        await self.context.send("This is help group")
    
   # !help <cog>
    async def send_cog_help(self, cog):
        await self.context.send("This is help cog")

bot.help_command = MyHelp()
```
Not only does HelpCommand looks better, it is also much more readable compared to the `bad way`.
Oh, did I mention that HelpCommand also handles invalid arguments for you? Yeah. It does.

#### <a name="utils"></a> 2. Utilities
HelpCommand contains a bunch of useful methods you can use in order to assist you in creating your
help command and formatting.

| Methods / Attributes                                   | Usage                                                                                                                                                                                                                                                                   |
|--------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [HelpCommand.filter_commands()][Hgetfilter]            | Filter commands to only show commands that the user can run. This help hide any secret commands from the general user.                                                                                                                                                  |
| [HelpCommand.clean_prefix][Hgetcleanprefix]            | Get a clean prefix that escape mentions and format them in a readable way such as `@Name` instead of `<@id>` format. **Works up to version 1.7.1.**                                                                                                                     |
| Context.clean_prefix                                   | HelpCommand.clean_prefix was removed in version 2.0 of discord.py and replaced with `Context.clean_prefix`                                                                                                                                                                                    |
| [HelpCommand.get_command_signature()][Hgetcommandsig]  | Get the command signature and format them such as `command [argument]` for optional and `command <argument>` for required.                                                                                                                                              |
| [HelpCommand.prepare_help_command()][Hgetprepare]      | Triggers before every `send_x_help` method are triggered, this work exactly like `command.before_invoke`                                                                                                                                                                |
| [HelpCommand.get_bot_mapping()][Hgetbotmap]            | Get all command that are available in the bot, sort them by Cogs and None for No Category as key in a dictionary. This method is triggered before HelpCommand.send_bot_help is triggered, and will get passed as the parameter.                                         |
| [HelpCommand.get_destination()][Hgetdestination]       | Returns a Messageable on where the help command was invoked.                                                                                                                                                                                                            |
| `HelpCommand.command_callback`                         | The method that handles all `help/help cog/ help command/ help group` and call which method appropriately. This is useful if you want to modify the behavour of this. Though more knowledge is needed for you to do that. Most don't use this.                          |
| [Context.send_help()][Csendhelp]                       | Calling `send_command_help` based on what the Context command object were. This is useful to be used when the user incorrectly invoke the command. Which you can call this method to show help quickly and efficiently. (Only works if you have HelpCommand configured) |

All of this does not exist when you set `bot.help_command` to `None`. You miss out on this.


### 3. Modular/Dynamic
Since it's a class, most people would make it modular. They put it in a cog for example. There is a common code given in `discord.py`
created by Vex. 
```python
class MyHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)

class MyCog(commands.Cog):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self
        
    def cog_unload(self):
        self.bot.help_command = self._original_help_command
```

#### What does this mean?
Well, first we have a `HelpCommand` made there called `MyHelpCommand`. When MyCog class is loaded,
`bot.help_command` is stored into `self._original_help_command`. This preserve the old help command that was attached to 
the bot, and then it is assigned to a new `HelpCommand` that you've made.

`cog_unload` is triggered when the cog is unloaded, which assign `bot.help_command` to the original help command.

#### What good does this give? 
For example, you have a custom help command that is currently attached to `bot.help_command`. But you want to develop a 
new help command or modify the existing without killing the bot. So you can just unload the cog, which will assign the old help command
to the bot so that you will always have a backup `HelpCommand` ready while you're modifying and testing your custom help.


## <a name="start"></a>Getting started
With that out of the way, let's get started. For subclassing HelpCommand, first, you would need to know the types of `HelpCommand`. 
Where each class has their own usage.
### <a name="start1"></a> Types of HelpCommand class
There are a few types of HelpCommand classes that you can choose;
1. [`DefaultHelpCommand`][defhelplink] a help command that is given by default.
2. [`MinimalHelpCommand`][minhelplink] a slightly better help command.
3. [`HelpCommand`][helplink] an empty class that is the base class for every HelpCommand you see. On its own, it will 
   not do anything.
   
By default, help command is using the class `DefaultHelpCommand`. This is stored in [`bot.help_command`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.help_command). This attribute 
will **ONLY** accept instances that subclasses `HelpCommand`. Here is how you were to use the `DefaultHelpCommand` instance.
```py
from discord.ext import commands
bot = commands.Bot(command_prefix="uwu ")
bot.help_command = commands.DefaultHelpCommand()

# OR

bot = commands.Bot(command_prefix="uwu ", help_command=commands.DefaultHelpCommand())
# Both are equivalent
```
#### Here's an example of what that looks like.
![img.png](https://media.discordapp.net/attachments/784735050071408670/787570202593460224/unknown.png)
_Now, of course, this is done by default. I'm only showing you this as a demonstration. Don't scream at me_ 

Let's do the same thing with `MinimalHelpCommand` next.

```py
from discord.ext import commands
bot = commands.Bot(command_prefix="uwu ")
bot.help_command = commands.MinimalHelpCommand()
```
#### This is how that would look like:

![minhelpcommand.png](https://cdn.discordapp.com/attachments/784735050071408670/787571374742962228/unknown.png)

##  <a name="start2"></a> Embed MinimalHelpCommand
Now say, you want the content to be inside an embed. But you don't want to change the content of
`DefaultHelpCommand`/`MinimalHelpCommand` since you want a simple HelpCommand with minimal work. There is a short code 
from `?tag embed help example` by `gogert` in [discord.py](https://discord.gg/dpy) server, a sample code you can follow 
shows this;
```py
import discord
from discord.ext import commands
bot = commands.Bot(command_prefix="uwu ")

class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)

bot.help_command = MyNewHelp()
```
The resulting code will show that it have the content of `MinimalHelpCommand` but in an embed.

![embedminimalhelp.png](https://cdn.discordapp.com/attachments/784735050071408670/787574637117833236/unknown.png)

### How does this work?
Looking over the `MinimalHelpCommand` source code, [here](https://github.com/Rapptz/discord.py/blob/master/discord/ext/commands/help.py#L1075-L1331).
Every method that is responsible for `<prefix>help <argument>` will call [`MinimalHelpCommand.send_pages`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.MinimalHelpCommand.send_pages)
when it is about to send the content. This makes it easy to just override `send_pages` without having to override any
other method there are in `MinimalHelpCommand`.

# <a name="helping"></a> HelpCommand
## <a name="helping1"></a> Basic methods to override
If you want to use `HelpCommand` class, we need to understand the basic of subclassing HelpCommand. 
Here are a list of HelpCommand relevant methods, and it's responsibility.

1. [`HelpCommand.send_bot_help(mapping)`][sendbothelp]
   Gets called with `<prefix>help`
2. [`HelpCommand.send_command_help(command)`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.HelpCommand.send_command_help)
   Gets called with `<prefix>help <command>`
3. [`HelpCommand.send_group_help(group)`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.HelpCommand.send_group_help)
   Gets called with `<prefix>help <group>`
4. [`HelpCommand.send_cog_help(cog)`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.HelpCommand.send_cog_help) 
   Gets called with `<prefix>help <cog>`
   
## <a name="helping2"></a> Useful attributes
1. [`HelpCommand.context`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.HelpCommand.context)
   the Context object in the help command.
2. [`HelpCommand.clean_prefix`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.HelpCommand.clean_prefix)
   a cleanup prefix version that remove any mentions.
   
For more, [`Click here`](#utils)

Seems simple enough? Now let's see what happens if you override one of the methods. Here's an example code of how you 
would do that. This override will say `"hello!"` when you type `<prefix>help` to demonstrate on what's going on. 

We'll use
[`HelpCommand.get_destination()`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.HelpCommand.get_destination)
to get the [`abc.Messageable`](https://discordpy.readthedocs.io/en/latest/api.html#discord.abc.Messageable)
instance for sending a message to the correct channel.

#### Code Example
```py
from discord.ext import commands
bot = commands.Bot(command_prefix="uwu ")

class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        channel = self.get_destination()
        await channel.send("hello!")

bot.help_command = MyHelp()
```
#### Output

![hellohelpcommand.png](https://media.discordapp.net/attachments/784735050071408670/787584311221813248/unknown.png)

Keep in mind, using `HelpCommand` class will require overriding every `send_x_help` methods. For example, `<prefix>help jsk` is 
a command that should call `send_command_help` method. However, since `HelpCommand` is an empty class, it will not say 
anything.

## <a name="helping_guide1"></a> help command
Let's work our way to create a `<prefix> help`. 
Given the documentation, [`await send_bot_help(mapping)`][sendbothelp] method receives `mapping(Mapping[Optional[Cog], List[Command]])`
as its parameter. `await` indicates that it should be an async function.
### What does this mean?
* `Mapping[]` is a [`collections.abc.Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping),
  for simplicity’s sake, this usually refers to a dictionary since it's under `collections.abc.Mapping`.
* `Optional[Cog]` is a [`Cog`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Cog)
object that has a chance to be `None`.
* `List[Command]` is a list of [`Command`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Command)
objects.
* `Mapping[Optional[Cog], List[Command]]` means it's a map object with `Optional[Cog]` as it's key and `List[Command]` as
its value.
  
_All of these are typehints in the `typing` module. You can learn more about it [here](https://docs.python.org/3/library/typing.html#module-typing)._

Now, for an example, we will use this `mapping` given in the parameter of `send_bot_help`. For each of the command, we'll
use [`HelpCommand.get_command_signature(command)`][Hgetcommandsig] to get the command signature of a command in an `str`
form.

#### Example Code
```py
import discord
from discord.ext import commands
bot = commands.Bot(command_prefix="uwu ")

class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help")
        for cog, commands in mapping.items():
           command_signatures = [self.get_command_signature(c) for c in commands]
           if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

bot.help_command = MyHelp()
```
### How does it work?
1. Create an embed.
2. Use dict.items() to get an iterable of `(Cog, list[Command])`.
3. Each element in `list[Command]`, we will call `self.get_command_signature(command)` to get the proper signature of 
   the command.
4. If the list is empty, meaning, no commands is available in the cog, we don't need to show it, hence 
   `if command_signatures:`.
5. `cog` has a chance to be `None`, this refers to No Category. We'll use [`getattr`](https://docs.python.org/3/library/functions.html#getattr)
   to avoid getting an error to get cog's name through [`Cog.qualified_name`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Cog.qualified_name).
6. Using [`str.join`](https://docs.python.org/3/library/stdtypes.html#str.join) each command will be displayed on a separate line.
7. Once all of this is finished, display it.

#### The result

![samplehelp.png](https://cdn.discordapp.com/attachments/784735050071408670/787610952690040852/unknown.png)

I agree, this does not look pretty. But this demonstrate how to create a help command with minimal effort. The reason why
it looks ugly, is that we're using [`HelpCommand.get_command_signature(command)`][Hgetcommandsig].
Let's override that method to make it a little more readable.

We'll borrow codes from [`MinimalHelpCommand.get_command_signature`](https://github.com/Rapptz/discord.py/blob/v1.5.1/discord/ext/commands/help.py#L1144).
Optionally, we can subclass `MinimalHelpCommand` instead of copying codes. I'm doing this as a demonstration of 
overriding other methods.

We'll also use [`HelpCommand.filter_commands`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.HelpCommand.filter_commands),
this method will filter commands by removing any commands that the user cannot use. It is a handy method to use.

#### The Example
```py
import discord
from discord.ext import commands
bot = commands.Bot(command_prefix="uwu ")

class MyHelp(commands.HelpCommand):
   def get_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help")
        for cog, commands in mapping.items():
           filtered = await self.filter_commands(commands, sort=True)
           command_signatures = [self.get_command_signature(c) for c in filtered]
           if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

bot.help_command = MyHelp()
```
#### The resulting output

![betterhelpcommand.png](https://cdn.discordapp.com/attachments/784735050071408670/787614011759919114/unknown.png)

This looks more readable than the other one. While this should cover most of your needs, you may want to know more helpful
attribute that is available on `HelpCommand` in the official documentation.

## <a name="helping_guide2"></a> help [argument] command
Now that the hard part is done, let's take a look at `<prefix>help [argument]`. The method responsible for this is as 
follows;
1. `send_command_help`
2. `send_cog_help`
3. `send_group_help`

As a demonstration, let's go for `send_command_help` this method receive a `Command` object. For this, it's simple, all 
you have show is the attribute of the command.

For example, this is your command code, your goal is you want to show the `help`,`aliases` and the `signature`.
#### Command Code
```py
@bot.command(help="Shows all bot's command usage in the server on a sorted list.",
             aliases=["br", "brrrr", "botranks", "botpos", "botposition", "botpositions"])
async def botrank(ctx, bot: discord.Member):
   pass
```

Then it's simple, you can display each of the attribute by [`Command.help`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Command.help)
and [`Command.aliases`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Command.aliases).

For the signature, instead of using the previous `get_command_signature`, we're going to subclass `MinimalHelpCommand`.

#### Help Code

```py
import discord
from discord.ext import commands
bot = commands.Bot(command_prefix="uwu ")

class MyHelp(commands.MinimalHelpCommand):
    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command))
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

bot.help_command = MyHelp()
```
#### What you get

![commandhelpcommand.png](https://cdn.discordapp.com/attachments/784735050071408670/787629706358292490/unknown.png)

As you can see, it is very easy to create `<prefix>help [argument]`. The class already handles the pain of checking whether
the given argument is a command, a cog, or a group command. It's up to you on how you want to display it, whether it's through 
a plain message, an embed or even using [`discord.ext.menus`](https://github.com/Rapptz/discord-ext-menus).

## <a name="command_attrs"></a> Command Attributes 
Let's say, someone is spamming your help command. For a normal command, all you have to do to combat this is using a 
[`cooldown`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.cooldown) decorator 
and slap that thing above the command declaration. Or, what about if you want an alias? Usually, you would put an 
aliases kwargs in the [`command`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.command)
decorator. However, HelpCommand is a bit special, It's a god damn class. You can't just put a decorator on it and expect 
it to work. 


That is when [`HelpCommand.command_attrs`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.HelpCommand.command_attrs)
come to the rescue. This attribute can be set during the HelpCommand declaration, or a direct attribute assignment. 
According to the documentation, it accepts exactly the same thing as a [`command`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.command)
decorator in a form of a dictionary.

For example, we want to rename the help command as `"hell"` instead of `"help"` for whatever reason. We also want to make
an alias for `"help"` so users can call the command with `"hell"` and `"help"`. Finally, we want to put a cooldown,
because help command messages are big, and we don't want people to spam those. So, what would the code look like?

#### Example Code
```py
from discord.ext import commands

attributes = {
   'name': "hell",
   'aliases': ["help", "helps"],
   'cooldown': commands.Cooldown(2, 5.0, commands.BucketType.user)
} 
# For 2.0, you would use CooldownMapping.from_cooldown(rate, per, type)
# because Cooldown no longer have type as it's arguments.

# During declaration
help_object = commands.MinimalHelpCommand(command_attrs=attributes)

# OR through attribute assignment
help_object = commands.MinimalHelpCommand()
help_object.command_attrs = attributes

bot = commands.Bot(command_prefix="uwu ", help_command=help_object)
```
### How does it work?
1. sets the name into `"hell"` is refers to here `'name': "hell"`.
2. sets the aliases by passing the list of `str` to the `aliases` key, which refers to here `'aliases': ["help", "helps"]`. 
3. sets the cooldown through the `"cooldown"` key by passing in a [`Cooldown`](https://github.com/Rapptz/discord.py/blob/v1.5.1/discord/ext/commands/cooldowns.py#L70-L134)
   object. This object will make a cooldown with a rate of 2, per 5 with a bucket type [`BucketType.user`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.discord.ext.commands.BucketType),
   which in simple terms, for every [`discord.User`](https://discordpy.readthedocs.io/en/latest/api.html#discord.User), 
   they can call the command twice, every 5 seconds.
4. We're going to use `MinimalHelpCommand` as the `HelpCommand` object.

#### The result
![cooldownhelp.png](https://cdn.discordapp.com/attachments/784735050071408670/789471505145659412/unknown.png)

As you can see, the name of the help command is now `"hell"`, and you can also trigger the help command by `"help"`. It 
will also raise an [`OnCommandCooldown`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.CommandOnCooldown)
error if it was triggered 3 times in 5 seconds due to our `Cooldown` object. Of course, I didn't show that in the result,
but you can try it yourself. You should handle the error in an error handler when an `OnCommandCooldown` is raised.

## <a name="error_handling"></a> Error handling for HelpCommand
### Basic error message override
What happens when `<prefix>help command` fails to get a command/cog/group? Simple, `HelpCommand.send_error_message` will
be called. HelpCommand will not call `on_command_error` when it can't find an existing command. It will also give you an 
`str` instead of an error instance.

```py
import discord
from discord.ext import commands
bot = commands.Bot(command_prefix="uwu ")

class MyHelp(commands.HelpCommand):
    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=error)
        channel = self.get_destination()
        await channel.send(embed=embed)

bot.help_command = MyHelp()
```
`error` is a string that will only contain the message, all you have to do is display the message.

#### The output:

![errorhelp.png](https://cdn.discordapp.com/attachments/784735050071408670/787639990515269662/unknown.png)

### How about a local error handler?

Indeed, we have it. [`HelpCommand.on_help_command_error`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.HelpCommand.on_help_command_error),
this method is responsible for handling any error just like any other local error handler.

#### Code
```py
import discord
from discord.ext import commands
bot = commands.Bot(command_prefix="uwu ")

class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        raise commands.BadArgument("Something broke")

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title="Error", description=str(error))
            await ctx.send(embed=embed)
        else:
            raise error

bot.help_command = MyHelp()
```
Rather basic, just raise an error that subclasses `commands.CommandError` such as `commands.BadArgument`. The error raised 
will cause `on_help_command_error` to be invoked. The code shown will catch this `commands.BadArgument` instance that is 
stored in `error` variable, and show the message.

#### Output:

![errorhandler.png](https://cdn.discordapp.com/attachments/784735050071408670/787645587004588052/unknown.png)

To be fair, you should create a proper error handler through this official documentation. [Here](https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#ext-commands-error-handler).

There is also a lovely example by `Mysty` on error handling in general. [Here](https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612).
This example shows how to properly create a global error handler and local error handler.

## <a name="cog"></a> Setting Cog for HelpCommand
### Super easy lol
It works just like setting a cog on a Command object, you basically have to assign a 
[`commands.Cog`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Cog) 
instance into [`HelpCommand.cog`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.HelpCommand.cog).
It is pretty common for discord.py users to put a HelpCommand into a cog/separate file
since people want organization.

### Code Example
This code example is if you're in a Cog file, which you have access to a Cog instance
```python
from discord.ext import commands

# Unimportant part
class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        channel = self.get_destination()
        await channel.send("hey")


class YourCog(commands.Cog):
    def __init__(self, bot):
       self.bot = bot
        
       # Focus here
       # Setting the cog for the help
       help_command = MyHelp()
       help_command.cog = self # Instance of YourCog class
       bot.help_command = help_command


def setup(bot):
    bot.add_cog(YourCog(bot))
```
### How does it work?
1. It instantiates the HelpCommand class. `help_command = MyHelp()`
2. It assigns the instance of `YourCog`(self) into `cog` attribute


# <a name="paginate_help"></a> Paginated Help Command
Seems like there are a lot of request for this to be made, and my original plan was to
wait for menus to be integrated with buttons. However, looking at the current event of
where it seems like that won't happen. To clarify, I will not be walking through all of the 
specific feature that the classes I'm using in this tutorial.

In this part, we will be using [discord-ext-menus](https://github.com/Rapptz/discord-ext-menus) to handle our pagination.
This is an external library that Danny wrote that seems to never reached 2.0. You might be asking, _"why even bother using it
if it won't ever reach 2.0"_. I will answer that by saying it is still useful for pagination use. You
can even use this for other pagination, not just for help command. Even with 2.0, you will be able
to use this efficiently with buttons. I will show that later in the walkthrough.

### <a name="paginate_help_1_7"></a> Pagination for 1.7.x
Now for the people who have never use ext-menus before, you may be asking me, 
_"Stella, what the hell is a MenuPages class"_. To explain, this class inherits Menu class which handles everything
such as waiting for user reactions, and adding reactions to your message. You can do fun things with Menu class such as 
a confirmation message with reactions which are shown [here](https://github.com/Rapptz/discord-ext-menus#getting-started).
But for our use, we will use them as the button for the pagination. For MenuPages, this class is specifically for 
handling pages, when you click on a reaction, it will show you the next page.

Now, here are the basic implementation for our use.

**Code Example For MenuPages**
```python
import discord
from discord.ext import menus

class MyMenuPages(menus.MenuPages, inherit_buttons=False):
    @menus.button("<:before_check:754948796487565332>", position=menus.First(1))
    async def go_before(self, payload):
        """Goes to the previous page."""
        await self.show_checked_page(self.current_page - 1)

    @menus.button("<:next_check:754948796361736213>", position=menus.Last(0))
    async def go_after(self, payload):
        """Goes to the next page."""
        await self.show_checked_page(self.current_page + 1)

    @menus.button("<:before_fast_check:754948796139569224>", position=menus.First(0))
    async def go_first(self, payload):
        """Goes to the first page."""
        await self.show_page(0)

    @menus.button("<:next_fast_check:754948796391227442>", position=menus.Last(1))
    async def go_last(self, payload):
        """Goes to the last page."""
        await self.show_page(self._source.get_max_pages() - 1)
    
    @menus.button("<:stop_check:754948796365930517>", position=menus.First(2))
    async def go_stop(self, payload):
        """Remove this message."""
        self.stop()
```
**Explanation**
1. `inherit_buttons` kwargs is set to False, this is to remove all default `menus.button` to set it your own.
2. `MenuPages.show_page` is to show the page at a position that you gave, in this case, `0`.
3. `MenuPages.show_checked_page` is to show a page, similar to `show_page`, but this will check if the position exist.
     `IndexError` error are ignored when it is raised.
4. `First`/`Last` class is an anchor during adding reaction. For example, when given as `First(0)`, `Last(0)`, `First(1)`
    `First(2)`, `Last(1)`. Regardless of order, `First(0)` reaction will be added first, followed by `First(1)`, `First(2)`.
   After that, `Last(0)` and `Last(1)` are added. There are also `Position`, but I don't use them here.
5. `MenuPages.stop()` will end the menu session, you can set them to delete the message by `delete_message_after` or
    `clear_reactions_after` to clear the reactions after the menu session ended.

You will need to create `ListPageSource` class to use with this class. [Jump Here](#list_page_source)

### <a name="paginate_help_2"></a> Pagination for 2.x
With the introduction of Buttons in 2.0. We are able to use them as a replacement of `MenuPages`. In fact, we
can even re-use the code in `MenuPages` and recreate them for pagination.

Similar to `MenuPages`, we have `View` that handles all the interaction with the user. This can be use in `Button`, 
`Select`. It is documented [here](https://discordpy.readthedocs.io/en/master/api.html#discord.ui.View). There are 
example usage for `View` written by Danny himself. This will help you understand how to use them, as I won't be explaining
every niche things about them. The example is found [here](https://github.com/Rapptz/discord.py/blob/master/examples/views/tic_tac_toe.py)
where he wrote a tictactoe game with [`View`](https://discordpy.readthedocs.io/en/master/api.html#discord.ui.View) and 
[`Button`](https://discordpy.readthedocs.io/en/master/api.html#discord.Button).

In order to create a Pagination view, we will also subclass the `MenuPages` class to borrow the features that are 
available from them. They handle the pages for us, which is insanely useful thanks to Danny's way of coding.

**Example Code for View Button**
```py
import discord
from discord import ui
from discord.ext import menus

class MyMenuPages(ui.View, menus.MenuPages):
    def __init__(self, source, *, delete_message_after=False):
        super().__init__(timeout=60)
        self._source = source
        self.current_page = 0
        self.ctx = None
        self.message = None
        self.delete_message_after = delete_message_after

    async def start(self, ctx, *, channel=None, wait=False):
        # We wont be using wait/channel, you can implement them yourself. This is to match the MenuPages signature.
        await self._source._prepare_once()
        self.ctx = ctx
        self.message = await self.send_initial_message(ctx, ctx.channel)

    async def _get_kwargs_from_page(self, page):
        """This method calls ListPageSource.format_page class"""
        value = await super()._get_kwargs_from_page(page)
        if 'view' not in value:
            value.update({'view': self})
        return value

    async def interaction_check(self, interaction):
        """Only allow the author that invoke the command to be able to use the interaction"""
        return interaction.user == self.ctx.author

    @ui.button(emoji='<:before_fast_check:754948796139569224>', style=discord.ButtonStyle.blurple)
    async def first_page(self, button, interaction):
        await self.show_page(0)

    @ui.button(emoji='<:before_check:754948796487565332>', style=discord.ButtonStyle.blurple)
    async def before_page(self, button, interaction):
        await self.show_checked_page(self.current_page - 1)

    @ui.button(emoji='<:stop_check:754948796365930517>', style=discord.ButtonStyle.blurple)
    async def stop_page(self, button, interaction):
        self.stop()
        if self.delete_message_after:
            await self.message.delete(delay=0)

    @ui.button(emoji='<:next_check:754948796361736213>', style=discord.ButtonStyle.blurple)
    async def next_page(self, button, interaction):
        await self.show_checked_page(self.current_page + 1)

    @ui.button(emoji='<:next_fast_check:754948796391227442>', style=discord.ButtonStyle.blurple)
    async def last_page(self, button, interaction):
        await self.show_page(self._source.get_max_pages() - 1)
```
**Explanation**
1. `ui.View` contains all the handling of Button interaction. While, we also need partial use of `menus.MenuPages` where
    it handles the core of pagination. This include calling `ListPageSource.format_page` which will be use.
2. We won't call `super().start(...)` because those handles reactions, we're only borrowing the methods from them.
3. `timeout=60` kwargs is passed to `ui.View`, Not `menus.MenuPages`. To understand how this works, learn Method
   Resolution Order (MRO). As I won't be covering them here.
4. [`View.interaction_check`](https://discordpy.readthedocs.io/en/master/api.html#discord.ui.View.interaction_check) is 
   for the check. You can check if the interaction is your author. Returns True will result in calling the Button 
   callback. Raising an error or returning False will prevent them from being called.
5. [`ui.button`](https://discordpy.readthedocs.io/en/master/api.html#discord.ui.button) basically is the button you're 
   adding to `View`.
6. for `show_check_page`/`show_page` are explained in the `1.7.x` section. [Jump Here](#paginate_help_1_7)
7. [`message.delete(delay=0)`](https://discordpy.readthedocs.io/en/latest/api.html#discord.Message.delete) is a way to 
   delete message without checking if they exist. When error, it silences them.

You will need to create `ListPageSource` class to use with this class. [Jump Here](#list_page_source)

### <a name="list_page_source"></a>  ListPageSource class
As I stated before, `ListPageSource` are only from the external library `discord-ext-menus`. Make sure to install them.

Now `MyMenuPages` are created for our use, lets create our `ListPageSource` now. To put it simply, `ListPageSource` is 
to format each page where `MyMenuPages` will call this class. There are also other types of class format. However, I 
will just use `ListPageSource` for simplicity sake.

If you want to read more about `ListPageSource`, you can read them here. [Click Here](https://github.com/Rapptz/discord-ext-menus#pagination).

Now this will be our basic implementation of `ListPageSource`.

**Example Code For ListPageSource**
```py
import discord
from itertools import starmap
from discord.ext import menus
class HelpPageSource(menus.ListPageSource):
    def __init__(self, data, helpcommand):
        super().__init__(data, per_page=6)
        self.helpcommand = helpcommand

    def format_command_help(self, no, command):
        signature = self.helpcommand.get_command_signature(command)
        docs = self.helpcommand.get_command_brief(command)
        return f"{no}. {signature}\n{docs}"
    
    async def format_page(self, menu, entries):
        page = menu.current_page
        max_page = self.get_max_pages()
        starting_number = page * self.per_page + 1
        iterator = starmap(self.format_command_help, enumerate(entries, start=starting_number))
        page_content = "\n".join(iterator)
        embed = discord.Embed(
            title=f"Help Command[{page + 1}/{max_page}]", 
            description=page_content,
            color=0xffcccb
        )
        author = menu.ctx.author
        embed.set_footer(text=f"Requested by {author}", icon_url=author.avatar_url)  # author.avatar in 2.0
        return embed
```
**Explanation**
1. `per_page` kwargs is the amount of elements from `data` that will be passed to `ListPageSource.format_page` as `entries`.
2. `starting_number` is just the starting number for the list of 6 that will be shown. So for example, at page 1, it will be
    1, at page 2, it will be 13 and page 3 would be 19. `menu.current_page` will start at 0, hence we add 1.`
3. [`itertools.starmap`](https://docs.python.org/3/library/itertools.html#itertools.starmap) 
   works exactly like `map` but it unpacks the argument when calling a function, in this case, `HelpPageSource.format_command_help`.
4. We can get Context from `menu.ctx` attribute.
5. For `ListPageSource.format_page`, whatever you return from this method, will be shown as a single page. You can return
    a `discord.Embed`, a `str` or a `dict` that will be as kwargs for `message.edit`.
   
The output of them are in the [Integrating class of pagination](#help_pagination_intergrate) section.


### <a name="help_pagination_intergrate"></a> Integrating classes of pagination
Now we will be creating the HelpCommand that uses classes that we've made. This HelpCommand class will also be able to
use the 2.0 button. Hence, why it's in its own section.

**Example Code**
```py
import discord
from itertools import chain
from discord.ext import commands

class MyHelp(commands.MinimalHelpCommand):
    def get_command_brief(self, command):
        return command.short_doc or "Command is not documented."
    
    async def send_bot_help(self, mapping):
        all_commands = list(chain.from_iterable(mapping.values()))
        formatter = HelpPageSource(all_commands, self)
        menu = MyMenuPages(formatter, delete_message_after=True)
        await menu.start(self.context)

bot = commands.Bot("uwu ", help_command=MyHelp())
```
**Explanation**
1. [`itertools.chain.from_iterable`](https://docs.python.org/3/library/itertools.html#itertools.chain.from_iterable) 
   flatten the result of `mapping.values()` into a single list. This is up to you on how you want to handle the command.
   I'm just making it flat to be as basic as possible.
2. `HelpPageSource` acts as the formatter, this class will be the one that gets the data and the one that shows each
    page to the user.
3. `MyMenuPages` depending on which class you're using, this will handle the `HelpPageSource` class. It will handle the
    buttons from the user, and determine whether to show the previous/next/forward/backward or stop.
4. [`Command.short_doc`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Command.short_doc)
   will show the value from `Command.brief` or if None, show the first sentence of `Command.help`.

### The Output for 1.7.x
![helpMenu](https://cdn.discordapp.com/attachments/652696440396840963/883637607882457099/unknown.png)

### The Output for 2.x
![helpMenu](https://cdn.discordapp.com/attachments/652696440396840963/883635346271764481/unknown.png)


# <a name="the_end"></a> The end
I hope that reading this walkthrough will assist you and give a better understanding on how to subclass [`HelpCommand`][helplink]. 
All the example code given are to demonstrate the feature of `HelpCommand` and feel free to try it. There are lots of 
creative things you can do to create a `HelpCommand`. 

If you need an inspiration, this is my help command. I mean, nobody asked but yeah here it is.
![helpEx](https://cdn.discordapp.com/attachments/784735050071408670/853268304565895188/unknown.png)

Here's my code if you want to take a look. It's a bit complicated, but you only have to focus on the
HelpCommand class [my help command](https://github.com/InterStella0/stella_bot/blob/master/cogs/helpful.py).

If you want a more easier help command, here's an example of a help command written by pikaninja
Here's the [code](https://mystb.in/EthicalBasketballPoliticians.python)
Here's how it looks like.

![help_simple](https://cdn.discordapp.com/attachments/652696440396840963/858616279715676180/unknown.png)

Now, of course, any question regarding `HelpCommand` should be asked in the [discord.py](https://discord.gg/dpy) server 
because I don't really check this gist as much, and because there is a lot of helpful discord.py helpers if you're nice 
enough to them. :D


[defhelplink]: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.DefaultHelpCommand
[minhelplink]: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.MinimalHelpCommand
[helplink]: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.HelpCommand
[sendbothelp]: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.HelpCommand.send_bot_help
[Hgetcommandsig]: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.HelpCommand.get_command_signature
[Hgetbotmap]: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.HelpCommand.get_bot_mapping
[Hgetdestination]: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.HelpCommand.get_destination
[Hgetprepare]: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.HelpCommand.prepare_help_command
[Hgetcleanprefix]: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.HelpCommand.clean_prefix
[Hgetfilter]: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.HelpCommand.filter_commands
[Csendhelp]: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Context.send_help