# Toonbot
A plugin for Slack's python-rtmbot to send web comics via direct messages.

## Install
**Warning: These instructions are incomplete and will be refined as the project matures**

* Create a MySQL database and user for Toonbot.
* Clone [python-rtmbot](https://github.com/slackhq/python-rtmbot) to a place on your server. _Follow the instructions there to configure it for your server._
* Change into the plugins directory.
* Clone this repo into the plugins directory
* Copy the example rtmbot.conf to the root of python-rtmbot.
* Edit it filling in your MySQL database details as well as Slack details.
* Switch to the db/base directory and import the database to MySQL.
* Go up one level and run `./migrate.py` to update the database with any last minute changes.
* Start rtmbot and talk to your Toonbot user on slack.

## Upgrading

**Please backup your database before upgrading**

**Automatic upgrade instructions to be added at a later date**

### Manual upgrade instructions
* Stop python-rtmbot.
* [Optional] Upgrade python-rtmbot.
* Enter the plugins/toonbot directory and run `git pull`.
* Enter the db directory and run `./migrate.py` to update the database.
* Start python-rtmbot

## Commands

* `list` - This will show a list of available webcomics Toonbot can deliever to you. It will also indicate which comics you have already subscribed to.
* `feedback` - This allows your users to send feedback to your Toonbot administrator.
* `announce` - **Admin users only** can broadcast a message to all users using the service. Toonbot will queue these messages and notify you when the message has been delivered and how many users you've reached. Note: Toonbot will **not** send announcements to users who have either never interacted with the bot, never subscribed to a comic, or have unsubscribed from all the comics.
* `start` - Change the time the bot will start sending you comics, please use the following format `HH:MM:SS`. This is a 24 hour clock. This should be set to your local time as Toonbot uses the timezone you've set on your Slack profile to determine when it's best to send you comics.
* `end` - Change the time the bot will stop sending you comics. Again, use the `HH:MM:SS` format when setting the time.
* `postcolour` - Change the colour of image attachments, please provide your colour in a hex format such as `#d3f6aa`.
* `posttextcolor` - Changes the colour of the attachments containing supplementary text used by some comics. Again, provide the colour in a hex format.
* `clear preferences` - This will clear all your custom preferences resetting them to the defaults. This will not unsubscribe you from comics.
* `help` - Display a short help message for users.
* `version` - Show version info.

Anything else passed to Toonbot is treated as a request to either subscribe or unsubscribe to a comic, if no comic matches what was entered, Toonbot will display an error.

As mentioned earlier, Toonbot uses the timezone you've set on your Slack profile to determine when it's best to send you comics. If you change your timezone, please allow for Toonbot to update its cache, this generally happens overnight depending on where you're located. Changes for DST are not required as Slack sends updated timezone offsets.

## Stored procedures

It's currently impossible to totally stop using the service, or to remove a comic from the database if someone's subscribed to it.

The following stored procedure can be run on the database in the event a user requires removing, this will also unsubscribe them from any comics:

```mysql
CALL delete_user('U12345678');
```

The following can be called to remove a comic and unsubscribe users from it:

```mysql
CALL delete_comic('comicname');
```

The following can be run to upgrade a user to an admin:

```mysql
CALL make_admin('U12345678');
```
