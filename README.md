#  VS-SynoIndex

VS-SynoIndex is a server-based wrapper for Synology's SynoIndex to enable indexing video files even from winthin docker container. It is designed to run as a task in Synology DSM.

It is essential for the automated toolchain which download, convert, rename and relocate video files for Synology's VideoStation (https://github.com/heimdall-syno/VS-Handbrake)

Check out the second part of the toolchain - VS-Handbrake (https://github.com/heimdall-syno/VS-Handbrake) - which performs the conversion and renaming.

## Overview of the VS-Components
```
+---------------------------------------------------------------------------------+
|                                  Synology DSM                                   |
+---------------------------------------------------------------------------------+
|                  +--------------------+  +-----------------+                    |
|                  |       Docker       |  |      Docker     |                    |
|                  |transmission.openVpn|  |     Handbrake   |                    |
|                  +--------------------+  +-----------------+                    |
| +------------+   | +---------------+  |  | +-------------+ |  +---------------+ |
| |VS-SynoIndex|   | |VS-Transmission|  |  | | VS-Handbrake| |  |VS-Notification| |
| |   (Task)   +---->+   (Script)    +------>+   (Script)  +--->+    (Task)     | |
| +------------+   | +---------------+  |  | +-------------+ |  +---------------+ |
|                  +--------------------+  +-----------------+                    |
|                                                                                 |
+---------------------------------------------------------------------------------+
```

Check out the other components:


VS-Transmission:   https://github.com/heimdall-syno/VS-Transmission

VS-Handbrake:      https://github.com/heimdall-syno/VS-Handbrake

VS-Notification:   https://github.com/heimdall-syno/VS-Notification

VS-Playlist-Share: https://github.com/heimdall-syno/VS-Playlist-Share

## Quick Start

1. Clone the repository inside an arbitrary directory e.g. the $home-directory.

2. Create a triggered task (Control Panel > Task Scheduler) for the Syno-Index server with the following settings:
	```
    Task:       VS-SynoIndex
    User:       <admin-user> (not root)
    Event:      System startup/boot
    Command:    python3 /volume1/homes/user/VS-SynoIndex/webservice.py (--dockerport <port> | --hostport <port>)
                                                                        --logs <path/to/logs>
    ```
	```
    +-------------------+-------------+------------------------------+----------------------+
    |     Arguments     | Description |           Function           |       Examples       |
    +-------------------+-------------+------------------------------+----------------------+
    | --dockerport/(-d) | Docker port | Whether the SynoIndex server |         32699        |
    |                   |             |  listen to the docker bridge |                      |
    |                   |             |    interface on given port   |                      |
    +-------------------+-------------+------------------------------+----------------------+
    | --hostport/(-e)   |  Host port  | Whether the SynoIndex server |         32698        |
    |                   |             |      listen to localhost     |                      |
    |                   |             |    interface on given port   |                      |
    +-------------------+-------------+------------------------------+----------------------+
    |    --logs/(-l)    |  Logs path  |    Path to logs directory    | /volume1/docker/logs |
    +-------------------+-------------+------------------------------+----------------------+

    Examples:
        python3 /volume1/homes/user/VS-SynoIndex/webservice.py --dockerport 32699 --logs /volume1/docker/logs
        python3 /volume1/homes/user/VS-SynoIndex/webservice.py --hostport 32698 --logs /volume1/docker/logs
    ```