# Rationale and design

## What's wrong with caplog?

There is no ready methods to filter interesting records.  It creates a mess from captured record at different stages.  `get_records()` allows to access records for the given stage, but `clear()` affects all.  `caplog.at_level()` / `caplog.set_level()` changes the state globally, so it's not possible to structure your tools without the risk of interference.  Even worse, using `logger` argument might prevent you from seeing some records in root logger.  There is not way to disable output of handled messages.  You watch a ton of messages without a chance to distinguish whether some `ERROR` is a deliberate while testing corner cases, or unexpected and requires your attention.


## Requirements

* (high/simple) Simple interface to match records similar to filters: by logger name, level, message pattern.
* (medium/simple) Some way to avoid interference of test parts.  For example, scopes to narrow what we capture.  Allow nesting if possible.
* (medium/hard) Clean output: allow marking records as handled in some way ("pop them out") and don't show them in the output.
* (low/hard) Option to switch whether to hide (default) or show handled messages in the output.
* (low/hard) Visualy mark handled messages in the output, when you opted to show them.
