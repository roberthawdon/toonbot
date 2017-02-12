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
* Say `claimadmin` to grant your user administrator privileges followed with `claimsuperadmin` to grant yourself super administrator status - **Note: Until this has been done, any user can promote themselves to (Super) Administrator**

## Upgrading

**Please backup your database before upgrading**

**Automatic upgrade instructions to be added at a later date**

### Manual upgrade instructions
* Stop python-rtmbot.
* [Optional] Upgrade python-rtmbot. (Highly recommended)
* Enter the plugins/toonbot directory and run `git pull`.
* Enter the db directory and run `./migrate.py` to update the database.
* Start python-rtmbot

## User Commands

* `list` - This will show a list of available webcomics Toonbot can deliever to you. It will also indicate which comics you have already subscribed to. The number of days the comic was last updated will also be indicated.
* `feedback` - This allows your users to send feedback to your Toonbot administrator.
* `start` - Change the time the bot will start sending you comics, please use the following format `HH:MM:SS`. This is a 24 hour clock. This should be set to your local time as Toonbot uses the timezone you've set on your Slack profile to determine when it's best to send you comics.
* `end` - Change the time the bot will stop sending you comics. Again, use the `HH:MM:SS` format when setting the time.
* `postcolour` - Change the colour of image attachments, please provide your colour in a hex format such as `#d3f6aa`.
* `posttextcolour` - Changes the colour of the attachments containing supplementary text used by some comics. Again, provide the colour in a hex format.
* `clear preferences` - This will clear all your custom preferences resetting them to the defaults. This will not unsubscribe you from comics.
* `show preferences` - To view all your current preferences.
* `claimadmin` - This sets your user as an administrator if no other users are administrators. This should be run when first setting up the bot. Should someone else have claimed the first administrator user, the stored procedure further on will allow you to manually force your user to become administrator.
* `help` - Display a short help message for users.
* `version` - Show version info.

Individual settings can be reset to defauls by passing `reset` as the argument.

Anything else passed to Toonbot is treated as a request to either subscribe or unsubscribe to a comic, if no comic matches what was entered, Toonbot will display an error.

## Administrator Commands

* `claimsuperadmin` - Promote the first admin user to super administrator status. Currently, this will ensure your administrator status can't be revoked by a standard administrator.
* `makeadmin` - Running this command followed by the name of a user (without the @) will promote them to administrator status. They will receive a notification telling them this.
* `revokeadmin` - Running this followed by the name of the user will revoke their admin permissions. They will be notified when this happens. **Note: You cannot revoke your own administrator privileges**
* `makesuperadmin` - This command followed by the name of a user will promote them to super administrator status.
* `revokesuperadmin` - Followed by the name of a user will strip **all** their administrator privileges returning them to a normal user.
* `announce` - Can broadcast a message to all users using the service. Toonbot will queue these messages and notify you when the message has been delivered and how many users you've reached. Note: Toonbot will **not** send announcements to users who have either never interacted with the bot, never subscribed to a comic, or have unsubscribed from all the comics.
* `comicadmin` - Allows you to manage the comics installed on the bot. Append the following:
  * `list`- Lists all comics installed in toonbot. It also lists how many users are subscribed to each comic, how long it's been since a new comic was fetched, and its current mode.
Set comics to various modes:
  * `activate` - Normal state, the comic is shown in the list, users can subscribe or unsubscribe to it, and comics will be posted when they're updated.
  * `deactivate` - The comic is removed from the list. Users will not be able to subscribe or unsubscribe to it, and new updates will not be fetched.
  * `disable` - The comic is shown in the list, users can subscribe or unsubscribe from it but updates will not be fetched. The last comic fetched will be posted to new subscribers if available.
  * `hidden` - The comic will not be shown in the list. The user can subscribe or unsubscribe from it, comics will be fetched and posted. This is useful for trialling new comics, or comics not indented for public consumption.
* `installpack` - Install comic pack from github repo.
* `deletepack` - Uninstall comic pack and unsubscribe all users to the comics in that pack.
* `packadmin` - Allows for bulk administration of comics by pack, uses the same modes as `comicadmin`:
  * `activate`
  * `deactivate`
  * `disable`
  * `hidden`
* `globalstarttime` - Defines the default start of day in the `HH:MM:SS` format. This will not affect users' own preferences.
* `globalendtime` - Defines the default end of day in the `HH:MM:SS` format. Again, this will not affect users' own preferences.
* `globalpostcolour` - Sets the default attachment colour, pass a colour value in hex format.
* `globalposttextcolour` - Sets the attachment colour of supplementary text used by some comics. Again, pass this colour in hex format.
* `fetchtimeout` - Sets the timeout value when checking for comics. The bot comes shipped with this value as `10` seconds.
* `janitortime` - This sets the time, in UTC, the janitor process, which checks user account statuses, is run at. Define a time in the `HH:MM:SS`. There is a 60 second tolerance for when the process is run. By default, the process runs at `02:05:30` which may be unsuitable for some timezones.

### Notes on timezones

As mentioned earlier, Toonbot uses the timezone you've set on your Slack profile to determine when it's best to send you comics. If you change your timezone, please allow for Toonbot to update its cache, this generally happens overnight depending on where you're located. Changes for DST are not required as Slack sends updated timezone offsets.

### Notes on feedback function

The feedback function can be disabled by changing the `FEEDBACK` setting in the rtmbot.conf file to `False`. If upgrading from an old version, this line will be absent. By default the bot assumes the feedback option should be enabled.

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

A whole comic pack can be removed from the database with this:

```mysql
CALL delete_comic_pack('packname');
```

The following can be run to upgrade a user to an admin:

```mysql
CALL make_admin('U12345678');
```
