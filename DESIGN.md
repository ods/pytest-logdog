# Rationale and design

## What's wrong with caplog?

There is no ready methods to filter interesting records.  It creates a mess from captured record at different stages.  `get_records()` allows to access records for the given stage, but `clear()` affects all.  `caplog.at_level()` / `caplog.set_level()` changes the state globally, so it's not possible to structure your tools without the risk of interference.  Even worse, using `logger` argument might prevent you from seeing some records in root logger.  There is not way to disable output of handled messages.  You watch a ton of messages without a chance to distinguish whether some `ERROR` is a deliberate while testing corner cases, or unexpected and requires your attention.


## Requirements

1. (high/simple) Simple interface to match records similar to filters: by logger name, level, message pattern.
2. (medium/simple) Some way to avoid interference of test parts.  For example, scopes to narrow what we capture.  Allow nesting if possible.
3. (medium/hard) Clean output: allow marking records as handled in some way ("pop them out") and don't show them in the output.
4. (low/hard) Option to switch whether to hide (default) or show handled messages in the output.
5. (low/hard) Visualy mark handled messages in the output, when you opted to show them.


## Ways to implement

### Wrapper around `caplog`

pros:
* Easiest way to reach requirement #1.

cons:
* No forseeable ways to get scoping and meet other requirements.

### Install single handler to root logger

pros:
* With single handler it should be easier to collect/mark handled messages (requirement #3).

cons:
* It's tricky to separate messages for each scope.
* Some loggers may have level set and thus fall out of consideration.

### Install separate handler for each scope

pros:
* Easy separation of messages for each scope.
* It's possible to attach capturer to specific logger and reset level for it.

cons:
* We need some additional global entity to collect/mark handled messages.


## Choosing the name

The current working name (`xcaplog`) is great for wrapper implementation, as it extends the original `caplog`.  But all other ways to implement it lead to quite different API and thus connection to `caplog` is arguable.
