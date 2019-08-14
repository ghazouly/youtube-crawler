# youtube-crawler

### Application design

#### Overview

> In this task I've maintained somehow Flask framework main directories like:
- flaskr: which represents the application layer; Bootstrapping, binding blueprints, routing, handling db and services.
- instance: represents a container for SQLite database file(s).
- tests: (TODO) contains testing methods.
- venv: for environment libraries and files 

#### Application Architecture Brief

Within the application layer `flaskr` I set `channels` as domains container, `static` for assets & downloads and `templates` for views.

> I've approached this design to achieve two points
- Domains/Channels singularity and scalability: We can headless plug-in any new channel to our tool and every channel has no link with others. it has only its specific implementation.
- Strategy-led behaviour: You don't need to control or even know explicitly what channel you're working with and how it'll handle things behind. Just ask the recognizer and he'll do answer.

#### Application Skeleton (flaskr)

- `channels` Domains to represent channels.
- `__init__.py` Application bootstrap.
- `db.y` Database connection and configuration.
- `crawler.py` Our only service and blueprint/router.
- `schema.sql` Simple database schema for required table.

#### Channels - Deep dive (Domains)

> As stated in Application architecture brief we should have an Interface `IChannelRecognizer` as a contract for defining minimal implementation among channels.

We've a class `ChannelRecognizer` shall implements the interface (TODO) and do `handle` crawling requesting by directing it to the right channel handler.

> To maintain strategy behaviour I made an adaptor `YoutubeAdaptor` for the Youtube channel.
 
In this `ChannelAdaptor` we implement the detailed methods that fulfill the channel needs only. 