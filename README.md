# hier_client

Python library for using [Hier](https://honorable-diligent-serval.anvil.app/) from the CLI.

## Install

The client requires Python >3.6. Just use `pip` to install:

```
$ pip install hier_client
```

## Quickstart

Before using the client, you must generate a Hier token.
Go to your profile page on [Hier](https://honorable-diligent-serval.anvil.app/).
Click the `Refresh token` button.

Back at the command-line, initialize the client.
You'll only have to do this once.

```
$ hier init
```

You'll be prompted for the email you used to register for Hier,
as well as the token you just generated.
If you do ever want to update your token,
you can always rerun `hier init`.

Now, add a note for today:

```
$ hier write "Learned about the Hier client."
```

If you've already made notes for today, no worries, just append to them:

```
$ hier write --append "Learned about the Hier client."
```

Or, if you just want to see what you've already written:

```
$ hier read
```
